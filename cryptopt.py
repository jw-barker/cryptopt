import argparse
import json
import os
import pip._vendor.requests


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

DATA_FILE = "portfolio_data.json"

def get_price(symbol: str, fiat: str = "AUD") -> float:
    """
    Queries the CoinMarketCap API to get the latest market price of a cryptocurrency symbol in a specified fiat currency.

    :param symbol: the symbol of the cryptocurrency to get the price for
    :param fiat: the fiat currency to convert the price to (default: AUD)
    :return: the latest market price of the cryptocurrency in the specified fiat currency
    """
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}&convert={fiat}"
    headers = {"X-CMC_PRO_API_KEY": API_KEY}
    response = pip._vendor.requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["data"][symbol]["quote"][fiat]["price"]
    else:
        return None


def save_portfolio(portfolio_id: str, holdings: dict) -> None:
    """
    Saves a portfolio identified by a unique ID, comprised of cryptocurrency symbols and their respective quantities, to a JSON file.

    :param portfolio_id: the unique ID of the portfolio to save
    :param holdings: a dictionary of cryptocurrency symbols and their respective quantities in the portfolio
    """
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
    with open(DATA_FILE) as f:
        data = json.load(f)
    data.update({portfolio_id: holdings})
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


def show_portfolio(portfolio_id: str, fiat: str = "AUD") -> None:
    """
    Reads a portfolio from the JSON file, calculates the approximate valuation of each cryptocurrency holding in the specified fiat currency,
    and prints the results to the console.

    :param portfolio_id: the unique ID of the portfolio to show
    :param fiat: the fiat currency to convert the valuation to (default: AUD)
    """
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
        print(f"{symbol} ({quantity} units): ${value:,.2f}")
    print(f"Total portfolio value: ${total_value:,.2f}")

if __name__ == "__main__":
    print(BANNER)

    # Prompt user to enter API key
    API_KEY = input("Enter your CoinMarketcap API key: ")

    while True:
        command = input("Enter command ('save', 'show', or 'help'): ")

        if command == "save":
            portfolio_id = input("Enter portfolio ID: ")
            holdings_input = input("Enter holdings (Comma-separated list of SYMBOL=<units_in_float_format> pairs): ")
            holdings = {}
            for pair in holdings_input.split(","):
                parts = pair.split("=")
                if len(parts) != 2:
                    print("Invalid format for holdings")
                    continue
                symbol = parts[0].upper()
                try:
                    quantity = float(parts[1])
                except ValueError:
                    print("Invalid format for quantity")
                    continue
                holdings[symbol] = quantity
            save_portfolio(portfolio_id, holdings)

        elif command == "show":
            portfolio_id = input("Enter portfolio ID: ")
            fiat_currency = input("Enter fiat currency: ")
            try:
                show_portfolio(portfolio_id, fiat_currency.upper())
            except ValueError as e:
                print(str(e))

        elif command == "help":
            print("List of commands:")
            print("save - Save portfolio holdings")
            print("show - Show portfolio holdings in a given fiat currency")
            print("help - Show list of commands")
            print("quit - Exit the program")

        else:
            print("Invalid command")

        exit_choice = input("Press 'q' or 'quit' to exit or any other key to continue: ")
        if exit_choice.lower() in ["q", "quit"]:
            break




# The get_price function queries the CoinMarketCap API to get the latest market price of a cryptocurrency symbol in a specified fiat currency. 
# The save_portfolio function saves a portfolio identified by a unique ID, comprised of cryptocurrency symbols and their respective quantities, to a JSON file. 
# The show_portfolio function reads a portfolio from the JSON file, calculates the approximate valuation of each cryptocurrency holding in the specified fiat currency, 
# and prints the results to the console.
