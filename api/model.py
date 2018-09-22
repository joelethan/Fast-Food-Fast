class Order():
    def __init__(self, order_id ,foodname, quantity, status):
        self.order_id = order_id
        self.foodname = foodname
        self.quantity = quantity
        self.status = status

    def order_input(self):
        data = {"order_id": self.order_id, "foodname": self.foodname, "quantity": self.quantity, "status":self.status}
        return data

class OrderList():

    def __init__(self):
        self.orders_list = []# {'order_id':1, 'foodname':'steak', 'quantity': 5,'status':'pending'},{'order_id':2, 'foodname':'pizza', 'quantity': 2,'status':'pending'}]

    def add_order(self, order_id, foodname, quantity, status):
        if not type(quantity) == int:
            raise ValueError('quantity must be an Integer!!')
        if not type(order_id) == int:
            raise ValueError('order_id must be an Integer!!')
        if not type(status) == str:
            raise ValueError('status must be a string!!')
        if not status.strip():
            raise ValueError('status cannot be empty!')
        if not type(foodname) == str:
            raise ValueError('foodname must be a string!!')
        if not foodname.strip():
            raise ValueError('foodname cannot be empty!')

        order = Order(order_id, foodname, quantity, status).order_input()
        self.orders_list.append(order)
        return order

    def update_status(self, order_id, status):
        for order in self.orders_list:
            if order['order_id']==order_id: 
                order['status']=status
                return order
            return False

    def get_all_orders(self):
        return self.orders_list

    def get_order(self, order_id):
        for order in self.orders_list:
            if order['order_id']==order_id:
                return order
            return False

    def delete_order(self, order_id):
        for order in self.orders_list:
            if order['order_id']==order_id:
                self.orders_list.remove(order)
                return order
            return False
 
    def find_specific_order(self, foodname):
        for order in self.orders_list:
            if order['foodname']==foodname:
                return order
