from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def get_courses():
    sql = "SELECT id, name, visible FROM courses"
    result = db.session.execute(sql)
    courses = result.fetchall()
    if courses:
        return courses 
    else:
        return []

def get_course(id):
    sql = "SELECT id, name, visible FROM courses WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    course = result.fetchone()
    if course:
        session["course_id"] = course.id
        return course 
    else:
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

def delete_course(id):
    try:
        sql = "UPDATE courses SET visible='f' WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
    except:
        return False
    del session["course_id"]
    return True

def add_textmaterial(course_id, textmaterial):
    try:
        sql = "INSERT INTO textmaterials (course_id, textmaterial, time) VALUES (:course_id, :textmaterial, NOW())"
        db.session.execute(sql, {"course_id":course_id, "textmaterial":textmaterial})
        db.session.commit()
    except:
        return False
    return True

def get_latest_textmaterial(course_id):
    sql = "SELECT textmaterial FROM textmaterials WHERE course_id=:course_id ORDER BY time DESC"
    result = db.session.execute(sql, {"course_id":course_id})
    material = result.fetchone()
    if material:
        return material
    else:
        return ""


