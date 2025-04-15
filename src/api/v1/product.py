from flask import jsonify, request, current_app
from ...models.product import Product
from ...extensions import db
from ...utils.auth import token_required
from . import api_v1
import uuid

@api_v1.route("/products", methods=["GET"])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products])
    except Exception as e:
        current_app.logger.error(f"Get products error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/products", methods=["POST"])
@token_required
def create_product(current_user):
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['name', 'price']):
            return jsonify({'error': 'Missing required fields'}), 400
            
        try:
            product = Product(
                id=str(uuid.uuid4()),
                name=data['name'],
                description=data.get('description', ''),
                price=float(data['price']),
                user_id=current_user.id
            )
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify(product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create product error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/products/<product_id>", methods=["GET"])
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify(product.to_dict())
    except Exception as e:
        current_app.logger.error(f"Get product error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/products/<product_id>", methods=["PUT"])
@token_required
def update_product(current_user, product_id):
    try:
        product = Product.query.get_or_404(product_id)
        
        if product.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        data = request.get_json()
        
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            try:
                product.price = float(data['price'])
            except ValueError:
                return jsonify({'error': 'Invalid price value'}), 400
        
        db.session.commit()
        return jsonify(product.to_dict())
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update product error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/products/<product_id>", methods=["DELETE"])
@token_required
def delete_product(current_user, product_id):
    try:
        product = Product.query.get_or_404(product_id)
        
        if product.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Delete product error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500