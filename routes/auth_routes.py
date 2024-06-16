from flask import request
from services.auth_service import AuthService
from utils.validators import AuthValidator
from flask_restx import Api, Namespace, Resource, fields

# Instantiate AuthService and AuthValidator classes
auth_service = AuthService()
auth_validator = AuthValidator()

# Create a Flask-RESTx Namespace for authentication-related operations
api = Namespace('auth', description='Authentication related operations')

# Define the user model for Swagger documentation
user_model = api.model('User', {
    'username': fields.String(required=True, description='The user username'),
    'password': fields.String(required=True, description='The user password')
})

class AuthController:
    @staticmethod
    @api.route('/register')  # Endpoint route for user registration
    class Register(Resource):
        @api.expect(user_model)  # Expect input to match the user_model
        def post(self):
            #Fetching data from request
            data = request.get_json()
            # Validate registration data
            validation_error = auth_validator.validate_registration(data)
            if validation_error:
                return {"error": validation_error}, 400

            result = auth_service.register(data)  # Call AuthService to register user
            if 'error' in result:
                return {"error": result['error']}, 400

            return result, 201

    @staticmethod
    @api.route('/login')  # Endpoint route for user login
    class Login(Resource):
        @api.expect(user_model)  # Expect input to match the user_model
        def post(self):

            #Parsing Input Data
            data = request.get_json()

            #Validating Input
            validation_error = auth_validator.validate_login(data)
            if validation_error:
                return {"error": validation_error}, 400

            result = auth_service.login(data)  # Call AuthService to authenticate user
            if 'error' in result:
                return {"error": result['error']}, 401

            return result, 200
