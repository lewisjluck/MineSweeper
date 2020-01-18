from flask_login import UserMixin, login_user, current_user
import sqlite3
from db import get_db, close_db

class User(UserMixin):
    def __init__(self, id_, username, email, profile_pic=None, hash=None, google_id=None):
        self.id = id_
        self.username = username
        self.email = email
        self.profile_pic = profile_pic or None
        self.hash = hash or None
        self.google_id = google_id or None

    @staticmethod
    def get(user_id):
        db = get_db()
        google_user = db.execute("SELECT * FROM users WHERE google_id = ?", (str(user_id),)).fetchone()
        if not google_user:
            user = db.execute("SELECT * FROM users WHERE id = ?", (str(user_id),)).fetchone()
            if not user:
                return None
            else:
                user = User(
                    id_ = user[0],
                    username=user[1],
                    email=user[2],
                    profile_pic=user[3],
                    hash=user[4]
                )
                return user
        else:
            user = User(
                id_ = user[0],
                username=user[1],
                email=user[2],
                profile_pic=user[3],
                google_id=user[5]
                )
            return user
        close_db()

    @staticmethod
    def create(username, email, profile_pic=None, hash=None, google_id=None,):
        db = get_db()
        db.commit()
        db.execute("INSERT INTO users (username, email, profile_pic, hash, google_id) VALUES (?, ?, ?, ?, ?)", (username, email, profile_pic, hash, google_id,))
        user = User.check_username(username)
        db.commit()
        return user

    @staticmethod
    def sign_in(username, email, pic, hash=None, id=None):
        if not User.get(id):
            id = User.create(username, email, pic, hash, id)
        return User(id, username, email, pic)

    @staticmethod
    def check_username(username):
        db = get_db()
        db.commit()
        result = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        print(result[0])
        if len(result) > 0:
            print(User.get(result[0]))
            return User.get(result[0])
        else:
            return None
