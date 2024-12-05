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
    pass  

@routes.route('/update-password', methods=['PUT'])
def update_password():
    pass  


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