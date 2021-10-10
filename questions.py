from db import db

def get_active_textquestions(course_id):
    sql = """SELECT id, question, answer FROM textquestions WHERE course_id=:course_id
             AND visible=true"""
    result = db.session.execute(sql, {"course_id":course_id})
    questions = result.fetchall()
    return questions

def get_active_multiquestions(course_id):
    sql = """SELECT id, question, choice1, choice2, choice3, answer
             FROM multiplechoicequestions WHERE course_id=:course_id
             AND visible=true"""
    result = db.session.execute(sql, {"course_id":course_id})
    questions = result.fetchall()
    return questions

def get_active_courses():
    sql = "SELECT id, name FROM courses WHERE visible = true "
    result = db.session.execute(sql)
    courses = result.fetchall()
    return courses

def get_statistics_for_all_courses(user_id):
    tables = [("textquestions", "textanswers"),
             ("multiplechoicequestions", "multiplechoiceanswers")]
    statistics = {}
    for table in tables:
        sql = f"""SELECT Q.id,
                        Q.name,
                        MAX(COALESCE(X.count,0)) correct,
                        COUNT(Z.id) questions
                FROM courses Q
            LEFT JOIN     (SELECT A.id,
                                    A.name,
                                    COUNT(*)
                            FROM courses A
                        LEFT JOIN {table[0]} B
                                ON A.id = B.course_id
                            WHERE B.id
                                IN    (SELECT B.id
                                        FROM {table[0]} B
                                    LEFT JOIN {table[1]} C
                                            ON B.id = C.question_id
                                        WHERE B.visible = true
                                        AND user_id = :user_id
                                        AND B.answer = C.answer
                                    GROUP BY B.id)
                        GROUP BY A.id) X
                    ON Q.id = X.id
            LEFT JOIN {table[0]} Z
                    ON Q.id = Z.course_id
                WHERE Q.visible = true
                    AND COALESCE(Z.visible, true) = true
            GROUP BY Q.id"""
        result = db.session.execute(sql, {"user_id":user_id})
        answers = result.fetchall()
        for i in answers:
            if i.name not in statistics:
                statistics[i.name] = [i.correct, i.questions]
            else:
                statistics[i.name][0] += i.correct
                statistics[i.name][1] += i.questions
    return statistics

def get_statistics_for_one_course(user_id, course_id):
    sql = """SELECT Q.id,
                    Q.name,
                    MAX(COALESCE(X.count,0)) correct,
                    COUNT(Z.id) questions
               FROM courses Q
          LEFT JOIN     (SELECT A.id,
                                A.name,
                                COUNT(*)
                           FROM courses A
                      LEFT JOIN textquestions B
                             ON A.id = B.course_id
                          WHERE B.id 
                             IN        (SELECT B.id
                                          FROM textquestions B
                                     LEFT JOIN textanswers C
                                            ON B.id = C.question_id
                                         WHERE B.visible = true
                                           AND user_id = :user_id
                                           AND B.answer = C.answer
                                      GROUP BY B.id)
                       GROUP BY A.id) X
                 ON Q.id = X.id
          LEFT JOIN textquestions Z
                 ON Q.id = Z.course_id
              WHERE Q.id = :course_id
                AND Q.visible = true 
                AND COALESCE(Z.visible, true) = true
           GROUP BY Q.id"""
    result = db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
    answers = result.fetchone()
    return answers

def get_multistatistics_for_all_courses(user_id):
    sql = """SELECT Q.id,
                    Q.name,
                    MAX(COALESCE(X.count,0)) correct,
                    COUNT(Z.id) questions
               FROM courses Q
          LEFT JOIN     (SELECT A.id,
                                A.name,
                                COUNT(*)
                           FROM courses A
                      LEFT JOIN multiplechoicequestions B
                             ON A.id = B.course_id
                          WHERE B.id
                             IN    (SELECT B.id
                                      FROM multiplechoicequestions B
                                 LEFT JOIN multiplechoiceanswers C
                                        ON B.id = C.question_id
                                     WHERE B.visible = true
                                       AND user_id = :user_id
                                       AND B.answer = C.answer
                                  GROUP BY B.id)
                       GROUP BY A.id) X
                 ON Q.id = X.id
          LEFT JOIN multiplechoicequestions Z
                 ON Q.id = Z.course_id
              WHERE Q.visible = true
                AND COALESCE(Z.visible, true) = true
           GROUP BY Q.id"""
    result = db.session.execute(sql, {"user_id":user_id})
    answers = result.fetchall()
    return answers

def get_multistatistics_for_one_course(user_id, course_id):
    sql = """SELECT Q.id,
                    Q.name,
                    MAX(COALESCE(X.count,0)) correct,
                    COUNT(Z.id) questions
               FROM courses Q
          LEFT JOIN     (SELECT A.id,
                                A.name,
                                COUNT(*)
                           FROM courses A
                      LEFT JOIN multiplechoicequestions B
                             ON A.id = B.course_id
                          WHERE B.id 
                             IN        (SELECT B.id
                                          FROM multiplechoicequestions B
                                     LEFT JOIN multiplechoiceanswers C
                                            ON B.id = C.question_id
                                         WHERE B.visible = true
                                           AND user_id = :user_id
                                           AND B.answer = C.answer
                                      GROUP BY B.id)
                       GROUP BY A.id) X
                 ON Q.id = X.id
          LEFT JOIN multiplechoicequestions Z
                 ON Q.id = Z.course_id
              WHERE Q.id = :course_id
                AND Q.visible = true 
                AND COALESCE(Z.visible, true) = true
           GROUP BY Q.id"""
    result = db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
    answers = result.fetchone()
    return answers

def add_textquestion(course_id, question, answer):
    visible = 'true'
    try:
        sql = """INSERT INTO textquestions (course_id, question, answer, visible)
                 VALUES (:course_id, :question, :answer, :visible)"""
        db.session.execute(sql, {"course_id":course_id, "question":question, "answer":answer,
                                 "visible":visible})
        db.session.commit()
    except:
        return False
    return True

def add_textanswer(user_id, question_id, answer):
    try:
        sql = """INSERT INTO textanswers (user_id, question_id, answer, time)
                 VALUES (:user_id, :question_id, :answer, NOW())"""
        db.session.execute(sql, {"user_id":user_id, "question_id":question_id, "answer":answer})
        db.session.commit()
    except:
        return False
    return True

def delete_textquestion(question_id):
    try:
        sql = "UPDATE textquestions SET visible='f' WHERE id=:question_id"
        db.session.execute(sql, {"question_id":question_id})
        db.session.commit()
    except:
        return False
    return True

def add_multiquestion(course_id, question, choice1, choice2, choice3, answer):
    print(course_id, question, choice1, choice2, choice3, answer)
    visible = 'true'
    try:
        sql = """INSERT INTO multiplechoicequestions
                 (course_id, question, choice1, choice2, choice3, answer, visible)
                 VALUES (:course_id, :question, :choice1, :choice2, :choice3, :answer, :visible)"""
        db.session.execute(sql, {"course_id":course_id, "question":question, "choice1":choice1,
                                 "choice2":choice2, "choice3":choice3, "answer":answer,
                                 "visible":visible})
        db.session.commit()
    except:
        return False
    return True

def add_multianswer(user_id, question_id, answer):
    try:
        sql = """INSERT INTO multiplechoiceanswers (user_id, question_id, answer, time)
                 VALUES (:user_id, :question_id, :answer, NOW())"""
        db.session.execute(sql, {"user_id":user_id, "question_id":question_id, "answer":answer})
        db.session.commit()
    except:
        return False
    return True

def delete_multiquestion(question_id):
    try:
        sql = "UPDATE multiplechoicequestions SET visible='f' WHERE id=:question_id"
        db.session.execute(sql, {"question_id":question_id})
        db.session.commit()
    except:
        return False
    return True
