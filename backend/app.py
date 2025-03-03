from flask import Flask, jsonify
from scraper import get_reddit_sentiment
from price_prediction import fetch_top_20_coins, get_current_price, predict_next_hour

app = Flask(__name__)

@app.route("/crypto-prices", methods=["GET"])
def get_crypto_prices():
    top_coins = fetch_top_20_coins()
    prices = {coin: get_current_price(coin) for coin in top_coins}
    return jsonify(prices)

@app.route("/sentiment/<coin>", methods=["GET"])
def get_sentiment(coin):
    sentiment = get_reddit_sentiment(coin)
    return jsonify({"coin": coin, "sentiment": sentiment})

@app.route("/price-predict/<coin>", methods=["GET"])
def get_price_prediction(coin):
    predicted_price = predict_next_hour(coin)
    return jsonify({"coin": coin, "predicted_price": predicted_price})

if __name__ == "__main__":
    app.run(debug=True)