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
    if users.login(username,  password):
        return redirect("/")
    else:
        return render_template("login.html", login_error=True)

@app.route("/signup",methods=["POST"])
def signup():
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    if users.signup(username,  password):
        return redirect("/")
    else: 
        return render_template("login.html", signup_error=True)
 
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/newcourse")
def new_course():
    return render_template("newcourse.html")

@app.route("/searchusers")    
def search_users():
    searchword = request.args["searchword"]
    user_list = users.search_users(searchword)
    return render_template("newcourse.html",  users=user_list)
    
@app.route("/searchcourses")    
def search_courses():
    searchword = request.args["searchword"]
    course_list = courses.search_courses(searchword)
    return render_template("index.html",  courses=course_list)

@app.route("/addcourse", methods=["POST"])
def add_course():
    course_name = request.form["course_name"].strip()
    course_teacher = request.form["course_teacher"].strip()
    teacher_id = users.get_user_id(course_teacher)
    if teacher_id == None:
        return render_template("newcourse.html",  error=True)
    else:
        if courses.add_course(course_name,  teacher_id):
            return redirect("/")
        else:
            return render_template("newcourse.html",  error=True)

@app.route("/newexercise", methods=["POST"])
def new_exercise():
    exercise_name = request.form["exercise_name"].strip()
    course_id = request.form["course_id"]
    exercises.add_exercise(exercise_name,  course_id)
    return redirect("/course/" + str(course_id))

@app.route("/exercise/<int:id>/newquestions",  methods=["POST"])
def new_questions(id):
    user_id = users.user_id()
    course_id = exercises.get_course_id_by_exercise(id)
    teacher_id = courses.get_teacher_id(course_id)
    if user_id != teacher_id:
        return redirect("/")
    choice_questions = int(request.form["choice_question_count"])
    text_questions = int(request.form["text_question_count"])
    if choice_questions == 0 and text_questions == 0:
        return redirect("/exercise/" + str(id) + "/")
    return render_template("newquestions.html", choice_question_count=choice_questions, text_question_count=text_questions, exercise_id=id)

@app.route("/addquestions", methods=["POST"])
def add_questions():
    exercise_id = request.form["exercise_id"]
    for i in range(0,10):
        question_title = request.form.get("choice_question["+str(i)+"]")
        if question_title == None:
            break
        elif not question_title.strip():
            continue
        else:
            answer = request.form.get("choice_question["+str(i)+"][answer]")
            points = int(request.form.get("choice_question["+str(i)+"][points]"))
            question_id = questions.add_question(question_title,  exercise_id,  1,  answer,  points)
            if question_id == 0:
                continue
            choice_list = request.form.getlist("choice_question["+str(i)+"][choice]")
            for choice in choice_list:
                if not choice.strip():
                    continue
                choices.add_choice(choice,  question_id)
    
    for i in range(0,10):
        question_title = request.form.get("text_question["+str(i)+"]")
        if question_title == None:
            break
        elif not question_title.strip():
            continue
        else:
            answer = request.form.get("text_question["+str(i)+"][answer]")
            points = int(request.form.get("text_question["+str(i)+"][points]"))
            question_id = questions.add_question(question_title,  exercise_id, 0, answer, points)
            if question_id == 0:
                continue
    return redirect("/exercise/" + str(exercise_id))

@app.route("/course/<int:id>/")
def course(id):
    course = courses.get_course_by_id(id)
    exercise_list = exercises.get_exercise_list(id)
    return render_template("course.html", exercises=exercise_list, course=course)
    
@app.route("/exercise/<int:id>/")
def exercise(id):
    user_id = users.user_id()
    exercise = exercises.get_exercise_by_id(id)
    course = courses.get_course_by_id(exercise[2])
    if user_id == course[2]:
        question_list = get_list_of_questions_and_answers(id)
        return render_template("exercise_teacher.html", questions=question_list, exercise=exercise, course=course)  
    result = results.get_result(id,  user_id)
    if result != None:
        answer_list = answers.get_answers(id,  user_id)
        return render_template("result.html", answers=answer_list, points=result[0], max_points=result[1], course=course)   
    else:
        question_list = get_list_of_questions_and_answers(id)
        return render_template("exercise.html", questions=question_list, exercise=exercise, course=course)    

#@app.route("/exercise/<int:id>/edit")
#def edit_exercise(id):
#    user_id = users.user_id()
#    course_id = exercises.get_course_id_by_exercise(id)
#    teacher_id = courses.get_teacher_id(course_id)
#    if user_id != teacher_id:
#        return redirect("/")
#    question_list = get_list_of_questions_and_answers(id)
#    return render_template("edit_exercise.html", questions=question_list, exercise_id=id,  course_id=course_id)  
    
@app.route("/exercise/<int:id>/save_changes", methods=["POST"])
def save_changes(id):
    question_list =questions.get_question_list(id)
    for question in question_list:
        remove_question = request.form.get("question_" + str(question[0]) + "_remove")
        if remove_question == "1":
            questions.hide_question(question[0])
    return redirect("/exercise/" + str(id))
    
@app.route("/answer", methods=["POST"])
def answer():
    user_id = users.user_id()
    exercise_id = request.form["exercise_id"]
    course_id = exercises.get_course_id_by_exercise(exercise_id)
    question_list =questions.get_question_list(exercise_id)
    points = 0
    max_points = 0
    user_answers = []
    for question in question_list:
        answer = request.form.get("answer_" + str(question[0]))
        user_answers.append([question[1], question[3], answer])
        max_points += question[4]
        answers.add_answer(answer, question[0], user_id)
        if answer == question[3]:
            points += question[4]
    results.add_result(points, max_points, exercise_id, user_id)
    return render_template("result.html", answers=user_answers, points=points, max_points=max_points, course_id=course_id)   
    
def get_list_of_questions_and_answers(exercise_id):
    question_list = questions.get_question_list(exercise_id)
    questions_choices = []
    for q in question_list:
        if q[2] == 1:
            choice_list = choices.get_choices_by_question(q[0])
            question = [q[0], q[1], True, q[3], q[4], choice_list]
            questions_choices.append(question)
        else:
            question = [q[0], q[1], False, q[3], q[4]]
            questions_choices.append(question)
    return questions_choices
