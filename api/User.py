import secrets
import uuid
import bcrypt
from flask_restful import Resource, reqparse
from mail.mail import GmailQRCodeSender
from constant import TOKEN_LENGTH, CONFIRM_USER_URL


service = GmailQRCodeSender()
service.init_mail_sender()
users = {}

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.uuid = str(uuid.uuid4())
        self.email = email
        self.password = self.hash_password(password)
        self.access_token = secrets.token_hex(32)
        self.validate = False

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def to_dict(self, include_sensitive=False):
        user_dict = {
            'username': self.username,
            'email': self.email,
        }
        if include_sensitive:
            user_dict.update({
                'uuid': self.uuid,
                'access_token': self.access_token
            })
        return user_dict

class UserResource(Resource):
    @staticmethod
    def get_user_by_id(user_id):
        if user_id not in users:
            return None
        return users[user_id]

    @staticmethod
    def get_user_by_email(email):
        for user in users.values():
            if user.email == email:
                return user
        return None

class CreateUser(UserResource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required.')
        parser.add_argument('email', type=str, required=True, help='Email is required.')
        parser.add_argument('password', type=str, required=True, help='Password is required.')
        args = parser.parse_args()

        new_user = User(args['username'], args['email'], args['password'])
        users[new_user.uuid] = new_user

        return {'message': 'User created successfully', 'user': new_user.to_dict(include_sensitive=True)}, 201

class GetUser(UserResource):
    def get(self, user_id):
        user = self.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'user': user.to_dict()}

class UpdateUser(UserResource):
    def put(self, user_id):
        user = self.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()

        if args['username']:
            user.username = args['username']
        if args['email']:
            user.email = args['email']

        return {'message': 'User updated successfully', 'user': user.to_dict()}, 200

class DeleteUser(UserResource):
    def delete(self, user_id):
        if user_id not in users:
            return {'error': 'User not found'}, 404
        del users[user_id]
        return {'message': 'User deleted successfully'}

class GetUserToken(UserResource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email is required.')
        parser.add_argument('password', type=str, required=True, help='Password is required.')
        args = parser.parse_args()

        user = self.get_user_by_email(args['email'])
        if not user or not user.check_password(args['password']):
            return {'error': 'Invalid email or password'}, 401

        return {'access_token': user.access_token}, 200

class GetUserUuid(UserResource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email is required.')
        parser.add_argument('password', type=str, required=True, help='Password is required.')
        args = parser.parse_args()

        user = self.get_user_by_email(args['email'])
        if not user or not user.check_password(args['password']):
            return {'error': 'Invalid email or password'}, 401
        if not user.validate:
            return {'error': 'The User is not validated'}, 401

        return {'user_uuid': user.uuid}, 200

class ValidateUser(UserResource):
    def get(self, user_id):
        user = self.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        qr_data = f"{CONFIRM_USER_URL}{user.uuid}"
        service.send_email_with_qrcode(user.email, qr_data)

        return {'message': 'QR code email sent successfully'}, 200

class CheckMailExist(UserResource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email input is required.')
        args = parser.parse_args()

        user = self.get_user_by_email(args['email'])
        if user:
            return {'message': 'The email exists.'}
        return {'message': "The email doesn't exist."}