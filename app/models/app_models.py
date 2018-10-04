class User():
    def __init__(self, user_id, username, email, password, admin):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin

class Order():
    def __init__(self, order_id ,foodname, quantity, status):
        self.order_id = order_id
        self.foodname = foodname
        self.quantity = quantity
        self.status = status

class Menu():
    def __init__(self, food_id ,foodname, price):
        self.food_id = food_id
        self.foodname = foodname
        self.price = price
