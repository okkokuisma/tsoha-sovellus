from db import db

def add_answer(answer,  question_id,  user_id):
    sql = "INSERT INTO Answers (answer, question_id, user_id) VALUES (:answer, :question_id, :user_id)"
    db.session.execute(sql, {"answer":answer, "question_id":question_id,  "user_id":user_id})
    db.session.commit()

def get_answers(exercise_id,  user_id):
    sql = "SELECT Q.question_title, Q.answer, A.answer FROM Questions Q, Answers A WHERE Q.id=A.question_id AND A.user_id=:user_id AND Q.exercise_id=:exercise_id"
    query_result = db.session.execute(sql, {"user_id":user_id,  "exercise_id":exercise_id})
    return query_result.fetchall()
