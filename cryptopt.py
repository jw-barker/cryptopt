#! /usr/local/bin/python
import argparse
import json
import os
import pip._vendor.requests
import re

BANNER = r"""
 _______  ______    __   __  _______  _______  _______  _______  _______ 
|       ||    _ |  |  | |  ||       ||       ||       ||       ||       |
|       ||   | ||  |  |_|  ||    _  ||_     _||   _   ||    _  ||_     _|
|       ||   |_||_ |       ||   |_| |  |   |  |  | |  ||   |_| |  |   |  
|      _||    __  ||_     _||    ___|  |   |  |  |_|  ||    ___|  |   |  
|     |_ |   |  | |  |   |  |   |      |   |  |       ||   |      |   |  
|_______||___|  |_|  |___|  |___|      |___|  |_______||___|      |___| 
        a cryptocurrency portfolio tracking tool
"""

# Constants
DATA_FILE = "data.json"  # File to store portfolio data
BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"


def get_price(symbol: str, fiat: str) -> float:
    """Get the latest price for a cryptocurrency symbol in the specified fiat currency."""
    headers = {"X-CMC_PRO_API_KEY": API_KEY}
    params = {"symbol": symbol, "convert": fiat}
    response = pip._vendor.requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["data"][symbol]["quote"][fiat]["price"]
    else:
        return None


def save_portfolio(portfolio_id: str, holdings: str) -> None:
    """Save a portfolio to the data file."""
    data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            data = json.load(f)
    holdings_dict = {}
    for holding in holdings.split(","):
        symbol, quantity = holding.split("=")
        holdings_dict[symbol.upper()] = float(quantity)
    data[portfolio_id] = holdings_dict
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def show_portfolio(portfolio_id: str, fiat: str = "AUD") -> None:
    """Show the approximate valuation of a portfolio in the specified fiat currency."""
    data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            data = json.load(f)
    if portfolio_id not in data:
        print(f"Portfolio '{portfolio_id}' not found")
        return
    total_value = 0
    for symbol, quantity in data[portfolio_id].items():
        price = get_price(symbol, fiat)
        if price is None:
            print(f"Unable to get price for '{symbol}'")
            continue
        value = price * quantity
        total_value += value
        print(f"{symbol} {value:,.3f}")
    print(f"Total portfolio value: {total_value:,.3f} {fiat}")

def validate_portfolio_id(portfolio_id):
    pattern = r'^[a-zA-Z0-9_-]+$'
    return re.match(pattern, portfolio_id) is not None

def validate_holdings(holdings):
    pattern = r'^[A-Z0-9]+=[0-9]*\.?[0-9]+$'
    return all(re.match(pattern, pair) for pair in holdings.split(','))

def validate_fiat(fiat):
    accepted_currencies = ['AUD', 'USD', 'EUR', 'GBP']
    return fiat in accepted_currencies
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cryptocurrency portfolio tracking tool.")
    parser.add_argument("command", choices=["save", "show"], help="Command to execute.")
    parser.add_argument("portfolio_id", help="Unique identifier for the portfolio.")
    parser.add_argument("--holdings", help="Comma-separated list of SYMBOL=QUANTITY pairs.")
    parser.add_argument("--fiat", default="AUD", help="Fiat currency to display valuation in.")
    args = parser.parse_args()

    if not validate_portfolio_id(args.portfolio_id):
        print("Error: Invalid portfolio identifier.")
    elif args.command == "save" and not validate_holdings(args.holdings):
        print("Error: Invalid holdings format.")
    elif not validate_fiat(args.fiat):
        print("Error: Invalid fiat currency code.")
    elif args.command == "save" and args.holdings:
        print(BANNER)
        print("Your profile has been created/updated.")
        save_portfolio(args.portfolio_id, args.holdings)
    elif args.command == "show":
        print(BANNER)
        API_KEY = os.environ.get('API_KEY')
        show_portfolio(args.portfolio_id, args.fiat)
    else:
        parser.print_help()
