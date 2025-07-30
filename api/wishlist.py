from flask import Blueprint, jsonify, request, g
from __init__ import app, db
from model.wishlist import Wishlist
from model.user import User
from model.product import Product
from api.jwt_authorize import token_required
from datetime import datetime

wishlist_api = Blueprint('wishlist_api', __name__, url_prefix='/api/wishlist')

# Get all products (dropdown for UI)
@wishlist_api.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return jsonify([
        {'id': p.id, 'name': p.name, 'availability': p.availability}
        for p in products
    ])

# Get user's wishlist
@wishlist_api.route('/', methods=['GET'])
@token_required()
def get_user_wishlist():
    current_user = g.current_user
    items = Wishlist.query.filter_by(user_uid=current_user._uid).all()

    response = []
    for item in items:
        response.append({
            'id': item.id,
            'product_id': item.product_id,
            'product_name': item.product.name,
            'availability': item.product.availability,
            'date_added': item.date_added.strftime('%Y-%m-%d'),
            'notify': item.notify
        })
    return jsonify(response)

# Add product to wishlist
@wishlist_api.route('/', methods=['POST'])
@token_required()
def add_to_wishlist():
    current_user = g.current_user
    data = request.get_json()

    product_id = data.get('product_id')
    notify = data.get('notify', False)

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    existing = Wishlist.query.filter_by(user_uid=current_user._uid, product_id=product_id).first()
    if existing:
        return jsonify({'error': 'Product already in wishlist'}), 400

    new_item = Wishlist(user_uid=current_user._uid, product_id=product_id, notify=notify)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Product added to wishlist'}), 201

# Update wishlist item (e.g., toggle notify)
@wishlist_api.route('/<int:id>', methods=['PUT'])
@token_required()
def update_wishlist(id):
    current_user = g.current_user
    item = Wishlist.query.get(id)

    if not item or item.user_uid != current_user._uid:
        return jsonify({'error': 'Wishlist item not found'}), 404

    data = request.get_json()
    if 'notify' in data:
        item.notify = data['notify']
        db.session.commit()
        return jsonify({'message': 'Notification preference updated'}), 200

    return jsonify({'error': 'No valid fields to update'}), 400

# Delete from wishlist
@wishlist_api.route('/<int:id>', methods=['DELETE'])
@token_required()
def delete_from_wishlist(id):
    current_user = g.current_user
    item = Wishlist.query.get(id)

    if not item or item.user_uid != current_user._uid:
        return jsonify({'error': 'Wishlist item not found'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Wishlist item removed'}), 200

# Admin: Update product availability
@wishlist_api.route('/availability/<int:product_id>', methods=['PUT'])
@token_required()
def update_product_availability(product_id):
    current_user = g.current_user
    if current_user.role != 'Admin':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    new_availability = data.get('availability')
    if new_availability not in ['in stock', 'out of stock']:
        return jsonify({'error': 'Invalid availability'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    product.availability = new_availability
    db.session.commit()

    # Notify users if the product is back in stock
    if new_availability == 'in stock':
        notify_users(product_id)

    return jsonify({'message': f'{product.name} marked as {new_availability}'}), 200

# Notify subscribed users (simulated print for now)
def notify_users(product_id):
    wishlist_items = Wishlist.query.filter_by(product_id=product_id, notify=True).all()
    for item in wishlist_items:
        user = User.query.get(item.user_uid)
        print(f"[NOTIFY] Notifying {user.name} ({user.email}) that {item.product.name} is now in stock.")