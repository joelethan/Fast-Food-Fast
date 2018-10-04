from app.controllers.database import DatabaseConnection

db_obj = DatabaseConnection()
con  = db_obj.create_connection()
db_obj.create_users_table()
db_obj.create_menu_table()
db_obj.create_orders_table()