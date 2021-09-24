from db import db
from flask import session

def get_active_textquestions(course_id):
    sql = "SELECT id, question, answer FROM textquestions WHERE course_id=:course_id AND visible=true "
    result = db.session.execute(sql, {"course_id":course_id})
    questions = result.fetchall()
    return questions

def get_active_courses():
    sql = "SELECT id, name FROM courses WHERE visible = true "
    result = db.session.execute(sql)
    courses = result.fetchall()
    return courses

def get_correct_answers(course_id, user_id):
    sql = """SELECT COUNT(*) FROM textquestions C LEFT JOIN textanswers D
            on C.id = D.question_id WHERE D.id IN (SELECT MAX(B.id) FROM textquestions A LEFT JOIN textanswers B
            ON A.id = B.question_id WHERE A.course_id=:course_id GROUP BY B.question_id) AND user_id=:user_id AND C.answer = D.answer"""
    result = db.session.execute(sql, {"course_id":course_id, "user_id":user_id})
    correct_answers = result.fetchone()[0]
    return correct_answers

def get_number_of_questions_by_course():
    sql = """SELECT Q.id, Q.name, COUNT(*) FROM courses Q LEFT JOIN textquestions Z ON Q.id = Z.course_id WHERE Q.visible = true AND
            COALESCE(Z.visible, true) = true GROUP BY Q.id"""
    result = db.session.execute(sql)
    questions = result.fetchall()
    return questions

def get_number_of_points_by_course(user_id):
    sql = """SELECT Q.id, Q.name, COALESCE(X.count,0) sum FROM courses Q LEFT JOIN (SELECT A.id, A.name, COUNT(*) FROM courses A 
            LEFT JOIN textquestions B ON A.id = B.course_id WHERE B.id IN (SELECT B.id FROM textquestions B 
            LEFT JOIN textanswers C ON B.id = C.question_id WHERE B.visible = true AND user_id = :user_id AND B.answer = C.answer GROUP BY B.id)
            GROUP BY A.id) X ON Q.id = X.id WHERE Q.visible = true"""
    result = db.session.execute(sql, {"user_id":user_id})
    answers = result.fetchall()
    return answers

def get_statistics_for_all_courses(user_id):
    sql = """SELECT Q.id, Q.name, MAX(COALESCE(X.count,0)) correct, COUNT(Z.id) questions FROM courses Q LEFT JOIN (SELECT A.id, A.name, COUNT(*) FROM courses A
            LEFT JOIN textquestions B ON A.id = B.course_id WHERE B.id IN (SELECT B.id FROM textquestions B
            LEFT JOIN textanswers C ON B.id = C.question_id WHERE B.visible = true AND user_id = :user_id AND B.answer = C.answer GROUP BY B.id)
            GROUP BY A.id) X ON Q.id = X.id LEFT JOIN textquestions Z ON Q.id = Z.course_id WHERE Q.visible = true AND COALESCE(Z.visible, true) = true
            GROUP BY Q.id"""
    result = db.session.execute(sql, {"user_id":user_id})
    answers = result.fetchall()
    return answers

def get_statistics_for_one_course(user_id, course_id):
    sql = """SELECT Q.id, Q.name, MAX(COALESCE(X.count,0)) correct, COUNT(Z.id) questions FROM courses Q LEFT JOIN (SELECT A.id, A.name, COUNT(*) FROM courses A
            LEFT JOIN textquestions B ON A.id = B.course_id WHERE B.id IN (SELECT B.id FROM textquestions B
            LEFT JOIN textanswers C ON B.id = C.question_id WHERE B.visible = true AND user_id = :user_id AND B.answer = C.answer GROUP BY B.id)
            GROUP BY A.id) X ON Q.id = X.id LEFT JOIN textquestions Z ON Q.id = Z.course_id WHERE Q.id = :course_id AND Q.visible = true AND COALESCE(Z.visible, true) = true
            GROUP BY Q.id"""
    result = db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
    answers = result.fetchone()
    return answers

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
