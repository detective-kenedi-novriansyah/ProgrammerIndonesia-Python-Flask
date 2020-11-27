# from app import db, login
from app.extension.modules import db, login
from flask_login import UserMixin
from datetime import datetime

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(225), nullable=False)
    profile = db.Column(db.String(225), nullable=True, default="profile.jpg")
    email = db.Column(db.String(225), nullable=True)
    password = db.Column(db.String(225), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    create_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow())
    update_at = db.Column(db.DateTime, nullable=True)

    