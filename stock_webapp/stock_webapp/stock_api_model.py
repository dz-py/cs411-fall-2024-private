import requests
import os
from flask import jsonify, current_app
from dotenv import load_dotenv
from stock_webapp.models.user_model import User

# Load the variables from .env file
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
    
    
    def buy_stock():
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
            total_cost = current_price * quantity

            user.add_stock(symbol, quantity, total_cost)

            return {
                "message": "Stock purchased successfully.",
                "symbol": symbol,
                "quantity": quantity,
                "price_per_share": current_price,
                "total_cost": total_cost,
            }
        except Exception as e:
            return {"error": str(e)}
    
    
    def sell_stock():
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

            if not user.has_stock(symbol, quantity):
                return {"error": "Insufficient shares to sell."}

            total_proceeds = current_price * quantity

            user.remove_stock(symbol, quantity)

            return {
                "message": "Stock sold successfully.",
                "symbol": symbol,
                "quantity": quantity,
                "price_per_share": current_price,
                "total_proceeds": total_proceeds,
            }
        except Exception as e:
            return {"error": str(e)}
