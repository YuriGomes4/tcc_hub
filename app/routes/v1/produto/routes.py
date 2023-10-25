# app/routes.py
from flask import Blueprint, render_template, request, abort, current_app, jsonify, abort
from app.controllers import crud_produto, crud_orderitem, crud_historico, crud_regras
from app.routines import produtos
from app.routes.auth.routes import token_required
from app.services import ml_api

produto_bp = Blueprint('produto', __name__, url_prefix='/produto')

@produto_bp.route('sync_ml/<int:seller_id>', methods=['GET'])
@token_required
def sync_ml(current_user, seller_id):
    #items = crud_produto.read_multi()
    #items = ml_api.get_all_products()
    items = produtos.sync_prods(seller_id)
    return jsonify([{"message": "Todos os produtos foram adicionados", "code": 200}])

@produto_bp.route('remove_ml/<int:seller_id>', methods=['GET'])
@token_required
def remove_ml(current_user, seller_id):
    #items = crud_produto.read_multi()
    #items = ml_api.get_all_products()
    produtos.remove_prods(seller_id)
    #items_list = [{"id": item.id, "nome": item.title} for item in items]
    return jsonify([{"message": "Todos os produtos foram deletados", "code": 200}])


@produto_bp.route('/all', methods=['GET'])
@token_required
def all_products(current_user):
    products = crud_produto.read_multi(schema=True)
    return jsonify({"result": products}), 200

@produto_bp.route('/<string:product_id>', methods=['GET'])
@token_required
def get_product_by_id(current_user, product_id):
    product = crud_produto.read(id=product_id, schema=True)

    if not product:
        abort(404, description="Produto não encontrado")

    return jsonify({"result": product}), 200

@produto_bp.route('/update', methods=['POST'])
@token_required
def update_product(current_user):
    data = request.get_json()  # Recebe os dados do JSON no corpo da solicitação
    if not data or 'id' not in data or 'updates' not in data or 'updates' not in data:
        return jsonify({"message": "Dados inválidos", "code": 400}), 400
    
    product_id = data['id']
    export = data['export']
    updates = data['updates']

    # Verifica se o produto existe antes de tentar atualizá-lo
    product = crud_produto.read(id=product_id)
    if not product:
        return jsonify({"message": "Produto não encontrado", "code": 404}), 404

    # Atualiza os campos do produto com os dados fornecidos
    for key, value in updates.items():
        try:
            setattr(product, key, value)
        except:
            pass

    if export:
        ml_api.alterar_produto(product_id, updates)

    # Persiste as atualizações no banco de dados
    crud_produto.update(product)

    return jsonify({"message": "Produto atualizado com sucesso", "code": 200}), 200
    

@produto_bp.route('sales/<int:seller_id>', methods=['GET'])
@token_required
def sales_product(current_user, seller_id):

    produtos.calc_sales(seller_id)

    return jsonify({"message": "Produtos atualizado com sucesso", "code": 200}), 200

@produto_bp.route('changes/<string:product_id>', methods=['GET'])
@token_required
def product_changes(current_user, product_id):

    historico = crud_historico.read_multi(ref_id=product_id, schema=True)

    return jsonify({"result": historico, "code": 200}), 200

@produto_bp.route('regras/<string:product_id>', methods=['GET'])
@token_required
def product_rules(current_user, product_id):

    regras = crud_regras.read_multi(ref_id_obj=product_id, schema=True)

    return jsonify({"result": regras, "code": 200}), 200

@produto_bp.route('regra/<int:regra_id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def product_rule(current_user, regra_id):

    if request.method == 'GET':

        regra = crud_regras.read(id=regra_id, schema=True)

        return jsonify({"result": regra, "code": 200}), 200
    
    elif request.method == 'PUT':
        data = request.json

        regra = crud_regras.read(id=regra_id)

        if not data or 'ref_id_obj' not in data or 'tabela_obj' not in data or 'coluna_obj' not in data or 'valor_obj' not in data or 'operador' not in data or 'tabela_new' not in data or 'coluna_new' not in data or 'valor_new' not in data:
            return jsonify({"message": "Dados inválidos", "code": 400}), 400
        
        print(type(regra.ref_id_obj), type(data['ref_id_obj']))
        
        regra.ref_id_obj = data['ref_id_obj']
        regra.tabela_obj = data['tabela_obj']
        regra.coluna_obj = data['coluna_obj']
        regra.valor_obj = data['valor_obj']
        regra.operador = data['operador']
        regra.tabela_new = data['tabela_new']
        regra.coluna_new = data['coluna_new']
        regra.valor_new = data['valor_new']

        crud_regras.update(regra)

        return jsonify({"result": "Regra atualizada", "code": 200}), 200
    
    elif request.method == 'DELETE':
        crud_regras.delete(id=regra_id)
        return jsonify({"result": "Regra deletada", "code": 200}), 200

@produto_bp.route('regra', methods=['POST'])
@token_required
def product_rule_add(current_user):
    data = request.json

    print(data)

    if not data or 'ref_id_obj' not in data or 'tabela_obj' not in data or 'coluna_obj' not in data or 'valor_obj' not in data or 'operador' not in data or 'tabela_new' not in data or 'coluna_new' not in data or 'valor_new' not in data:
        return jsonify({"message": "Dados inválidos", "code": 400}), 400
    
    crud_regras.create(
        ref_id_obj = data['ref_id_obj'],
        tabela_obj = data['tabela_obj'],
        coluna_obj = data['coluna_obj'],
        valor_obj = data['valor_obj'],
        operador = data['operador'],
        funcao = data['funcao'],
        ref_id_new = data['ref_id_new'],
        tabela_new = data['tabela_new'],
        coluna_new = data['coluna_new'],
        valor_new = data['valor_new'],
        feito = False,
    )

    return jsonify({"result": "Regra adicionada", "code": 200}), 200