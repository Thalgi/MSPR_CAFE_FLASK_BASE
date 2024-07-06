import secrets
import uuid

from flask_restful import Resource, reqparse

from mail.mail import init_mail_sender, send_email_with_qrcode


service = init_mail_sender()

users = {}

import bcrypt


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
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def to_dict_full(self):
        return {
            'username': self.username,
            'uuid': self.uuid,
            'email': self.email,
            'access_token': self.access_token
        }

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
        }

    def to_uuid(self):
        return {
            'username': self.username,
            'uuid': self.uuid,
        }


class CreateUser(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required and must be a string.')
        parser.add_argument('email', type=str, required=True, help='Email is required and must be a string.')
        parser.add_argument('password', type=str, required=True, help='Password is required and must be a string.')
        args = parser.parse_args()

        new_user = User(args['username'], args['email'], args['password'])
        users[new_user.uuid] = new_user

        return {'message': 'User created successfully', 'user': new_user.to_uuid()}, 201


class GetUser(Resource):
    def get(self, user_id):
        if user_id not in users:
            return {'error': 'User not found'}, 404

        user = users[user_id]
        return {'user': user.to_dict()}


class UpdateUser(Resource):
    def put(self, user_id):
        if user_id not in users:
            return {'error': 'User not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username must be a string.')
        parser.add_argument('email', type=str, help='Email must be a string.')
        args = parser.parse_args()

        user = users[user_id]
        if args['username'] is not None:
            user.username = args['username']
        if args['email'] is not None:
            user.email = args['email']

        return {'message': 'User updated successfully', 'user': user.to_dict()},201


class DeleteUser(Resource):
    def delete(self, user_id):
        if user_id not in users:
            return {'error': 'User not found'}, 404

        del users[user_id]
        return {'message': 'User deleted successfully'}


class GetUserToken(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email is required and must be a string.')
        parser.add_argument('password', type=str, required=True, help='Password is required and must be a string.')
        args = parser.parse_args()

        user = None
        for u in users.values():
            if u.email == args['email'] and u.check_password(args['password']):
                user = u
                break

        if user is None:
            return {'error': 'Invalid email or password'}, 401

        return {'access_token': user.access_token}, 201


class GetUserUuid(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email is required and must be a string.')
        parser.add_argument('password', type=str, required=True, help='Password is required and must be a string.')
        args = parser.parse_args()

        user = None
        for u in users.values():
            if u.email == args['email']:
                user = u
                if u.check_password(args['password']):
                    if user.validate:
                        break
                    else:
                        return {'error': 'The User is not validated'}, 401

        if user is None:
            return {'error': 'Invalid email or password'}, 401

        return {'user_uuid': user.uuid}, 201


class ValidateUser(Resource):
    def get(self, user_id):
        if user_id not in users:
            return {'error': 'User not found'}, 404

        user = users[user_id]

        to_email = str(user.email)
        qr_data = "https://7695-2a01-cb19-d81-c600-dd62-6606-ee27-e4bb.ngrok-free.app/confirm_user" + str(user.uuid)
        send_email_with_qrcode(service, to_email, qr_data)

        return {'message': 'QR code email sent successfully'}, 201


class CheckMailExist(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email input is required and must be a string.')
        args = parser.parse_args()
        email = args['email']

        for u in users.values():
            if email == u.email:
                return {'message': 'The email exists.'}
            else:
                return {'message': "The email doesn't exist."}
