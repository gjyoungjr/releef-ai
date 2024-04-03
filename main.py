from flask import Flask
from api.extract import extract_blueprint

app = Flask(__name__)

# Register the blueprints/routes
app.register_blueprint(extract_blueprint, url_prefix='/')


@app.route('/')
def home():
    return 'Go Perennial <33', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    
    
    
    
    