from db import db

def add_result(result, max_points,   exercise_id,  user_id):
    sql = "INSERT INTO Results (result, max_points, exercise_id, user_id) VALUES (:result, :max_points, :exercise_id, :user_id)"
    db.session.execute(sql, {"result":result, "max_points":max_points, "exercise_id":exercise_id, "user_id":user_id})
    db.session.commit()

def get_result(exercise_id,  user_id):
    sql = "SELECT result, max_points FROM Results WHERE exercise_id=:exercise_id AND user_id=:user_id"
    query_result = db.session.execute(sql, {"exercise_id":exercise_id, "user_id":user_id})
    return query_result.fetchone()
    
def get_course_results(user_id, course_id):
    sql = "SELECT e.id, e.name, r.result, r.max_points FROM results r, exercises e WHERE r.exercise_id IN (SELECT id FROM exercises WHERE course_id=:course_id) AND user_id=:user_id AND r.exercise_id=e.id"
    query_result = db.session.execute(sql, {"course_id":course_id, "user_id":user_id})
    return query_result.fetchall()
