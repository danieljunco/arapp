import os
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json, sys
from sqlalchemy.orm import backref, relation, relationship
from sqlalchemy.sql.sqltypes import DateTime, Float
from sqlalchemy.sql import func

database_path = os.environ["DATABASE_URL"]

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()

class Owner(db.Model):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.transaction_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.transaction_timestamp())
    items = relationship("Item", backref="owners", lazy=True)

    def __init__(self, email, name):
        self.email = email
        self.name = name
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    
    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def format(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Item(db.Model):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    sku = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("owners.id", ondelete="CASCADE"), nullable=False)
    item_type_id = Column(Integer, ForeignKey("item_types.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.transaction_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.transaction_timestamp())
    items_info = relationship("Item_info", backref="items", lazy=True)
    item_images = relationship("Item_image", backref="items", lazy=True)

    def __init__(self, name, description, sku, user_id, item_type_id):
        self.name = name
        self.description = description
        self.sku = sku
        self.user_id = user_id
        self.item_type_id = item_type_id
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    
    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'sku': self.sku,
            'user_id': self.user_id,
            'item_type_id': self.item_type_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Item_image(db.Model):
    __tablename__ = "item_images"

    id = Column(Integer, primary_key=True)
    image_url = Column(String, nullable=False)
    item_id = Column(Integer, ForeignKey("items.id", ondelete='CASCADE'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.transaction_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.transaction_timestamp())

    def __init__(self, image_url, item_id):
        self.image_url = image_url,
        self.item_id = item_id

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    
    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def format(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'item_id': self.item_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Item_type(db.Model):
    __tablename__ = "item_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.transaction_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.transaction_timestamp())
    items = relationship("Item", backref="item_types", lazy=True)

    def __init__(self, name):
        self.name = name

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    
    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Item_info(db.Model):
    __tablename__ = "items_info"

    id = Column(Integer, primary_key=True)
    purchase_date = Column(DateTime, nullable=True)
    purchase_price = Column(Float, nullable=True)
    seller_id = Column(Integer, ForeignKey('sellers.id', ondelete='CASCADE'), nullable=True)
    item_id = Column(Integer, ForeignKey('items.id', ondelete='CASCADE'), nullable=False)
    inventory_location_id = Column(Integer, ForeignKey('inventory_locations.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.transaction_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.transaction_timestamp())

    def __init__(self, purchase_date, purchase_price, seller_id, item_id, inventory_location_id):
        self.purchase_date = purchase_date
        self.purchase_price = purchase_price
        self.seller_id = seller_id
        self.item_id = item_id
        self.inventory_location_id = inventory_location_id

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def format(self):
        return {
            'id': self.id,
            'purchase_date': self.purchase_date,
            'purchase_price': self.purchase_price,
            'seller_id': self.seller_id,
            'item_id': self.item_id,
            'inventory_location': self.inventory_location_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        

class Inventory_location(db.Model):
    __tablename__ = "inventory_locations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.transaction_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.transaction_timestamp())
    items_info = relationship("Item_info", backref="location", lazy=True)

    def __init__(self, name, address, description, image_url):
        self.name = name
        self.address = address
        self.description = description
        self.image_url = image_url

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'description': self.description,
            'image_url': self.image_url,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Seller(db.Model):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)
    website_url = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address_id = Column(Integer, ForeignKey("addresses.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.transaction_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.transaction_timestamp())
    items_info = relationship("Item_info", backref="sellers", lazy=True)

    def __init__(self, name, logo_url, website_url, email, address_id):
        self.name = name
        self.logo_url = logo_url
        self.website_url = website_url
        self.email = email
        self.address_id = address_id

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'logo_url': self.logo_url,
            'website_url': self.website_url,
            'email': self.email,
            'address_id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Address(db.Model):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    street_address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    zipcode = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.transaction_timestamp())
    updated_at = Column(DateTime(timezone=True), onupdate=func.transaction_timestamp())
    sellers = relationship("Seller", backref="addresses", lazy=True)

    def __init__(self, street_address, city, zipcode):
        self.street_address = street_address
        self.city = city
        self.zipcode = zipcode

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    
    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
            print(sys.exc_info())

    def format(self):
        return {
            'id': self.id,
            'email': self.street_address,
            'city': self.city,
            'zipcode': self.zipcode,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }