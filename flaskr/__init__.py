from flask import Flask, jsonify
from flask_cors import CORS  

from models import setup_db, Owner, Item

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    
    @app.route('/')
    def hello():
         return jsonify({'message': 'Hello world'})

    @app.route('/smiley')
    def smiley():
        return ':)'

    @app.route('/devices/<int:device_id>', methods=['GET', 'POST'])
    def retrieve_device(device_id):
        return 'Device %d' % device_id

    @app.route('/owners', methods=['GET'])
    def retrieve_owners():
        owners = Owner.query.all()
        formatted_owner = [owner.format() for owner in owners]

        return jsonify({
            'success': True,
            'owners': formatted_owner
        })

    @app.route('/items', methods=['GET'])
    def retrieve_items():
        items = Item.query.all()
        formatted_items = [item.format() for item in items]

        return jsonify({
            'success': True,
            'items': formatted_items
        })
 
    return app