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

    def generate_salt(self):
        """
        Generates a random salt.

        Returns:
            str: A random salt as a hex string
        """
        return os.urandom(32).hex()

    def hash_password(self, password, salt):
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
    
    def get_holdings(self):
        """
        Method to retrieve all the stock holdings associated with the user.
        Assuming there is a `Holding` model that stores user stock holdings.

        Returns:
            list: List of holdings (each holding as a dictionary with `symbol` and `quantity`)
        """
        holdings = Holding.query.filter_by(user_id=self.id).all()
        return [{"symbol": holding.symbol, "quantity": holding.quantity} for holding in holdings]
    

class Holding(db.Model):
    """
    Represents a stock holding for a user

    Attributes:
        id (int): Primary key for the holding
        user_id (int): Foreign key for the associated user
        symbol (str): Stock symbol (e.g., "AAPL")
        quantity (int): Number of shares held by the user
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', backref=db.backref('holdings', lazy=True))
