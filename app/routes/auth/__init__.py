#from app.routes.v1 import produto
from app.routes.auth.routes import auth_bp


def init_app(routes_bp):
    """
    It registers the admin_bp blueprint to the v1_bp blueprint
    
    :param v1_bp: The blueprint for the version 1 of the API
    """
    #produto.init_app(auth_bp)
    routes_bp.register_blueprint(auth_bp)
