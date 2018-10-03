from flask import Flask, jsonify, request, make_response
from api.database import DatabaseConnection 
from api.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import os

db = DatabaseConnection()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'


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
def add_user():

    data = request.get_json()
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])

    if not type(username) == str:
        return jsonify({'message':'Username must be string'})
    if not type(email) == str:
        return jsonify({'message':'email must be string'})
    if not type(password) == str:
        return jsonify({'message':'password must be string'})
    if not username.strip():
        return jsonify({'message':'Username cannot be empty'})
    if not email.strip():
        return jsonify({'message':'email cannot be empty'})



    if not password.strip():
        return jsonify({'message':'password cannot be empty'})
    if len(username)<5:
        return jsonify({'message':'Username too short, should have atleast 5 character'})
    if len(password)<5:
        return jsonify({'message':'password too short, should have atleast 5 character'})
    if not '@' in email:
        return jsonify({'message':'Invalid email format'})
    if db.get_user('username', username):
        return jsonify({'message':'Username already taken'})
    if db.get_user('email', email):
        return jsonify({'message':'Your email address is already registered'})

    db.add_user(username, email, password)
    return jsonify({'message':'User created'}), 201

@app.route('/auth/login', methods=['POST'])
def login():

    data = request.get_json()
    req_username = data['username']
    req_password = data['password']

    db_user = db.get_user('username', req_username)

    if not db_user:
        return make_response('Could not verify', 401, 
                {'WWW-Authenticate' : 'Basic realm="User not registered!"'})

    user = User(db_user[0], db_user[1], db_user[2], db_user[3], db_user[4])

    if user.username == req_username and check_password_hash\
                        ( user.password, req_password):
        token = jwt.encode({'email':user.email, 'exp':datetime.datetime.utcnow()
                     + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')}), 200


    return make_response('Could not verify', 401, 
            {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/users/orders', methods=['POST'])
@token_required
def add_order(current_user):

    data = request.get_json()

    user_id = data['user_id']
    food_id = data['food_id']
    quantity = data['quantity']
    
    db.place_order(user_id, food_id, quantity)
    return jsonify({'message' : 'Order recieved'}), 201


@app.route('/api/orders/hist/<int:id>', methods=['GET'])
@token_required
def get_history_by_userid(current_user, id):
    orders = db.get_history_by_userid(id)
    return jsonify({'Order' : orders})


@app.route('/api/orders', methods=['GET'])
@token_required
def get_orders(current_user):

    # if not current_user.admin:
    #     return jsonify({'message' : 'You have limited access!'}), 403

    orders = db.get_orders()
    return jsonify({'Orders' : orders})


@app.route('/api/orders/<int:id>', methods=['GET'])
@token_required
def get_an_order(current_user, id):

    # if not current_user.admin:
    #     return jsonify({'message' : 'You have limited access!'}), 403
        
    order = db.get_an_order('order_id', id)
    return jsonify({'Order' : order})


@app.route('/api/orders/<int:id>', methods=['PUT'])
@token_required
def update_status(current_user, id):

    # if not current_user.admin:
    #     return jsonify({'message' : 'You have limited access!'}), 403

    data = request.get_json()
    status = data['status']
    db.update_status(id, status)
    return jsonify({'message' : 'Order status Updated'})


@app.route('/api/menu', methods=['GET'])
# @token_required
def get_menu():
    menu = db.get_menu()
    return jsonify({'Orders' : menu})


@app.route('/api/menu', methods=['POST'])
@token_required#,current_user
def add_2_menu(current_user):

    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'}), 403

    data = request.get_json()
    foodname = data['foodname']
    price = data['price']
    db.add_food_to_menu(foodname, price)
    return jsonify({'Order' : '{} added to the Menu'.format(foodname.title())})


@app.route('/api/users/<int:id>', methods=['PUT'])
@token_required
def user_2_admin(current_user, id):

    # if not current_user.admin:
    #     return jsonify({'message' : 'Cannot perform that function!'}), 403

    db_user = db.get_user('user_id', id)
    user = User(db_user[0], db_user[1], db_user[2], db_user[3], db_user[4])
    
    db.promote_user(id)

    return jsonify({'message' : 'User {} has been promoted'
                    .format(user.username)})