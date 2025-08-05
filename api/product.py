from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from __init__ import app, db
from model.product import Product, initProducts

# Create Blueprint
inventory_api = Blueprint('inventory_api', __name__, url_prefix='/api/inventory')
api = Api(inventory_api)

class InventoryAPI:
    class _CRUD(Resource):
        def post(self):
            """Create a new product"""
            data = request.get_json()
            if not data:
                return {'message': 'No input data provided'}, 400
            
            required = ['product_id', 'name', 'stock', 'aisle', 'price']
            if not all(key in data for key in required):
                return {'message': f'Required fields: {required}'}, 400

            # Check if product_id already exists
            if Product.query.filter_by(product_id=data['product_id']).first():
                return {'message': f'Product ID {data["product_id"]} already exists'}, 409

            try:
                product = Product(
                    product_id=data['product_id'],
                    name=data['name'],
                    stock=data['stock'],
                    aisle=data['aisle'],
                    price=data['price']
                )

                if not product.create():
                    return {'message': 'Product creation failed'}, 500
                
                return jsonify(product.read())
            except IntegrityError as e:
                db.session.rollback()
                return {'message': 'Database error: ' + str(e.orig)}, 500
        def get(self):
            """Get product by ID"""
            product_id = request.args.get('product_id')
            if not product_id:
                return {"message": "Product ID required"}, 400
            
            product = Product.query.get(product_id)
            if not product:
                return {"message": "Product not found"}, 404
            
            return jsonify(product.read())

        def put(self):
            """Update product stock/price"""
            data = request.get_json()
            if not data or 'product_id' not in data:
                return {"message": "Product ID required"}, 400
            
            product = Product.query.get(data['product_id'])
            if not product:
                return {"message": "Product not found"}, 404
            
            try:
                updates = {k: v for k, v in data.items() if k in ['stock', 'price', 'aisle']}
                if not product.update(**updates):
                    return {"message": "Update failed"}, 500
                return jsonify(product.read())
            except Exception as e:
                return {"message": str(e)}, 500

        def delete(self):
            """Delete product (admin-only)"""
            product_id = request.args.get('product_id')
            if not product_id:
                return {"message": "Product ID required"}, 400
            
            product = Product.query.get(product_id)
            if not product:
                return {"message": "Product not found"}, 404
            
            if not product.delete():
                return {"message": "Deletion failed"}, 500
            return {"message": "Product deleted"}

    class _SEARCH(Resource):
        def get(self):
            """Search products by name/aisle"""
            query = request.args.get('query')
            if not query:
                return {"message": "Search query required"}, 400
            
            products = Product.query.filter(
                or_(
                    Product.name.ilike(f'%{query}%'),
                    Product.aisle.ilike(f'%{query}%')
                )
            ).limit(50).all()
            
            return jsonify([p.read() for p in products])

    class _LOW_STOCK(Resource):
        def get(self):
            """Get low-stock items (stock < threshold)"""
            threshold = int(request.args.get('threshold', 5))
            products = Product.query.filter(Product.stock < threshold).all()
            return jsonify([p.read() for p in products])
    class _ALL(Resource):
        def get(self):
            """Get all products"""
            products = Product.query.all()
            return jsonify([p.read() for p in products])


# Register endpoints
api.add_resource(InventoryAPI._CRUD, '/')
api.add_resource(InventoryAPI._SEARCH, '/search')
api.add_resource(InventoryAPI._LOW_STOCK, '/low-stock')
api.add_resource(InventoryAPI._ALL, '/all')

# Initialize data (call once)
initProducts()