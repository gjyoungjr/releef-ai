from flask import Flask
from api import query_blueprint, analyze_blueprint, embed_blueprint

app = Flask(__name__)

# Register the blueprints/routes
app.register_blueprint(query_blueprint, url_prefix='/')
app.register_blueprint(analyze_blueprint, url_prefix='/')
app.register_blueprint(embed_blueprint, url_prefix='/')


@app.route('/')
def default():
    return 'OK', 200


@app.route('/health')
def health_check():
    print('healthy..')
    return 'OK', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    
    
    
    
    