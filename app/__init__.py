# app/__init__.py
import json
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response
from jsonschema import validate

# local import
from instance.config import app_config

# For password hashing
from flask_bcrypt import Bcrypt

# initialize db
db = SQLAlchemy()

def create_app(config_name):

    from app.models import User, Cart

    app = FlaskAPI(__name__, instance_relative_config=True)
    # overriding Werkzeugs built-in password hashing utilities using Bcrypt.
    bcrypt = Bcrypt(app)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    @app.route('/')
    def index():
        return "<h1>WSCartAPI</h1>"

    @app.route('/shopping-cart/', methods=['POST', 'GET'])
    def shopping_cart():
        try:
            # get the access token
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                abort(make_response(jsonify(message="Bad Request."), 400))

            access_token = auth_header.split(" ")[1]

            if access_token:
                user_id = User.decode_token(access_token)
                if not isinstance(user_id, str):
                    # Go ahead and handle the request, the user is authed
                    if request.method == "POST":
                        schema_item_chart_data = {
                                                    "type" : "object",
                                                    "properties" : {
                                                        "item_id" : {"type" : "number"},
                                                        "item_name" : {"type" : "string"},
                                                        "item_price" : {"type" : "number"},
                                                        "amount" : {"type" : "number"}
                                                    },
                                                 }
                        # Get country based on data user
                        country_iso2 = User.get_user_country(user_id)
                        cart_data = request.data.get('cart_data', '')
                        # Validate the schema and type data input
                        for cdata in cart_data:
                            validate(cdata, schema_item_chart_data)
                        cart = Cart()
                        cart.save(user_id=user_id, country_iso2=country_iso2, cart_data=cart_data)
                        response = {'message': 'Cart created successfully.'}
                        data = {
                            'id': cart.id,
                            'date_created': cart.date_created,
                            'date_modified': cart.date_modified,
                            'created_by': cart.created_by,
                            'country_iso2': cart.country_iso2,
                            'status_id': cart.status_id                            
                        }
                        response['data'] = data
                        return make_response(jsonify(response)), 201

                    else:
                        # GET
                        # get all the cart for this user
                        carts = Cart.get_all(user_id)
                        response = {'message': 'Request success.'}
                        results = []

                        for cart in carts:
                            obj = {
                                    'id': cart.id,
                                    'date_created': cart.date_created,
                                    'date_modified': cart.date_modified,
                                    'created_by': cart.created_by,
                                    'country_iso2': cart.country_iso2,
                                    'status_id': cart.status_id,
                                    'items': []
                                   }
                            for item in cart.item_carts:
                                icart = {
                                            'id': item.id,      
                                            'cart_id': item.cart_id,
                                            'item_id': item.item_id,
                                            'item_name': item.item_name,
                                            'item_price': item.item_price,
                                            'amount': item.amount,
                                        }
                                obj['items'].append(icart)
                            results.append(obj)
                        response['data'] = results
                        return make_response(jsonify(response)), 200
                else:
                    # user is not legit, so the payload is an error message
                    message = user_id
                    response = {
                        'message': message
                    }
                    return make_response(jsonify(response)), 401
        except Exception as e:
            response = {
                'message': 'Request / Input data is not valid. Error in ' + str(e)
            }
            return make_response(jsonify(response)), 500
    @app.route('/shopping-cart/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def shopping_cart_get(id, **kwargs):

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            abort(make_response(jsonify(message="Bad Request."), 400))
            
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                cart = Cart.get_one(user_id,id)
                if not cart:
                    # Raise an HTTPException with a 404 not found status code
                    abort(make_response(jsonify(message="Cart not found."), 404))

                if request.method == "GET":
                    # GET
                    response = {'message': 'Request success.'}
                    results = {
                                'id': cart.id,
                                'date_created': cart.date_created,
                                'date_modified': cart.date_modified,
                                'created_by': cart.created_by,
                                'country_iso2': cart.country_iso2,
                                'status_id': cart.status_id,
                                'items': []
                               }
                    for item in cart.item_carts:
                        icart = {
                                    'id': item.id,      
                                    'cart_id': item.cart_id,
                                    'item_id': item.item_id,
                                    'item_name': item.item_name,
                                    'item_price': item.item_price,
                                    'amount': item.amount,
                                }
                        results['items'].append(icart)
                    response['data'] = results
                    return make_response(jsonify(response)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app

