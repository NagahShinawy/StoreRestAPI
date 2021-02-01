from flask import Flask
from flask_restful import Api
from src.resources.items import Item, ItemsList, CreateItem
from src.resources.user import UserRegister, UserList
from src.resources.store import StoreList, CreateStore, Store
from src.resources.student import Student
from flask_jwt import JWT
from src.security import authenticate, identity
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False  # to avoid taking much resource (turn off SQlAlchemy modification tracker

dev_db = "sqlite:///" + os.path.join(basedir, "data.db")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", dev_db
)  # comes from production Heroku config vars


app.secret_key = "SECRET-KEY"
api = Api(
    app, prefix="/api/v1"
)  # The main entry point for the application. (routes) (endpoints)


# just like the line ==> 44 ==> with app.app_context()  ==> no need to call function manual.


jwt = JWT(app, authenticate, identity)  # generate ==> BASE_URL/auth endpoint


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
    api.add_resource(StoreList, "/stores/")
    api.add_resource(CreateStore, "/store/")
    api.add_resource(Store, "/store/<string:name>/")
    app.run(debug=True)
