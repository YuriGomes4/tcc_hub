# app/routes.py
from datetime import datetime
from flask import Blueprint, render_template, request, abort, current_app, jsonify, abort
from app.controllers import crud_vendedor
from app.routes.auth.routes import token_required

from app.services import ml_api

vendedor_bp = Blueprint('vendedor', __name__, url_prefix='/vendedor')

@vendedor_bp.route('/all', methods=['GET'])
@token_required
def all_sellers(current_user):
    sellers = crud_vendedor.read_multi(schema=True)
    return jsonify({"result": sellers}), 200

@vendedor_bp.route('/<int:seller_id>', methods=['GET'])
@token_required
def get_seller_by_id(current_user, seller_id):
    seller = crud_vendedor.read(id=seller_id, schema=True)

    if not seller:
        abort(404, description="Vendedor não encontrado")

    return jsonify({"result": seller}), 200

@vendedor_bp.route('/<int:seller_id>/visitas', methods=['GET'])
@token_required
def get_seller_visits(current_user, seller_id):

    date_from_str = request.args.get('date_from')
    date_to_str = request.args.get('date_to')

    print(date_from_str, date_to_str)

    if date_from_str and date_to_str:
        # Converta as strings de data para objetos datetime
        date_from = datetime.strptime(date_from_str, "%Y-%m-%d")
        date_to = datetime.strptime(date_to_str, "%Y-%m-%d")

        visitas = ml_api.visitas_seller(seller_id, date_from_str, date_to_str)

        return jsonify({"result": visitas}), 200
    else:
        return jsonify({"result": "Datas não preenchidas"}), 404

    #return jsonify({"result": seller}), 200