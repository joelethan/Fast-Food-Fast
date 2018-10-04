from flask import Flask, jsonify, request, make_response
from ..controllers.database import DatabaseConnection 
from ..models.app_models import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flasgger import Swagger, swag_from

import datetime
from functools import wraps
import os


db = DatabaseConnection()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'

Swagger(app) 

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            db_user = db.get_user('email', data['email'])
            current_user = User(db_user[0], db_user[1], db_user[2], 
                            db_user[3], db_user[4])
        except:
            return jsonify({'message':'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/')
def index():
    return "<h2 style='text-align: center'>Welcome 2 Week 2</h2>"

@app.route('/auth/signup', methods=['POST'])
@swag_from('../Docs/signup.yml')
def add_user():

    data = request.get_json()
    username = (data['username']).strip()
    email = (data['email']).strip()
    password = generate_password_hash(data['password'])

    if not type(username) == str:
        return jsonify({'message':'Username must be string'}), 400

    if not type(email) == str:
        return jsonify({'message':'email must be string'}), 400

    if not type(password) == str:
        return jsonify({'message':'password must be string'}), 400

    if not username.strip():
        return jsonify({'message':'Username cannot be empty'}), 400

    if not email.strip():
        return jsonify({'message':'email cannot be empty'}), 400

    if not password.strip():
        return jsonify({'message':'password cannot be empty'}), 400

    if len(username)<5:
        return jsonify({'message':'Username too short, should have atleast 5 character'}), 400

    if len(password)<5:
        return jsonify({'message':'password too short, should have atleast 5 character'}), 400

    if not '@' in email:
        return jsonify({'message':'Invalid email format'}), 400

    if db.get_user('username', username):
        return jsonify({'message':'Username already taken'}), 400

    if db.get_user('email', email):
        return jsonify({'message':'Your email address is already registered'}), 400

    db.add_user(username, email, password)
    return jsonify({'message':'User {} created'.format(username)}), 201

@app.route('/auth/login', methods=['POST'])
def login():

    data = request.get_json()
    req_username = (data['username']).strip()
    req_password = (data['password']).strip()

    db_user = db.get_user('username', req_username)

    if not db_user:
        return make_response('Could not verify', 401, 
                {'WWW-Authenticate' : 'Basic realm="User not registered!"'})

    user = User(db_user[0], db_user[1], db_user[2], db_user[3], db_user[4])

    if user.username == req_username and check_password_hash( user.password, req_password):
        token = jwt.encode({'email':user.email, 'admin':user.admin, 'exp':datetime.datetime.utcnow()+ datetime.timedelta(hours=60)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8'), 'message':'User logged-in'}), 200


    return make_response('Could not verify', 401, 
            {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/users/orders', methods=['POST'])
@token_required
def add_order(current_user):

    """ To be implemented with name,
    not just ids to be shown in postman"""

    data = request.get_json()

    user_id = data['user_id']
    food_id = data['food_id']
    quantity = data['quantity']


    if not type(user_id) == int:
        return jsonify({'message':'User_id must be Int'}), 400
    
    db.place_order(user_id, food_id, quantity)
    return jsonify({'message' : 'Order recieved'}), 201


@app.route('/api/orders/hist/<int:id>', methods=['GET'])
@token_required
def get_history_by_userid(current_user, id):
    orders = db.get_history_by_userid(id)
    return jsonify({'Order' : orders}), 200


@app.route('/api/orders', methods=['GET'])
@token_required
def get_orders(current_user):

    if not current_user.admin:
        return jsonify({'message':'You don\'t have access to this function!!!!'}), 403

    orders = db.get_orders()
    return jsonify({'Orders' : orders}), 200


@app.route('/api/orders/<int:id>', methods=['GET'])
@token_required
def get_an_order(current_user, id):

    if not current_user.admin:
        return jsonify({'message':'You don\'t have access to this function!!!!'}), 403
        
    order = db.get_an_order('order_id', id)
    return jsonify({'Order' : order}), 200


@app.route('/api/orders/<int:id>', methods=['PUT'])
@token_required
def update_status(current_user, id):

    if not current_user.admin:
        return jsonify({'message':'You don\'t have access to this function!!!!'}), 403


    data = request.get_json()
    status = (data['status']).strip()

    if not type(status) == str:
        return jsonify({'message':'Status must be String'}), 400
    if not status.strip():
        return jsonify({'message':'Status cannot be empty'}), 400
    if not status.title() in ['New','Processing','Cancelled','Complete']:
        return ({'message':"Status must be in the given list: ['New','Processing','Cancelled','Complete']"})

    db.update_status(id, status)
    return jsonify({'message' : 'Order status Updated to {}'.format(status)}), 202


@app.route('/api/menu', methods=['GET'])
@token_required
def get_menu(current_user):

    menu = db.get_menu()
    return jsonify({'Orders' : menu}), 200


@app.route('/api/menu', methods=['POST'])
@token_required
def add_2_menu(current_user):

    if not current_user.admin:
        return jsonify({'message':'You don\'t have access to this function!!!!'}), 403


    data = request.get_json()
    foodname = (data['foodname']).strip()
    price = data['price']

    if not type(price) == int:
        return jsonify({'message':'Price must be an Int!!'}), 400

    if not type(foodname) == str:
        return jsonify({'message':'Foodname must be String!!'}), 400

    if not foodname.strip():
        return jsonify({'message':'Foodname cannot be empty!!'}), 400

    
    db.add_food_to_menu(foodname, price)
    return jsonify({'Order' : '{} added to the Menu'.format(foodname.title())}), 201


@app.route('/api/users/<int:id>', methods=['PUT'])
@token_required
def user_2_admin(current_user, id):

    db_user = db.get_user('user_id', id)
    user = User(db_user[0], db_user[1], db_user[2], db_user[3], db_user[4])
    
    db.promote_user(id)

    return jsonify({'message' : 'User {} has been promoted'
                    .format(user.username)}), 202

@app.errorhandler(405)
def url_not_found(error):
    return jsonify({'message':'Requested method not allowed, try a different method'}), 405

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message':'page not found on server, check the url'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message':'internal server error, check the inputs'}), 500