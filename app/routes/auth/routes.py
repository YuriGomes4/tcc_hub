# flask imports
from flask import Blueprint, Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid # for public id
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

from app.controllers import crud_usuario

from config import Config
  
# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, Config.SECRET_KEY)
            current_user = crud_usuario.read(id_publico = data['id_publico'])
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated
  
# User Database Route
# this route sends back list of users
@auth_bp.route('/verify', methods =['GET'])
@token_required
def verify(current_user):

    return jsonify({'result': "Aprovado"})
  
# route for logging user in
@auth_bp.route('/login', methods =['POST'])
def login():
    
    # creates dictionary of form data
    auth = request.form
  
    if not auth or not auth.get('email') or not auth.get('senha'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
  
    user = crud_usuario.read(email = auth.get('email'))
  
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
  
    if check_password_hash(user.senha, auth.get('senha')):
        # generates the JWT Token
        token = jwt.encode({
            'id_publico': user.id_publico,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, Config.SECRET_KEY)
  
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )
  
# signup route
@auth_bp.route('/signup', methods =['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form
  
    # gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')
  
    # checking for existing user
    user = crud_usuario.read(email = email)
    if not user:
        # database ORM object
        user = crud_usuario.create(
            data_criacao = datetime.today(),
            data_alteracao = datetime.today(),
            id_publico = str(uuid.uuid4()),
            nome = name,
            email = email,
            senha = generate_password_hash(password)
        )
  
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)