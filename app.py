from flask import Flask, render_template, request, session

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("homepage.html")

@app.route("/play", methods=["GET", "POST"])
def play():
    if request.method == "GET":
        return render_template("start.html")
    else:
        if not request.form.get("difficulty"):
            return render_template("error.html", message="Please select a valid difficulty!", address="/play")
        else:
            return render_template("play.html", d=int(request.form.get("difficulty")))

@app.route("/scores")
def scores():
    return render_template("error.html", message="This page is still in development.", address="/")

@app.route("/login")
def login():
    return render_template("error.html", message="This page is still in development.", address="/")

@app.route("/register")
def register():
    return render_template("error.html", message="This page is still in development.", address="/")
