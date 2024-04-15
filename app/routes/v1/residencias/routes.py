# app/routes.py
from datetime import datetime
from flask import Blueprint, render_template, request, abort, current_app, jsonify, abort
from app.controllers import crud_residencia, crud_usuario, crud_area_residencia
from app.routes.auth.routes import token_required

residencias_bp = Blueprint('residencias', __name__, url_prefix='/residencias')

@residencias_bp.route('', methods=['GET', 'POST', 'DELETE', 'PUT'])
@token_required
def get(current_user):

    if request.method == 'GET':
        pi_usuario = request.args.get('usuario')

        usuario = crud_usuario.read(id_publico=pi_usuario)

        if not usuario:
            usuario = current_user

        try:
            residencias = crud_residencia.read_multi(id_usuario=usuario.id, schema=True)
            return jsonify({"result": residencias, "code": 200})
        except:
            return jsonify({"message": "ID do usuario incorreto", "code": 404})
        
    elif request.method == 'POST':
            
        nome = request.args.get('nome')

        if nome and nome != '':

            crud_residencia.create(
                nome=nome,
                id_usuario=current_user.id,
                data_criacao=datetime.now(),
                data_alteracao=datetime.now()
            )

            return jsonify({"message": "Residencia cadastrada"}), 200
        else:
            return jsonify({"message": "Dados insuficientes"}), 400
        
@residencias_bp.route('areas', methods=['GET'])
@token_required
def get_areas(current_user):

    #pi_usuario = request.args.get('usuario')

    if request.method == 'GET':

        #usuario = crud_usuario.read(id_publico=pi_usuario)

        try:
            residencias = crud_residencia.read_multi(id_usuario=current_user.id)

            areas = []

            for residencia in residencias:
                areas += crud_area_residencia.read_multi(id_residencia=residencia.id, schema=True)

            return jsonify({"result": areas, "code": 200})
        except:
            return jsonify({"message": "ID do usuario incorreto", "code": 404})

@residencias_bp.route('<int:residencia_id>/areas', methods=['GET', 'POST', 'DELETE'])
@token_required
def get_areas_resid(current_user, residencia_id):

    #pi_usuario = request.args.get('usuario')

    if request.method == 'POST':
        nome = request.args.get('nome')

        if nome and nome != '':

            residencia = crud_residencia.read(id=residencia_id)

            crud_area_residencia.create(
                nome=nome,
                id_residencia=residencia.id,
                data_criacao=datetime.now(),
                data_alteracao=datetime.now()
            )

            return jsonify({"message": "Area cadastrada"}), 200
        else:
            return jsonify({"message": "Dados insuficientes"}), 400
        
    elif request.method == 'GET':

        residencia = crud_residencia.read(id=residencia_id)

        try:
            residencias = crud_area_residencia.read_multi(id_residencia=residencia.id, schema=True)
            return jsonify({"result": residencias, "code": 200})
        except:
            return jsonify({"message": "ID da residencia incorreto", "code": 404})
        
    elif request.method == 'DELETE':

        area_id = request.args.get('id')

        area = crud_area_residencia.read(id=area_id)

        if area:

            crud_area_residencia.delete(id=area_id)

            return jsonify({"message": "Areas deletadas"}), 200
        else:
            return jsonify({"message": "ID da residencia incorreto"}), 404
        
@residencias_bp.route('<int:residencia_id>/areas/<int:area_id>', methods=['GET', 'PUT'])
@token_required
def get_area(current_user, residencia_id, area_id):
    
    if request.method == 'GET':
        area = crud_area_residencia.read(id=area_id, schema=True)

        return jsonify({"result": area}), 200
    
    elif request.method == 'PUT':
        nome = request.args.get('nome')

        if nome and nome != '':

            area = crud_area_residencia.read(id=area_id)

            area.nome = nome
            area.data_alteracao = datetime.now()

            crud_area_residencia.update(area)


            return jsonify({"message": "Area atualizada"}), 200
        else:
            return jsonify({"message": "Dados insuficientes"}), 400
    
@residencias_bp.route('<int:residencia_id>', methods=['GET', 'DELETE', 'PUT'])
@token_required
def get_residencia(current_user, residencia_id):

    if request.method == 'DELETE':
        residencia = crud_residencia.read(id=residencia_id)

        if residencia:
            crud_residencia.delete(id=residencia_id)
            return jsonify({"message": "Residencia deletada"}), 200
        else:
            return jsonify({"message": "ID da residencia incorreto"}), 404
        
    elif request.method == 'GET':
        residencia = crud_residencia.read(id=residencia_id, schema=True)

        return jsonify({"result": residencia}), 200
    
    elif request.method == 'PUT':
        nome = request.args.get('nome')

        if nome and nome != '':

            residencia = crud_residencia.read(id=residencia_id)

            residencia.nome = nome
            residencia.data_alteracao = datetime.now()

            crud_residencia.update(residencia)


            return jsonify({"message": "Residencia atualizada"}), 200
        else:
            return jsonify({"message": "Dados insuficientes"}), 400