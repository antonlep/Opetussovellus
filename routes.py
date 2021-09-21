from app import app
from flask import redirect, render_template, request, session
import users, courses, questions

@app.route("/")
def index():
    course_list = courses.get_active_courses()
    return render_template("index.html", courses=course_list)

@app.route("/courses/<int:id>")
def course_pages(id):
    user_id = session["user_id"]
    course = courses.get_course(id)
    textmaterial = courses.get_latest_textmaterial(id)
    textquestions = questions.get_active_textquestions(id)
    textanswers = questions.get_textanswers(id, user_id)
    print(checked_questions)
    if course:
        return render_template("course.html", course=course, textmaterial=textmaterial, textquestions=textquestions)
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

@app.route("/add_textquestion", methods=["POST"])
def add_textquestion():
    textquestion = request.form["textquestion"]
    textanswer = request.form["textanswer"]
    course_id = session["course_id"]
    if questions.add_textquestion(course_id, textquestion, textanswer):
        return redirect(f"/courses/{course_id}")
    else:
        return render_template("error.html", message="Kysymyksen lisääminen ei onnistu")

@app.route("/delete_textquestion", methods=["POST"])
def delete_textquestion():
    course_id = session["course_id"]
    question_id = request.form["question_id"]
    if questions.delete_textquestion(question_id):
        return redirect(f"/courses/{course_id}")
    else:
        return render_template("error.html", message="Kysymyksen poistaminen ei onnistu")

@app.route("/answer_textquestion", methods=["POST"])
def answer_textquestion():
    course_id = session["course_id"]
    user_id = session["user_id"]
    question_id = request.form["question_id"]
    answer = request.form["textanswer"]
    if questions.add_textanswer(user_id, question_id, answer):
        return redirect(f"/courses/{course_id}")
    else:
        return render_template("error.html", message="Vastaaminen ei onnistu")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")