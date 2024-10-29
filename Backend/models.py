from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, joinedload, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, ForeignKey, select

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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    flag = db.Column(db.Boolean, default = False)  # in/out flag switch
    
    # Define the back reference to Users
    user = db.relationship("Users", back_populates="location")
