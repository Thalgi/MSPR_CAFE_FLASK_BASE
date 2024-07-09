from flask import Flask
from flask_restful import Api
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from blueprints.user_blueprint import user_blueprint
from api.basics import HelloWorld, Echo, CheckAPI
from constant import SECRET_KEY, DEBUG, HOST, PORT, SSL_CERT_PATH, SSL_KEY_PATH

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = SECRET_KEY

# Configurez le limiteur
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Enregistrez le blueprint utilisateur
app.register_blueprint(user_blueprint, url_prefix='/user')

####### Test Appel API Basique

api.add_resource(HelloWorld, '/')
api.add_resource(CheckAPI, '/check')
api.add_resource(Echo, '/echo')

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT, ssl_context=(SSL_CERT_PATH, SSL_KEY_PATH))