import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    MONGODB_SETTINGS = {
        'db': os.getenv('MONGO_DB_NAME'),
        'host': os.getenv('MONGO_URI')
    }
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() in ['true', '1', 't']
