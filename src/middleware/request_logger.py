from flask import request, current_app
from functools import wraps
import time
import logging
import json

def request_logger(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        start_time = time.time()
        request_id = request.headers.get('X-Request-ID', 'N/A')
        
        # Log request
        log_data = {
            'request_id': request_id,
            'method': request.method,
            'path': request.path,
            'remote_addr': request.remote_addr,
            'headers': dict(request.headers)
        }
        
        if request.is_json:
            log_data['body'] = request.get_json()
        
        current_app.logger.info(f"Request: {json.dumps(log_data)}")
        
        try:
            response = f(*args, **kwargs)
            duration = time.time() - start_time
            
            # Log response
            response_data = {
                'request_id': request_id,
                'status_code': response.status_code,
                'duration': f"{duration:.2f}s"
            }
            current_app.logger.info(f"Response: {json.dumps(response_data)}")
            
            return response
        except Exception as e:
            duration = time.time() - start_time
            current_app.logger.error(f"Error processing request {request_id}: {str(e)}, duration: {duration:.2f}s")
            raise
            
    return decorated