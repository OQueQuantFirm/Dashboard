import time
import openai
import os
from dotenv import load_dotenv
import logging
import yfinance as yf
from pycoingecko import CoinGeckoAPI

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

cg = CoinGeckoAPI()

def fetch_latest_crypto_data():
    """
    Fetch latest cryptocurrency data using yfinance and CoinGecko.
    """
    btc_yfinance = yf.Ticker("BTC-USD")
    yf_data = btc_yfinance.history(period="1d")

    # Fetch Bitcoin data from CoinGecko
    cg_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=1)

    return yf_data, cg_data

def analyze_crypto_news(news_cache, sleep_duration=120):
    while True:
        yf_data, cg_data = fetch_latest_crypto_data()
        yf_news = str(yf_data.iloc[-1].to_dict())  # Convert the last row of yfinance data to a string
        cg_news = str(cg_data)  # Convert CoinGecko data to a string

        news_items = [yf_news, cg_news]

        for news in news_items:
            news_hash = hash(news)
            if news_hash not in news_cache:
                try:
                    response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=f"Provide insights on the following cryptocurrency data: {news}",
                        max_tokens=60
                    )
                    analysis = response.choices[0].text.strip()
                    logging.info(f"Analysis: {analysis}")
                    news_cache.add(news_hash)
                except Exception as e:
                    logging.error(f"Error during analysis: {str(e)}")

        time.sleep(sleep_duration)

# Run the function
if __name__ == "__main__":
    news_cache = set()
    analyze_crypto_news(news_cache)
