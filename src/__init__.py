from flask import Flask, jsonify
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate
from .api.v1 import api_v1

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    app.register_blueprint(api_v1, url_prefix="/api/v1")
    
    @app.route("/")
    def health_check():
        return jsonify({
            "status": "Healthy",
            "version": "1.0",
            "database": "connected" if db.engine.connect() else "disconnected"
        })
    
    return app