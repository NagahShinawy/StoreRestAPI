from sqlalchemy.orm import validates

from src.db import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        # cls.query = query builder
        user = cls.query.filter_by(username=username)
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
