# app/routes.py
from datetime import datetime
from flask import Blueprint, render_template, request, abort, current_app, jsonify, abort
from app.controllers import crud_dispositivo, crud_residencia, crud_usuario
from app.routes.auth.routes import token_required
import json

dispositivos_bp = Blueprint('dispositivos', __name__, url_prefix='/dispositivos')

@dispositivos_bp.route('', methods=['GET', 'POST', 'DELETE', 'PUT'])
@token_required
def add_dispositivo(current_user):

    if request.method == 'POST':

        nome = request.args.get('nome')
        tipo = request.args.get('tipo')
        id_residencia = request.args.get('residencia')
        id_area = request.args.get('area')
        codigo = request.args.get('codigo')

        if not nome or not tipo or not id_residencia or not id_area or not codigo or nome == '' or tipo == '' or id_residencia == '' or id_area == '' or codigo == '':
            return jsonify({"message": "Dados insuficientes"}), 400
        else:

            crud_dispositivo.create(
                nome=nome,
                tipo=tipo,
                id_residencia=int(id_residencia),
                id_area_residencia=int(id_area),
                codigo=codigo,
                data_criacao=datetime.now(),
                data_alteracao=datetime.now(),
                info={"temp": 0} if tipo == "termometro" else {}
            )

            return jsonify({"message": "Dispositivo cadastrado"}), 200
        
    elif request.method == 'GET':

        id_disp = request.args.get('id')

        if id_disp:
            dispositivo = crud_dispositivo.read(id=int(id_disp), schema=True)

            return jsonify({"result": dispositivo}), 200
        
        else:
            return jsonify({"message": "ID do dispositivo incorreto"}), 404
        
    elif request.method == 'DELETE':
            
        id_disp = request.args.get('id')

        if id_disp:
            dispositivo = crud_dispositivo.read(id=int(id_disp))

            if dispositivo:
                crud_dispositivo.delete(id=int(id_disp))
                return jsonify({"message": "Dispositivo deletado"}), 200
            else:
                return jsonify({"message": "ID do dispositivo incorreto"}), 404
        else:
            return jsonify({"message": "ID do dispositivo ausente"}), 400
        
    elif request.method == 'PUT':
            
        id_disp = request.args.get('id')

        if id_disp and id_disp != '':

            dispositivo = crud_dispositivo.read(id=int(id_disp))

            if dispositivo:

                old_nome = dispositivo.nome
                old_residencia = dispositivo.id_residencia
                old_area = dispositivo.id_area_residencia
                old_codigo = dispositivo.codigo

                nome = request.args.get('nome')

                if nome and nome != '':
                    dispositivo.nome = nome

                id_residencia = request.args.get('residencia')

                if id_residencia and id_residencia != '':
                    dispositivo.id_residencia = id_residencia

                id_area = request.args.get('area')

                if id_area and id_area != '':
                    dispositivo.id_area_residencia = id_area

                codigo = request.args.get('codigo')

                if codigo and codigo != '':
                    dispositivo.codigo = codigo

                if old_nome != dispositivo.nome or old_residencia != dispositivo.id_residencia or old_area != dispositivo.id_area_residencia or old_codigo != dispositivo.codigo:

                    crud_dispositivo.update(dispositivo)

                    return jsonify({"message": "Dispositivo atualizado"}), 200
                
                else:
                    return jsonify({"message": "Nada foi alterado"}), 402
                
            else:
                return jsonify({"message": "ID do dispositivo incorreto"}), 404
                
        else:
            return jsonify({"message": "ID do dispositivo ausente"}), 400

@dispositivos_bp.route('info/<string:dispositivo_id>', methods=['GET', 'POST'])
@token_required
def get_info(current_user, dispositivo_id):

    if request.method == 'GET':

        try:
            dispositivo = crud_dispositivo.read(codigo=dispositivo_id)
            info = json.loads(dispositivo.info)
            #print(type(info), info)
            info['tipo'] = dispositivo.tipo
            info['nome'] = dispositivo.nome
            return jsonify({"result": info}), 200
        except:
            return jsonify({"message": "ID do dispositivo incorreto"}), 404
        
    elif request.method == 'POST':


        dispositivo = crud_dispositivo.read(codigo=dispositivo_id)

        if dispositivo:
            
            if dispositivo.tipo == 'termometro':
                data = request.get_json()
                try:
                    info_json = json.loads(data)
                except:
                    info_json = data
                dispositivo.info = info_json

            dispositivo.data_alteracao = datetime.now()

            crud_dispositivo.update(dispositivo)

            return jsonify({"message": "Informações atualizadas"}), 200
        else:
            return jsonify({"message": "ID do dispositivo incorreto"}), 404
        
@dispositivos_bp.route('info', methods=['GET', 'POST'])
@token_required
def att_infos(current_user):
        
    if request.method == 'POST':

        data = request.get_json()

        try:
            data_json = json.loads(data)
        except:
            data_json = data

        if type(data_json) == dict:

            atulizou = False

            for dispositivo_id in data_json.keys():

                dispositivo = crud_dispositivo.read(codigo=dispositivo_id)

                if dispositivo:
                    
                    try:
                        info_json = json.loads(data_json[dispositivo_id])
                    except:
                        info_json = data_json[dispositivo_id]

                    if type(info_json) == dict:

                        dispositivo.info = info_json

                        dispositivo.data_alteracao = datetime.now()

                        crud_dispositivo.update(dispositivo)

                        atulizou = True

            if atulizou:
                return jsonify({"message": "Informações atualizadas"}), 200
            else:
                return jsonify({"message": "Nada foi atualizado"}), 402

        else:
            return jsonify({"message": "Dados incorretos"}), 400
    
@dispositivos_bp.route('search', methods=['GET'])
#@token_required
def search_dispositivos():

    area = request.args.get('area')

    try:
        dispositivo = crud_dispositivo.read_multi(id_area_residencia=area, schema=True)
        return jsonify({"result": dispositivo}), 200
    except:
        return jsonify({"message": "ID do dispositivo incorreto"}), 404
    
@dispositivos_bp.route('user', methods=['GET'])
@token_required
def dispositivos_usuario(current_user):

    #email = request.args.get('email')

    #usuario = crud_usuario.read(email=email)
    resis = crud_residencia.read_multi(id_usuario=current_user.id)

    if resis:

        disps = []

        for res in resis:

            disps += crud_dispositivo.read_multi(id_residencia=res.id, schema=True)

        return jsonify({"result": disps}), 200
    
    else:
        return jsonify({"message": "Usuario nao possui residencias"}), 404
