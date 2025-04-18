from flask import Blueprint
from ...middleware import limiter, request_logger

# Create the blueprint
api_v1 = Blueprint("api_v1", __name__)

# Apply rate limiting to all routes
limiter.limit("1000/day;100/hour")(api_v1)

# Apply request logger as before_request middleware on the blueprint
api_v1.before_request(request_logger)

# Import routes to register them
from . import user, product, transaction
