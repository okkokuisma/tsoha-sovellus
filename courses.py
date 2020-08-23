from db import db
from werkzeug.security import generate_password_hash

def get_course_list():
    query_result = db.session.execute("SELECT id, name, teacher_id FROM Courses WHERE visible=1")
    course_list = query_result.fetchall()
    return course_list
    
def get_registered_courses(user_id):
    sql = "SELECT id, name, teacher_id FROM Courses WHERE id IN (SELECT course_id FROM registrations WHERE user_id=:id) AND visible=1"
    query_result = db.session.execute(sql, {"id":user_id})
    course_list = query_result.fetchall()
    return course_list

def add_course(course_name,  teacher_id,  course_key):
    if course_key == None:
        sql = "INSERT INTO Courses (name, teacher_id) VALUES (:course_name, :teacher_id)"
        db.session.execute(sql, {"course_name":course_name, "teacher_id":teacher_id})
        db.session.commit()
    else:
        hash_value = generate_password_hash(course_key)
        sql = "INSERT INTO Courses (name, teacher_id, course_key) VALUES (:course_name, :teacher_id, :course_key)"
        db.session.execute(sql, {"course_name":course_name, "teacher_id":teacher_id, "course_key":hash_value})
        db.session.commit()

def get_teacher_id(course_id):
    query_result = db.session.execute("SELECT teacher_id FROM Courses WHERE id=:id",  {"id":course_id})
    teacher_id = query_result.fetchone()[0]
    return teacher_id
    
def search_courses(searchword):
    sql = "SELECT id, name, teacher_id FROM Courses WHERE UPPER(name) LIKE UPPER(:searchword) AND visible=1 LIMIT 30"
    result = db.session.execute(sql,  {"searchword":"%"+searchword+"%"})
    users = result.fetchall()
    return users
    
def get_course_by_id(course_id):
    query_result = db.session.execute("SELECT id, name, teacher_id, course_key FROM Courses WHERE id=:id",  {"id":course_id})
    course = query_result.fetchone()
    return course

