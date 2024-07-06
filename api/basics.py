from flask_restful import Resource, reqparse


class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}


class CheckAPI(Resource):
    def get(self):
        return {'status': 'The API is alive'}


class Echo(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('text', type=str, required=True, help='Text input is required and must be a string.')
        args = parser.parse_args()
        return {'echo': args['text']}