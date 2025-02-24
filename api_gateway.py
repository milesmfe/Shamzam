from flask import Flask
from microservices.catalogue.route import catalogue_bp
from microservices.catalogue.db.database import create_database
from microservices.lookup.route import lookup_bp

app = Flask(__name__)

create_database()

app.register_blueprint(catalogue_bp, url_prefix='/catalogue')
app.register_blueprint(lookup_bp, url_prefix='/lookup')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
