from flask import Flask, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields, Api
from datetime import datetime
from services.item_service import ItemService
from utils.decorators import ItemOwnerChecker
from utils.validators import ItemValidator

#Initialize Flask app
app = Flask(__name__)

# Define authorizations for Swagger UI
authorizations = {
    'BearerAuth': {
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header',
        'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
    }
}

# Initialize Flask-RESTx API instance
api_instance = Api(app, version='1.0', title='Item API', description='A simple Item API',
                   authorizations=authorizations, security='BearerAuth')

# Initialize ItemService, ItemValidator, and ItemOwnerChecker instances
item_service = ItemService()
item_validator = ItemValidator()
item_owner_checker = ItemOwnerChecker()

# Create a Namespace for item-related operations
item_ns = Namespace('item', description='Item Related Operations', security='BearerAuth')

# Define the item model for Swagger documentation
item_model = item_ns.model('Item', {
    'name': fields.String(required=True, description='The item name'),
    'description': fields.String(required=True, description='The item description'),
    'created_at': fields.DateTime(description='The date the item was created')
})

class ItemController:
    @staticmethod
    @item_ns.route('/')
    class ItemList(Resource):
        @item_ns.expect(item_model)  # Specify the expected input model for Swagger documentation
        @item_ns.doc(security='BearerAuth')  # Document the security requirement for Swagger
        @jwt_required()  # Ensure JWT token is required for access
        def post(self):
            current_user = get_jwt_identity()  # Get current user from JWT token
            data = request.get_json()
            validation_error = item_validator.validate(data)
            if validation_error:
                return {"error": validation_error}, 400

            result = item_service.create_item(data, current_user)

            if isinstance(result.get('created_at'), datetime):
                result['created_at'] = result['created_at'].isoformat()  # Convert created_at to ISO format string
            return result, 201

        @item_ns.doc(security='BearerAuth')  # Document the security requirement for Swagger
        @jwt_required()  # Ensure JWT token is required for access
        def get(self):
            current_user = get_jwt_identity()  # Get current user from JWT token
            result = item_service.get_items(current_user)  # Retrieve items for the current user

            if not result:
                return {"error": "No items"}, 404  # Return error if no items found with status code 404

            for item in result:
                if isinstance(item.get('created_at'), datetime):
                    item['created_at'] = item['created_at'].isoformat()  # Convert created_at to ISO format string

            return result, 200

    @staticmethod
    @item_ns.route('/<string:id>')  # Define route parameter for item identifier
    @item_ns.param('id', 'The item identifier')  # Document the route parameter for Swagger
    class Item(Resource):
        @item_ns.doc(security='BearerAuth')
        @jwt_required()
        @item_owner_checker.check
        def get(self, id):
            result = item_service.get_item(id)
            if 'error' in result:
                return {"error": "Invalid"}, 404

            if isinstance(result.get('created_at'), datetime):
                result['created_at'] = result['created_at'].isoformat()
            return result, 200

        @item_ns.expect(item_model)  # Specify the expected input model for Swagger documentation
        @item_ns.doc(security='BearerAuth')
        @jwt_required()
        @item_owner_checker.check  # Use decorator to check if current user is the owner of the item
        def put(self, id):
            data = request.get_json()
            validation_error = item_validator.validate(data)
            if validation_error:
                return {"error": "validation_error"}, 400

            result = item_service.update_item(id, data)  # Update item using ItemService
            if 'error' in result:
                return {"error": result['error']}, 404

            if isinstance(result.get('created_at'), datetime):
                result['created_at'] = result['created_at'].isoformat()

            return result, 200

        @item_ns.doc(security='BearerAuth')
        @jwt_required()
        @item_owner_checker.check  # Use decorator to check if current user is the owner of the item
        def delete(self, id):
            result = item_service.delete_item(id)
            if 'error' in result:
                return {"error": result['error']}, 404

            return '', 204  # Return successful response with status code 204

# Add the Namespace to the API
api_instance.add_namespace(item_ns, path='/item')

if __name__ == '__main__':
    app.run(debug=True)
