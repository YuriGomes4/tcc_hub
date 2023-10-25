from flask import Blueprint, request
import threading
from app.services.retornos import novo_retorno

retornos_bp = Blueprint('retornos', __name__, url_prefix='/retornos')

@retornos_bp.route('/<int:seller_id>', methods=['POST'])
def retorno(seller_id):
    json_data = request.json  # Dados JSON recebidos na requisição

    # Criar uma nova thread para executar novo_retorno
    thread = threading.Thread(target=novo_retorno, args=(json_data,))
    thread.start()

    return "Ok", 200
