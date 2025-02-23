from flask import Flask
from route import lookup_bp

app = Flask(__name__)
app.register_blueprint(lookup_bp, url_prefix='/lookup')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
