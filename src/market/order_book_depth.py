import ccxt

def order_book_depth(exchange_id, symbol, depth_level=5):
    """
    Perform an advanced analysis of the order book depth for a given exchange and symbol.

    :param exchange_id: The ID of the exchange (e.g., 'binance').
    :param symbol: The trading symbol (e.g., 'BTC/USDT').
    :param depth_level: The number of levels to consider for depth analysis.
    :return: Advanced analysis of the order book depth.
    """
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({'enableRateLimit': True})

    try:
        order_book = exchange.fetch_order_book(symbol)
        bids = order_book['bids']
        asks = order_book['asks']

        # Spread calculation
        highest_bid = bids[0][0] if bids else 0
        lowest_ask = asks[0][0] if asks else 0
        spread = lowest_ask - highest_bid

        # Depth calculation for specified levels
        bid_depth = sum([amount for price, amount in bids[:depth_level]])
        ask_depth = sum([amount for price, amount in asks[:depth_level]])

        # Liquidity calculation (sum of top n bids and asks)
        liquidity = bid_depth + ask_depth

        # Order book imbalance
        imbalance = bid_depth - ask_depth

        return {
            'spread': spread,
            'highest_bid': highest_bid,
            'lowest_ask': lowest_ask,
            'bid_depth': bid_depth,
            'ask_depth': ask_depth,
            'liquidity': liquidity,
            'imbalance': imbalance
        }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
# exchange_id = 'binance'
# symbol = 'BTC/USDT'
# analysis_results = order_book_depth(exchange_id, symbol)
# print(analysis_results)
