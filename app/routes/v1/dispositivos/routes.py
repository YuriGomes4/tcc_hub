# app/routes.py
from flask import Blueprint, render_template, request, abort, current_app, jsonify, abort
from app.controllers import crud_dispositivo, crud_residencia, crud_usuario
from app.routes.auth.routes import token_required
import json

dispositivos_bp = Blueprint('dispositivos', __name__, url_prefix='/dispositivos')

@dispositivos_bp.route('info/<int:dispositivo_id>', methods=['GET'])
#@token_required
def get_info(dispositivo_id):

    try:
        dispositivo = crud_dispositivo.read(id=dispositivo_id)
        info = json.loads(dispositivo.info)
        #print(type(info), info)
        info['tipo'] = dispositivo.tipo
        info['nome'] = dispositivo.nome
        return jsonify([{"result": info, "code": 200}])
    except:
        return jsonify([{"message": "ID do dispositivo incorreto", "code": 404}])
    
@dispositivos_bp.route('search', methods=['GET'])
#@token_required
def search_dispositivos():

    area = request.args.get('area')

    try:
        dispositivo = crud_dispositivo.read_multi(id_area_residencia=area, schema=True)
        return jsonify([{"result": dispositivo, "code": 200}])
    except:
        return jsonify([{"message": "ID do dispositivo incorreto", "code": 404}])
    
@dispositivos_bp.route('user', methods=['GET'])
#@token_required
def dispositivos_usuario():

    email = request.args.get('email')

    try:
        usuario = crud_usuario.read(email=email)
        resis = crud_residencia.read_multi(id_usuario=usuario.id)

        disps = []

        for res in resis:

            disps += crud_dispositivo.read_multi(id_residencia=res.id, schema=True)

        return jsonify({"result": disps, "code": 200})
    except:
        return jsonify([{"message": "ID do dispositivo incorreto", "code": 404}])