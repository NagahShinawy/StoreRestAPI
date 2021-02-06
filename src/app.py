from flask import Flask, jsonify
from flask_restful import Api
from src.resources.items import Item, ItemsList, CreateItem
from src.resources.user import UserRegister, UserList, User, UserLogin, TokenRefresh
from src.resources.store import StoreList, CreateStore, Store
from src.resources.student import Student
from flask_jwt_extended import JWTManager
from src.common.constant import ADMIN_USERNAME
# from src.utils.admin import is_admin
# from flask_jwt import JWT
# from src.security import authenticate, identity  # old way for auth and identity
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False  # to avoid taking much resource (turn off SQlAlchemy modification tracker

app.config["PROPAGATE_EXCEPTIONS"] = True  # show error details
app.config["JWT_SECRET_KEY"] = "changeme"
# app.config["SECRET_KEY"] = "changeme"  default if you don't use JWT_SECRET_KEY

dev_db = "sqlite:///" + os.path.join(basedir, "data.db")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", dev_db
)  # comes from production Heroku config vars


app.secret_key = "SECRET-KEY"

api = Api(
    app, prefix="/api/v1"
)  # The main entry point for the application. (routes) (endpoints)


# just like the line ==> 44 ==> with app.app_context()  ==> no need to call function manual.


# jwt = JWT(app, authenticate, identity)  # generate ==> BASE_URL/auth endpoint  (old way)
jwt = JWTManager(
    app
)  # generate ==> you have to create your endpoint by your self ==> /login (new way). it authenticates the user


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    """adding more info (claims) to jwt
    check with jwt.io to see jwt more info that you add it like "is_admin"
    """
    if os.environ.get("admin") == identity:  # change hard coding
        return {"is_admin": True, "full_access": True}
    return {"is_admin": False, "full_access": False}


@jwt.expired_token_loader
def expired_token_callback():
    """
    custom json response when token was expired
    :return:
    """
    return (
        jsonify({"description": "the token Was expired", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """
    custom json response when token is invalid
    :return:
    """
    return (
        jsonify(
            {"description": "Signature verification failed", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    """
    custom json response when no jwt added to request
    :return:
    """
    return (
        jsonify({"description": "Request does't not contain access token", "error": "unauthorized_required"}),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    """
    custom json response when jwt not fresh
    :return:
    """
    return (
        jsonify({"description": "The token is not fresh", "error": "fresh_token_required"}),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    """
    custom json response when jwt
    :return:
    """
    return (
        jsonify({"description": "The token has been revoked", "error": "token_revoked"}),
        401,
    )


if __name__ == "__main__":
    from db import (
        db,
    )  # import here because of circular import issue (import x & x import y and y import x ... so on)

    db.init_app(app)
    # with app.app_context():  # create db schema
    #     db.create_all()

    api.add_resource(
        Student, "/student/<string:name>/", "/student/"
    )  # means add Student resource(get, post, put, patch, delete) to be as API(views)

    api.add_resource(ItemsList, "/items/")
    api.add_resource(CreateItem, "/item/")
    api.add_resource(Item, "/item/<string:item_name>/")
    api.add_resource(UserRegister, "/register/")
    api.add_resource(UserList, "/users/")
    api.add_resource(
        User, "/user/<string:username_or_id>/", "/user/<int:username_or_id>/"
    )
    api.add_resource(UserLogin, "/login/")
    api.add_resource(TokenRefresh, "/refresh/")
    api.add_resource(StoreList, "/stores/")
    api.add_resource(CreateStore, "/store/")
    api.add_resource(Store, "/store/<string:name>/")
    app.run(debug=True, port=5050)
