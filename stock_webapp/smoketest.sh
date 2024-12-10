#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://127.0.0.1:5000"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Account Routes
#
###############################################

# Function to create a new user account
create_account() {
  username=$1
  password=$2

  echo "Creating account for ($username)..."
  response=$(curl -s -X POST "$BASE_URL/create-account" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"password\":\"$password\"}")

  # Print the response to debug
  echo "Response: $response"

  if echo "$response" | grep -q '"message": "Account created successfully."'; then
    echo "Account created successfully."
  else
    echo "Failed to create account."
    exit 1
  fi
}

# Function to log in a user
login() {
  username=$1
  password=$2

  echo "Logging in user ($username)..."
  response=$(curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"password\":\"$password\"}")
  if echo "$response" | grep -q '"message": "Login successful."'; then
    echo "Login successful."
  else
    echo "Failed to log in."
    exit 1
  fi
}

# Function to update a user's password
update_password() {
  username=$1
  old_password=$2
  new_password=$3

  echo "Updating password for user ($username)..."
  response=$(curl -s -X PUT "$BASE_URL/update-password" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"old_password\":\"$old_password\", \"new_password\":\"$new_password\"}")
  if echo "$response" | grep -q '"message": "Password updated successfully."'; then
    echo "Password updated successfully."
  else
    echo "Failed to update password."
    exit 1
  fi
}

# Function to set a user's balance
set_balance() {
  user_id=$1
  balance=$2

  echo "Setting balance for user ID ($user_id) to $balance..."
  response=$(curl -s -X PUT "$BASE_URL/update-balance" -H "Content-Type: application/json" \
    -d "{\"user_id\":$user_id, \"balance\":$balance}")

  if echo "$response" | grep -q '"message": "Balance updated successfully."'; then
    echo "Balance updated successfully."
  else
    echo "Failed to update balance."
    echo "Error response: $response"  # Print the full response for debugging
    exit 1
  fi
}


###############################################
#
# Stock Routes
#
###############################################

# Function to check the health of the API
check_health() {
  echo "Checking health status..."
  response=$(curl -s -X GET "$BASE_URL/health")
  if echo "$response" | grep -q '"status": "Alpha Vantage API is healthy"'; then
    echo "API is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to view the user's portfolio
view_portfolio() {
  user_id=$1

  echo "Viewing portfolio for user ID ($user_id)..."
  response=$(curl -s -X GET "$BASE_URL/portfolio/view?user_id=$user_id")
  if echo "$response" | grep -q '"portfolio"'; then
    echo "Portfolio retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Portfolio JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to view portfolio."
    exit 1
  fi
}

# Function to buy stock
buy_stock() {
  user_id=$1
  symbol=$2
  quantity=$3

  echo "Buying stock ($symbol) for user ID ($user_id)..."
  response=$(curl -s -X POST "$BASE_URL/portfolio/buy" -H "Content-Type: application/json" \
    -d "{\"user_id\":$user_id, \"symbol\":\"$symbol\", \"quantity\":$quantity}")

  # Print the full response for debugging
  echo "Response: $response"

  # Check if the response contains 'message' indicating success
  if echo "$response" | grep -q '"message": "Stock purchased successfully."'; then
    echo "Stock bought successfully."
  else
    echo "Failed to buy stock."
    echo "Error: $response"  # Print the error response
    exit 1
  fi
}

# Function to sell stock
sell_stock() {
  user_id=$1
  symbol=$2
  quantity=$3

  echo "Selling stock ($symbol) for user ID ($user_id)..."
  response=$(curl -s -X POST "$BASE_URL/portfolio/sell" -H "Content-Type: application/json" \
    -d "{\"user_id\":$user_id, \"symbol\":\"$symbol\", \"quantity\":$quantity}")
  if echo "$response" | grep -q '"message": "Transaction successful"'; then
    echo "Stock sold successfully."
  else
    echo "Failed to sell stock."
    exit 1
  fi
}

# Function to get stock info
get_stock_info() {
  symbol=$1

  echo "Getting info for stock ($symbol)..."
  response=$(curl -s -X GET "$BASE_URL/stock/$symbol/info")
  if echo "$response" | grep -q "\"symbol\": \"$symbol\""; then
    echo "Stock info retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Stock info JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve stock info."
    exit 1
  fi
}

# Function to calculate portfolio value
calculate_portfolio_value() {
  user_id=$1

  echo "Calculating portfolio value for user ID ($user_id)..."
  response=$(curl -s -X GET "$BASE_URL/portfolio/value?user_id=$user_id")
  if echo "$response" | grep -q '"portfolio_value"'; then
    echo "Portfolio value calculated successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Portfolio value JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to calculate portfolio value."
    exit 1
  fi
}

###############################################
#
# Run the Tests
#
###############################################

echo "Starting StockWebApp smoke tests..."

# Health check
check_health

# Account Routes
# Generate a unique username to avoid conflicts
USERNAME="testuser$(date +%s)"
create_account "$USERNAME" "password123"
login "$USERNAME" "password123"
update_password "$USERNAME" "password123" "newpassword123"

# Stock Routes
# Test with a user_id that exists in your database
USER_ID=1

# Set the user's balance to ensure they can afford the stock purchase
set_balance $USER_ID 10000.0  # Set initial balance of 10000.0

# Fetch stock info first
get_stock_info "AAPL"  # View stock info before proceeding with buy

# Ensure user has some stock holdings before viewing portfolio
buy_stock $USER_ID "AAPL" 10  # Buying 10 AAPL stocks

# Test portfolio and other stock routes
view_portfolio $USER_ID
sell_stock $USER_ID "AAPL" 10
calculate_portfolio_value $USER_ID

echo "All tests completed successfully!"
