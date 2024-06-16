from datetime import datetime
from models.item import Item
from models.user import User

class ItemService:
    # Method to Create an item
    def create_item(self, data, user_id):

        # Retrieve the user object based on user_id
        user = User.objects(id=user_id).first()

        if not user:
            return {"error": "User not found"}  # Return error if user does not exist

        # Create a new Item object with data provided
        item = Item(
            name=data.get('name'),
            description=data.get('description'),
            user=user
        )

        item.save()  # Save the item to the database

        # Return item details as dictionary
        return item.to_dict()

    # Method to retrieve an item by item_id
    def get_item(self, item_id):
        item = Item.objects(id=item_id).first()

        if not item:
            return {"error": "Item not found"}  # Return error if item does not exist

        return item.to_dict()  # Return item details as dictionary

    # Method to retrieve list of items associated with the user_id
    def get_items(self, user_id):

        items = Item.objects(user=user_id)

        return [item.to_dict() for item in items]  # Return list of item details as dictionaries

    # Method to update the item object based on item_id
    def update_item(self, item_id, data):
        # Retrieve the item object based on item_id
        item = Item.objects(id=item_id).first()
        if not item:
            return {"error": "Item not found"}  # Return error if item does not exist

        # Update item fields with new data
        item.update(
            set__name=data.get('name'),
            set__description=data.get('description'),
            set__created_at=datetime.utcnow()  # Update the created_at timestamp
        )
        return {"message": "Item updated successfully"}  # Return success message

    # Method to delete item based on item_id
    def delete_item(self, item_id):
        # Retrieve the item object based on item_id
        item = Item.objects(id=item_id).first()
        if not item:
            return {"error": "Item not found"} # Return error if item does not exist

        item.delete()  # Delete the item from the database
        return {"message": "Item deleted successfully"} # Return success message
