from flask import Blueprint

# Create the blueprint
api_v1 = Blueprint("api_v1", __name__)

# Import routes to register them
from . import user, product