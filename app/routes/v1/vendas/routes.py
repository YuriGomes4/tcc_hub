# app/routes.py
from datetime import datetime
from flask import Blueprint, render_template, request, abort, current_app, jsonify, abort
from app.controllers import crud_produto
from app.routines import vendas
from app.routes.auth.routes import token_required

import threading

vendas_bp = Blueprint('vendas', __name__, url_prefix='/vendas')

@vendas_bp.route('list/<int:seller_id>', methods=['GET'])
@token_required
def list_orders(current_user, seller_id):

    listar_vendas = threading.Thread(target=vendas.list_orders, args=(seller_id,))

    listar_vendas.start()

    return jsonify({"result": "As vendas estão sendo listadas"}), 200

@vendas_bp.route('remove/<int:seller_id>', methods=['GET'])
@token_required
def remove_orders(current_user, seller_id):

    vendas.remove_orders(seller_id)
    return jsonify({"result": "Pronto"}), 200

@vendas_bp.route('all/<int:seller_id>', methods=['GET'])
@token_required
def get_all_orders(current_user, seller_id):

    date_from_str = request.args.get('date_from')
    date_to_str = request.args.get('date_to')
    
    if date_from_str and date_to_str:
        # Converta as strings de data para objetos datetime
        date_from = datetime.strptime(date_from_str, "%Y-%m-%d %H:%M:%S")
        date_to = datetime.strptime(date_to_str, "%Y-%m-%d %H:%M:%S")
        
        orders = vendas.get_all_orders(seller_id, date_from, date_to)
    else:
        orders = vendas.get_all_orders(seller_id)
    return jsonify({"result": orders}), 200

@vendas_bp.route('<int:seller_id>/<string:order_id>/shipment', methods=['GET'])
@token_required
def get_order_shipment(current_user, seller_id, order_id):
    
    return jsonify({"result": vendas.get_order_shipment(seller_id, order_id)}), 200


