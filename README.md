# Stock Web Application

This is a Flask-based web application that interacts with the Alpha Vantage API to manage stock portfolios. The application allows users to create accounts, log in, buy and sell stocks, view portfolio summaries, and calculate the total value of their portfolios.

## Route Documentation

### Route: `/create-account`
- **Request Type**: POST
- **Purpose**: Creates a new user account with a username and password.
- **Request Body**:
  - `username` (String): User's chosen username.
  - `password` (String): User's chosen password.
- **Response Format**: JSON
  - **Success Response Example**:
    - Code: 200
    - Content: 
      ```json
      { "message": "Account created successfully" }
      ```
- **Example Request**:
  ```json
  {
    "username": "newuser123",
    "password": "securepassword"
  }
  ```
- **Example Response**:
  ```json
  {
    "message": "Account created successfully",
    "status": "200"
  }
  ```

### Route: `/login`
- **Request Type**: POST
- **Purpose**: Logs the user in by verifying the provided username and password.
- **Request Body**:
  - `username` (String): User's chosen username.
  - `password` (String): User's chosen password.
- **Response Format**: JSON
  - **Success Response Example**:
    - Code: 200
    - Content: 
      ```json
      { "message": "Login successful" }
      ```
- **Example Request**:
  ```json
  {
    "username": "existing_user",
    "password": "password123"
  }
  ```
- **Example Response**:
  ```json
  {
    "message": "Login successful",
    "status": "200"
  }
  ```

### Route: `/update-password`
- **Request Type**: PUT
- **Purpose**: Allows users to update their password.
- **Request Body**:
  - `username` (String): User's username.
  - `old_password` (String): The current password.
  - `new_password` (String): The new password.
- **Response Format**: JSON
  - **Success Response Example**:
    - Code: 200
    - Content: 
      ```json
      { "message": "Password updated successfully" }
      ```
- **Example Request**:
  ```json
  {
    "username": "existing_user",
    "old_password": "oldpassword123",
    "new_password": "newpassword123"
  }
  ```
- **Example Response**:
  ```json
  {
    "message": "Password updated successfully",
    "status": "200"
  }
  ```

### Route: `/health`
- **Request Type**: GET
- **Purpose**: Checks the health of the Alpha Vantage API.
- **Response Format**: JSON
  - **Success Response Example**:
    - Code: 200
    - Content: 
      ```json
      { "status": "Alpha Vantage API is healthy" }
      ```
- **Example Request**:
  (No request body)
- **Example Response**:
  ```json
  {
    "status": "Alpha Vantage API is healthy"
  }
  ```

### Route: `/portfolio/view`
- **Request Type**: GET
- **Purpose**: Views the current portfolio of a user.
- **Request Body**:
  - `user_id` (int): The ID of the user whose portfolio is being viewed.
- **Response Format**: JSON
  - **Success Response Example**:
    - Code: 200
    - Content:
      ```json
      {
        "AAPL": {
          "quantity": 10,
          "current_price": 150.0,
          "total_value": 1500.0
        },
        "GOOG": {
          "quantity": 5,
          "current_price": 2800.0,
          "total_value": 14000.0
        },
        "total_portfolio_value": 15500.0
      }
      ```
- **Example Request**:
  ```json
  {
    "user_id": 1
  }
  ```
- **Example Response**:
  ```json
  {
    "AAPL": {
      "quantity": 10,
      "current_price": 150.0,
      "total_value": 1500.0
    },
    "GOOG": {
      "quantity": 5,
      "current_price": 2800.0,
      "total_value": 14000.0
    },
    "total_portfolio_value": 15500.0
  }
  ```

### Route: `/portfolio/buy`
- **Request Type**: POST
- **Purpose**: Allows a user to buy a stock.
- **Request Body**:
  - `user_id` (int): The ID of the user making the purchase.
  - `symbol` (String): The stock symbol to buy (e.g., 'AAPL').
  - `quantity` (int): The number of shares to buy.
- **Response Format**: JSON
  - **Success Response Example**:
    - Code: 200
    - Content:
      ```json
      {
        "message": "Stock purchased successfully",
        "symbol": "AAPL",
        "quantity": 5,
        "price_per_share": 150.0,
        "total_cost": 750.0
      }
      ```
- **Example Request**:
  ```json
  {
    "user_id": 1,
    "symbol": "AAPL",
    "quantity": 5
  }
  ```
- **Example Response**:
  ```json
  {
    "message": "Stock purchased successfully",
    "symbol": "AAPL",
    "quantity": 5,
    "price_per_share": 150.0,
    "total_cost": 750.0
  }
  ```

### Route: `/portfolio/sell`
- **Request Type**: POST
- **Purpose**: Allows a user to sell a stock.
- **Request Body**:
  - `user_id` (int): The ID of the user making the sale.
  - `symbol` (String): The stock symbol to sell (e.g., 'AAPL').
  - `quantity` (int): The number of shares to sell.
- **Response Format**: JSON
  - **Success Response Example**:
    - Code: 200
    - Content:
      ```json
      {
        "message": "Stock sold successfully",
        "symbol": "AAPL",
        "quantity": 3,
        "price_per_share": 150.0,
        "total_proceeds": 450.0
      }
      ```
- **Example Request**:
  ```json
  {
    "user_id": 1,
    "symbol": "AAPL",
    "quantity": 3
  }
  ```
- **Example Response**:
  ```json
  {
    "message": "Stock sold successfully",
    "symbol": "AAPL",
    "quantity": 3,
    "price_per_share": 150.0,
    "total_proceeds": 450.0
  }
  ```

### Route: `/stock/<symbol>/info`
- **Request Type**: GET
- **Purpose**: Retrieves stock information.
- **Request Body**:
  - `symbol` (String): The stock symbol to lookup (e.g., 'AAPL').
- **Response Format**: JSON
  - **Success Response Example**:
    - Code: 200
    - Content:
      ```json
      {
        "symbol": "AAPL",
        "company_name": "Apple Inc.",
        "current_price": 150.0,
        "previous_close": 148.0,
        "high": 151.0,
        "low": 147.5,
        "volume": 1200000
      }
      ```
- **Example Request**:
  ```json
  {
    "symbol": "AAPL"
  }
  ```
- **Example Response**:
  ```json
  {
    "symbol": "AAPL",
    "company_name": "Apple Inc.",
    "current_price": 150.0,
    "previous_close": 148.0,
    "high": 151.0,
    "low": 147.5,
    "volume": 1200000
  }
  ```

### Route: `/portfolio/value`
- **Request Type**: GET
- **Purpose**: Calculates the total value of the user's portfolio.
- **Request Body**:
  - `user_id` (int): The ID of the user whose portfolio value is being calculated.
- **Response Format**: JSON
  - **Success Response Example**:
    - Code: 200
    - Content:
      ```json
      {
        "AAPL": {
          "quantity": 10,
          "current_price": 150.0,
          "stock_value": 1500.0
        },
        "GOOG": {
          "quantity": 5,
          "current_price": 2800.0,
          "stock_value": 14000.0
        },
        "total_portfolio_value": 15500.0
      }
      ```
- **Example Request**:
  ```json
  {
    "user_id": 1
  }
  ```
- **Example Response**:
  ```json
  {
    "AAPL": {
      "quantity": 10,
      "current_price": 150.0,
      "stock_value": 1500.0
    },
    "GOOG": {
      "quantity": 5,
      "current_price": 2800.0,
      "stock_value": 14000.0
    },
    "total_portfolio_value": 15500.0
  }
  ```
