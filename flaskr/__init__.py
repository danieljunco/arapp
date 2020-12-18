from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import abort  

from models import setup_db, Owner, Item, Item_image, Item_type, Item_info, Inventory_location, Seller, Address

ITEMS_PER_PAGE = 10

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

    
    @app.route('/item/types', methods=['POST'])
    def create_item_types():
        
        body = request.get_json()
        new_name = body.get('name', None)

        if new_name is None:
            abort(400)
        
        type = Item_type(name=new_name)
        type.insert()

        return jsonify({
            'id': type.id
        })


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

    ## Error Handling

    @app.error_handler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }) , 400

    @app.error_handler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }) , 401

    @app.error_handler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }) , 403

    @app.error_handler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }) , 404

    @app.error_handler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }) , 405

    @app.error_handler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }) , 500
 
    return app

def paginate_items(request, selection):

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    items = [item.format() for item in selection]

    return items[start:end]

