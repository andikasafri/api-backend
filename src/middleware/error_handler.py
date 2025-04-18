from flask import jsonify
import logging

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        logging.error(f"Bad Request: {str(e)}")
        return jsonify(error=str(e)), 400

    @app.errorhandler(401)
    def unauthorized(e):
        logging.error(f"Unauthorized: {str(e)}")
        return jsonify(error="Unauthorized"), 401

    @app.errorhandler(403)
    def forbidden(e):
        logging.error(f"Forbidden: {str(e)}")
        return jsonify(error="Forbidden"), 403

    @app.errorhandler(404)
    def not_found(e):
        logging.error(f"Not Found: {str(e)}")
        return jsonify(error="Resource not found"), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        logging.error(f"Method Not Allowed: {str(e)}")
        return jsonify(error="Method not allowed"), 405

    @app.errorhandler(429)
    def too_many_requests(e):
        logging.error(f"Too Many Requests: {str(e)}")
        return jsonify(error="Too many requests"), 429

    @app.errorhandler(500)
    def internal_server_error(e):
        logging.error(f"Internal Server Error: {str(e)}")
        return jsonify(error="Internal server error"), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error(f"Unhandled Exception: {str(e)}")
        return jsonify(error="An unexpected error occurred"), 500