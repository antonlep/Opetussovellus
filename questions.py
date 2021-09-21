from db import db
from flask import session

def get_active_textquestions(course_id):
    sql = "SELECT id, question, answer FROM textquestions WHERE course_id=:course_id AND visible=true "
    result = db.session.execute(sql, {"course_id":course_id})
    questions = result.fetchall()
    return questions

def get_correct_answers(course_id, user_id):
    sql = """SELECT COUNT(*) FROM textquestions C LEFT JOIN textanswers D
            on C.id = D.question_id WHERE D.id IN (SELECT MAX(B.id) FROM textquestions A LEFT JOIN textanswers B
            ON A.id = B.question_id WHERE A.course_id=:course_id GROUP BY B.question_id) AND user_id=:user_id AND C.answer = D.answer"""
    result = db.session.execute(sql, {"course_id":course_id, "user_id":user_id})
    correct_answers = result.fetchone()[0]
    return correct_answers

def add_textquestion(course_id, question, answer):
    visible = 'true'
    try:
        sql = "INSERT INTO textquestions (course_id, question, answer, visible) VALUES (:course_id, :question, :answer, :visible)"
        db.session.execute(sql, {"course_id":course_id, "question":question, "answer":answer, "visible":visible})
        db.session.commit()
    except:
        return False
    return True

def add_textanswer(user_id, question_id, answer):
    try:
        sql = "INSERT INTO textanswers (user_id, question_id, answer, time) VALUES (:user_id, :question_id, :answer, NOW())"
        db.session.execute(sql, {"user_id":user_id, "question_id":question_id, "answer":answer})
        db.session.commit()
    except:
        return False
    return True

def delete_textquestion(id):
    try:
        sql = "UPDATE textquestions SET visible='f' WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
    except:
        return False
    return True
