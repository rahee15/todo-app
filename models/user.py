from mongoengine import Document, StringField

class User(Document):
    """
    Represents a user document in the database.

    Attributes:
        username (StringField): The username of the user, required, unique, and limited to 80 characters.
        password (StringField): The hashed password of the user, required and limited to 200 characters.
    """
    username = StringField(required=True, unique=True, max_length=80)
    password = StringField(required=True, max_length=200)
