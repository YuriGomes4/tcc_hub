import requests


area = "cozinha"

url = 'http://179.34.4.73:5000/api/v1/residencias/1/areas'
resposta = requests.get(url=url)
data = resposta.json()[0]['result']

id_area = 0

for d_area in data:
    if str(d_area['nome']).lower() == area.lower():
        id_area = d_area['id']
        
url = f'http://179.34.4.73:5000/api/v1/dispositivos/search?area={id_area}'
resposta = requests.get(url=url)
data = resposta.json()[0]['result']

id_disp = data[0]['id']

url = f'http://179.34.4.73:5000/api/v1/dispositivos/info/{id_disp}'
resposta = requests.get(url=url)
data = resposta.json()[0]['result']

print(f"A temperatura da {area} esta em {data['temp']} graus")