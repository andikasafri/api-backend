from flask import Flask, jsonify
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate
from .api.v1 import api_v1
from .middleware import (
    limiter, 
    request_logger, 
    register_error_handlers,
    security,
    compression
)
import logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    # Initialize middleware
    CORS(app)
    limiter.init_app(app)
    security.init_app(app)
    compression.init_app(app)
    register_error_handlers(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints with middleware
    app.register_blueprint(api_v1, url_prefix="/api/v1")
    
    @app.route("/")
    @limiter.limit("10 per minute")
    def health_check():
        return jsonify({
            "status": "Healthy",
            "version": "1.0",
            "database": "connected" if db.engine.connect() else "disconnected"
        })
    
    return app