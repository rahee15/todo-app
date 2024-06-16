Flask Application to manage a collection of ToDos with MongoDB and JWT Authentication.
## Features

- User registration and login with JWT-based authentication.
- CRUD operations for items, each linked to a user.
- MongoDB schema defined using MongoEngine.

## Project Structure

flask_app/
│
├── app.py
├── config.py
├── requirements.txt
├── models/
│   ├── item.py
│   └── user.py
├── routes/
│   ├── auth_routes.py
│   └── item_routes.py
├── services/
│   ├── auth_service.py
│   └── item_service.py
├── utils/
│   ├── decorators.py
│   └── validators.py
└── tests/
    ├── test_auth.py
    ├── test_item.py
    └── test_validation.py

## Getting Started

### Prerequisites

- Python 3.7+
- MongoDB
- Virtualenv (recommended)

### Installation

1. Clone the repository (git clone <git_repo_link>)
2. Create and activate a virtual environment
3. Install the required packages (pip install -r requirements.txt)


### Running the Application
1. Run the Flask application: python app.py
   The application will be available at http://localhost:5000.

