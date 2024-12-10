import requests
import os
from flask import jsonify, current_app
from dotenv import load_dotenv
from stock_webapp.models import User
from stock_webapp.extensions import db  
from stock_webapp.models import Holding

# Load the variables from the .env file
load_dotenv()

class AlphaVantageAPI:
    """
    A class to interact with the Alpha Vantage API and retrieve stock data.
    """

    BASE_URL = "https://www.alphavantage.co/query"
    API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")  

    @staticmethod
    def health_check():
        """
        Simple health check to confirm the application is running.

        Returns:
            Response:
                - 200: If the application is healthy
        """
        current_app.logger.info('Health check requested')
        return jsonify({"status": "Application is running"}), 200

    def view_portfolio(self, user_holdings):
        """
        Retrieves and calculates the current portfolio data.

        Args:
            user_holdings (list[dict]): A list of user's stock holdings.
                Each holding is a dict with keys: "symbol" and "quantity".

        Returns:
            dict: Portfolio summary including current values of each stock and total portfolio value.
        """
        current_app.logger.info('Retrieving portfolio data for user holdings: %s', user_holdings)
        portfolio_summary = {}
        total_portfolio_value = 0.0

        for holding in user_holdings:
            symbol = holding.get("symbol")
            quantity = holding.get("quantity", 0)

            current_app.logger.info('Fetching data for stock symbol: %s with quantity: %d', symbol, quantity)

            try:
                response = requests.get(
                    self.BASE_URL,
                    params={
                        "function": "GLOBAL_QUOTE",
                        "symbol": symbol,
                        "apikey": self.API_KEY,  
                    },
                )

                if response.status_code == 200:
                    data = response.json()
                    try:
                        current_price = float(data["Global Quote"]["05. price"])
                        stock_value = current_price * quantity
                        total_portfolio_value += stock_value

                        portfolio_summary[symbol] = {
                            "quantity": quantity,
                            "current_price": current_price,
                            "total_value": stock_value,
                        }
                        current_app.logger.info('Stock data for %s: current_price = %.2f, stock_value = %.2f', symbol, current_price, stock_value)
                    except (KeyError, ValueError) as e:
                        portfolio_summary[symbol] = {"error": f"Invalid data from API: {str(e)}"}
                        current_app.logger.error('Error processing stock data for %s: %s', symbol, str(e))
                else:
                    portfolio_summary[symbol] = {"error": "API request failed"}
                    current_app.logger.error('API request failed for symbol %s, status_code: %d', symbol, response.status_code)

            except requests.exceptions.RequestException as e:
                portfolio_summary[symbol] = {"error": "Request failed"}
                current_app.logger.error('Request exception for symbol %s: %s', symbol, str(e))

        portfolio_summary["total_portfolio_value"] = total_portfolio_value
        current_app.logger.info('Portfolio summary: %s', portfolio_summary)
        return portfolio_summary
    
    
    def buy_stock(self, symbol, quantity, user):
        try:
            # Fetch the current stock price
            response = requests.get(
                self.BASE_URL,
                params={
                    "function": "GLOBAL_QUOTE",
                    "symbol": symbol,
                    "apikey": self.API_KEY,
                },
            )

            if response.status_code != 200:
                return {"error": "Failed to fetch stock data."}

            # Log the response to check its structure
            current_app.logger.info(f"API Response: {response.json()}")

            # Extract the price from the response
            data = response.json()
            
            # Safely get the 'Global Quote' key
            if 'Global Quote' not in data:
                return {"error": "Failed to find 'Global Quote' in the API response."}
            
            current_price = float(data["Global Quote"]["05. price"])

            # Check if the user has a valid balance
            if user.balance is None:
                user.balance = 0.0  # Set default balance if None

            # Calculate total cost of the stock purchase
            total_cost = current_price * quantity
            current_app.logger.info(f"Stock Price: {current_price}, Quantity: {quantity}, Total Cost: {total_cost}")

            # Check if the user can afford the stock purchase
            if user.balance < total_cost:
                current_app.logger.info(f"User balance: {user.balance}, Total cost: {total_cost}")
                return {"error": "Insufficient funds to buy the stock."}

            # Retrieve the user's existing stock holdings for this symbol
            holding = Holding.query.filter_by(user_id=user.id, symbol=symbol).first()

            if holding:
                # If stock already exists in the portfolio, update the quantity and total cost
                holding.quantity += quantity
                holding.total_cost += total_cost
            else:
                # If stock doesn't exist, create a new holding
                holding = Holding(
                    user_id=user.id,
                    symbol=symbol,
                    quantity=quantity,
                    price_per_share=current_price,
                    total_cost=total_cost,
                )
                db.session.add(holding)

            # Deduct the total cost from the user's balance
            user.balance -= total_cost

            # Commit the changes to the database
            db.session.commit()

            return {
                "message": "Stock purchased successfully.",
                "symbol": symbol,
                "quantity": quantity,
                "price_per_share": current_price,
                "total_cost": total_cost,
            }

        except Exception as e:
            current_app.logger.error(f"Error occurred while buying stock: {str(e)}")
            return {"error": str(e)}


    def sell_stock(self, symbol, quantity, user):
        try:
            response = requests.get(
                self.BASE_URL,
                params={
                    "function": "GLOBAL_QUOTE",
                    "symbol": symbol,
                    "apikey": self.API_KEY,
                },
            )

            if response.status_code != 200:
                return {"error": "Failed to fetch stock data."}

            data = response.json()
            current_price = float(data["Global Quote"]["05. price"])

            # Check if the user has enough stock to sell
            holding = Holding.query.filter_by(user_id=user.id, symbol=symbol).first()

            if not holding or holding.quantity < quantity:
                return {"error": "Insufficient shares to sell."}

            total_proceeds = current_price * quantity

            # Update the holding after selling
            holding.quantity -= quantity
            # If quantity reaches zero, delete the holding
            if holding.quantity == 0:
                db.session.delete(holding)

            # Add the proceeds from the sale to the user's balance
            user.balance += total_proceeds

            # Commit the changes to the database
            db.session.commit()

            return {
                "message": "Stock sold successfully.",
                "symbol": symbol,
                "quantity": quantity,
                "price_per_share": current_price,
                "total_proceeds": total_proceeds,
            }
        except Exception as e:
            return {"error": str(e)}

    def get_stock_info(self, symbol):
        current_app.logger.info(f"Fetching stock data for symbol: {symbol}")

        try:
            response = requests.get(
                self.BASE_URL,
                params={
                    "function": "GLOBAL_QUOTE",
                    "symbol": symbol,
                    "apikey": self.API_KEY,
                },
            )

            if response.status_code == 200:
                data = response.json()

                # Check if 'Global Quote' and '05. price' exist
                if "Global Quote" not in data or "05. price" not in data["Global Quote"]:
                    current_app.logger.error(f"'05. price' field is missing for symbol {symbol}.")
                    return {"error": "'05. price' field not found in the API response"}

                stock_data = {
                    "symbol": symbol,
                    "company_name": data["Global Quote"].get("01. symbol", "N/A"),
                    "current_price": float(data["Global Quote"]["05. price"]),
                    "previous_close": float(data["Global Quote"]["08. previous close"]),
                    "high": float(data["Global Quote"]["03. high"]),
                    "low": float(data["Global Quote"]["04. low"]),
                    "volume": int(data["Global Quote"]["06. volume"]),
                }
                current_app.logger.info(f"Stock data for {symbol}: {stock_data}")
                return stock_data
            else:
                current_app.logger.error(f"API request failed for {symbol}, status_code: {response.status_code}")
                return {"error": f"API request failed for {symbol}"}
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Request exception for symbol {symbol}: {e}")
            return {"error": f"Request failed for {symbol}: {str(e)}"}

    def calculate_portfolio_value(self, user_holdings):
        current_app.logger.info(f"Calculating portfolio value for holdings: {user_holdings}")
        portfolio_summary = {}
        total_value = 0.0

        for holding in user_holdings:
            symbol = holding.get("symbol")
            quantity = holding.get("quantity", 0)

            stock_info = self.get_stock_info(symbol)
            if "error" not in stock_info:
                current_price = stock_info["current_price"]
                stock_value = current_price * quantity
                total_value += stock_value

                portfolio_summary[symbol] = {
                    "quantity": quantity,
                    "current_price": current_price,
                    "stock_value": stock_value,
                }
            else:
                portfolio_summary[symbol] = {"error": stock_info["error"]}

        portfolio_summary["total_portfolio_value"] = total_value
        current_app.logger.info(f"Portfolio value: {total_value}")
        return portfolio_summary