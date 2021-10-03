from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db


def user_id():
    return session.get("user_id", 0)

def is_admin():
    return session.get("admin", 'false')

def valid_input(input):
    return 1 <= len(input) <= 50

def check(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return bool(user)

def login(username, password):
    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["admin"] = user.admin
        session["username"] = username
        return True
    return False

def register(username, password, teacher):
    hash_value = generate_password_hash(password)
    if teacher == ['1']:
        admin = 'true'
    else:
        admin='false'
    try:
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)"
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]
    del session["admin"]
    del session["username"]
