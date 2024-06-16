import re

#Validates whether the required field "name" is present
class ItemValidator:
    def validate(self, data):
        if not data.get('name'):
            return 'Name is required'
        return None

class AuthValidator:
    #Validates that Username and Password are present
    def validate_registration(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username:
            return 'Username is required'
        if len(username) < 3 or len(username) > 20:
            return 'Username must be between 3 and 20 characters'
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return 'Username can only contain letters, numbers, and underscores'

        if not password:
            return 'Password is required'
        if len(password) < 8:
            return 'Password must be at least 8 characters long'
        if not re.search("[a-z]", password):
            return 'Password must contain at least one lowercase letter'
        if not re.search("[A-Z]", password):
            return 'Password must contain at least one uppercase letter'
        if not re.search("[0-9]", password):
            return 'Password must contain at least one number'
        if not re.search("[@#$%^&+=!]", password):
            return 'Password must contain at least one special character (@#$%^&+=!)'

        # Check for potential injection characters in username and password
        if re.search(r'[\'"\\;]', username):
            return 'Username contains invalid characters'
        if re.search(r'[\'"\\;]', password):
            return 'Password contains invalid characters'
        return None

    #Validates that Username and Password are present
    def validate_login(self, data):
        username = data.get('username')
        password = data.get('password')
        if not data.get('username'):
            return 'Username is required'
        if not data.get('password'):
            return 'Password is required'
        # Check for potential injection characters in username and password
        if re.search(r'[\'"\\;]', username):
            return 'Username contains invalid characters'
        if re.search(r'[\'"\\;]', password):
            return 'Password contains invalid characters'
        return None
