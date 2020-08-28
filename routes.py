from app import app
from flask import render_template, request, redirect,  session
import users,  courses,  exercises,  questions,  choices,  results,  answers,  registrations
from werkzeug.security import check_password_hash

@app.route("/")
def index():
    if users.user_id() != 0:
        course_list = courses.get_course_list()
        return render_template("index.html", courses=course_list)
    else:
        return render_template("login.html")
    
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    if users.login(username,  password):
        return redirect("/")
    else:
        return render_template("login.html", login_error=True)

@app.route("/signup",methods=["POST"])
def signup():
    username = request.form["username"].strip()
    password = request.form["password"].strip()
    if not username or not password:
        return render_template("login.html", signup_error=True)
    if users.signup(username,  password):
        return render_template("login.html", signup_error=False)
    else: 
        return render_template("login.html", username_duplicate=True)
 
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/newcourse")
def new_course():
    if users.user_is_admin() != True:
        return redirect("/")
    teachers = users.get_teachers()
    return render_template("newcourse.html", teachers=teachers)
    
@app.route("/teachers")
def teachers():
    if users.user_is_admin() != True:
        return redirect("/")
    return render_template("teachers.html")
    
@app.route("/registeredcourses")    
def registered_courses():
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/")
    course_list = courses.get_registered_courses(user_id)
    return render_template("index.html", courses=course_list)

@app.route("/searchusers")    
def search_users():
    if users.user_is_admin() != True:
        return redirect("/")
    searchword = request.args["searchword"]
    user_list = users.search_users(searchword)
    return render_template("teachers.html",  users=user_list)
    
@app.route("/course/<int:id>/searchattendees")    
def search_attendees(id): 
    course = courses.get_course_by_id(id)
    if users.user_id() != course[2] and users.user_is_admin() != True:
        return redirect("/")
    searchword = request.args["searchword"]
    attendee_list = users.search_attendees(id, searchword)
    return render_template("attendees_teacher.html", attendees=attendee_list, course=course)
    
@app.route("/searchcourses")    
def search_courses():
    if users.user_id() == 0:
        return redirect("/")
    searchword = request.args["searchword"]
    course_list = courses.search_courses(searchword)
    return render_template("index.html",  courses=course_list)

@app.route("/addcourse", methods=["POST"])
def add_course():
    if users.user_is_admin() != True:
        return redirect("/")
    course_name = request.form["course_name"].strip()
    teacher_id = request.form.get("teacher_id")
    course_key = request.form.get("course_key").strip()
    if teacher_id == None or not course_name:
        teachers = users.get_teachers()
        return render_template("newcourse.html", teachers=teachers, error=True)
    if not course_key:
        courses.add_course(course_name,  teacher_id,  None)
        return redirect("/")
    course_id = courses.add_course(course_name,  teacher_id,  course_key)
    registrations.add_registration(teacher_id, course_id)
    return redirect("/")
    
@app.route("/addteacher", methods=["POST"])
def add_teacher():
    if users.user_is_admin() != True:
        return redirect("/")
    username = request.form.get("username").strip()
    user_id = users.get_user_id(username)
    if user_id == 0:
        return render_template("teachers.html", error=True)
    users.add_teacher(user_id)
    return render_template("teachers.html", error=False)

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
            question_id = questions.add_question(question_title, exercise_id, 1, answer, points)
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
            question_id = questions.add_question(question_title, exercise_id, 0, answer, points)
            if question_id == 0:
                continue
    return redirect("/exercise/" + str(exercise_id))

@app.route("/course/<int:id>/")
def course(id):
    if users.user_id == 0:
        return redirect("/")
    user_id = users.user_id()
    course = courses.get_course_by_id(id)
    if not registrations.check_registration(user_id, id) and session["admin"] == False:
        if course[3] == None:
            return render_template("registration.html", course=course)
        return render_template("registration.html",  course=course, course_key=True)
    exercise_list = exercises.get_exercise_list(id)
    return render_template("course.html", exercises=exercise_list, course=course)
    
@app.route("/course/<int:id>/register", methods=["POST"])
def register(id):
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/")
    course = courses.get_course_by_id(id)
    if course[3] == None:
        registrations.add_registration(user_id, course[0])
        return redirect("/course/" + str(id))
    course_key = request.form.get("course_key")
    if check_password_hash(course[3],course_key):
        registrations.add_registration(user_id, course[0])
        return redirect("/course/" + str(id))
    return render_template("registration.html", course=course, course_key=True, course_key_error=True)
    
@app.route("/course/<int:id>/attendees")
def attendees(id):
    user_id = users.user_id()
    course = courses.get_course_by_id(id)
    if user_id != course[2]:
        return redirect("/")
    attendees = users.get_attendees(course[0])
    return render_template("attendees_teacher.html", attendees=attendees, course=course)
    
@app.route("/course/<int:course_id>/attendees/<int:user_id>/")
def attendee_results(course_id, user_id):
    session_id = users.user_id()
    course = courses.get_course_by_id(course_id)
    if session_id != course[2]:
        return redirect("/")
    result_list = results.get_course_results(user_id, course_id)
    return render_template("attendee_results.html", results=result_list, course=course)
    
@app.route("/exercise/<int:id>/")
def exercise(id):
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/")
    exercise = exercises.get_exercise_by_id(id)
    course = courses.get_course_by_id(exercise[2])
    if user_id == course[2]:
        question_list = get_list_of_questions_and_answers(id)
        return render_template("exercise_teacher.html", questions=question_list, exercise=exercise, course=course)  
    result = results.get_result(id,  user_id)
    if result != None:
        answer_list = answers.get_answers(id,  user_id)
        return render_template("result.html", answers=answer_list, points=result[0], max_points=result[1], course=course)   
    question_list = get_list_of_questions_and_answers(id)
    return render_template("exercise.html", questions=question_list, exercise=exercise, course=course)      
    
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
    if user_id == 0:
        return redirect("/")
    exercise_id = request.form["exercise_id"]
    course_id = exercises.get_course_id_by_exercise(exercise_id)
    course = courses.get_course_by_id(course_id)
    question_list =questions.get_question_list(exercise_id)
    points = 0
    max_points = 0
    user_answers = []
    for question in question_list:
        answer = request.form.get("answer_" + str(question[0]))
        if answer == None:
            answer = ""
        user_answers.append([question[1], question[3], answer])
        max_points += question[4]
        answers.add_answer(answer, question[0], user_id)
        if answer.upper() == question[3].upper():
            points += question[4]
    results.add_result(points, max_points, exercise_id, user_id)
    return render_template("result.html", answers=user_answers, points=points, max_points=max_points, course=course)   
    
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
