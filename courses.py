from flask import session
from db import db

def get_active_courses():
    sql = "SELECT id, name, visible FROM courses WHERE visible = true"
    result = db.session.execute(sql)
    courses = result.fetchall()
    return courses

def get_course(course_id):
    print(course_id)
    sql = "SELECT id, name, visible FROM courses WHERE id=:course_id"
    result = db.session.execute(sql, {"course_id":course_id})
    course = result.fetchone()
    print(course)
    if course:
        session["course_id"] = course.id
        return course
    return None

def add_course(name):
    visible = 'true'
    try:
        sql = "INSERT INTO courses (name, visible) VALUES (:name, :visible)"
        db.session.execute(sql, {"name":name, "visible":visible})
        db.session.commit()
    except:
        return False
    return True

def delete_course(course_id):
    try:
        sql = "UPDATE courses SET visible='f' WHERE id=:course_id"
        db.session.execute(sql, {"course_id":course_id})
        db.session.commit()
    except:
        return False
    del session["course_id"]
    return True

def check_if_user_in_course(user_id, course_id):
    sql = "SELECT id FROM courseusers WHERE user_id=:user_id AND course_id=:course_id"
    result = db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
    check = result.fetchone()
    if check:
        return True
    return False

def add_user_to_course(user_id, course_id):
    try:
        sql = """INSERT INTO courseusers (user_id, course_id) VALUES (:user_id, :course_id)
                 ON CONFLICT DO NOTHING"""
        db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
        db.session.commit()
    except:
        return False
    return True

def remove_user_from_course(user_id, course_id):
    print(course_id, user_id)
    try:
        sql = "DELETE FROM courseusers WHERE course_id=:course_id AND user_id=:user_id"
        db.session.execute(sql, {"user_id":user_id, "course_id":course_id})
        db.session.commit()
    except:
        return False
    return True

def add_textmaterial(course_id, textmaterial):
    try:
        sql = """INSERT INTO textmaterials (course_id, textmaterial)
                 VALUES (:course_id, :textmaterial)"""
        db.session.execute(sql, {"course_id":course_id, "textmaterial":textmaterial})
        db.session.commit()
    except:
        return False
    return True

def get_latest_textmaterial(course_id):
    sql = "SELECT textmaterial FROM textmaterials WHERE course_id=:course_id ORDER BY id DESC"
    result = db.session.execute(sql, {"course_id":course_id})
    material = result.fetchone()
    return material
