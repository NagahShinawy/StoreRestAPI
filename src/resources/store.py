from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from src.models.store import StoreModel
from flask import request
from utils.http import status


class StoreList(Resource):
    def get(self):
        # return {
        #     "stores": list(map(lambda store: store.to_json(), StoreModel.query.all()))
        # }
        return {"stores": [store.to_json() for store in StoreModel.query.all()]}, status.HTTP_200_OK


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
            return {"details": f"item with name ({store_name}) already exists"},

        if store_name:
            try:
                store = StoreModel(store_name)
                store.save_to_db()
                return store.to_json(), status.HTTP_201_CREATED
            except Exception as error:
                return {"msg": f"server error {error} "}, status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"details": "missing data"}, status.HTTP_400_BAD_REQUEST


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.to_json(), status.HTTP_201_CREATED
        return {"msg": f"store '{name}' not found"}, status.HTTP_404_NOT_FOUND

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {"msg": "deleted"}, status.HTTP_204_NO_CONTENT
