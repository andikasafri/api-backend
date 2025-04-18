from functools import wraps
from flask import request, jsonify, current_app
from ..models.user import User
import secrets
import jwt
from datetime import datetime, timedelta
import logging

def generate_api_key():
    return secrets.token_hex(32)

def generate_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({"error": "Missing token"}), 401
            
            # Handle both JWT and API key authentication
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
                # Try JWT first
                user_id = verify_jwt_token(token)
                if user_id:
                    user = User.query.get(user_id)
                else:
                    # Fall back to API key
                    user = User.query.filter_by(api_key=token).first()
            else:
                # Treat as API key
                user = User.query.filter_by(api_key=auth_header).first()
            
            if not user:
                return jsonify({"error": "Invalid token"}), 401
            
            if not user.is_active:
                return jsonify({"error": "User account is deactivated"}), 403
            
            return f(user, *args, **kwargs)
        except Exception as e:
            logging.error(f"Authentication error: {str(e)}")
            return jsonify({"error": "Authentication failed"}), 401
    return decorated