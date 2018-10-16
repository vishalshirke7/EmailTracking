import datetime
from Scripts.Hyrelabs.app.db import db


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(200))
    tokens = db.Column(db.Text)
    sent_mail = db.relationship('Email', backref="user")
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)


class Email(db.Model):

    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, default=datetime.datetime.now)
    read = db.Column(db.Integer, default=0)