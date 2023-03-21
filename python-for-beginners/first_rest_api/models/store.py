from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores' # We gonna create / a table called "items" for this class & all the obj in this class

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic") # lazy="dynamic": The item here are not going to fetched from the db until we tell it to
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")