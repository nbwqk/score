from datetime import datetime

from flask_login import UserMixin

from exts import db


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(150),nullable=False)
    phone=db.Column(db.String(11),nullable=False,unique=True)
    email=db.Column(db.String(50))
    udatetime=db.Column(db.DateTime,default=datetime.now)
    isforbid=db.Column(db.Boolean,default=0)
    isadmin=db.Column(db.Boolean,default=0)
    exams=db.relationship('Exam',backref='user')

    def __str__(self):
        return self.username

class Clazz(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    c_name=db.Column(db.String(10),nullable=False,unique=True)
    exams=db.relationship('Exam',backref='clazz')

    def __str__(self):
        return self.c_name

class Course(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    cou_name=db.Column(db.String(10),nullable=False,unique=True)
    exams = db.relationship('Exam', backref='course')

    def __str__(self):
        return self.cou_name