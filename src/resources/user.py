from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from src.models.user import UserModel
from src.utils.data import body_values_to_lower

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
        data = body_values_to_lower(data)
        if UserModel.find_by_username(data["username"]):
            return {"msg": "username already exists"}, 400

        user = UserModel(
            **data
        )  # ===> username = data.get("username") , password = data.get("password")
        user.save_to_db()
        return {"message": "user created"}, 201


class UserList(Resource):

    @jwt_required()
    def get(self):
        users = UserModel.query.all()
        return [user.to_json() for user in users]


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", required=True, type=str, help="username is required"
    )

    @jwt_required()
    def get(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return {"data": user.to_json()}
        return {"details": f"user '{username}' not found"}, 404

    @jwt_required()
    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user:
            user.delete_from_db()
            return {"details": "user deleted"}, 204
        return {"details": "Not found to delete"}, 404

    @jwt_required
    def patch(self, username):
        original_user = UserModel.find_by_username(username)
        data = User.parser.parse_args()
        if original_user:

            user = UserModel.find_by_username(data.get("username"))
            if user:
                return {"msg": f"can not update with username '{data.get('username').lower()}'. it is exist"}, 400
            original_user.username = data.get("username")
            original_user.save_to_db()
            return {"details": f"user updated from '{username}' to '{data.get('username')}'"}, 202
        return {"details": f"not found '{data.get('username')}'"}, 404