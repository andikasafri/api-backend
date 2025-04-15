from flask import jsonify, request, current_app
from ...models.user import User
from ...extensions import db
from ...utils.auth import token_required, generate_api_key
from . import api_v1
import uuid

@api_v1.route("/auth/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
            
        if User.query.filter_by(email=data['email'].lower()).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        user = User(
            id=str(uuid.uuid4()),
            email=data['email'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            api_key=generate_api_key()
        )
        
        try:
            user.set_password(data['password'])
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'api_key': user.api_key
        }), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        user = User.query.filter_by(email=data['email'].lower()).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'api_key': user.api_key
        })
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/users", methods=["GET"])
@token_required
def get_users(current_user):
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        current_app.logger.error(f"Get users error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/users/<user_id>", methods=["GET"])
@token_required
def get_user(current_user, user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict())
    except Exception as e:
        current_app.logger.error(f"Get user error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@api_v1.route("/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    return jsonify(current_user.to_dict())

@api_v1.route("/profile", methods=["PUT"])
@token_required
def update_profile(current_user):
    try:
        data = request.get_json()
        
        if 'email' in data and data['email'] != current_user.email:
            if User.query.filter_by(email=data['email'].lower()).first():
                return jsonify({'error': 'Email already exists'}), 409
            current_user.email = data['email']
        
        if 'first_name' in data:
            current_user.first_name = data['first_name']
        if 'last_name' in data:
            current_user.last_name = data['last_name']
        if 'password' in data:
            try:
                current_user.set_password(data['password'])
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
        
        db.session.commit()
        return jsonify(current_user.to_dict())
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update profile error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500