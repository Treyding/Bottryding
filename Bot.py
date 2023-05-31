import os
import time
import json
from binance.client import Client
from database import Database

# Load config file
with open("config.json") as f:
    config = json.load(f)

# Initialize Binance client and database
client = Client(config["api_key"], config["api_secret"])
db = Database()

def get_current_price():
    """Get current price of the symbol"""
    ticker = client.get_symbol_ticker(symbol=config["symbol"])
    return float(ticker["price"])

def place_order(side, price):
    """Place an order (buy or sell) at the given price"""
    quantity = config["order_size"] / price
    if side == "BUY":
        order = client.order_limit_buy(
            symbol=config["symbol"],
            quantity=quantity,
            price=price
        )
    elif side == "SELL":
        order = client.order_limit_sell(
            symbol=config["symbol"],
            quantity=quantity,
            price=price
        )
    else:
        raise ValueError(f"Invalid order side: {side}")

    return order

def main():
    while True:
        try:
            price = get_current_price()
            print(f"Current {config['symbol']} price: {price}")

            if price <= get_current_price() * config["buy_threshold"]:
                print("Placing buy order...")
                place_order("BUY", price)
                db.add_transaction("BUY", config["symbol"], config["order_size"], price)
                print("Buy order placed.")

            if price >= get_current_price() * config["sell_threshold"]:
                print("Placing sell order...")
                place_order("SELL", price)
                db.add_transaction("SELL", config["symbol"], config["order_size"], price)
                print("Sell order placed.")

            time.sleep(config["trade_frequency_seconds"])
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(config["trade_frequency_seconds"])

if __name__ == "__main__":
    main()
