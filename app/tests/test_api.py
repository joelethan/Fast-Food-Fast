import json
from unittest import TestCase
from ..controllers.database import DatabaseConnection 
from ..views.app_views import db,app


class APITestCase(TestCase):
    def setUp(self):
        
        self.client = app.test_client()
        self.user_signUp = {"username": "joeffl2","email":"joel@gm","password": "password"}
        self.user_login = {"username": "joeffl2","password": "password"}

        # with app.app_context():
        #     connection = db
        #     connection.drop_tables()
        #     connection.create_tables()
        # db.drop_tables()
        db.create_tables()

    def tearDown(self):
        # with app.app_context():
        #     connection = db
        #     connection.drop_tables()
        #     connection.create_tables()
        # db.drop_tables()
        db.create_tables()

    def test_db(self):
        self.assertIsInstance(db, DatabaseConnection)

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_empty_menu(self):
        self.assertEqual(len(db.get_menu()), 0) 

    def test_empty_orders(self):
        self.assertEqual(len(db.get_orders()), 0) 

    def test_empty_users(self):
        self.assertEqual(len(db.get_users()), 0) 




    def test_signup(self):
        self.assertFalse(db.get_users())
        self.assertEqual(len(db.get_users()), 0)
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        self.assertTrue(db.get_users())
        self.assertEqual(len(db.get_users()), 1)
        self.assertEqual(response.status_code, 201)
        self.assertIn('joeffl2', json.loads(response.data)['message'])

    def test_get_menu(self):
        db.add_food_to_menu('Chicken', 20000)
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        response = self.client.get('/api/menu', headers=({"x-access-token": login_resp.json['token']}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Chicken', str(response.json['Orders'])) 

    # def test_get_orders(self):
    #     .