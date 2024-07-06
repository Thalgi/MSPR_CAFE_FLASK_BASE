import os

from flask import Flask
from flask_restful import Api

from os import environ

from api.User import CreateUser, UpdateUser, DeleteUser, GetUserToken, GetUser, ValidateUser, GetUserUuid, \
    CheckMailExist
from api.basics import HelloWorld, Echo, CheckAPI


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')


####### Test Appel API Basique

api.add_resource(HelloWorld, '/')
api.add_resource(CheckAPI, '/check')
api.add_resource(Echo, '/echo')

####### API User qui récupère nos usagers et les stockes

api.add_resource(CreateUser, '/create_user')
api.add_resource(UpdateUser, '/update_user/<string:user_id>')
api.add_resource(DeleteUser, '/delete_user/<string:user_id>')
api.add_resource(GetUser, '/get_user/<string:user_id>')
api.add_resource(GetUserToken, '/get_user_token')
api.add_resource(GetUserUuid, '/get_user_uuid')
api.add_resource(ValidateUser, '/validate_user/<string:user_id>')
api.add_resource(CheckMailExist, '/check_mail_exist')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=("C:\\Users\\thalg\\Desktop\\python\\server.crt",
                                                                "C:\\Users\\thalg\\Desktop\\python\\server.key"))
