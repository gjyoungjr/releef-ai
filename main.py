from flask import Flask, request, jsonify
from services.extract import extract_blueprint

app = Flask(__name__)

# Register the blueprints/routes
app.register_blueprint(extract_blueprint, url_prefix='/extract')


@app.route('/')
def home():
    return 'Hello, World!', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)