from app import db
from flask_bcrypt import Bcrypt
from flask import current_app
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload

class User(db.Model):
    """This class defines the users table """

    __tablename__ = 'users'
    # Define the columns of the users table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    country_iso2 = db.Column(db.String(2), nullable=False)
    charts = db.relationship(
        'Cart', order_by='Cart.id', cascade="all, delete-orphan")

    def __init__(self, email, password, country_iso2):
        """Initialize the user with an email and a password."""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.country_iso2 = country_iso2.upper()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """Generates the access token to be used as the Authorization header"""
        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def get_user_country(user_id):
        """Get the user properties, e.g country_iso2"""
        user_login = User.query.filter_by(id=user_id).first()
        return user_login.country_iso2

    @staticmethod
    def decode_token(token):
        """Decode the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please log in to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"

class ItemCart(db.Model):
    """This class defines the item_carts table which save detail every item in the chart."""

    __tablename__ = 'item_carts'   

    # define the columns of the table, starting with its primary key     
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'))
    item_id = db.Column(db.Integer) #item_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    item_name = db.Column(db.String(64))
    item_price = db.Column(db.Float)    
    amount = db.Column(db.Integer)
    cart = db.relationship('Cart', backref=db.backref('item_carts', lazy=True))
    # product = db.relationship('Product', backref=db.backref('products', lazy=True))

    def __repr__(self):
        """Return a representation of a ItemCart instance."""
        return "<ItemCart: {}>".format(self.id)

class Cart(db.Model):
    """This class defines the carts table."""
    
    __tablename__ = 'carts'
    
    # define the columns of the table, starting with its primary key
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    country_iso2 = db.Column(db.String(2), nullable=False)
    status_id = db.Column(db.Integer, default=0)
    cart = db.relationship('User', backref=db.backref('users', lazy=True))

    def save(self, user_id, country_iso2, cart_data):
        """Save a shopping cart"""     
        self.created_by = user_id
        self.country_iso2 = country_iso2
        self.cart_data = cart_data
        db.session.add(self)
        db.session.flush()
        for data in self.cart_data:
            icart = ItemCart(item_id=data['item_id'],item_name=data['item_name'],item_price=data['item_price'],
                     amount=data['amount'],cart_id=self.id)
            db.session.add(icart)
        db.session.commit()
        

    @staticmethod
    def get_all(user_id):
        """This method gets all the cart for a given user."""
        return Cart.query.options(joinedload('item_carts')).filter_by(created_by=user_id)
        # return session.query(Chart,ItemCart).filter_by(created_by=user_id)

    @staticmethod
    def get_one(user_id, id):
        """This method gets specific cart id for a given user."""
        return Cart.query.options(joinedload('item_carts')).filter_by(created_by=user_id).filter_by(id=id).first()
        # return session.query(Chart,ItemCart).filter_by(created_by=user_id)
    
    def __repr__(self):
        """Return a representation of a Cart instance."""
        return "<Cart: {}>".format(self.id)


u = User(country_iso2='co', email='rrobles9112@gmail.com', password='12345')

