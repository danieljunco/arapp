import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Owner, Item, Item_image, Item_type, Item_info, Inventory_location, Seller, Address

class ArarInventoryTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables "and initialize the app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "arar_inventory_test"
        self.database_path = "postgres://{}@{}/{}".format('danieljunco', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_item_type = {
            "name": "Printer"
        }

        #binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after react test"""
        pass

    def test_create_new_item_type(self):
        res = self.client().post('/items/types', json=self.new_item_type)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['id'])
        self.assertEqual(data['name'], self.new_item_type['name'])
        self.assertTrue(data['created_at'])

    def test_get_paginated_item_types(self):
        res = self.client().get('/items/types')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['pagination'])
        self.assertTrue(data['items'])


# Make the test conveniently executable
if __name__ == "__main__":
    unittest.main()