import sqlite3
from flask_restful import Resource, reqparse
from src.models.user import UserModel

# resources is the logical part like views in django


class UserRegister(Resource):  # connect user
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", required=True, type=str, help="username is required"
    )
    parser.add_argument(
        "password", required=True, type=str, help="password is required"
    )

    def post(self):
        # check unique
        data = (
            UserRegister.parser.parse_args()
        )  # custom validation and parsing to request body
        if UserModel.find_by_username(data["username"]):
            return {"msg": "username already exists"}, 400

        user = UserModel(
            **data
        )  # ===> username = data.get("username") , password = data.get("password")
        user.save_to_db()
        return {"message": "user created"}, 201


class UserList(Resource):
    def get(self):
        users = UserModel.query.all()
        return [{"id": user.id, "username": user.username} for user in users]
