from flask import Blueprint
from flask_restful import Api
from api.User import CreateUser, UpdateUser, DeleteUser, GetUserToken, GetUser, ValidateUser, GetUserUuid, CheckMailExist

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint)

api.add_resource(CreateUser, '/create')
api.add_resource(UpdateUser, '/update/<string:user_id>')
api.add_resource(DeleteUser, '/delete/<string:user_id>')
api.add_resource(GetUser, '/get/<string:user_id>')
api.add_resource(GetUserToken, '/get_token')
api.add_resource(GetUserUuid, '/get_uuid')
api.add_resource(ValidateUser, '/validate/<string:user_id>')
api.add_resource(CheckMailExist, '/check_mail_exist')