from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

# User Model
class User(db.Model):
    id = db.Column(db.String(11), primary_key=True, default=get_uuid)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Category Model
class Category(db.Model):
    id = db.Column(db.String(11), primary_key=True, default=get_uuid)
    name = db.Column(db.String(100), unique=True, nullable=False)
    expenses = db.relationship('Expense', backref='category', lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"

# Expense Model
class Expense(db.Model):
    id = db.Column(db.String(11), primary_key=True, default=get_uuid)
    name = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f"Expense('{self.name}', '{self.amount}', '{self.date}')"