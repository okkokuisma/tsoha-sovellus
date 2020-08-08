from db import db

def add_result(result, max_points,   exercise_id,  user_id):
    sql = "INSERT INTO Results (result, max_points, exercise_id, user_id) VALUES (:result, :max_points, :exercise_id, :user_id)"
    db.session.execute(sql, {"result":result, "max_points":max_points, "exercise_id":exercise_id, "user_id":user_id})
    db.session.commit()

def get_result(exercise_id,  user_id):
    try:
        sql = "SELECT result, max_points FROM Results WHERE exercise_id=:exercise_id AND user_id=:user_id"
        query_result = db.session.execute(sql, {"exercise_id":exercise_id, "user_id":user_id})
        return query_result.fetchone()
    except:
        return None
