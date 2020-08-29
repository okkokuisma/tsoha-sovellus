from db import db

def add_exercise(exercise_name,  course_id):
    if not exercise_name or course_id == None:
        return 0
    try:
        sql = "INSERT INTO Exercises (name, course_id) VALUES (:exercise_name, :course_id) RETURNING id"
        result = db.session.execute(sql, {"exercise_name":exercise_name, "course_id":course_id})
        db.session.commit()
        exercise_id = result.fetchone()[0]
        return exercise_id
    except:
        return 0
 
def get_exercise_by_id(exercise_id): 
    query_result = db.session.execute("SELECT id, name, course_id FROM Exercises WHERE id=:id",  {"id":exercise_id})
    exercise = query_result.fetchone()
    return exercise
    
def get_exercise_list(course_id):
    sql = "SELECT id, name, course_id FROM Exercises WHERE course_id=:id AND visible=1"
    query_result = db.session.execute(sql, {"id":course_id})
    return query_result.fetchall()
    
def get_course_id_by_exercise(exercise_id):
    sql = "SELECT course_id FROM Exercises WHERE id=:id"
    query_result = db.session.execute(sql, {"id":exercise_id})
    course_id = query_result.fetchone()
    if course_id == None:
        return 0
    else:
        return course_id[0]

def hide_exercise(exercise_id):
    sql = "UPDATE exercises SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":exercise_id})
    db.session.commit()
