import asyncio
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

async def fetch_latest_crypto_news():
    # Placeholder function to fetch latest cryptocurrency news
    # Replace this with actual code to fetch news from a reliable source
    return "Bitcoin price surges amid global economic uncertainty. Ethereum follows the trend."

async def analyze_crypto_news():
    while True:
        # Fetch latest cryptocurrency news
        crypto_news = await fetch_latest_crypto_news()

        # Use OpenAI to analyze the news
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Provide insights on the following cryptocurrency news: {crypto_news}",
            max_tokens=60
        )

        analysis = response.choices[0].text.strip()
        print(f"Analysis: {analysis}")

        # Sleep for 120 seconds
        await asyncio.sleep(120)

# Run the async function
asyncio.run(analyze_crypto_news())
