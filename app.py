# Flask libraries
from flask import Flask, render_template, request, url_for, redirect
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import yagmail

# Standard libraries
import os
import sqlite3
import json

# user and db management
import db
from user import User

# Config for Google login
GOOGLE_CLIENT_ID = "699163467220-8nqbu924qosnuhv94q21fc6pl090ugo3.apps.googleusercontent.com" #os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = "pvIJpV8r4Y9zUVS62-6fx37i" #os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# OAuth setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/login"

@login_manager.user_loader
def get_user(user_id):
    return User.get(user_id)

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
@login_required
def scores():
    return render_template("error.html", message="This page is still in development.", address="/")

@app.route("/login/call", methods=["GET", "POST"])
def call():
    cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    auth_endpoint = cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        auth_endpoint,
        redirect_uri=request.base_url + "/back",
        scope=["openid", "email", "profile"]
    )
    return redirect(request_uri)

@app.route("/login/call/back", methods=["GET", "POST"])
def callback():
    code = request.args.get("code")
    cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers = headers, data = body)
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return render_template("error.html", message="User email not available or not verified by Google.", address="/login")
    print(unique_id, users_name, users_email, picture)
    login_user(User.sign_in(users_name, users_email, picture, unique_id))
    return redirect("/profile")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        if not (username and password and email):
            return render_template("error.html", message="Please enter a valid email, username and password to sign up.", address="/register")
        user = User.check_username(username)
        print(user)
        if user:
            return render_template("error.html", message="Another account already uses this username.", address="/register")
        else:
            User.create(username, email, hash=generate_password_hash(password))
            login_user(User.check_username(username))
            yagmail.SMTP("lewisjluck@gmail.com").send(to=user.email, subject="Thanks for signing up to Minesweeper!", contents=f"Hi, {{user.username}}. Thanks for signing up to Minesweeper! We hope to see you playing soon!")
            return redirect("/profile")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("confirm")
        if not (username and password):
            return render_template("error.html", message="Please enter a valid username and password to login.", address="/login")
        user = User.check_username(username)
        if user and check_password_hash(user.hash, password):
            login_user(user)
            return redirect("/profile")
        else:
            return render_template("error.html", message="Incorrect Password.", address="/login")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        return render_template("profile.html")
    else:
        logout_user()
        return redirect("/")

if __name__ == "__main__":
   app.run(debug=True)
