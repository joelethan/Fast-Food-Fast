from flask import Flask, jsonify, request, json
from app.model import OrderList 

app = Flask(__name__)
order = OrderList() 

@app.route('/')
def index():
    return "<h2 style='text-align: center;'>Welcome to Fast-Food-Fast</h2>"

@app.route('/api/v1/orders', methods=['GET','POST'])
def get_orders():
    if request.method == 'GET':
        return jsonify({ 'Orders': order.get_all_orders() }), 200
    else:
        data = request.get_json()
        if data:
        # if data not in order.get_all_orders():
            new_order = order.add_order(data['order_id'], data['foodname'], data['quantity'], data['status'])
            return jsonify({"Added Order":new_order}), 201
        # return jsonify({"Added Order":'new_order'}), 201
            


@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE','GET','PUT']) 
def get_order(order_id):
    if request.method == 'GET':
        # Get an Order
        if order.get_order(order_id):
            return jsonify({"Search":order.get_order(order_id)}), 200
        return jsonify("Order Not Found"), 400
    
    elif request.method == 'DELETE': 
        # Delete an Order
        if order.delete_order(order_id):
            return jsonify("Order Deleted"), 202
        return jsonify("Order Not Found"), 400
    else: 
        # Update status
        data = request.get_json()
        if data['status']:
            if order.get_order(order_id):
                return jsonify({"Search":order.update_status(order_id, data['status'])}), 200
            return jsonify("Order Not Found"), 400
        return jsonify('No status')
