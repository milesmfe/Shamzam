from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask

from services.catalogue.app import app as catalogue_app
from services.recognition.app import app as recognition_app

gateway = Flask(__name__)

# Configure path routing
applications = {
    '/catalogue': catalogue_app,  # Points to catalogue Flask app
    '/recognition': recognition_app  # Points to recognition Flask app
}

# Health check endpoint
@gateway.route('/health')
def health():
    return 'Gateway operational', 200

# Create middleware dispatcher
application = DispatcherMiddleware(gateway, applications)

if __name__ == '__main__':
    # Production-ready server with concurrency
    run_simple(
        hostname='localhost',
        port=8000,
        application=application,
        use_debugger=False,
        use_reloader=True,
        threaded=True,
    )