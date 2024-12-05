from stock_webapp.extensions import db
from werkzeug.security import generate_password_hash

"""
This file defines the database models using SQLAlchemy
Each model corresponds to a table in the database and includes any related methods
"""

class User(db.Model):
    """
    Represents a user in the application

    Attributes:
        id (int): Primary key for the user
        username (str): The user's unique username
        password_hash (str): The hashed password of the user
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        """
        Initializes a new user instance

        Args:
            username (str): The username of the user
            password (str): The plaintext password to hash and store
        """
        self.username = username
        self.password_hash = generate_password_hash(password)