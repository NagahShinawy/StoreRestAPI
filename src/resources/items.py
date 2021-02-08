from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from flask import request

from src.models.user import UserModel
from src.models.items import ItemModel
from flask_jwt_extended import (
    jwt_required as jwt_required_extended,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required,
    jwt_refresh_token_required,
)
from utils.http import status


# resources is the logical part like views in django


class Item(Resource):
    # todo : define as class attrs to be shared because validation shared between all items not just single obj ,
    #  you can use it at every method
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="price field can not left black",
    )  # adding custom validation on request body (go to string docs to read docs of class)
    parser.add_argument(
        "item_name",
        type=str,
        required=True,
        help="item name field can not left black",
    )

    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="every item needs store id",
    )

    @jwt_required()
    def get(self, item_name=None):
        item = ItemModel.find_by_name(item_name)
        if item:
            return {"item": item.to_json()}
        return {"msg": "no item found"}, status.HTTP_404_NOT_FOUND

    def put(self, item_name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(item_name)

        if item is None:
            item = ItemModel(
                item_name=item_name,
                price=data.get("price"),
                store_id=data.get("store_id"),
            )
        else:
            item.price = data.get("price")

        item.save_to_db()
        return item.to_json(), status.HTTP_201_CREATED

    def patch(self, item_name=None):
        return request.get_json()

    # @jwt_required()  # for jwt
    @jwt_required_extended  # for jwtManager
    def delete(self, item_name):
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"msg": "need Admin permission to delete an item"}, status.HTTP_401_UNAUTHORIZED
        item = ItemModel.find_by_name(item_name)
        if item:
            item.delete_from_db()
            return "Deleted", status.HTTP_204_NO_CONTENT
        return {"details": "Not Found to delete"}, status.HTTP_404_NOT_FOUND


class ItemsList(Resource):
    @jwt_optional
    def get(self):
        identity = (
            get_jwt_identity()
        )  # get jwt if it exist because it is @jwt_optional (return saving identity in this case username)
        items = ItemModel.find_all()
        # user = UserModel.find_by_username(username=identity)
        if identity:  # identity is username
            return {"items": [item.to_json() for item in items]}, status.HTTP_200_OK
        return {
            "items": [item.item_name for item in items],
            "msg": "more data available if you are login",
        }, status.HTTP_200_OK

    # return {"items": list(map(lambda item: item.to_json(), ItemModel.query.all()))} ==> it works
    # return {"items": ItemModel.query.all()} error ==>TypeError: Object of type 'ItemModel' is not JSON serializable


class CreateItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="price field can not left black",
    )
    parser.add_argument(
        "item_name",
        type=str,
        required=True,
        help="item name field can not left black",
    )

    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="every item needs a store id",
    )

    @fresh_jwt_required  # means required "access token" but fresh=True
    def post(self):
        # data = request.get_json(force=True, silent=True)
        data = CreateItem.parser.parse_args()  # add custom validation on body data
        item_name = data.get("item_name")
        if ItemModel.find_by_name(item_name):
            return {"details": f"item with name ({item_name}) already exists"}, status.HTTP_400_BAD_REQUEST

        price = data.get("price")
        store_id = data.get("store_id")
        required_fields = [item_name, price, store_id]
        if all(required_fields):
            try:
                item = ItemModel(item_name, price, store_id)
                item.save_to_db()
                return item.to_json()
            except Exception as error:
                return {"msg": f"server error {error}"}, status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"details": "missing data"}, status.HTTP_400_BAD_REQUEST
