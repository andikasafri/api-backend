from flask import jsonify, request, current_app
from ...models.transaction import Transaction, TransactionItem
from ...models.product import Product
from ...extensions import db
from ...utils.auth import token_required
from . import api_v1
import uuid

@api_v1.route("/transactions", methods=["GET"])
@token_required
def get_transactions(current_user):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = Transaction.query.filter_by(user_id=current_user.id)\
            .order_by(Transaction.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'transactions': [t.to_dict() for t in pagination.items],
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get transactions error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/transactions", methods=["POST"])
@token_required
def create_transaction(current_user):
    try:
        data = request.get_json()
        if not data or 'items' not in data:
            return jsonify({'error': 'Missing required data'}), 400
        
        # Validate and calculate total
        total_amount = 0
        items_data = []
        
        for item in data['items']:
            product = Product.query.get(item.get('product_id'))
            if not product:
                return jsonify({'error': f'Product not found: {item.get("product_id")}'}), 404
            
            quantity = int(item.get('quantity', 0))
            if quantity <= 0:
                return jsonify({'error': 'Invalid quantity'}), 400
            
            item_total = product.price * quantity
            total_amount += item_total
            
            items_data.append({
                'product_id': product.id,
                'quantity': quantity,
                'price_at_time': product.price
            })
        
        # Create transaction
        transaction = Transaction(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            total_amount=total_amount,
            status='pending'
        )
        
        # Add items
        for item_data in items_data:
            item = TransactionItem(
                id=str(uuid.uuid4()),
                transaction_id=transaction.id,
                **item_data
            )
            db.session.add(item)
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify(transaction.to_dict()), 201
    except ValueError as ve:
        db.session.rollback()
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create transaction error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/transactions/<transaction_id>", methods=["GET"])
@token_required
def get_transaction(current_user, transaction_id):
    try:
        transaction = Transaction.query.filter_by(id=transaction_id, user_id=current_user.id).first_or_404()
        return jsonify(transaction.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Get transaction error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/transactions/<transaction_id>/status", methods=["PUT"])
@token_required
def update_transaction_status(current_user, transaction_id):
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        transaction = Transaction.query.filter_by(id=transaction_id, user_id=current_user.id).first_or_404()
        transaction.status = data['status']
        
        db.session.commit()
        return jsonify(transaction.to_dict()), 200
    except ValueError as ve:
        db.session.rollback()
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update transaction status error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500