import ccxt
import openai
import os
from dotenv import load_dotenv

from src.market.order_book_depth import order_book_depth
from src.market.order_book_imbalance import order_book_imbalance

# Load OpenAI API key
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

def market_analyze(exchange_id, symbol, timeframe):
    """
    Fetch OHLCV data, perform technical analysis, and use OpenAI for further analysis.

    :param exchange_id: The ID of the exchange (e.g., 'binance').
    :param symbol: The trading symbol (e.g., 'BTC/USDT').
    :param timeframe: The timeframe for OHLCV data (e.g., '1d', '5m').
    :return: Analysis results from OpenAI.
    """
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({'enableRateLimit': True})

    # Fetch OHLCV data
    ohlcv_data = exchange.fetch_ohlcv(symbol, timeframe)

    # Perform technical analysis using imported functions
    depth_analysis = order_book_depth(exchange_id, symbol)
    imbalance_analysis = order_book_imbalance(exchange_id, symbol)

    # Prepare data for OpenAI analysis
    analysis_prompt = f"""
    Perform a technical analysis based on the following data:
    OHLCV Data: {ohlcv_data}
    Order Book Depth Analysis: {depth_analysis}
    Order Book Imbalance Analysis: {imbalance_analysis}
    """

    # Use OpenAI for advanced analysis
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=analysis_prompt,
        max_tokens=100
    )

    return response.choices[0].text.strip()

# Dynamic example usage
if __name__ == "__main__":
    exchange_id = input("Enter the exchange ID (e.g., 'binance'): ")
    symbol = input("Enter the symbol (e.g., 'BTC/USDT'): ")
    timeframe = input("Enter the timeframe (e.g., '1d', '5m'): ")
    result = market_analyze(exchange_id, symbol, timeframe)
    print(result)
