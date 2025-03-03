import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

# Reddit API credentials (replace with your own)
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="crypto-sentiment-analysis by /u/YOUR_USERNAME",
)

analyzer = SentimentIntensityAnalyzer()

def get_reddit_sentiment(coin_name):
    """Scrape Reddit for sentiment on a given cryptocurrency."""
    subreddits = ["cryptocurrency", "bitcoin", "ethereum"]  # Expand as needed
    posts = []
    
    # Search posts mentioning the coin
    for subreddit in subreddits:
        for submission in reddit.subreddit(subreddit).search(coin_name, limit=50):
            text = submission.title + " " + submission.selftext
            text = re.sub(r'http\S+', '', text)  # Remove URLs
            posts.append(text)
    
    if not posts:
        return 0.0  # Neutral if no data
    
    # Calculate average sentiment
    sentiment_scores = [analyzer.polarity_scores(post)["compound"] for post in posts]
    return sum(sentiment_scores) / len(sentiment_scores)

if __name__ == "__main__":
    print(get_reddit_sentiment("bitcoin"))