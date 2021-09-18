from flask import Flask
from flask import render_template
from os import getenv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")