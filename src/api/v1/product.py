from flask import jsonify, request, current_app
from ...models.product import Product
from ...extensions import db
from ...utils.auth import token_required
from . import api_v1
import uuid

# Helper for pagination defaults
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 20

@api_v1.route("/products", methods=["GET"])
def get_products():
    try:
        # Pagination params
        page = request.args.get('page', DEFAULT_PAGE, type=int)
        per_page = request.args.get('per_page', DEFAULT_PER_PAGE, type=int)
        # Optional filter by current user
        user_only = request.args.get('user_only', None)

        query = Product.query
        if user_only in ('true', '1'):
            # require auth if filtering by user
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            current_user = token_required(lambda u: u)(token)
            query = query.filter_by(user_id=current_user.id)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        products = [p.to_dict() for p in pagination.items]
        return jsonify({
            'products': products,
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get products error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/products", methods=["POST"])
@token_required
def create_product(current_user):
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    price = data.get('price')

    # Basic request validation
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    try:
        price = float(price)
    except (TypeError, ValueError):
        return jsonify({'error': 'Price must be a number'}), 400

    try:
        product = Product(
            id=str(uuid.uuid4()),
            name=name,
            description=data.get('description', '').strip(),
            price=price,
            user_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
    except ValueError as ve:
        db.session.rollback()
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create product unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/products/<string:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify(product.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Get product error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/products/<string:product_id>", methods=["PUT"])
@token_required
def update_product(current_user, product_id):
    data = request.get_json() or {}
    try:
        product = Product.query.get_or_404(product_id)
        if product.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403

        # Update fields if provided
        if 'name' in data:
            name = data['name'].strip()
            if not name:
                return jsonify({'error': 'Name cannot be empty'}), 400
            product.name = name
        if 'description' in data:
            product.description = data['description'].strip()
        if 'price' in data:
            try:
                product.price = float(data['price'])
            except (TypeError, ValueError) as ve:
                return jsonify({'error': 'Invalid price value'}), 400

        db.session.commit()
        return jsonify(product.to_dict()), 200
    except ValueError as ve:
        db.session.rollback()
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update product error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/products/<string:product_id>", methods=["DELETE"])
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
        current_app.logger.error(f"Delete product error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
