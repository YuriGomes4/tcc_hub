import requests
from dateutil import parser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from your_models_file import Base, Order, Buyer, Seller, OrderItem, Payment
from app.controllers import crud_vendas, crud_buyer, crud_orderitem, crud_payment, crud_vendedor
import app.services.ml_api as ml_api

def add_order(sale):

    if not(str(sale["id"]) in crud_vendas.read_ids()):
        crud_vendas.create(
            id=sale["id"],
            date_created=parser.isoparse(sale["date_created"]),
            date_closed=parser.isoparse(sale["date_closed"]),
            last_updated=parser.isoparse(sale["last_updated"]),
            total_amount=sale["total_amount"],
            paid_amount=sale["paid_amount"],
            expiration_date=parser.isoparse(sale["expiration_date"]),
            currency_id=sale["currency_id"],
            status=sale["status"],
            status_detail=sale["status_detail"],
            buyer_id=sale["buyer"]["id"],
            seller_id=sale["seller"]["id"],
            pack_id=sale["pack_id"],
            pickup_id=sale["pickup_id"],
            comment=sale["comment"],
            manufacturing_ending_date=sale["manufacturing_ending_date"],
            shipping=sale["shipping"],
            json = str(sale)
        )

        for item in sale["order_items"]:
            crud_orderitem.create(
                order_id=sale["id"],
                item_id=item["item"]["id"],
                title=item["item"]["title"],
                category_id=item["item"]["category_id"],
                variation_id=item["item"]["variation_id"],
                warranty=item["item"]["warranty"],
                condition=item["item"]["condition"],
                unit_price=item["unit_price"],
                currency_id=item["currency_id"],
                quantity=item["quantity"],
                requested_quantity=item["requested_quantity"],
                sale_fee=item["sale_fee"],
                listing_type_id=item["listing_type_id"],
                seller_id=sale["seller"]["id"]
            )
    else:
        print(str(sale["id"]),"Já tem")

    if not(str(sale["buyer"]["id"]) in crud_buyer.read_ids()):
        crud_buyer.create(
            id=sale["buyer"]["id"],
            nickname=sale["buyer"]["nickname"],
            #first_name=sale["buyer"]["first_name"],
            #last_name=sale["buyer"]["last_name"]
        )
    
    for payment in sale["payments"]:
        if not(str(payment["id"]) in crud_payment.read_ids()):
            crud_payment.create(
                id=payment["id"],
                order_id=sale["id"],
                payer_id=payment["payer_id"],
                payment_method_id=payment["payment_method_id"],
                currency_id=payment["currency_id"],
                transaction_amount=payment["transaction_amount"],
                status=payment["status"]
            )


def list_orders(sell_id):

    sales_data = ml_api.get_all_orders(sell_id)

    try:
        # Processar e adicionar os dados das vendas ao banco de dados
        cont = 0
        for sale in sales_data:
            #print(str(sale["id"]),crud_vendas.read_ids())
            #print(str(sale["id"]) in crud_vendas.read_ids())
            #print(crud_vendas.read_ids())
            sale['shipping'] = str(ml_api.order_shipment(sell_id, sale["id"]))

            add_order(sale)
            cont += 1 
            print(cont)

        print("Sales data added to the database successfully.")
    except:
        pass

def remove_orders(seller):
    try:
        seller_id = int(crud_vendedor.read(id=seller).id_ml)
        crud_vendas.delete(seller_id=seller_id)
        crud_orderitem.delete(seller_id=seller_id)
        print("Todos os itens da tabela foram removidos com sucesso.")
    except Exception as e:
        #session.rollback()
        print(f"Erro ao remover itens da tabela: {e}")

def get_all_orders(seller, date_from=None, date_to=None):
    try:
        seller_id = int(crud_vendedor.read(id=seller).id_ml)
        if date_from and date_to:
            vendas = crud_vendas.read_multi(seller_id=seller_id, date_created=(date_from, date_to), schema=True)
        else:
            vendas = crud_vendas.read_multi(seller_id=seller_id, schema=True)
        print("As vendas foram listadas com sucesso.")

        return vendas
    except Exception as e:
        #session.rollback()
        print(f"Erro ao listar as vendas: {e}")


def get_order_shipment(seller, order_id):

    try:

        return ml_api.order_shipment(seller, order_id)
    
    except:

        return "erro"

