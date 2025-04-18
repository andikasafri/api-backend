from flask import Blueprint, current_app, redirect, request, url_for, jsonify
from ...utils.oauth import oauth, create_oauth_user
from ...utils.auth import generate_jwt_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/google')
def google_login():
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/google/callback')
def google_callback():
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')
        if not user_info:
            raise ValueError("Failed to get user info from Google")
            
        user = create_oauth_user(user_info)
        jwt_token = generate_jwt_token(user.id)
        
        return jsonify({
            'token': jwt_token,
            'user': user.to_dict()
        })
    except Exception as e:
        current_app.logger.error(f"OAuth callback error: {str(e)}")
        return jsonify({'error': 'Authentication failed'}), 401