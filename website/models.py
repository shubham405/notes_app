from . import db
from sqlalchemy.sql import func
#this is custom class to give user information to log user in
from flask_login import UserMixin

#here each class represent database table
class Notes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    data=db.Column(db.String(50000))
    date=db.Column(db.DateTime(timezone=True),default=func.now())
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))

class User(db.Model,UserMixin):
    #defining schema of user here using python only 
    #col_name=db.Column(db.type,primary_key=True/False)
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    first_name=db.Column(db.String(150))
    last_name=db.Column(db.String(150))
    note=db.relationship('Notes')
