import requests
import json
import time

# Function to retrieve current stock price of Nvidia
def get_stock_price(symbol):
    url = "https://api.iextrading.com/1.0/stock/{}/quote".format(symbol)
    response = requests.get(url)
    data = json.loads(response.text)
    return float(data["latestPrice"])

# Function to calculate support level and resistance level
def calculate_support_and_resistance(symbol):
    # Retrieve historical stock data for the past 30 days
    url = "https://api.iextrading.com/1.0/stock/{}/chart/1m".format(symbol)
    response = requests.get(url)
    data = json.loads(response.text)

    # Extract closing prices
    closing_prices = [entry["close"] for entry in data]

    # Calculate support level and resistance level
    support_level = min(closing_prices)
    resistance_level = max(closing_prices)

    return support_level, resistance_level

# Function to buy stock within 15% of support level
def buy_within_support_level(symbol, quantity, support_level):
    # Calculate 15% below support level
    target_price = support_level * 0.85

    # Keep checking stock price every 5 seconds until it reaches target price
    while get_stock_price(symbol) > target_price:
        time.sleep(5)

    # Buy stock at current price
    buy_stock(symbol, quantity)

# Function to sell stock within 20% of resistance level
def sell_within_resistance_level(symbol, quantity, resistance_level):
    # Calculate 20% above resistance level
    target_price = resistance_level * 1.2

    # Keep checking stock price every 5 seconds until it reaches target price
    while get_stock_price(symbol) < target_price:
        time.sleep(5)

    # Sell stock at current price
    sell_stock(symbol, quantity)

# Function to buy stock
def buy_stock(symbol, quantity):
    # Place buy order through API or connect to broker API to execute trade
    print("Buying {} shares of {} at current price: {}".format(quantity, symbol, get_stock_price(symbol)))

# Function to sell stock
def sell_stock(symbol, quantity):
    # Place sell order through API or connect to broker API to execute trade
    print("Selling {} shares of {} at current price: {}".format(quantity, symbol, get_stock_price(symbol)))

# Main function
def main():
    # Set symbol and quantity
    symbol = "NVDA"
    quantity = 100

    # Retrieve support level and resistance level
    support_level, resistance_level = calculate_support_and_resistance(symbol)

    # Buy stock within 15% of support level
    buy_within_support_level(symbol, quantity, support_level)

    # Sell stock within 20% of resistance level
    sell_within_resistance_level(symbol, quantity, resistance_level)

# Execute main function
if __name__ == "__main__":
    main()