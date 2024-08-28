from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # `tasks = db.relationship('Task', backref='owner', lazy=True)` creates a link to all tasks of a person,
    # labels each task with the owner, and only fetches tasks when needed.
    tasks = db.relationship('Task', backref='owner', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
