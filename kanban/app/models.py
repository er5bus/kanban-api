from . import db
from sqlalchemy.orm import validates


class Task(db.Model):
    __tablename__ = 'tasks'
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    status = db.Column(db.String(200))


class Analytics(db.Model):
    __tablename__ = 'analytics'
    _id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.Text, nullable=True)
    data = db.Colmun(db.PickleType, nullable=True)
