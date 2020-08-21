from db import db

def get_course_list():
    query_result = db.session.execute("SELECT id, name, teacher_id FROM Courses WHERE visible=1")
    course_list = query_result.fetchall()
    return course_list

def add_course(course_name,  teacher_id):
    if not course_name:
        return False
    try:
        sql = "INSERT INTO Courses (name, teacher_id) VALUES (:course_name, :teacher_id)"
        db.session.execute(sql, {"course_name":course_name, "teacher_id":teacher_id})
        db.session.commit()
        return True
    except:
        return False

def get_teacher_id(course_id):
    query_result = db.session.execute("SELECT teacher_id FROM Courses WHERE id=:id",  {"id":course_id})
    teacher_id = query_result.fetchone()[0]
    return teacher_id
    
def search_courses(searchword):
    sql = "SELECT id, name, teacher_id FROM Courses WHERE UPPER(name) LIKE UPPER(:searchword) AND visible=1 LIMIT 30"
    result = db.session.execute(sql,  {"searchword":"%"+searchword+"%"})
    users = result.fetchall()
    return users
