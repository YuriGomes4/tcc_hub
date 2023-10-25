from app.controllers import crud_vendedor, crud_produto, crud_historico, crud_vendas, crud_buyer, crud_orderitem, crud_payment
from app.routines import produtos, vendas
from . import ml_api, regras
import json
from datetime import datetime
from dateutil import parser

def order_v2(json_p):
    vendedor = crud_vendedor.read(id_ml=json_p['user_id'])
    seller_id = vendedor.id

    vendedor.last_updated = datetime.now()
    crud_vendedor.update(vendedor)

    order_id = str(json_p['resource']).replace("/orders/", "")
    

    sale = ml_api.get_order(seller_id, order_id)

    try:
        vendas.add_order(sale)
    except:
        pass

    produtos.calc_sales(seller_id)

    print(crud_vendas.read(id=order_id))

def items(json_p):
    vendedor = crud_vendedor.read(id_ml=json_p['user_id'])
    seller_id = vendedor.id

    vendedor.last_updated = datetime.now()
    crud_vendedor.update(vendedor)

    product_id = str(json_p['resource']).replace("/items/", "")

    new_json = str(ml_api.get_product(seller_id, product_id)).replace("'", '"').replace("None", '""').replace("True", 'true').replace("False", 'false')
    product = crud_produto.read(id=product_id)
    old_json = str(product.json).replace("'", '"').replace("None", '""').replace("True", 'true').replace("False", 'false')

    #print(new_json)

    new_json_obj = json.loads(new_json)
    old_json_obj = json.loads(old_json)

    ignorelist = ['last_updated', 'permalink', 'expiration_time', 'sale_fee', 'shipping_free_cost', 'sale_terms', 'tags']
    diferente = False

    #print(json_obj1)
    
    for key in new_json_obj:
        if key in old_json_obj and not(key in ignorelist):
            #print(key)
            value1 = new_json_obj[key]
            value2 = old_json_obj[key]
            if value1 != value2:
                diferente = True
                print(f"Atributo '{key}' tem valores diferentes:")
                print(f"Valor no JSON novo: {value1}")
                print(f"Valor no JSON antigo: {value2}")
                print()
                crud_historico.create(
                    date=datetime.now(),
                    seller=json_p['user_id'],
                    type="items",
                    ref_id=product_id,
                    change=key,
                    old_value=str(value2),
                    new_value=str(value1),
                )
        elif not(key in ignorelist):
            print(f"Atributo {key} ausente no JSON antigo")

    for key in old_json_obj:
        if not(key in new_json_obj) and not(key in ignorelist):
            print(f"Atributo {key} ausente no JSON novo")

    if diferente == True:
        product.id = new_json_obj['id']
        product.category_id = new_json_obj['category_id']
        #product.cost = 0
        product.price = new_json_obj['price']
        product.title = new_json_obj['title']
        product.listing_type_id = new_json_obj['listing_type_id']
        product.free_shipping = new_json_obj['shipping']['free_shipping']
        #product.shipping_free_cost = new_json_obj['shipping_free_cost']
        #product.sale_fee = new_json_obj['sale_fee']
        #product.seller = int(seller_id)
        #product.sales = 0
        #product.invoicing = 0
        product.json = new_json

        crud_produto.update(product)

def novo_retorno(json):

    tipo = json['topic']
    print(tipo)

    match tipo:
        case "orders_v2":
            order_v2(json)
        case "items":
            items(json)
        case _:
            print("Tópico não reconhecido:", tipo)

    regras.verificar()