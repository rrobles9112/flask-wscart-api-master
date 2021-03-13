import os
import unittest

# class for handling a set of commands
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app

# initialize the app with all its configurations
app = create_app(config_name=os.getenv('FLASK_APP_SETTINGS'))
print(os.getenv('FLASK_APP_SETTINGS'))
migrate = Migrate(app, db)
# create an instance of class that will handle our commands
manager = Manager(app)

# Define the migration command to always be preceded by the word "db"
# Example usage: python manage.py db init
manager.add_command('db', MigrateCommand)
# Add initial data for testing product
# Usage: python manage.py seed
# @manager.command
# def seed():
# 	from app.models import Cart, ItemCart
# 	cart_data = [{'item_id':1, 'item_name': 'ananas', 'item_price':0.12, 'amount':3},
#                  {'item_id':2, 'item_name': 'mango', 'item_price':0.23, 'amount':4},
#                  {'item_id':3, 'item_name': 'papaija', 'item_price':0.34, 'amount':1},
#                  {'item_id':4, 'item_name': 'mustikka', 'item_price':0.45, 'amount':1},]

# 	new_cart = Cart(created_by=1, country_iso2='FI')
# 	db.session.add(new_cart)
# 	db.session.flush()

# 	for data in cart_data:
# 		icart = ItemCart(item_id=data['item_id'],item_name=data['item_name'],item_price=data['item_price'],
# 				 amount=data['amount'],cart_id=new_cart.id)
# 		db.session.add(icart)

# 	db.session.commit()

# define our command for testing called "test"
# Usage: python manage.py test
@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
