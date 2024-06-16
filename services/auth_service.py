from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models.user import User

class AuthService:
    def register(self, data):

        # Extract username and password from input data
        username = data.get('username')
        password = data.get('password')

        # Check if a user with the same username already exists
        if User.objects(username=username).first():
            return {"error": "User already exists"}

        hashValueToBeStoredInDB = username + "" + password

        # Generate hashed password for security using SHA256 Algo
        hashed_password = generate_password_hash(hashValueToBeStoredInDB)

        # Create new User object with hashed password and save to database
        user = User(username=username, password=hashed_password)
        user.save()

        return {"message": "User registered successfully"}  # Return success message upon successful registration

    def login(self, data):
        # Extract username and password from input data
        username = data.get('username')
        password = data.get('password')

        # Query database for user with provided username
        user = User.objects(username=username).first()

        hashValueToBeCheckedInDB = username + "" + password

        # Check if user does not exist or if password does not match
        if not user or not check_password_hash(user.password, hashValueToBeCheckedInDB):
            return {"error": "Invalid username and password combination"}

        # Generate access token for user authentication
        access_token = create_access_token(identity=str(user.id))

        return {"access_token": access_token}  # Return access token upon successful login
