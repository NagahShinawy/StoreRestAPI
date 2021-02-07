from flask_jwt import jwt_required
from flask_jwt_extended import (
    jwt_required as jwt_required_extended,
    get_jwt_claims,
    jwt_refresh_token_required,
    get_jwt_identity, get_raw_jwt,
)
from flask_restful import Resource, reqparse
from src.models.user import UserModel
from src.utils.data import body_values_to_lower
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from src.blacklist import BLACKLIST

# resources is the logical part like views in django
_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username", required=True, type=str, help="username is required"
)
_user_parser.add_argument(
    "password", required=True, type=str, help="password is required"
)


class UserRegister(Resource):  # connect user
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", required=True, type=str, help="username is required"
    )
    parser.add_argument(
        "password", required=True, type=str, help="password is required"
    )

    parser.add_argument("email", required=True, type=str, help="email is required")

    parser.add_argument("country", required=True, type=str, help="country is required")

    def post(self):
        # check unique
        data = (
            UserRegister.parser.parse_args()
        )  # custom validation and parsing to request body
        data = body_values_to_lower(data)
        if UserModel.find_by_username(data["username"]):
            return {"msg": "username already exists"}, 400

        if UserModel.find_by_email(data["email"]):
            return {"msg": "email already exists"}, 400
        data["password"] = generate_password_hash(data.get("password"))
        user = UserModel(
            **data
        )  # ===> username = data.get("username") , password = data.get("password", email=''', country='''')
        user.save_to_db()
        return {"message": "user created", "data": user.to_json()}, 201


class UserList(Resource):
    # @jwt_required()  # for jwt
    @jwt_required_extended  # for jwtManager
    def get(self):
        users = UserModel.query.all()
        return [user.to_json() for user in users]


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", required=True, type=str, help="username is required"
    )

    # @jwt_required()  # for jwt
    @jwt_required_extended  # for jwtManager
    def get(self, username_or_id):
        user_by_name = UserModel.find_by_username(username_or_id)
        user_by_id = UserModel.find_by_id(username_or_id)
        if user_by_name:
            return {"data": user_by_name.to_json()}
        if user_by_id:
            return {"data": user_by_id.to_json()}

        return {"details": f"user '{username_or_id}' not found"}, 404

    # @jwt_required()  # for jwt
    @jwt_required_extended  # for jwtManager
    def delete(self, username_or_id):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"msg": "Admin privilege required"}, 401
        user_by_name = UserModel.find_by_username(username_or_id)
        user_by_id = UserModel.find_by_id(username_or_id)

        if user_by_name:
            user_by_name.delete_from_db()

        if user_by_id:
            user_by_id.delete_from_db()

        if any([user_by_name, user_by_id]):
            return {"details": "user deleted"}, 204

        return {"details": "Not found to delete"}, 404

    @jwt_required()
    def patch(self, username):
        original_user = UserModel.find_by_username(username)
        data = User.parser.parse_args()
        if original_user:

            user = UserModel.find_by_username(data.get("username"))
            if user:
                return {
                    "msg": f"can not update with username '{data.get('username').lower()}'. it is exist"
                }, 400
            original_user.username = data.get("username")
            original_user.save_to_db()
            return {
                "details": f"user updated from '{username}' to '{data.get('username')}'"
            }, 202
        return {"details": f"not found '{data.get('username')}'"}, 404


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = (
            _user_parser.parse_args()
        )  # custom validation and parsing to request body
        if request.is_json:  # check if data comes from json or html form
            data = request.json
        else:
            data = request.form
        username = data.get("username")
        plain_text_password = data.get("password")
        # user = User.query.filter_by(email=email, password=password).first()
        user = UserModel.query.filter_by(username=username).first()
        if user:
            hashed_password = user.password
            if check_password_hash(hashed_password, plain_text_password):
                access_token = create_access_token(
                    identity=username,
                    fresh=True,
                    expires_delta=datetime.timedelta(minutes=15),
                )
                refresh_token = create_refresh_token(identity=username)
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }, 200
        return {"msg": "invalid credentials"}, 401  # mean permissions denied


class UserLogout(Resource):

    @jwt_required_extended
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user, fresh=False)
        return {"new_access_token": new_access_token}, 200
