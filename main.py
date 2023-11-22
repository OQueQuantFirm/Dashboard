import ccxt
import openai
import os
from dotenv import load_dotenv

# Adjust the import paths based on the directory structure
from src.market.order_book_depth import order_book_depth
from src.market.order_book_imbalance import order_book_imbalance

# Load OpenAI API key
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

def analyze_crypto(symbol, timeframe, exchange_id='binance'):
    """
    Fetch OHLCV data, perform technical analysis, and use OpenAI for further analysis.

    :param symbol: The trading symbol (e.g., 'BTC/USDT').
    :param timeframe: The timeframe for OHLCV data (e.g., '1d', '5m').
    :param exchange_id: The ID of the exchange (default 'binance').
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

# Example usage
# result = analyze_crypto('BTC/USDT', '1d')
# print(result)
