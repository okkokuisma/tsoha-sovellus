from flask import Flask
from flask import render_template, request, redirect,  session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///ogkuisma"
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    if 'username' in session:
        result = db.session.execute("SELECT * FROM Courses")
        list = result.fetchall()
        return render_template("index.html", courses=list)
    else:
        return render_template("login.html")
    
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password, admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        return redirect("/")
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            if user[1] == 1:
                session["admin"] = True
        else:
            return redirect("/")
    return redirect("/")
 
@app.route("/signup",methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, 0)"
    db.session.execute(sql, {"username":username,"password":hash_value})
    db.session.commit()
    return redirect("/")
 
@app.route("/logout")
def logout():
    if 'username' in session:
        del session["username"]
    if 'admin' in session:
        del session["admin"]
    return redirect("/")

@app.route("/newcourse")
def newcourse():
    return render_template("newcourse.html")

@app.route("/searchusers")    
def searchusers():
    searchword = request.args["searchword"]
    sql = "SELECT username FROM Users WHERE username LIKE :searchword LIMIT 20"
    result = db.session.execute(sql,  {"searchword":"%"+searchword+"%"})
    users = result.fetchall()
    return render_template("newcourse.html",  users=users)

@app.route("/addcourse", methods=["POST"])
def addcourse():
    course_name = request.form["course_name"]
    course_teacher = request.form["course_teacher"]
    sql = "SELECT id FROM Users WHERE username=:course_teacher"
    result = db.session.execute(sql,  {"course_teacher":course_teacher})
    teacher_id = result.fetchone()[0]
    if teacher_id == None:
        return redirect("/")
    else:
        sql = "INSERT INTO Courses (name, teacher_id) VALUES (:course_name, :teacher_id)"
        db.session.execute(sql, {"course_name":course_name, "teacher_id":teacher_id})
        db.session.commit()
        return redirect("/")

@app.route("/newexercise", methods=["POST"])
def newexercise():
    exercise_name = request.form["exercise_name"]
    course_id = request.form["course_id"]
    sql = "INSERT INTO Exercises (name, course_id) VALUES (:exercise_name, :course_id) RETURNING id"
    result = db.session.execute(sql, {"exercise_name":exercise_name, "course_id":course_id})
    exe_id = result.fetchone()[0]
    db.session.commit()
    
    choice_questions = request.form["choice_question_count"]
    text_questions = request.form["text_question_count"]
    return render_template("newexercise.html", choice_question_count=int(choice_questions), text_question_count=int(text_questions), exercise_id=exe_id)

@app.route("/addquestions", methods=["POST"])
def addquestions():
    exercise_id = request.form["exercise_id"]
    for i in range(0,10):
        choice_question_title = request.form.get("choice_question["+str(i)+"]")
        if choice_question_title == None:
            break
        else:
            choices = request.form.getlist("choice_question["+str(i)+"][choice]")
            right_answer = request.form.get("choice_question["+str(i)+"][answer]")
            points = int(request.form.get("choice_question["+str(i)+"][points]"))
            sql = "INSERT INTO Questions (question_title, exercise_id, choice_question, answer, points) VALUES (:question_title, :exercise_id, 1, :answer, :points) RETURNING id"
            result = db.session.execute(sql, {"question_title":choice_question_title, "exercise_id":exercise_id,  "answer":right_answer,  "points":points})
            question_id = result.fetchone()[0]
            db.session.commit()
            sql = "INSERT INTO Choices (choice_title, question_id) VALUES (:choice_title, :question_id)"
            for choice in choices:		
                db.session.execute(sql, {"choice_title":choice, "question_id":question_id})
                db.session.commit()
    for i in range(0,10):
        text_question_title = request.form.get("text_question["+str(i)+"]")
        if text_question_title == None:
            break
        else:
            right_answer = request.form.get("text_question["+str(i)+"][answer]")
            points = int(request.form.get("text_question["+str(i)+"][points]"))
            sql = "INSERT INTO Questions (question_title, exercise_id, choice_question, answer, points) VALUES (:question_title, :exercise_id, 0, :answer, :points)"
            db.session.execute(sql, {"question_title":text_question_title, "exercise_id":exercise_id,  "answer":right_answer,  "points":points})
            db.session.commit()
    return redirect("/exercise/" + str(exercise_id))

@app.route("/course/<int:id>/")
def course(id):
    sql = "SELECT username FROM Users WHERE id = (SELECT teacher_id FROM Courses WHERE id=:id)"
    result = db.session.execute(sql, {"id":id})
    teacher_username = result.fetchone()[0]
    sql = "SELECT * FROM Exercises WHERE course_id=:id"
    result = db.session.execute(sql, {"id":id})
    list = result.fetchall()
    return render_template("course.html", exercises=list, course_id=id,  teacher_username=teacher_username)
    
@app.route("/exercise/<int:id>/")
def exercise(id):
    questions = []
    sql = "SELECT * FROM Questions WHERE exercise_id=:id"
    result = db.session.execute(sql, {"id":id})
    question_list = result.fetchall()
    for q in question_list:
        if q[3] == 1:
            sql = "SELECT id, choice_title FROM Choices WHERE question_id=:id"
            result = db.session.execute(sql, {"id":q[0]})
            choice_list = result.fetchall()
            question = [q[1], True,  choice_list,  q[0]]
            questions.append(question)
        else:
            question = [q[1],  False,  q[0]]
            questions.append(question)
    return render_template("exercise.html", questions=questions, exercise_id=id)    

@app.route("/answer",  methods=["POST"])
def answer():
    exercise_id = request.form["exercise_id"]
    sql = "SELECT * FROM Questions WHERE exercise_id=:id"
    result = db.session.execute(sql, {"id":exercise_id})
    question_list = result.fetchall()
    points = 0
    max_points = 0
    answers = []
    for question in question_list:
        answer = request.form.get("answer_" + str(question[0]))
        answers.append([question[1],  question[4],  answer])
        max_points += question[5]
        if answer == question[4]:
            points += question[5]
    return render_template("result.html", answers=answers, points=points,  max_points=max_points)    
    
@app.route("/teachers")
def teachers():
    result = db.session.execute("SELECT * FROM Opettajat")
    list = result.fetchall()
    return render_template("teachers.html", teachers=list)
