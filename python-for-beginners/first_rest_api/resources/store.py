import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema

# !Error catching
def store_not_found():
    abort(404, message="Store not found.")

# blueprint in flask-smorest is used to divide an API into multiple segments
blp = Blueprint("Stores", __name__, description = "Operations on stores")

# TODO: Connect the flask-smorest with the flask MethodView below
@blp.route("/store/<int:store_id>")
class Store(MethodView):

    # GET specific store
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
        
    # DELETE specific store
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted successfully"}

@blp.route("/store")
class StoreList(MethodView):

    # GET store list
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    # POST store
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):    
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store


# ** passing keyword args to a constructor(unpack the data in the store_data dictionary and include them in new dictionary)