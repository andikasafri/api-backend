from authlib.integrations.flask_client import OAuth
from flask import current_app, url_for
from functools import wraps
import jwt
import uuid

oauth = OAuth()

def setup_oauth(app):
    oauth.init_app(app)
    
    oauth.register(
        name='google',
        client_id=app.config['OAUTH_GOOGLE_CLIENT_ID'],
        client_secret=app.config['OAUTH_GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )

def create_oauth_user(user_info):
    from ..models.user import User
    from ..extensions import db
    
    email = user_info.get('email')
    if not email:
        raise ValueError("Email not provided by OAuth provider")
        
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            first_name=user_info.get('given_name'),
            last_name=user_info.get('family_name'),
            oauth_provider='google',
            oauth_id=user_info.get('sub'),
            api_key=secrets.token_hex(32)
        )
        db.session.add(user)
        db.session.commit()
        
    return user