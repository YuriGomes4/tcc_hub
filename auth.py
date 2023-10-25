import requests
from app.controllers import crud_vendedor

conta = 6

vendedor = crud_vendedor.read(id=conta)

CLIENT_ID = vendedor.client_ml
CLIENT_SECRET = vendedor.secret_ml

# Substitua essas informações pelas suas credenciais e configurações
#CLIENT_ID = "3286322038423355"
#CLIENT_SECRET = "rQ5ri5T4RYC1F4cjwUJMqlfS3HCSOgwD"
#ACCESS_TOKEN = "APP_USR-8228774779066849-082210-6040cbc7406412056e8df5df9381fdb3-1163179144"
#SELLER_ID = "1163179144"

code = "TG-64f8fbc6ad0b1b0001c39017-1380664144"
redirect_uri = "https://localhost:3000"
state = "12345"

# URL base da API do Mercado Livre
BASE_URL = "https://api.mercadolibre.com"

headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
}

data = f'grant_type=authorization_code&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&code={code}&redirect_uri={redirect_uri}'

response = requests.post(f'{BASE_URL}/oauth/token', headers=headers, data=data)

retorno = response.json()

print(retorno)

vendedor.id_ml = retorno['user_id']
vendedor.refresh_tk_ml = retorno['refresh_token']
vendedor.tk_ml = retorno['access_token']

crud_vendedor.update(vendedor)