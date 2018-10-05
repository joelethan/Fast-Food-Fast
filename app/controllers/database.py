import psycopg2
import os

class DatabaseConnection:
	def __init__(self):
		try:
			postgres = "postgres"
			# if os.getenv('APP_SETTINGS') == 'testing':
			# 	postgres = "mydb"
			# print(os.getenv('APP_SETTINGS'))
			self.connection = psycopg2.connect(database=postgres,
								user="postgres",
								host="localhost",
								password="166091postgres",
								port="5432")
			self.connection.autocommit = True
			self.cursor = self.connection.cursor()

		except Exception as e:
			print(e)
			print('Failed to connect to db')


	def create_tables(self):

		""" Create all database tables"""

		create_table = "CREATE TABLE IF NOT EXISTS users \
			( user_id SERIAL PRIMARY KEY, username VARCHAR(10), \
			email VARCHAR(100), password VARCHAR(100), admin BOOLEAN NOT NULL);"
		self.cursor.execute(create_table)

		create_table = "CREATE TABLE IF NOT EXISTS menu \
			( food_id SERIAL PRIMARY KEY, foodname VARCHAR(15), price INTEGER);"
		self.cursor.execute(create_table)

		create_table = "CREATE TABLE IF NOT EXISTS orders \
			( order_id SERIAL PRIMARY KEY, \
			user_id INTEGER NOT NULL REFERENCES users(user_id), \
			food_id INTEGER NOT NULL REFERENCES menu(food_id), \
			quantity INTEGER, status VARCHAR(10));"
		self.cursor.execute(create_table)
		


	def add_user(self, username, email, password):
		query = "INSERT INTO users (username, email, password, admin) VALUES\
			('{}', '{}', '{}', False);".format(username, email, password)
		self.cursor.execute(query)


	def add_food_to_menu(self, foodname, price):
		query = "INSERT INTO menu (foodname, price) VALUES ('{}', '{}');"\
			.format(foodname, price)
		self.cursor.execute(query)


	def get_orders(self):
		# query = "SELECT row_to_json(row) FROM () row;"
		query = "SELECT * FROM orders;"
		self.cursor.execute(query)
		orders = self.cursor.fetchall()
		return orders


	def get_users(self):
		query = "SELECT * FROM users;"
		self.cursor.execute(query)
		users = self.cursor.fetchall()
		return users


	def get_menu(self):
		query = "SELECT row_to_json(row) FROM (SELECT * FROM menu) row;"
		self.cursor.execute(query)
		menu = self.cursor.fetchall()
		return menu


	def get_an_order(self, column, value):
		# query = "SELECT row_to_json(row) FROM () row;"
		query = "SELECT * FROM orders WHERE {} = '{}'".format(column, value)
		self.cursor.execute(query)
		user = self.cursor.fetchone()
		return user


	def get_user(self, column, value):
		# query = "SELECT row_to_json(row) FROM (SELECT * FROM users WHERE {} = '{}') row;".format(column, value)
		query = "SELECT * FROM users WHERE {} = '{}';".format(column, value)
		self.cursor.execute(query)
		user = self.cursor.fetchone()
		print(user)
		return user


	def promote_user(self, order_id):
		query = "UPDATE users SET admin = True WHERE user_id = '{}';\
		".format(order_id)
		self.cursor.execute(query)


	def place_order(self, user_id, food_id, quantity):
		query = "INSERT INTO orders (user_id, food_id, quantity, status) \
			VALUES ('{}', '{}', '{}', 'New');".format(user_id, food_id, quantity)
		self.cursor.execute(query)


	def update_status(self, order_id, status):
		query = "UPDATE orders SET status = '{}' WHERE order_id = '{}';\
		".format(status, order_id)
		self.cursor.execute(query)


	def get_history_by_userid(self, userid):
		# query = "SELECT row_to_json(row) FROM () row;"
		query = "SELECT * FROM orders WHERE user_id = '{}'".format(userid)
		self.cursor.execute(query)
		history = self.cursor.fetchall()
		return history
		

	def auto_admin(self):
		query = "UPDATE users SET admin = True WHERE user_id < 2;"
		self.cursor.execute(query)


	def drop_tables(self):
		query = "DROP TABLE orders;DROP TABLE menu;DROP TABLE users; "
		self.cursor.execute(query)
		return "Droped"

	def duplicate_in_Items(self, table, column, value):
		query = "SELECT * FROM {} WHERE {} = '{}';".format(table, column, value)
		self.cursor.execute(query)
		meal = self.cursor.fetchone()
		if meal:
			return True
		return False

# print(DatabaseConnection())
# print(DatabaseConnection().duplicate_in_Items('menu','foodname','food'))

# (DatabaseConnection().add_user('joel1', 'joel@mail', 'password'))			#

# (DatabaseConnection().place_order(2, 1, 9))								#

# print(DatabaseConnection().get_an_order('order_id', 2))					#

# print(DatabaseConnection().update_status( 2, 'Pending'))					#

# print(DatabaseConnection().get_menu())									#

# (DatabaseConnection().add_food_to_menu('Beef', 20000))					#

# print(DatabaseConnection().get_history_by_userid(1))						#

# print(DatabaseConnection().get_orders())									#

# print(DatabaseConnection().get_users())									#

# (DatabaseConnection().drop_tables())									

# print(DatabaseConnection().get_user('username', 'joejl'))						#