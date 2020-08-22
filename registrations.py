from db import db

def add_registration(user_id,  course_id):
    sql = "INSERT INTO registrations (user_id, course_id) VALUES (:user_id, :course_id)"
    db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
    db.session.commit()
    
def check_registration(user_id,  course_id):
    sql = "SELECT id FROM registrations WHERE user_id=:user_id AND course_id=:course_id"
    query_result = db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
    if query_result.fetchone() == None:
        return False
    return True
    
