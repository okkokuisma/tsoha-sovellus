from db import db

def add_choice(choice_title,  question_id):
    sql = "INSERT INTO Choices (choice_title, question_id) VALUES (:choice_title, :question_id)"
    db.session.execute(sql, {"choice_title":choice_title, "question_id":question_id})
    db.session.commit()
    
def get_choices_by_question(question_id):
    sql = "SELECT id, choice_title FROM Choices WHERE question_id=:id"
    result = db.session.execute(sql, {"id":question_id})
    return result.fetchall()
