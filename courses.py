from db import db
from flask import session

def get_active_courses():
    sql = "SELECT id, name, visible FROM courses WHERE visible = true"
    result = db.session.execute(sql)
    courses = result.fetchall()
    return courses 

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
        sql = "INSERT INTO textmaterials (course_id, textmaterial) VALUES (:course_id, :textmaterial)"
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




