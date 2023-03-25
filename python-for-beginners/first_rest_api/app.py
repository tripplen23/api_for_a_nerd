import os
import secrets

from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

# Factory pattern
def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/" # To tell flask smorest to where the route the API is
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui" # To tell flask smorest to where the route the API is
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)

    api = Api(app)

    #Set a secret key , And the secret key for signing the JWT secrets.SystemRandom().getrandbits(128)
    app.config["JWT_SECRET_KEY"] = "Ben"
    # Create an instance of the JWT manager
    jwt = JWTManager(app)

    @app.before_first_request 
    def create_tables():
        db.create_all()
        

    # blp variable in the resources file
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app

    '''
    Decorating the responses lets us more easily define 
    what will be returned for each status code, and also
    it lets us define a bit more easily what status code will returned
    and also populated documentation 
    '''