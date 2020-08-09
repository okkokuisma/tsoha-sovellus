from db import db

def get_course_list():
    query_result = db.session.execute("SELECT * FROM Courses")
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
