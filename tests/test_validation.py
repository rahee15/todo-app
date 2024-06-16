import unittest
from utils.validators import AuthValidator

class AuthValidatorTestCase(unittest.TestCase):
    def setUp(self):
        self.validator = AuthValidator()

    def test_validate_registration_missing_username(self):
        data = {'password': 'testPassword1@'}
        result = self.validator.validate_registration(data)
        self.assertEqual(result, 'Username is required')

    def test_validate_registration_short_username(self):
        data = {'username': 'ab', 'password': 'testPassword1@'}
        result = self.validator.validate_registration(data)
        self.assertEqual(result, 'Username must be between 3 and 20 characters')

    def test_validate_registration_long_username(self):
        data = {'username': 'a' * 21, 'password': 'testPassword1@'}
        result = self.validator.validate_registration(data)
        self.assertEqual(result, 'Username must be between 3 and 20 characters')

    def test_validate_registration_invalid_characters_username(self):
        data = {'username': 'user;name', 'password': 'testPassword1@'}
        result = self.validator.validate_registration(data)
        self.assertEqual(result, 'Username can only contain letters, numbers, and underscores')

    def test_validate_registration_missing_password(self):
        data = {'username': 'username'}
        result = self.validator.validate_registration(data)
        self.assertEqual(result, 'Password is required')

    def test_validate_registration_short_password(self):
        data = {'username': 'username', 'password': 'pass1@'}
        result = self.validator.validate_registration(data)
        self.assertEqual(result, 'Password must be at least 8 characters long')

    def test_validate_registration_no_lowercase_password(self):
        data = {'username': 'username', 'password': 'PASSWORD1@'}
        result = self.validator.validate_registration(data)
        self.assertEqual(result, 'Password must contain at least one lowercase letter')

    def test_validate_registration_no_uppercase_password(self):
        data = {'username': 'username', 'password': 'password1@'}
        result = self.validator.validate_registration(data)
        self.assertEqual(result, 'Password must contain at least one uppercase letter')

    def test_validate_registration_no_number_password(self):
        data = {'username': 'username', 'password': 'Password@'}
        result = self.validator.validate_registration(data)
        self.assertEqual(result, 'Password must contain at least one number')

    def test_validate_registration_no_special_char_password(self):
        data = {'username': 'username', 'password': 'Password1'}
        result = self.validator.validate_registration(data)
        self.assertEqual(result, 'Password must contain at least one special character (@#$%^&+=!)')

    def test_validate_registration_invalid_characters_password(self):
        data = {'username': 'username', 'password': 'P@ass;word1"'}
        result = self.validator.validate_registration(data)
        self.assertEqual(result, 'Password contains invalid characters')

    def test_validate_login_missing_username(self):
        data = {'password': 'testPassword1@'}
        result = self.validator.validate_login(data)
        self.assertEqual(result, 'Username is required')

    def test_validate_login_missing_password(self):
        data = {'username': 'username'}
        result = self.validator.validate_login(data)
        self.assertEqual(result, 'Password is required')

    def test_validate_login_invalid_characters_username(self):
        data = {'username': 'user;name', 'password': 'testPassword1@'}
        result = self.validator.validate_login(data)
        self.assertEqual(result, 'Username contains invalid characters')

    def test_validate_login_invalid_characters_password(self):
        data = {'username': 'username', 'password': 'pass;word1'}
        result = self.validator.validate_login(data)
        self.assertEqual(result, 'Password contains invalid characters')

if __name__ == '__main__':
    unittest.main()
