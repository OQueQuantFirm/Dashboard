import os
import ccxt
from dotenv import load_dotenv

def initialize_exchange(exchange_id, passphrase=None):
    """
    Initialize and connect to the desired exchange with API credentials.

    :param exchange_id: The ID of the exchange (e.g., 'binance', 'coinbasepro').
    :param passphrase: The passphrase for the exchange (if applicable).
    :return: An instance of the exchange.
    """
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv('API_KEY')
    secret = os.getenv('SECRET')

    exchange_class = getattr(ccxt, exchange_id)
    params = {'apiKey': api_key, 'secret': secret}

    if passphrase:
        params['password'] = passphrase  # Some exchanges use 'password' instead of 'passphrase'

    exchange = exchange_class(params)
    return exchange

def fetch_all_symbols(exchange):
    """
    Fetch all available symbols from an exchange.

    :param exchange: The initialized exchange instance.
    :return: A list of symbols or a message if the operation fails.
    """
    try:
        markets = exchange.load_markets()
        return list(markets.keys())
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
exchange_id_input = input("Enter the exchange ID (e.g., 'binance', 'coinbasepro'): ")
passphrase = os.getenv('PASSPHRASE')  # Optional
exchange = initialize_exchange(exchange_id_input, passphrase)

symbols = fetch_all_symbols(exchange)
print(symbols)

