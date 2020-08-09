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
    
    
def get_exercise_list(course_id):
    sql = "SELECT * FROM Exercises WHERE course_id=:id"
    query_result = db.session.execute(sql, {"id":course_id})
    return query_result.fetchall()
