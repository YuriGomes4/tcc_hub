# app/routes.py
from flask import Blueprint, render_template, request, abort, current_app, jsonify, abort
from app.controllers import crud_dispositivo
from app.routes.auth.routes import token_required

dispositivos_bp = Blueprint('dispositivos', __name__, url_prefix='/dispositivos')

@dispositivos_bp.route('info/<int:dispositivo_id>', methods=['GET'])
#@token_required
def get_info(dispositivo_id):

    print(dispositivo_id)

    try:
        dispositivo = crud_dispositivo.read(id=dispositivo_id)
        print(dispositivo)
        return jsonify([{"result": dispositivo.info, "code": 200}])
    except:
        return jsonify([{"message": "ID do dispositivo incorreto", "code": 404}])
