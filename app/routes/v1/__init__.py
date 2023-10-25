#from app.routes.v1 import produto, vendedor, vendas, retornos
from app.routes.v1 import dispositivos
from app.routes.v1.routes import v1_bp


def init_app(routes_bp):
    """
    It registers the admin_bp blueprint to the v1_bp blueprint
    
    :param v1_bp: The blueprint for the version 1 of the API
    """
    #produto.init_app(v1_bp)
    #vendedor.init_app(v1_bp)
    #vendas.init_app(v1_bp)
    #retornos.init_app(v1_bp)
    dispositivos.init_app(v1_bp)
    routes_bp.register_blueprint(v1_bp)
