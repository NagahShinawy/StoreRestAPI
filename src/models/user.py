from sqlalchemy.orm import validates
from sqlalchemy import func
from src.db import db
from sqlalchemy_utils import EmailType


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = db.Column(EmailType)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def find_by_username(cls, username):
        # cls.query = query builder
        user = cls.query.filter_by(
            username=func.lower(username)
        )  # case-insensitive-flask-sqlalchemy-query
        # user = cls.query.filter_by(username=UserModel.username.ilike(username))
        if user:
            return user.first()

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=func.lower(email))
        if user:
            return user.first()

    @classmethod
    def find_by_id(cls, user_id):
        # cls.query = query builder
        user = cls.query.filter_by(id=user_id)
        if user:
            return user

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @validates("username")
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError("username must be at least 3 chars")

        if len(username) > 20:
            raise ValueError("username must be max 20 chars")
        return username

    def to_json(self):
        return {"userid": self.id, "username": self.username, "email": self.email}

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
