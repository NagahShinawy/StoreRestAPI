from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from src.models.store import StoreModel
from flask import request


class StoreList(Resource):
    def get(self):
        return {
            "stores": list(map(lambda store: store.to_json(), StoreModel.query.all()))
        }


class CreateStore(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name",
        type=float,
        required=True,
        help="store name field can not left black",
    )

    @jwt_required()
    def post(self):
        data = request.get_json(force=True, silent=True)
        store_name = data.get("name")
        if StoreModel.find_by_name(store_name):
            return {"details": f"item with name ({store_name}) already exists"}, 400

        if store_name:
            try:
                store = StoreModel(store_name)
                store.save_to_db()
                return store.to_json(), 201
            except Exception as error:
                return {"msg": f"server error {error} "}, 500
        return {"details": "missing data"}, 400


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.to_json(), 201
        return {"msg": f"store '{name}' not found"}, 404

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"msg": "deleted"}, 204
