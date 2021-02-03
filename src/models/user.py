from sqlalchemy.orm import validates
from sqlalchemy import func
from src.db import db
from sqlalchemy_utils import EmailType
import sqlalchemy as sa
from src.validators import users


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    email = sa.Column(EmailType)
    country = db.Column(db.String(80))

    def __init__(self, username, password, email, country):
        self.username = username
        self.password = password
        self.email = email
        self.country = country

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
        response_data = {"userid": self.id, "username": self.username, "email": self.email}
        country = users.validate_country(self.country)
        if country is not None:
            response_data.update({"country": {"code": country[0], "name": country[1]}})
            return response_data
        return response_data

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
