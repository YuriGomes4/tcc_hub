import warnings

from flask import Flask

#from app.db import db
#from app.services import cache, jwt, migrate, apispec, cors
from app import routes, controllers


def create_app():
    """create and configure the flask application"""
    # app
    app = Flask(__name__)
    #app.config.from_object("config.Config")

    # services
    #cors.init_app(app, resources={r"*": {"origins": "*"}})
    #cache.init_app(app)
    #jwt.init_app(app)
    #db.init_app(app)
    #migrate.init_app(app, db, compare_type=True)

    warnings.filterwarnings("ignore", category=UserWarning)


    # routes
    routes.init_app(app)

    # init api spec
    #apispec.init_app(app)

    return app


from . import models, schemas
