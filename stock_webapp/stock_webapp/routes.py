from flask import Blueprint, request, jsonify
from stock_webapp.models import User
from stock_webapp.extensions import db
from stock_webapp.stock_api_model import AlphaVantageAPI

"""
This file contains all route definitions for the Flask app.
Routes define the endpoints and the logic to handle incoming HTTP requests.
"""

routes = Blueprint('routes', __name__)

# initialize API model
api = AlphaVantageAPI()

# ---------------------------
# Account Routes
# ---------------------------

@routes.route('/create-account', methods=['POST'])
def create_account():
    """
    Handles the creation of a new user account.

    Request:
        JSON object containing:
            username (str): The username
            password (str): The password

    Returns:
        Response:
            - 201: Account successfully created
            - 400: Missing or invalid data in the request
            - 409: Username already exists
            - 500: Server error during account creation
    """
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required.'}), 400

    username = data['username']
    password = data['password']

    # cehck if the username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists.'}), 409

    # create the user and save to the database
    try:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Account created successfully.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@routes.route('/login', methods=['POST'])
def login():
    """
    Handles user login by verifying username and password.

    Request:
        JSON object containing:
            username (str): The username
            password (str): The password

    Returns:
        Response:
            - 200: Successful login
            - 400: Missing or invalid data in the request
            - 401: Incorrect username or password
            - 500: Server error during login
    """
    data = request.get_json()

    # Check username and password in request
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required.'}), 400

    username = data['username']
    password = data['password']

    # Check if the user exists in the db
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'Incorrect username or password.'}), 401

    # Hash password with the stored salt and compare with stored hash
    if user.password_hash != user.hash_password(password, user.salt):
        return jsonify({'error': 'Incorrect username or password.'}), 401

    # Successful 
    return jsonify({'message': 'Login successful.'}), 200  


@routes.route('/update-password', methods=['PUT'])
def update_password():
    """
    Handles the update of an existing user's password.

    Request:
        JSON object containing:
            username (str): The username of the user
            old_password (str): The current password
            new_password (str): The new password

    Returns:
        Response:
            - 200: Password successfully updated
            - 400: Missing or invalid data in the request
            - 401: Unauthorized (incorrect old password)
            - 404: User not found
            - 500: Server error during password update
    """
    data = request.get_json()

    # Ensure all required fields are in the request
    if not data or 'username' not in data or 'old_password' not in data or 'new_password' not in data:
        return jsonify({'error': 'Username, old password, and new password are required.'}), 400

    username = data['username']
    old_password = data['old_password']
    new_password = data['new_password']

    # Check if the user exists in the database
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    # Hash the old password with the user's salt and compare
    if user.password_hash != user.hash_password(old_password, user.salt):
        return jsonify({'error': 'Incorrect old password.'}), 401

    # Generate a new salt and hash the new password
    try:
        new_salt = user.generate_salt()
        new_password_hash = user.hash_password(new_password, new_salt)

        # Update the user's password and salt
        user.salt = new_salt
        user.password_hash = new_password_hash
        db.session.commit()

        return jsonify({'message': 'Password updated successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ---------------------------
# Stock Routes (API Model)
# ---------------------------

@routes.route('/health', methods=['GET'])
def health_check():
    pass

# Stock Price Lookup Route
@routes.route('/stock/<symbol>/price', methods=['GET'])
def get_stock_price(symbol):
    pass


# Stock Information Lookup Route
@routes.route('/stock/<symbol>/info', methods=['GET'])
def get_stock_info(symbol):
    pass

# Buy Stock Route
@routes.route('/buy', methods=['POST'])
def buy_stock():
    pass


# Portfolio Value Calculation Route
@routes.route('/portfolio/value', methods=['GET'])
def get_portfolio_value():
    pass


if __name__ == "__main__":
    routes.run(debug=True)