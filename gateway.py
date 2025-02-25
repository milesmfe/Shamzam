from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.middleware.proxy_fix import ProxyFix
from services.catalogue.app import app as catalogue_app
from services.recognition.app import app as recognition_app
from threading import Thread
from werkzeug.serving import run_simple

def run_service(app, host, port):
    run_simple(host, port, app, use_reloader=False, use_debugger=True)

def create_gateway():
    """Combine multiple Flask apps under path-based routing"""
    service_mapping = {
        '/catalogue': catalogue_app,
        '/recognition': recognition_app
    }

    # Add fallback handler for root requests
    def fallback_app(environ, start_response):
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'404 - Service not found']

    application = DispatcherMiddleware(fallback_app, service_mapping)
    
    return ProxyFix(
        application,
        x_for=1,
        x_proto=1,
        x_host=1
    )

application = create_gateway()

if __name__ == '__main__':
    # Run services on separate threads
    Thread(target=run_service, args=(catalogue_app, 'localhost', 5001)).start()
    Thread(target=run_service, args=(recognition_app, 'localhost', 5002)).start()
    run_simple('localhost', 8000, application, use_reloader=True, use_debugger=True)
