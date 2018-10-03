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