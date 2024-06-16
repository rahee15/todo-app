from functools import wraps
from flask_jwt_extended import get_jwt_identity
from models.item import Item
from bson import ObjectId

class ItemOwnerChecker:
    def check(self, fn):
        @wraps(fn)  # Preserve original function metadata
        def wrapper(*args, **kwargs):
            item_id = kwargs.get('id')
            current_user = get_jwt_identity()  # Get current user's identity from JWT

            # Validate the provided ID
            if not ObjectId.is_valid(item_id):
                return {"error": "Invalid ID format"}, 400

            # Query the Item collection for an item with given id and owned by current_user
            item = Item.objects(id=item_id, user=current_user).first()

            # If item is not found or does not belong to current_user, return 404 error
            if item is None:
                return {'error': 'Item not found or unauthorized access'}, 404

            # Otherwise, execute the original function with its arguments and return its result
            return fn(*args, **kwargs)

        # Return the wrapped function with added authorization check
        return wrapper
