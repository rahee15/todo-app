import unittest
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager
from flask import Flask
from services.auth_service import AuthService
from models.user import User

# Initialize Flask app and JWT manager for testing
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random key
jwt = JWTManager(app)


class AuthServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.auth_service = AuthService()

    @patch('models.user.User.objects')
    def test_register_user_success(self, mock_user_objects):
        # Mock the return value for User.objects(username=username).first()
        mock_user_objects.return_value.first.return_value = None

        # Mock the save method of User
        with patch.object(User, 'save', return_value=None) as mock_save:
            data = {
                'username': 'testuser',
                'password': 'testpassword'
            }
            response = self.auth_service.register(data)
            self.assertEqual(response, {"message": "User registered successfully"})
            self.assertTrue(mock_save.called)

    @patch('models.user.User.objects')
    def test_register_user_already_exists(self, mock_user_objects):
        # Mock the return value for User.objects(username=username).first()
        mock_user_objects.return_value.first.return_value = User(username='existinguser', password='existingpassword')

        data = {
            'username': 'existinguser',
            'password': 'newpassword'
        }
        response = self.auth_service.register(data)
        self.assertEqual(response, {"error": "User already exists"})

    @patch('models.user.User.objects')
    def test_login_success(self, mock_user_objects):
        # Create a mock user with a hashed password
        username = 'loginuser'
        password = 'loginpassword'
        hashed_password = generate_password_hash(username + password)
        mock_user_objects.return_value.first.return_value = User(username=username, password=hashed_password)

        data = {
            'username': username,
            'password': password
        }
        with app.app_context():
            response = self.auth_service.login(data)
            self.assertIn('access_token', response)

    @patch('models.user.User.objects')
    def test_login_invalid_user(self, mock_user_objects):
        # Mock the return value for User.objects(username=username).first()
        mock_user_objects.return_value.first.return_value = None

        data = {
            'username': 'nonexistentuser',
            'password': 'somepassword'
        }
        response = self.auth_service.login(data)
        self.assertEqual(response, {"error": "Invalid username and password combination"})

    @patch('models.user.User.objects')
    def test_login_invalid_password(self, mock_user_objects):
        # Create a mock user with a correct hashed password
        username = 'userwithwrongpassword'
        correct_password = 'correctpassword'
        wrong_password = 'wrongpassword'
        hashed_password = generate_password_hash(username + correct_password)
        mock_user_objects.return_value.first.return_value = User(username=username, password=hashed_password)

        data = {
            'username': username,
            'password': wrong_password
        }
        response = self.auth_service.login(data)
        self.assertEqual(response, {"error": "Invalid username and password combination"})


