import json
from unittest import TestCase
from ..controllers.database import DatabaseConnection 
from ..views.app_views import db,app


class APITestCase(TestCase):
    def setUp(self):
        
        self.client = app.test_client()
        self.user_signUp = {"username": "joelethan","email":"joelethan@gm","password": "password"}
        self.user_login = {"username": "joelethan","password": "password"}
        self.neworder = {"user_id": 1,"food_id": 1,"quantity": 10}
        self.newfood = {"foodname":"food","price":20000}

        db.create_tables()

    def tearDown(self):
        db.drop_tables()



    def test_empty_users(self):
        self.assertFalse(db.get_users())

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        len1 = len(db.get_users())
        response = self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        len2 = len(db.get_users())
        self.assertEqual(len2, 1+len1)
        self.assertEqual(response.status_code, 201)
        self.assertIn('joelethan', json.loads(response.data)['message'])

    def test_signin(self):
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        self.assertEqual(login_resp.status_code, 200)
        


    def test_get_menu(self):
        db.add_food_to_menu('Chicken', 20000)
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        response = self.client.get('/api/menu', headers=({"x-access-token": login_resp.json['token']}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Chicken', str(response.json['Orders'])) 


    def test_history(self):
        db.add_food_to_menu('Chicken',20000)
        db.add_food_to_menu('meat',20000)
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        db.place_order(1,1,10)
        db.place_order(1,2,10)
        response = self.client.get('/api/orders/hist/1', headers=({"x-access-token": login_resp.json['token']}))
        self.assertEqual(response.status_code, 200)



    def test_get_orders(self):
        db.add_food_to_menu('meat',10000)
        db.add_food_to_menu('Chicken',20000)
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        db.auto_admin()
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        db.add_user('joelggfh','joel@hhd','password')
        db.place_order(2,2,10)
        db.place_order(2,2,7)
        response = self.client.get('/api/orders', headers=({"x-access-token": login_resp.json['token']}))
        self.assertEqual(response.status_code, 200)


    def test_update_status(self):
        db.add_food_to_menu('meat',10000)
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        db.auto_admin()
        login_resp = self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        db.add_user('joelggfh','joel@hhd','password')
        db.place_order(2,1,10)
        response = self.client.put('/api/orders/1', data=json.dumps({"status":"Processing"}), 
            headers=({"x-access-token": login_resp.json['token']}),  content_type='application/json')
        self.assertEqual(response.status_code, 202)


    def test_user_to_admin(self):
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        db.auto_admin()
        login_resp=self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        db.add_user('joelhtest','joelh@test','password')
        respons = self.client.put('/api/users/2', headers=({"x-access-token": login_resp.json['token']}))
        self.assertEqual(respons.status_code, 202)


    def test_user_to_admin_by_non_user(self):
        self.client.post('/auth/signup', data=json.dumps(self.user_signUp),
                            content_type='application/json')
        db.auto_admin()
        self.client.post('/auth/login', data=json.dumps(self.user_login), 
                            content_type='application/json')
        db.add_user('joelhtest','joelh@test','password')
        respons = self.client.put('/api/users/2')
        self.assertEqual(respons.status_code, 401)