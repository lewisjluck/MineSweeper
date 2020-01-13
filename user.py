from flask_login import UserMixin, login_user, current_user
import sqlite3
from db import get_db

class User(UserMixin):
    def __init__(self, id_, username, email, profile_pic, hash=None):
        self.id = id_
        self.username = username
        self.email = email
        self.profile_pic = profile_pic
        self.hash = hash

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if not user:
            return None
        user = User(
            id_ = user[0],
            username=user[1],
            email=user[2],
            profile_pic=user[3] or None,
            hash=user[4] or None
        )
        return user

    @staticmethod
    def create(id_, username, email, profile_pic=None, hash=None):
        db = get_db()
        db.commit()
        db.execute("INSERT INTO users (id, username, email, profile_pic, hash) VALUES (?, ?, ?, ?, ?)", (id_, username, email, profile_pic, hash,))
        db.commit()

    @staticmethod
    def sign_in(id, username, email, pic):
        if not User.get(id):
            User.create(id, username, email, pic)
            db.execute("SELECT * FROM users WHERE id=?")
        return User(id, username, email, pic)
