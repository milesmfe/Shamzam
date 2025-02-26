import os
from dotenv import load_dotenv
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask, request
from flask_limiter import Limiter

from services.catalogue.app import app as catalogue_app
from services.recognition.app import app as recognition_app

gateway = Flask(__name__)

# Configure path routing
applications = {
    '/catalogue': catalogue_app,  # Points to catalogue Flask app
    '/recognition': recognition_app  # Points to recognition Flask app
}

limiter = Limiter(
    app=gateway,
    key_func=lambda: request.headers.get('X-Real-IP', request.remote_addr),
    default_limits=["200 per day", "50 per hour"]
)

@gateway.before_request
def validate_external_requests():
    if request.path.startswith('/catalogue'):
        # Allow internal service-to-service communication
        if request.headers.get('X-Internal-Request') == 'true':
            return
        # Enforce rate limits for external API consumers
        limiter.check()

# Health check endpoint
@gateway.route('/health')
def health():
    return 'Gateway operational', 200

# Create middleware dispatcher
application = DispatcherMiddleware(gateway, applications)

if __name__ == '__main__':
    # Production-ready server with concurrency
    
    load_dotenv()
    GATEWAY_HOST = os.getenv('GATEWAY_HOST')
    GATEWAY_PORT = int(os.getenv('GATEWAY_PORT'))
    
    run_simple(
        hostname=GATEWAY_HOST,
        port=GATEWAY_PORT,
        application=application,
        use_debugger=False,
        use_reloader=True,
        threaded=True,
    )