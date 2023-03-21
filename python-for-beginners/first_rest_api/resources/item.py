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
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    # DELETE item from specific store    
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted successfully"}

    # PUT item in specific store
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id): 
        item = ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id,**item_data)

        db.session.add(item)
        db.session.commit()
    
        return item
    
# TODO: GET, POST item
@blp.route("/item")
class ItemList(MethodView):
    
    # GET item list
    @blp.response(200, ItemSchema(many=True)) #List => many = True
    def get(self):
        return ItemModel.query.all()
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