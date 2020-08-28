from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,  password):
    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        return False
    else:
        hash_value = user[1]
        if check_password_hash(hash_value,password):
            session["username"] = username
            session["user_id"] = user[0]
            if user[2] == 1:
                session["admin"] = True
            else:
                session["admin"] = False
            return True
        else:
            return False
 
def signup(username,  password):
    if (not username or not password) or (username.isspace() or password.isspace()):
        return False
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, 0)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
        return True
    except:
        return False
 
def logout():
    if 'username' in session:
        del session["username"]
    if 'user_id' in session:
        del session["user_id"]
    if 'admin' in session:
        del session["admin"]

def user_id():
    return session.get("user_id", 0)
    
def get_user_id(username):
    sql = "SELECT id FROM Users WHERE username=:username"
    query_result = db.session.execute(sql,  {"username":username})
    user_id = query_result.fetchone()
    if user_id == None:
        return 0
    else:
        return user_id[0]

def get_username(user_id):
    sql = "SELECT username FROM Users WHERE id=:id"
    query_result = db.session.execute(sql,  {"id":user_id})
    username = query_result.fetchone()
    if username == None:
        return None
    else:
        return username[0]
    
def search_users(searchword):
    sql = "SELECT id, username FROM Users WHERE username LIKE :searchword LIMIT 30"
    result = db.session.execute(sql,  {"searchword":"%"+searchword+"%"})
    users = result.fetchall()
    return users
    
def get_attendees(course_id):
    sql = "SELECT id, username FROM Users WHERE id IN (SELECT user_id FROM registrations WHERE course_id=:course_id) LIMIT 30"
    result = db.session.execute(sql,  {"course_id":course_id})
    attendees = result.fetchall()
    return attendees
    
def search_attendees(course_id, searchword):
    sql = "SELECT id, username FROM Users WHERE id IN (SELECT user_id FROM registrations WHERE course_id=:course_id) AND username LIKE :searchword"
    result = db.session.execute(sql,  {"course_id":course_id, "searchword":"%"+searchword+"%"})
    attendees = result.fetchall()
    return attendees
    
def add_teacher(user_id):
    sql = "UPDATE users SET teacher=1 WHERE id=:id"
    db.session.execute(sql, {"id":user_id})
    db.session.commit()
    
def get_teachers():
    result = db.session.execute("SELECT id, username FROM Users WHERE teacher=1")
    teachers = result.fetchall()
    return teachers
