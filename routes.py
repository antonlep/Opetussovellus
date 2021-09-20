from app import app
from flask import redirect, render_template, request, session
import users, courses

@app.route("/")
def index():
    course_list = courses.get_courses()
    visible_course_list = [c for c in course_list if c.visible == True]
    return render_template("index.html", courses=visible_course_list)

@app.route("/courses/<int:id>")
def course_pages(id):
    course = courses.get_course(id)
    textmaterial = courses.get_latest_textmaterial(id)
    if course:
        return render_template("course.html", course=course, textmaterial=textmaterial)
    else:
        return render_template("error.html", message="Kurssia ei löydy")

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

@app.route("/delete_course")
def delete_course():
    if courses.delete_course(session["course_id"]):
        return redirect("/")
    else:
        return render_template("error.html", message="Kurssin lisääminen ei onnistu")

@app.route("/add_textmaterial", methods=["POST"])
def add_textmaterial():
    textmaterial = request.form["textmaterial"]
    course_id = session["course_id"]
    if courses.add_textmaterial(course_id, textmaterial):
        return redirect(f"/courses/{course_id}")
    else:
        return render_template("error.html", message="Materiaalin lisääminen ei onnistu")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")