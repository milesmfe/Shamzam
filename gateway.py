# gateway.py
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.middleware.proxy_fix import ProxyFix
from services.catalogue.app import app as catalogue_app
from services.recognition.app import app as recognition_app

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
    from werkzeug.serving import run_simple
    run_simple('localhost', 8000, application, use_reloader=True, use_debugger=True)
