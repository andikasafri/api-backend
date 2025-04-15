from functools import wraps
from flask import request, jsonify, current_app
from ..models.user import User
import secrets
import logging

def generate_api_key():
    return secrets.token_hex(32)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"error": "Missing token"}), 401
            
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            user = User.query.filter_by(api_key=token).first()
            if not user:
                return jsonify({"error": "Invalid token"}), 401
            
            if not user.is_active:
                return jsonify({"error": "User account is deactivated"}), 403
            
            return f(user, *args, **kwargs)
        except Exception as e:
            logging.error(f"Authentication error: {str(e)}")
            return jsonify({"error": "Authentication failed"}), 401
    return decorated