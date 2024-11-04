import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, joinedload, Mapped, mapped_column
from sqlalchemy import DateTime, Integer, String, Boolean, ForeignKey, func, select

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    username = db.Column(db.String)
    role = db.Column(db.String)
    active = db.Column(db.Boolean)
    
    # One-to-one relationship with userInOrOut
    location = db.relationship(
        "userInOrOut", back_populates="user", uselist=False
    )

class TokenBlacklist(db.Model):
    __tablename__ = 'token_blacklist'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String)

class userInOrOut(db.Model):
    __tablename__ = 'user_in_or_out'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.username"))
    flag = db.Column(db.Boolean, default=False)  # in/out flag switch
    time = db.Column(DateTime, default=func.now())  # Log the recognition time by default
    
    # Define the back reference to Users
    user = db.relationship("Users", back_populates="location")

class RecognitionLog(db.Model):
    __tablename__ = 'recognition_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("users.username"))
    recognition_time = db.Column(DateTime, default=datetime.now)