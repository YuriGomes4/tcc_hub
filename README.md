# Taplean-Hub
 
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

alembic init migrations

sqlalchemy.url = sqlite:///database.db

project_folder/
│
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── pessoa.py
│
├── migrations/
│
├── alembic.ini
├── run.py

## Configurar servidor

Comece configurando o nginx no ambiente

```
sudo apt install nginx

sudo mv certificado/certificate.crt certificado/backup_certificate.crt

cat certificado/backup_certificate.crt certificado/ca_bundle.crt >> certificado/certificate.crt

sudo cp nginx.conf /etc/nginx/sites-available/taplean_hub

sudo nano /etc/nginx/sites-available/taplean_hub
```

Troque o caminho de **ssl_certificate** e **ssl_certificate_key** para os caminhos corretos para os arquivos do certificado SSL

```
sudo nano /etc/hosts
```

Adicione `0.0.0.0 tapleanhub.dnsfree.com` logo abaixo dos outros IPs

```
sudo nginx -t

sudo systemctl restart nginx
```

## Comandos Alembic

#### Criação de nova migração
```
alembic revision --autogenerate -m "Criacao da tabela user"
```

#### Atualiza o banco de dados para a ultima migração
```
alembic upgrade head
```

## Comandos gerais

#### Iniciar servidor Flask com Gunicorn
```
gunicorn --bind 0.0.0.0:5000 -b unix:Taplean_Hub.sock wsgi:app
```
