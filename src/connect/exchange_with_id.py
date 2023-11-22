import ccxt
from src.connect.exchange_instantiate import initialize_exchange

def get_all_exchanges_with_ids():
    """
    Fetch all available exchanges on CCXT and their respective IDs.

    :return: A dictionary where keys are exchange names and values are their IDs.
    """
    exchanges_with_ids = {}
    for exchange_id in ccxt.exchanges:
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class()
        exchanges_with_ids[exchange.name] = exchange_id
    return exchanges_with_ids

def user_select_exchange(exchanges_with_ids):
    """
    Allow the user to select an exchange.

    :param exchanges_with_ids: Dictionary of exchange names and IDs.
    :return: Selected exchange instance.
    """
    print("Available exchanges:")
    for name, exchange_id in exchanges_with_ids.items():
        print(f"{name}: {exchange_id}")

    selected_exchange_id = input("Enter the ID of the exchange you prefer: ")
    if selected_exchange_id in ccxt.exchanges:
        return initialize_exchange(selected_exchange_id)
    else:
        print("Invalid exchange ID.")
        return None

# Example usage
if __name__ == "__main__":
    exchanges_with_ids = get_all_exchanges_with_ids()
    selected_exchange = user_select_exchange(exchanges_with_ids)
    if selected_exchange:
        print(f"Selected exchange: {selected_exchange}")
