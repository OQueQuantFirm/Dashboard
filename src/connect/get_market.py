import os
from src.connect.exchange_instantiate import initialize_exchange

def get_markets(exchange):
    """
    Get available markets from the exchange.
    
    :param exchange: Initialized exchange instance.
    :return: Dictionary of available markets.
    """
    markets = exchange.load_markets()
    market_types = {'spot': [], 'margin': [], 'futures': [], 'other': []}

    for symbol, details in markets.items():
        if 'spot' in details and details['spot']:
            market_types['spot'].append(symbol)
        if 'margin' in details and details['margin']:
            market_types['margin'].append(symbol)
        if 'future' in details and details['future']:
            market_types['futures'].append(symbol)
        if not any(key in details and details[key] for key in ['spot', 'margin', 'future']):
            market_types['other'].append(symbol)
    
    return market_types

def user_select_market(market_types):
    """
    Allow user to select a market type and display available symbols for that market.

    :param market_types: Dictionary of available markets.
    """
    print("Available market types: ", list(market_types.keys()))
    selected_market = input("Select a market type: ").lower()

    if selected_market in market_types:
        print(f"Symbols available in {selected_market} market: ", market_types[selected_market])
    else:
        print("Invalid market type selected.")

# Example usage
if __name__ == "__main__":
    exchange_id_input = input("Enter the exchange ID (e.g., 'binance', 'coinbasepro'): ")
    passphrase = os.getenv('PASSPHRASE')  # Optional, use only if needed
    exchange = initialize_exchange(exchange_id_input, passphrase)
    available_markets = get_markets(exchange)
    user_select_market(available_markets)
