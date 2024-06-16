from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datetime import datetime
from .user import User

class Item(Document):
    # Define fields for the Item document
    name = StringField(required=True, max_length=80)
    description = StringField(max_length=120)
    created_at = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(User, required=True)  # Reference to the User who created the item, required

    # Convert the Item object to a dictionary representation
    def to_dict(self):
        return {
            'id': str(self.id),  # Convert ObjectId to string for JSON compatibility
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'user_id': str(self.user.id)  # User ID who created the item, converted to string
        }
