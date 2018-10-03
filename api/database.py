import psycopg2

class DatabaseConnection:
	def __init__(self):
		try:
			self.connection = psycopg2.connect(database="postgres",
								user="postgres",
								host="localhost",
								password="166091postgres",
								port="5432")
			self.connection.autocommit = True
			self.cursor = self.connection.cursor()
			print('Conneced to db')

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
		
