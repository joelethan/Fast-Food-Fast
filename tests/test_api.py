import json
import unittest
# from app import model #OrderList
from app.model import OrderList

from app.views import app, order



class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        # self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.order = order
        self.new_order={
                            "foodname": "steak",
                            "order_id": 1,
                            "quantity": 5,
                            "status": "pending"
                        }
        self.order2={
                        "foodname": "pizza",
                        "order_id": 2,
                        "quantity": 2,
                        "status": "status"
                    }
        self.status={
                        "status": "status"
                    }
    

    def tearDown(self):
        self.order.orders_list=[]
    

    def test_order_type(self):
        self.assertIsInstance(self.order, OrderList)


    def test_list_is_empty(self):
        self.assertFalse(OrderList().get_all_orders())


    def test_index(self):
        resp_get = self.client.get('/')
        self.assertEqual(resp_get.status_code, 200)


    def test_get_highest_order_id(self):
        self.assertEqual(self.order.get_highest_order_id(), 0)
        self.client.post('/api/v1/orders', data=json.dumps(self.new_order), content_type='application/json')
        self.assertEqual(self.order.get_highest_order_id(), 1)


    def test_add_order(self):
        self.assertFalse(self.order.get_all_orders())
        self.assertEqual(len(self.order.get_all_orders()), 0)
        resp_add = self.client.post('/api/v1/orders', data=json.dumps(self.new_order), content_type='application/json')
        self.assertEqual(resp_add.status_code, 201)
        self.assertTrue(self.order.get_all_orders())
        self.assertEqual(len(self.order.get_all_orders()), 1)


    def test_get_order(self):
        self.assertFalse(self.order.get_all_orders())
        self.client.post('/api/v1/orders', data=json.dumps(self.new_order), content_type='application/json')
        resp_get = self.client.get('/api/v1/orders/1')
        self.assertEqual(resp_get.status_code, 200)
        resp_get = self.client.get('/api/v1/orders/4')
        self.assertEqual(resp_get.status_code, 400)


    def test_get_all_order(self):
        self.assertFalse(self.order.get_all_orders())
        self.client.post('/api/v1/orders', data=json.dumps(self.new_order), content_type='application/json')
        resp_get = self.client.get('/api/v1/orders')
        self.assertEqual(resp_get.status_code, 200)


    def test_change_status(self):
        self.assertFalse(self.order.get_all_orders())
        resp_post = self.client.post('/api/v1/orders', data=json.dumps({"foodname": " w","order_id": 1,"quantity": 5,"status": "pending"}), content_type='application/json')
        self.assertIn('pending', str(resp_post.data))
        resp_chang = self.client.put('/api/v1/orders/1', data=json.dumps(self.status), content_type='application/json')
        self.assertNotIn('pending', str(resp_chang.data))
        self.assertEqual(resp_chang.status_code, 200)
        resp_chang = self.client.put('/api/v1/orders/4', data=json.dumps(self.status), content_type='application/json')
        self.assertEqual(resp_chang.status_code, 400)
    

    def test_empty_status(self):
        self.assertFalse(self.order.get_all_orders())
        self.assertRaises(ValueError, self.order.add_order, 1, 'r', 5, ' ')


    def test_status_type(self):
        self.assertFalse(self.order.get_all_orders())
        self.assertRaises(ValueError, self.order.add_order, 1, '7', 5, ['pending'])
    

    def test_empty_foodname(self):
        self.assertFalse(self.order.get_all_orders())
        self.assertRaises(ValueError, self.order.add_order, 1, '', 5, 'pending')


    def test_foodname_type(self):
        self.assertFalse(self.order.get_all_orders())
        self.assertRaises(ValueError, self.order.add_order, 1, 7, 5, 'pending')
    

    def test_order_id_type(self):
        self.assertFalse(self.order.get_all_orders())
        self.assertRaises(ValueError, self.order.add_order, '1', 'foodname', 5, 'pending')
    

    def test_quantity_type(self):
        self.assertFalse(self.order.get_all_orders())
        self.assertRaises(ValueError, self.order.add_order, 1, 'foodname', '5', 'pending')


    def test_url_not_found(self):
        resp_get = self.client.get('/api/v1/orders/food')
        self.assertEqual(resp_get.status_code, 404)
        

    @unittest.skip(' ')
    def test_delete_order(self):
        self.assertFalse(self.order.get_all_orders())
        resp_post = self.client.post('/api/v1/orders', data=json.dumps({"foodname": "","order_id": 1,"quantity": 5,"status": "pending"}), content_type='application/json')
        self.assertEqual(resp_post.status_code, 201)
        resp = self.client.delete('/api/v1/orders/1')
        self.assertEqual(resp.status_code, 202)

