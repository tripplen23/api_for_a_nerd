from sqlalchemy import ForeignKey
from db import db

# Create a map
class ItemModel(db.Model):
    __tablename__ = 'items' # We gonna create / a table called "items" for this class & all the obj in this class

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False) # Column store_id map to stores_id
    store = db.relationship("StoreModel", back_populates="items") # Grab me a store object or a store model object that has the above store_id set
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags") # In relationship to tags
# Benefits of using ForeignKey is that you won't be able to create a item that has a store_id that
# doesn't have an equal value in the stores table