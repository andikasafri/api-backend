from functools import wraps
from flask import request, jsonify
from ..models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Missing token"}), 401
        
        # Simple token lookup (replace with JWT or database check)
        user = User.query.filter_by(api_key=token).first()
        if not user:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(user, *args, **kwargs)
    return decorated