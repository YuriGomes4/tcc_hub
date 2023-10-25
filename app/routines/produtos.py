import app.services.ml_api as ml_api
from app.controllers import crud_produto, crud_orderitem

def sync_prods(seller_id):
    products = ml_api.get_all_products(seller_id)

    print(products[0])

    for prod in products:
        if prod['id'] not in crud_produto.read_ids():

            crud_produto.create(
                id = prod['id'],
                category_id = prod['category_id'],
                cost = 0,
                price = prod['price'],
                title = prod['title'],
                listing_type_id = prod['listing_type_id'],
                free_shipping = prod['shipping']['free_shipping'],
                shipping_free_cost = prod['shipping_free_cost'],
                sale_fee = prod['sale_fee'],
                seller = int(seller_id),
                sales = 0,
                invoicing = 0,
                json = str(prod),
            )

    print("Atualizado")

def remove_prods(seller_id):
    try:
        seller_id = int(seller_id)
        crud_produto.delete(seller=seller_id)
        print("Todos os itens da tabela foram removidos com sucesso.")
    except Exception as e:
        #session.rollback()
        print(f"Erro ao remover itens da tabela: {e}")

def calc_sales(seller_id):
    
    products = crud_produto.read_multi(seller=seller_id)
    order_items = crud_orderitem.read_multi()

    for product in products:
        sales = 0
        invoicing = 0

        for item in order_items:
            if item.item_id == product.id:
                sales = sales + item.quantity
                invoicing = invoicing + (item.quantity * item.unit_price)

        setattr(product, 'sales', sales)
        setattr(product, 'invoicing', invoicing)

        crud_produto.update(product)