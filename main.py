from flask import Flask, request, jsonify
from services.extract import extract_blueprint

app = Flask(__name__)

# Register the blueprints/routes
app.register_blueprint(extract_blueprint, url_prefix='/extract')


@app.route('/')
def home():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)