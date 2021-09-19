from app import app
from flask import redirect, render_template, request, session
import users, courses

@app.route("/")
def index():
    course_names = courses.get_courses()
    return render_template("index.html", courses=course_names)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        teacher = request.form.getlist("teacher")
        print(teacher)
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.check(username):
            return render_template("error.html", message="Käyttäjätunnus on jo olemassa")
        if users.register(username, password1, teacher):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/add_course", methods=["POST"])
def add_course():
    course_name = request.form["course_name"]
    if courses.add_course(course_name):
        return redirect("/")
    else:
        return render_template("error.html", message="Kurssin lisääminen ei onnistu")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")