from src.app import api
from src.resources.items import Item, ItemsList, CreateItem
from src.resources.user import UserRegister, UserList, User
from src.resources.store import StoreList, CreateStore, Store

api.add_resource(ItemsList, "/items/")
api.add_resource(CreateItem, "/item/")
api.add_resource(Item, "/item/<string:item_name>/")
api.add_resource(UserRegister, "/register/")
api.add_resource(UserList, "/users/")
api.add_resource(User, "/user/<username>/")
api.add_resource(StoreList, "/stores/")
api.add_resource(CreateStore, "/store/")
api.add_resource(Store, "/store/<string:name>/")
