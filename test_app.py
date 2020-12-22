import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Owner, Item, Item_image, Item_type, Item_info, Inventory_location, Seller, Address

token_manager = os.environ['MANAGER_TOKEN']
token_client = os.environ['CLIENT_TOKEN']

manager_auth_header = {"Authorization": "Bearer " + str(token_manager)}
client_auth_header = {"Authorization": "Bearer " + str(token_client)}

class ArarInventoryTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables "and initialize the app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "arar_inventory_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_item_type = {
            "name": "Printer"
        }

        self.bad_new_item_type = {
            "api": "Printer"
        } 
        
        self.new_owner = {
            "name": "Daniel Kahneman",
            "email": "daniel@kahneman.de"
        }

        self.wrong_new_owner = {
            "api": "pendejo"
        }
        

        #binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after react test"""
        pass

    def test_create_new_item_type_as_manager(self):
        res = self.client().post("/items/types", headers=manager_auth_header, json=self.new_item_type)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["id"])
        self.assertEqual(data["name"], self.new_item_type["name"])
        self.assertTrue(data["created_at"])

    # def test_delete_item_type_as_manager(self):
    #     id = Item_type.query.order_by(Item_type.id.desc()).first().id
    #     res = self.client().delete(f'/items/types/{id}', headers=manager_auth_header )
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["id"])

    # def test_delete_item_type_as_client(self):
    #     id = Item_type.query.order_by(Item_type.id.desc()).first().id
    #     res = self.client().delete(f'/items/types/{id}', headers=client_auth_header )
    #     data = json.loads(res.data)

    #     self.assertTrue(data["message"])
    #     self.assertEqual(data["success"], False)

    # def test_get_paginated_item_types(self):
    #     res = self.client().get("/items/types")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["pagination"])
    #     self.assertTrue(data["items"])
    
    # def test_422_if_page_is_less_or_equal_than_zero(self):
    #     res = self.client().get("/items/types?page=0")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "Unprocessable")

    # def test_404_if_page_does_not_exist(self):
    #     res = self.client().get("/items/types/fafaf")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], 'Not found')
    
    # def test_400_if_wrong_item_type_fields_sent(self):
    #     res = self.client().post("/items/types", headers=manager_auth_header, json=self.bad_new_item_type)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "Bad request")

    # def test_edit_item_type(self):
    #     res = self.client().patch("/items/types/1", headers=manager_auth_header, json={"name": "printer1"})        
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["id"])
    #     self.assertEqual(data["name"], "printer1")
    #     self.assertTrue(data["created_at"])

    # def test_create_new_owner_as_manager(self):
    #     res = self.client().post("/owners", headers=manager_auth_header, json=self.new_owner)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["id"])
    #     self.assertEqual(data["name"], self.new_owner["name"])
    #     self.assertTrue(data["created_at"])

    # def test_create_new_owner_as_client(self):
    #     res = self.client().post("/owners", headers=client_auth_header, json=self.new_owner)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 403)
    #     self.assertTrue(data["message"])
    #     self.assertEqual(data["success"], False)

    # def test_get_paginated_owners_as_manager(self):
    #     res = self.client().get("/owners", headers=manager_auth_header) 
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["pagination"])
    #     self.assertTrue(data["items"])

    # def test_403_get_paginated_owners_as_client(self):
    #     res = self.client().get("/owners", headers=client_auth_header) 
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 403)
    #     self.assertTrue(data["message"])
    #     self.assertEqual(data["success"], False)

    # def test_401_get_paginated_owners_no_auth_header(self):
    #     res = self.client().get("/owners") 
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertTrue(data["message"])
    #     self.assertEqual(data["success"], False)

    # def test_422_if_owner_page_is_less_or_equal_than_zero_as_manager(self):
    #     res = self.client().get("/owners?page=0", headers=manager_auth_header)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "Unprocessable")
    
    # def test_404_if_owner_page_does_not_exist(self):
    #     res = self.client().get("/owners/fafaf")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], 'Not found')
        
    # def test_edit_owner_as_manager(self):
    #     res = self.client().patch("/owners/1", headers=manager_auth_header, json={"name": "peni parker", "email": "peni@parker.de"})        
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["email"], "peni@parker.de")
    #     self.assertEqual(data["name"], "peni parker")
    #     self.assertTrue(data["created_at"])

    # def test_403_edit_owner_as_client(self):
    #     res = self.client().patch("/owners/1", headers=client_auth_header, json={"name": "peni parker", "email": "peni@parker.de"})        
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 403)
    #     self.assertTrue(data["message"])
    #     self.assertEqual(data["success"], False)

    # def test_400_if_wrong_owner_fields_sent_as_manager(self):
    #     res = self.client().post("/owners", headers=manager_auth_header, json=self.wrong_new_owner)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "Bad request")




# Make the test conveniently executable
if __name__ == "__main__":
    unittest.main()