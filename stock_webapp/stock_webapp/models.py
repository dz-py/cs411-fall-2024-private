from stock_webapp.extensions import db
from werkzeug.security import generate_password_hash
import os
import hashlib

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
        salt (str): The unique salt for the user
        password_hash (str): The hashed password of the user
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    salt = db.Column(db.String(64), nullable=False)  # Salt stored as a hex string
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        """
        Initializes a new user instance

        Args:
            username (str): The username of the user
            password (str): The plaintext password to hash and store
        """
        self.username = username
        self.salt = self.generate_salt()
        self.password_hash = self.hash_password(password, self.salt)

    def generate_salt():
        """
        Generates a random salt.

        Returns:
            str: A random salt as a hex string
        """
        return os.urandom(32).hex()

    def hash_password(password, salt):
        """
        Hashes the password with the provided salt using SHA-256.

        Args:
            password (str): The plaintext password to hash
            salt (str): The salt to use in hashing

        Returns:
            str: The hashed password as a string
        """
        salted_password = f"{salt}{password}"
        return hashlib.sha256(salted_password.encode()).hexdigest()
