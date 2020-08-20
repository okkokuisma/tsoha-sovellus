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

def hide_question(question_id):
    sql = "UPDATE Questions SET visible=0 WHERE id=:id"
    db.session.execute(sql, {"id":question_id})
    db.session.commit()
    
def get_question_list(exercise_id):
    sql = "SELECT id, question_title, choice_question, answer, points FROM Questions WHERE exercise_id=:id AND visible=1"
    result = db.session.execute(sql, {"id":exercise_id})
    return result.fetchall()
