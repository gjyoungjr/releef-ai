from flask import Flask
from services.ingest import ingest_blueprint

app = Flask(__name__)

# Register the blueprints/routes
app.register_blueprint(ingest_blueprint, url_prefix='/')


@app.route('/')
def home():
    return 'Hello, World!', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)