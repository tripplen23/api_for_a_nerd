import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db

from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

# !Error catching
def item_not_found():
    abort(404, message="Item not found.")

blp = Blueprint("Items", __name__, description="Operations on items")

# TODO: GET, DELETE, PUT specific item dictionary
@blp.route("/item/<string:item_id>")
class Item(MethodView):

    # GET item in specific store
    @blp.response(200, ItemSchema) # Main success response: Use whenever there is a returned item from the server
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            item_not_found()

    # DELETE item from specific store    
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            item_not_found()

    # PUT item in specific store
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        '''
        There's more validation to do here:
        Like making sure price is a number, and also both items are optional
        Difficult to do with an if statement...
        '''
        try:
            item = items[item_id]
            item.update(item_data)  # New dictionary update operator

            return item
        except KeyError:
            item_not_found()
    
# TODO: GET, POST item
@blp.route("/item")
class ItemList(MethodView):
    
    # GET item list
    @blp.response(200, ItemSchema(many=True)) #List => many = True
    def get(self):
        return items.values()
    '''
    Here not only we need to validate data exists,
    but also what type of data. Price should be a float =>
    Solution: Using Marshmallow schema
    '''

    ## POST item list
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item