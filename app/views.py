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
            order_id = 1+order.get_highest_order_id()
            new_order = order.add_order(order_id, data['foodname'], data['quantity'], data['status'])
            return jsonify({"Added Order":new_order}), 201
            


@app.route('/api/v1/orders/<int:order_id>', methods=['DELETE','GET','PUT']) 
def get_order(order_id):
    if request.method == 'GET':
        # Get an Order
        if order.get_order(order_id):
            return jsonify({"Search":order.get_order(order_id)}), 200
        return jsonify("Order Not Found"), 400

    # will be implemented later
    # elif request.method == 'DELETE': 
    #     # Delete an Order
    #     if order.delete_order(order_id):
    #         return jsonify("Order Deleted"), 202
    #     return jsonify("Order Not Found"), 400
    else: 
        # Update status
        data = request.get_json()
        if order.get_order(order_id):
            return jsonify({"Search":order.update_status(order_id, data['status'])}), 200
        return jsonify("Order Not Found"), 400

@app.errorhandler(405)
def url_not_found(error):
    return jsonify({'message':'Requested method not allowed, try a different method'}), 405

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message':'page not found on server, check the url'}), 404
