from flask import Flask
from route import catalogue_bp

app = Flask(__name__)
app.register_blueprint(catalogue_bp, url_prefix='/catalogue')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
