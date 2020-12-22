from flask import Flask, json, jsonify, request
from flask_cors import CORS
from flask_migrate import current
from sqlalchemy.orm import query
from werkzeug.exceptions import abort
import math


from auth.auth import AuthError, requires_auth
from models import (
    setup_db,
    Owner,
    Item,
    Item_image,
    Item_type,
    Item_info,
    Inventory_location,
    Seller,
    Address
    )

ITEMS_PER_PAGE = 10


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    return app


app = create_app()


@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type, Authorization')
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET, POST, PATCH, DELETE, OPTIONS')
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
@requires_auth('post:item-types')
def create_item_types(jwt):

    body = request.get_json()
    new_name = body.get('name')

    if new_name is None:
        abort(400)

    item_type = Item_type(name=new_name)
    item_type.insert()

    return jsonify(item_type.format()), 200


@app.route('/items/types/<int:item_type_id>', methods=['PATCH'])
@requires_auth('patch:item-types')
def edit_item_type(jwt, item_type_id):
    try:
        body = request.get_json()
        item_type = Item_type.query.filter(
            Item_type.id == item_type_id).one_or_none()

        if item_type:
            item_type.name = body.get('name') if body.get(
                'name') else item_type.name
            item_type.update()
            return jsonify(item_type.format()), 200

        else:
            abort(404)
    except BaseException:
        abort(500)


@app.route('/items/types/<int:item_type_id>', methods=['DELETE'])
@requires_auth('delete:item-types')
def remove_item_type(jwt, item_type_id):
    try:
        item_type = Item_type.query.filter(
            Item_type.id == item_type_id).one_or_none()
        item_type.delete()
        return jsonify(item_type.format()), 200
    except BaseException:
        abort(404)


@app.route('/owners', methods=['GET'])
@requires_auth('get:owners')
def retrieve_owners(jwt):
    owners = Owner.query.all()
    current_items = paginate_items(request, owners)

    return jsonify(current_items), 200


@app.route('/owners', methods=['POST'])
@requires_auth('post:owners')
def create_owners(jwt):
    body = request.get_json()
    new_email = body.get('email')
    new_name = body.get('name')

    if new_email is None or new_name is None:
        abort(400)

    owner = Owner(email=new_email, name=new_name)
    owner.insert()

    return jsonify(owner.format()), 200


@app.route('/owners/<int:owner_id>', methods=['PATCH'])
@requires_auth('patch:owners')
def edit_owner(jwt, owner_id):
    body = request.get_json()
    try:
        owner = Owner.query.filter(Owner.id == owner_id).one_or_none()

        if owner:
            owner.name = body.get('name') if body.get('name') else owner.name
            owner.email = body.get('email') if body.get(
                'email') else owner.email
            owner.update()
            return jsonify(owner.format()), 200
        else:
            abort(404)
    except BaseException:
        abort(500)


@app.route('/owners/<int:owner_id>', methods=['DELETE'])
@requires_auth('delete:owners')
def remove_owner(jwt, owner_id):
    try:
        owner = Owner.query.filter(Owner.id == owner_id).one_or_none()
        owner.delete()
        return jsonify(owner.format()), 200
    except BaseException:
        abort(404)


@app.route('/inventory-locations', methods=['GET'])
def retrieve_inventory_locations():
    locations = Inventory_location.query.all()
    current_locations = paginate_items(request, locations)

    return jsonify(current_locations), 200


@app.route('/inventory-locations', methods=['POST'])
@requires_auth('post:inventory-locations')
def create_inventory_location(jwt):

    body = request.get_json()
    new_name = body.get('name')
    new_address = body.get('address')
    new_description = body.get('description', '')
    new_image_url = body.get('image_url', '')

    if new_name is None or new_address is None:
        abort(400)

    inventory_location = Inventory_location(
        name=new_name,
        address=new_address,
        description=new_description,
        image_url=new_image_url)
    inventory_location.insert()

    return jsonify(inventory_location.format()), 200


@app.route('/inventory-locations/<int:inventory_location_id>',
           methods=['PATCH'])
@requires_auth('patch:inventory-locations')
def edit_inventory_location(jwt, inventory_location_id):
    try:
        body = request.get_json()
        inventory_location = Inventory_location.query.filter(
            Inventory_location.id == inventory_location_id).one_or_none()

        if inventory_location:
            inventory_location.name = body.get('name') if body.get(
                'name') else inventory_location.name
            inventory_location.address = body.get('address') if body.get(
                'address') else inventory_location.address
            inventory_location.update()
            return jsonify(inventory_location.format()), 200

        else:
            abort(404)
    except BaseException:
        abort(500)


@app.route('/inventory-locations/<int:inventory_location_id>',
           methods=['DELETE'])
@requires_auth('delete:inventory-locations')
def remove_inventory_location(jwt, inventory_location_id):
    try:
        inventory_location = Inventory_location.query.filter(
            Inventory_location.id == inventory_location_id).one_or_none()
        inventory_location.delete()
        return jsonify(inventory_location.format()), 200
    except BaseException:
        abort(404)


@app.route('/items/<int:item_id>images', methods=['GET'])
def retrieve_item_images(item_id):
    try:
        image = Item_image.query.get(item_id)
        if image:
            images = Item.join(Item_image).all()
            current_images = paginate_items(request, images)
            return jsonify(current_images), 200

        else:
            abort(404)
    except BaseException:
        abort(500)


@app.route('/items', methods=['GET'])
def retrieve_items():
    items = Item.query.all()
    current_items = paginate_items(request, items)

    return jsonify(current_items), 200

# Error Handling


@app.errorhandler(AuthError)
def authentification_failed(AuthError):
    return jsonify({
        'success': False,
        'error': AuthError.status_code,
        'message': AuthError.error['description']
    }), AuthError.status_code


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed"
    }), 405


@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal server error"
    }), 500

# return app


def paginate_items(request, selection):

    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', ITEMS_PER_PAGE, type=int)
    if(page <= 0 or size <= 0):
        abort(422)
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
