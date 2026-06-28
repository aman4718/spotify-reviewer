import os
import praw
from datetime import datetime
from typing import List
from models import Review
from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "ReviewDiscoveryEngine/1.0")

def get_reddit_client():
    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        return None
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

def scrape_reddit(subreddit_name: str = "spotify", limit: int = 50) -> List[Review]:
    """
    Scrape hot posts and comments from a given subreddit as reviews/feedback.
    """
    reddit = get_reddit_client()
    if not reddit:
        print("Warning: Reddit credentials not found. Skipping Reddit scraping.")
        return []

    subreddit = reddit.subreddit(subreddit_name)
    scraped_reviews = []

    for post in subreddit.hot(limit=limit):
        # We can treat the post text itself as a review, or comments.
        # Often, posts are long-form feedback.
        if post.selftext: # Only take text posts
            scraped_reviews.append(
                Review(
                    platform="Reddit",
                    review_text=f"{post.title}\n{post.selftext}",
                    rating=None, # Reddit doesn't have 1-5 rating, maybe derive later via AI
                    username=post.author.name if post.author else "Deleted",
                    country=None, # Reddit doesn't provide user country
                    review_date=datetime.fromtimestamp(post.created_utc),
                    review_url=post.url,
                    language="en"
                )
            )

    return scraped_reviews

if __name__ == "__main__":
    # Test the scraper (will only work if REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET are in .env)
    test_reviews = scrape_reddit(limit=2)
    for rev in test_reviews:
        print(rev.model_dump_json(indent=2))
