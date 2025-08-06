from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    activity = db.Column(db.Float)
    bmr = db.Column(db.Float)
    tdee = db.Column(db.Float)
    recommended_calories = db.Column(db.Float)
