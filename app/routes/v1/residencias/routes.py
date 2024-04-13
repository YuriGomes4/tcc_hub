# app/routes.py
from flask import Blueprint, render_template, request, abort, current_app, jsonify, abort
from app.controllers import crud_residencia, crud_usuario, crud_area_residencia
from app.routes.auth.routes import token_required

residencias_bp = Blueprint('residencias', __name__, url_prefix='/residencias')

@residencias_bp.route('', methods=['GET'])
@token_required
def get(current_user):

    pi_usuario = request.args.get('usuario')

    usuario = crud_usuario.read(id_publico=pi_usuario)

    if not usuario:
        usuario = current_user

    try:
        residencias = crud_residencia.read_multi(id_usuario=usuario.id, schema=True)
        return jsonify({"result": residencias, "code": 200})
    except:
        return jsonify({"message": "ID do usuario incorreto", "code": 404})

@residencias_bp.route('<int:residencia_id>/areas', methods=['GET'])
@token_required
def get_areas(current_user, residencia_id):

    #pi_usuario = request.args.get('usuario')

    residencia = crud_residencia.read(id=residencia_id)

    try:
        residencias = crud_area_residencia.read_multi(id_residencia=residencia.id, schema=True)
        return jsonify({"result": residencias, "code": 200})
    except:
        return jsonify({"message": "ID da residencia incorreto", "code": 404})