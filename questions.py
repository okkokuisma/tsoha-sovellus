from db import db

def add_question(question_title,  exercise_id,  choice_question,  answer,  points):
    if not answer:
        return 0
    try:
        sql = "INSERT INTO Questions (question_title, exercise_id, choice_question, answer, points) VALUES (:question_title, :exercise_id, :choice_question, :answer, :points) RETURNING id"
        result = db.session.execute(sql, {"question_title":question_title, "exercise_id":exercise_id, "choice_question":choice_question, "answer":answer, "points":points})
        db.session.commit()
        question_id = result.fetchone()[0]
        return question_id
    except:
        return 0
    
def get_question_list(exercise_id):
    sql = "SELECT * FROM Questions WHERE exercise_id=:id"
    result = db.session.execute(sql, {"id":exercise_id})
    return result.fetchall()
