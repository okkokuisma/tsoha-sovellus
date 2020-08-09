from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,  password):
    sql = "SELECT password, admin, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user == None:
        return False
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
            session["user_id"] = user[2]
            if user[1] == 1:
                session["admin"] = True
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
    sql = "SELECT username FROM Users WHERE username LIKE :searchword LIMIT 20"
    result = db.session.execute(sql,  {"searchword":"%"+searchword+"%"})
    users = result.fetchall()
    return users
