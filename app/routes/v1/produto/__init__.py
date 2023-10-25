from app.routes.v1.produto.routes import produto_bp


def init_app(routes_bp):
    """
    It registers the state_bp blueprint with the routes_bp
    
    :param routes_bp: The Flask application instance
    """
    routes_bp.register_blueprint(produto_bp)