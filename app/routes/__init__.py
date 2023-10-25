from app.routes import v1, auth
from app.routes.routes import routes_bp

teste_bp = None

def init_app(main_bp):
    global teste_bp
    """
    It registers the admin_bp blueprint to the v1_bp blueprint
    
    :param v1_bp: The blueprint for the version 1 of the API
    """
    v1.init_app(routes_bp)
    auth.init_app(routes_bp)
    teste_bp = main_bp
    main_bp.register_blueprint(routes_bp)

