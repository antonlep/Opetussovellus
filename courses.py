from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def get_courses():
    sql = "SELECT name, visible FROM courses"
    result = db.session.execute(sql)
    courses = result.fetchall()
    if courses:
        return courses 
    else:
        return []

def add_course(name):
    visible = 'true'
    try:
        sql = "INSERT INTO courses (name, visible) VALUES (:name, :visible)"
        db.session.execute(sql, {"name":name, "visible":visible})
        db.session.commit()
    except:
        return False
    return True

