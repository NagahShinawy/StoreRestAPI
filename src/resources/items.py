from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from flask import request
from models.items import ItemModel

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
        return {"msg": "no item found"}, 404

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
        return item.to_json(), 201

    def patch(self, item_name=None):
        return request.get_json()

    @jwt_required()
    def delete(self, item_name):
        item = ItemModel.find_by_name(item_name)
        if item:
            item.delete_from_db()
            return "Deleted", 204
        return {"details": "Not Found to delete"}, 404


class ItemsList(Resource):
    def get(self):
        return {"items": [item.to_json() for item in ItemModel.query.all()]}

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

    @jwt_required()
    def post(self):
        # data = request.get_json(force=True, silent=True)
        data = CreateItem.parser.parse_args()  # add custom validation on body data
        item_name = data.get("item_name")
        if ItemModel.find_by_name(item_name):
            return {"details": f"item with name ({item_name}) already exists"}, 400

        price = data.get("price")
        store_id = data.get("store_id")
        required_fields = [item_name, price, store_id]
        if all(required_fields):
            try:
                item = ItemModel(item_name, price, store_id)
                item.save_to_db()
                return item.to_json()
            except Exception as error:
                return {"msg": f"server error {error}"}, 500
        return {"details": "missing data"}, 400
