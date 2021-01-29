from db import db


class ItemModel(db.Model):
    __tablename__ = (
        "items"  # table name on db ==> default is (item_model) from (ItemModel)
    )

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100))
    price = db.Column(db.Float(precision=2))  # numbers after decimal point (precision)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id")
    )  # one inside many ( 1 to many relationship). "stores" is __tablename__
    store = db.relationship("StoreModel")  # StoreModel is class name. (store 'One' in relationship)

    def __init__(self, item_name, price, store_id):
        self.item_name = item_name
        self.price = price
        self.store_id = store_id

    def to_json(self):
        return {"id": self.id, "item_name": self.item_name, "price": self.price, "store": self.store.name}

    @classmethod
    def find_by_name(cls, item_name):
        # return ItemModel.query.filter_by(item_name=item_name, id=item_id)  # filter by name & id
        # cls.query = query builder
        qs = cls.query.filter_by(item_name=item_name)  # cls = ItemModel
        if qs:
            return qs.first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)  # inset or update obj(self) on db
        db.session.commit()
