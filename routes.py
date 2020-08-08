from app import app
from flask import render_template, request, redirect,  session
import users,  courses,  exercises,  questions,  choices,  results,  answers

@app.route("/")
def index():
    if 'username' in session:
        course_list = courses.get_course_list()
        return render_template("index.html", courses=course_list)
    else:
        return render_template("login.html")
    
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    users.login(username,  password)
    return redirect("/")
 
@app.route("/signup",methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    users.signup(username,  password)
    return redirect("/")
 
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/newcourse")
def newcourse():
    return render_template("newcourse.html")

@app.route("/searchusers")    
def search_users():
    searchword = request.args["searchword"]
    user_list = users.search_users(searchword)
    return render_template("newcourse.html",  users=user_list)

@app.route("/addcourse", methods=["POST"])
def addcourse():
    course_name = request.form["course_name"]
    course_teacher = request.form["course_teacher"]
    teacher_id = users.get_user_id(course_teacher)
    if teacher_id == None:
        return redirect("/")
    else:
        courses.add_course(course_name,  teacher_id)
        return redirect("/")

@app.route("/newexercise", methods=["POST"])
def newexercise():
    exercise_name = request.form["exercise_name"]
    course_id = request.form["course_id"]
    exercise_id = exercises.add_exercise(exercise_name,  course_id)
    
    choice_questions = request.form["choice_question_count"]
    text_questions = request.form["text_question_count"]
    return render_template("newexercise.html", choice_question_count=int(choice_questions), text_question_count=int(text_questions), exercise_id=exercise_id)

@app.route("/addquestions", methods=["POST"])
def addquestions():
    exercise_id = request.form["exercise_id"]
    for i in range(0,10):
        question_title = request.form.get("choice_question["+str(i)+"]")
        if question_title == None:
            break
        else:
            answer = request.form.get("choice_question["+str(i)+"][answer]")
            points = int(request.form.get("choice_question["+str(i)+"][points]"))
            question_id = questions.add_question(question_title,  exercise_id,  1,  answer,  points)
            choice_list = request.form.getlist("choice_question["+str(i)+"][choice]")
            for choice in choice_list:		
                choices.add_choice(choice,  question_id)
    
    for i in range(0,10):
        question_title = request.form.get("text_question["+str(i)+"]")
        if question_title == None:
            break
        else:
            answer = request.form.get("text_question["+str(i)+"][answer]")
            points = int(request.form.get("text_question["+str(i)+"][points]"))
            questions.add_question(question_title,  exercise_id,  0,  answer,  points)
    return redirect("/exercise/" + str(exercise_id))

@app.route("/course/<int:id>/")
def course(id):
    teacher_id = courses.get_teacher_id(id)
    teacher_username = users.get_username(teacher_id)
    exercise_list = exercises.get_exercise_list(id)
    return render_template("course.html", exercises=exercise_list, course_id=id,  teacher_username=teacher_username)
    
@app.route("/exercise/<int:id>/")
def exercise(id):
    user_id = users.user_id()
    result = results.get_result(id,  user_id)
    if result != None:
        answer_list = answers.get_answers(id,  user_id)
        return render_template("result.html", answers=answer_list, points=result[0],  max_points=result[1])   
    else:
        question_list = questions.get_question_list(id)
        questions_choices = []
        for q in question_list:
            if q[3] == 1:
                choice_list = choices.get_choices_by_question(q[0])
                question = [q[1], True,  choice_list,  q[0]]
                questions_choices.append(question)
            else:
                question = [q[1],  False,  q[0]]
                questions_choices.append(question)
        return render_template("exercise.html", questions=questions_choices, exercise_id=id)    

@app.route("/answer",  methods=["POST"])
def answer():
    user_id = users.user_id()
    exercise_id = request.form["exercise_id"]
    question_list =questions.get_question_list(exercise_id)
    points = 0
    max_points = 0
    user_answers = []
    for question in question_list:
        answer = request.form.get("answer_" + str(question[0]))
        user_answers.append([question[1],  question[4],  answer])
        max_points += question[5]
        answers.add_answer(answer, question[0], user_id)
        if answer == question[4]:
            points += question[5]
    results.add_result(points, max_points, exercise_id, user_id)
    return render_template("result.html", answers=user_answers, points=points,  max_points=max_points)   
