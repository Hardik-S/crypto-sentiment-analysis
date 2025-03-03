import requests
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import json
import os

COINGECKO_API = "https://api.coingecko.com/api/v3"

def fetch_top_20_coins():
    """Get the top 20 coins by market cap."""
    url = f"{COINGECKO_API}/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=20&page=1"
    response = requests.get(url)
    return [coin["id"] for coin in response.json()]

def fetch_price_history(coin_id, hours=6):
    """Fetch last 6 hours of price data for a coin."""
    url = f"{COINGECKO_API}/coins/{coin_id}/market_chart?vs_currency=usd&days=1&interval=hourly"
    response = requests.get(url)
    prices = response.json()["prices"][-hours:]  # Last 6 hourly prices
    return [price[1] for price in prices]  # Extract price values

def predict_next_hour(coin_id):
    """Predict next hour's price using Linear Regression."""
    prices = fetch_price_history(coin_id)
    if len(prices) < 6:
        return prices[-1] if prices else 0  # Fallback to last price
    
    # Prepare data for Linear Regression
    X = np.array(range(len(prices))).reshape(-1, 1)  # Time steps: [0, 1, 2, 3, 4, 5]
    y = np.array(prices)  # Prices
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict for the next hour (time step 6)
    next_hour = np.array([[len(prices)]])
    predicted_price = model.predict(next_hour)[0]
    return max(predicted_price, 0)  # Ensure non-negative

def get_current_price(coin_id):
    """Fetch current price for a coin."""
    url = f"{COINGECKO_API}/simple/price?ids={coin_id}&vs_currencies=usd"
    response = requests.get(url)
    return response.json()[coin_id]["usd"]

if __name__ == "__main__":
    top_coins = fetch_top_20_coins()
    print(predict_next_hour(top_coins[0]))