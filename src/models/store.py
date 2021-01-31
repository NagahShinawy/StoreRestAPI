from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship(
        "ItemModel", lazy="dynamic"
    )  # it tells sqlalchemy there is a relationship with ItemModel. please sqlalchemy check it. (items = many)
    # items: list of items comes from ItemModel because there is a one-many relationship
    # lazy ="dynamic" to make items query builder not items objs from ItemModel

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.to_json() for item in self.items.all()],
        }

    @classmethod
    def find_by_name(cls, store_name):
        # cls.query = query builder
        store = cls.query.filter_by(name=store_name)
        if store:
            return store.first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
