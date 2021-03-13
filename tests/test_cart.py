import unittest
import os
import json
from app import create_app, db


class ShoppingCartTestCase(unittest.TestCase):
    """This class represents the cart test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.data =  json.dumps({'cart_data':[
                                                {'item_id':1, 'item_name': 'ananas', 'item_price':0.12, 'amount':8},
                                                {'item_id':2, 'item_name': 'mango', 'item_price':0.23, 'amount':4}
                                            ]})

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234", country_iso2="FI"):
        user_data = {
            'email': email,
            'password': password,
            'country_iso2': country_iso2
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def test_api_cart_creation(self):
        """Test API can create a cart (POST request)"""

        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client().post('/shopping-cart/',headers=dict(Authorization="Bearer " + access_token), data=self.data,
                       content_type='application/json')
        json_data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json_data['message'], 'Cart created successfully.')
        self.assertIn('id', json_data['data'])
        self.assertIn('country_iso2', json_data['data'])
        self.assertEqual(json_data['data']['country_iso2'], 'FI')

    def test_api_can_get_all_carts(self):
        """Test API can get all of user carts (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/shopping-cart/',headers=dict(Authorization="Bearer " + access_token), data=self.data,
                       content_type='application/json')
        res = self.client().get(
            '/shopping-cart/',
            headers=dict(Authorization="Bearer " + access_token),
        )
        json_data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['message'], 'Request success.')
        self.assertEqual(json_data['data'][0]['country_iso2'], 'FI')
        self.assertEqual(len(json_data['data'][0]['items']), 2)

    def test_api_can_get_one_cart(self):
        """Test API can get one cart based on input id (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/shopping-cart/',headers=dict(Authorization="Bearer " + access_token), data=self.data,
                       content_type='application/json')
        res = self.client().get(
            '/shopping-cart/1',
            headers=dict(Authorization="Bearer " + access_token),
        )
        json_data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(json_data['message'], 'Request success.')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data['message'], 'Request success.')
        self.assertIn('id', json_data['data'])
        self.assertEqual(json_data['data']['id'], 1)
        self.assertIn('country_iso2', json_data['data'])
        self.assertEqual(json_data['data']['country_iso2'], 'FI')

    def test_api_cart_not_found(self):
        """Test API response cart not found (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        res = self.client().post('/shopping-cart/',headers=dict(Authorization="Bearer " + access_token), data=self.data,
                       content_type='application/json')
        res = self.client().get(
            '/shopping-cart/100',
            headers=dict(Authorization="Bearer " + access_token),
        )
        json_data = json.loads(res.data.decode('utf-8'))
        self.assertEqual(json_data['message'], 'Cart not found.')
        self.assertEqual(res.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
