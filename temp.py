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

@app.route("/login", methods=["GET", "POST"])
def login():
    user = User.sign_in("Lewis", "lewisluck2003", "lewisluck2003@gmail.com", "Big Daddy")
    login_user(user)
    return render_template("login.html")

@app.route("/login/call", methods=["GET", "POST"])
def call():
    cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    auth_endpoint = cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        auth_endpoint,
        redirect_uri=request.base_url + "/back",
        scope=["openid", "email", "profile"]
    )
    print(request.base_url + "/back")
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
    User.sign_in(unique_id, users_name, users_email, picture)
    return redirect("/profile")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("error.html", message="This page is still in development.", address="/")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if current_user.is_authenticated:
        return (
            "<p>Hello, {}! You're logged in! Email: {}</p>"
            "<div><p>Google Profile Picture:</p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<a class="button" href="/logout">Logout</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    # return render_template("error.html", message="This page is still in development.", address="/")

#if __name__ == "__main__":
 #   app.run(debug=True, ssl_context=("cert.pem", "key.pem"))
