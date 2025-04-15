# src/__init__.py
from flask import Flask
from .config import Config
from .extensions import db, migrate  
from .api.v1 import api_v1

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Link Alembic to db
    
    # Register blueprints
    app.register_blueprint(api_v1, url_prefix="/api/v1")
    
    return app