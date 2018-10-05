from app.controllers.database import DatabaseConnection

db = DatabaseConnection()
db.create_tables()