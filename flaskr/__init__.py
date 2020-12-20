from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import current
from werkzeug.exceptions import abort  
import math

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


    @app.route('/items/types', methods=['GET'])
    def retrieve_item_types():
        
        item_types = Item_type.query.order_by(Item_type.id).all()
        current_items = paginate_items(request, item_types)
        

        return jsonify(current_items), 200
    
    @app.route('/items/types', methods=['POST'])
    def create_item_types():
        
        body = request.get_json()
        new_name = body.get('name', None)

        if new_name is None:
            abort(400)
        
        item_type = Item_type(name=new_name)
        item_type.insert()

        return jsonify(item_type.format()), 200

    @app.route('/items/types/<int:item_type_id>', methods=['PATCH'])
    def edit_item_type(item_type_id):
        try:
            body = request.get_json()
            print(item_type_id)
            item_type = Item_type.query.filter(Item_type.id == item_type_id).one_or_none()
            
            if item_type:
                item_type.name = body.get('name') if body.get('name') else item_type.name
                item_type.update()
                return jsonify(item_type.format()), 200

            else:
                abort(404)
        except:
            abort(500)

    @app.route('/items/types/<int:item_type_id>', methods=['DELETE'])
    def remove_item_type(item_type_id):
        try:
            item_type = Item_type.query.filter(Item_type.id == item_type_id).one_or_none()
            item_type.delete()
            return jsonify(item_type.format()), 200
        except:
            abort(404)

    @app.route('/owners', methods=['GET'])
    def retrieve_owners():
        owners = Owner.query.all()
        current_items = paginate_items(request, owners)

        return jsonify(current_items), 200

    @app.route('/items', methods=['GET'])
    def retrieve_items():
        items = Item.query.all()
        current_items = paginate_items(request, items)

        return jsonify(current_items), 200

    ## Error Handling

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }) , 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }) , 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }) , 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }) , 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }) , 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }) , 500
 
    return app

def paginate_items(request, selection):

    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', ITEMS_PER_PAGE, type=int)
    start = (page - 1) * size
    end = start + size
    items = [item.format() for item in selection]

    return {
        'items': items[start:end],
        'pagination': {
            'currentPage': page,
            'itemsPerPage': size,
            'totalItems': len(selection),
            'totalPages': math.ceil(len(selection) / size)
        }
    } 

