import requests

from app.controllers import crud_vendedor, crud_produto

BASE_URL = 'https://api.mercadolibre.com'



def req_prods(id):
    global BASE_URL

    vendedor = crud_vendedor.read(id=id)
    access_token = vendedor.tk_ml
    seller_id = vendedor.id_ml

    params = {
        #'seller_id': seller_id,  # Substitua pelo ID do vendedor desejado
        'access_token': access_token,
        #'limit': 50,  # O máximo permitido é 50 por página
    }

    # URL da API do Mercado Livre para obter os produtos
    url = f'{BASE_URL}/users/{seller_id}/items/search'
    #url = f'{BASE_URL}/users/me'

    # Fazendo a solicitação à API
    response = requests.get(url, params=params)
    #response = requests.get(url)

    return response

def verify_refresh_token(id):

    global BASE_URL

    vendedor = crud_vendedor.read(id=id)
    client_id = vendedor.client_ml
    client_secret = vendedor.secret_ml
    access_token = vendedor.tk_ml
    seller_id = vendedor.id_ml
    refresh_token = vendedor.refresh_tk_ml

    response = req_prods(id)

    #print(response.json())

    if response.status_code != 200:
        #if response.json()['message'] == 'invalid_token':
        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
        }

        data = {
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
        }

        response = requests.post(f'{BASE_URL}/oauth/token', headers=headers, data=data)

        try:
            vendedor_db = crud_vendedor.read(id=id)
            vendedor_db.tk_ml = response.json()['access_token']
            vendedor_db.refresh_tk_ml = response.json()['refresh_token']
            crud_vendedor.update(vendedor_db)

            return vendedor_db.tk_ml

            #response = req_prods(id)
        except:
            print(f'Falha na solicitação. Código de status: {response.status_code}')
            print(response.json())

            return None

def get_all_products(id):

    global BASE_URL

    vendedor = crud_vendedor.read(id=id)
    client_id = vendedor.client_ml
    client_secret = vendedor.secret_ml
    access_token = vendedor.tk_ml
    seller_id = vendedor.id_ml
    refresh_token = vendedor.refresh_tk_ml

    #print(seller_id)

    params = {
        #'seller_id': seller_id,  # Substitua pelo ID do vendedor desejado
        'access_token': access_token,
        #'limit': 50,  # O máximo permitido é 50 por página
    }
    
    response = req_prods(id)

    products = []

    nat = verify_refresh_token(id)

    if nat != None:
        access_token = nat

    if response.status_code == 200:
        data = response.json()
        #print(data)
        mlbs = data['results']


        # Aqui você tem a lista de todos os produtos da conta
        for mlb in mlbs:
            # Aqui você pode processar as informações dos produtos conforme necessário
            url = f'{BASE_URL}/items/{mlb}'
            response = requests.get(url, params=params)
            product = response.json()

            url = f'{BASE_URL}/sites/MLB/listing_prices?price={product["price"]}&listing_type_id={product["listing_type_id"]}&category_id={product["category_id"]}'
            response = requests.get(url, params=params)

            sale_fee = response.json()['sale_fee_amount']

            product['sale_fee'] = sale_fee

            if product['shipping']['free_shipping'] == 1:

                url = f'{BASE_URL}/items/{mlb}/shipping_options'
                params = {'access_token': access_token, 'zip_code': '04913000'}
                response = requests.get(url, params=params)

                #print(response.json())

                ship_cost = response.json()['options'][0]['list_cost']

            else:
                ship_cost = 0

            product['shipping_free_cost'] = ship_cost

            #print(product['shipping_free_cost'])

            products.append(product)

            #print(data)

        print(f'Produtos: {len(mlbs)}')
    else:
        print(f'Falha na solicitação. Código de status: {response.status_code}')
        print(response.json())

    return products

def get_all_orders(id):
    global BASE_URL

    vendedor = crud_vendedor.read(id=id)
    access_token = vendedor.tk_ml
    seller_id = vendedor.id_ml

    nat = verify_refresh_token(id)

    if nat != None:
        access_token = nat

    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    params = {
        'seller': seller_id,
        'q': ""
    }

    response = requests.get(f"{BASE_URL}/orders/search", headers=headers, params=params)
    sales_data = response.json()

    total = int(sales_data["paging"]["total"])
    limit = int(sales_data["paging"]["limit"])

    if total > limit:

        div_inteira = total // limit
        div_resto = total % limit

        vendas = []

        for ind in range(div_inteira+1):
            print("loop")
            params = {
                'seller': seller_id,
                'offset': (ind * limit),
                'q': ""
            }

            response = requests.get(f"{BASE_URL}/orders/search", headers=headers, params=params)
            vendas += response.json()["results"]

        print(len(vendas))

        return vendas

    return sales_data["results"]

def get_product(id, product_id):
    global BASE_URL

    vendedor = crud_vendedor.read(id=id)
    access_token = vendedor.tk_ml

    nat = verify_refresh_token(id)

    if nat != None:
        access_token = nat

    params = {'access_token': access_token}

    response = requests.get(f"{BASE_URL}/items/{product_id}", params=params)

    product = response.json()

    return product

def get_order(id, order_id):
    global BASE_URL

    vendedor = crud_vendedor.read(id=id)
    #print(vendedor)
    #client_id = vendedor.client_ml
    #client_secret = vendedor.secret_ml
    access_token = vendedor.tk_ml
    #seller_id = vendedor.id_ml
    #refresh_token = vendedor.refresh_tk_ml

    nat = verify_refresh_token(id)

    if nat != None:
        access_token = nat

    params = {'access_token': access_token}

    #ACCESS_TOKEN = "APP_USR-8228774779066849-082210-6040cbc7406412056e8df5df9381fdb3-1163179144"
    #SELLER_ID = "1163179144"

    # URL base da API do Mercado Livre
    #BASE_URL = "https://api.mercadolibre.com"

    #params = {'access_token': ACCESS_TOKEN, 'seller': SELLER_ID}
    #print(params)

    response = requests.get(f"{BASE_URL}/orders/{order_id}", params=params)
    #print(response.content)

    sale_data = response.json()

    response = requests.get(f"{BASE_URL}/orders/{order_id}/shipments", params=params)

    sale_data['shipping'] = str(response.json())

    return sale_data


def alterar_produto(item_id, data):
    global BASE_URL

    produto = crud_produto.read(id=item_id)
    #print(type(produto.seller), produto.seller)
    vendedor = crud_vendedor.read(id=produto.seller)
    access_token = vendedor.tk_ml

    nat = verify_refresh_token(produto.seller)

    if nat != None:
        access_token = nat

    params = {'access_token': access_token}

    response = requests.put(f"{BASE_URL}/items/{item_id}", params=params, json=data)

    resp = response.json()

    #print(resp)

    return resp

def visitas_seller(seller, date_from, date_to):
    global BASE_URL

    vendedor = crud_vendedor.read(id=seller)
    access_token = vendedor.tk_ml
    seller_id = vendedor.id_ml

    nat = verify_refresh_token(seller)

    if nat != None:
        access_token = nat

    params = {
        'access_token': access_token,
        'date_from': date_from,
        'date_to': f"{date_to}T23:59:59Z",
    }

    print(params)

    response = requests.get(f"{BASE_URL}/users/{seller_id}/items_visits", params=params)

    print(response.content)
    resp = response.json()


    return resp["total_visits"]

def order_shipment(seller, order_id):
    global BASE_URL

    vendedor = crud_vendedor.read(id=seller)
    access_token = vendedor.tk_ml
    #seller_id = vendedor.id_ml

    nat = verify_refresh_token(seller)

    if nat != None:
        access_token = nat

    params = {
        'access_token': access_token
    }

    response = requests.get(f"{BASE_URL}/orders/{order_id}/shipments", params=params)

    resp = response.json()

    return resp