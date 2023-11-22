import ccxt

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

# Fetch and display the exchanges with their IDs
exchanges_with_ids = get_all_exchanges_with_ids()
for name, exchange_id in exchanges_with_ids.items():
    print(f"{name}: {exchange_id}")
