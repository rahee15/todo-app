from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from config import Config
from flask_restx import Api
from routes.auth_routes import api as auth_api
from routes.item_routes import item_ns as item_api

#Initialize MongoDB database instance
db = MongoEngine()

# Define authorizations for Swagger UI
authorizations = {
    'BearerAuth': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
    }
}

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)  # Load configuration from Config class
        db.init_app(self.app)  # Initialize MongoDB with the Flask application

        #Initialize Flask-RestX API with Swagger settings
        self.api = Api(self.app,
                       version='1.0',
                       title='Item API',
                       description='A simple Item API',
                       authorizations=authorizations,
                       security='BearerAuth',
                       doc='/swagger/')
        self.jwt = JWTManager(self.app)  # Initialize JWT Manager for authentication
        self.register_routes()  # Register API routes
        self.print_routes()

    # Add namespaces (blueprints) to the API instance
    def register_routes(self):
        self.api.add_namespace(auth_api)
        self.api.add_namespace(item_api)

    # Print all accessible routes within the Flask application
    def print_routes(self):
        with self.app.app_context():
            for rule in self.app.url_map.iter_rules():
                print(f"Endpoint: {rule.endpoint}, URL: {rule}")
        print("Routes printed")

    def run(self):
        self.app.run(debug=self.app.config['DEBUG'])

if __name__ == '__main__':
    flask_app = FlaskApp()
    flask_app.run()
