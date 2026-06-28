from google_play_scraper import Sort, reviews
from models import Review
from typing import List
from datetime import datetime

def scrape_google_play(app_id: str = 'com.spotify.music', count: int = 100) -> List[Review]:
    """
    Scrape recent reviews from Google Play Store for a given app.
    """
    result, continuation_token = reviews(
        app_id,
        lang='en', # default language
        country='us', # default country
        sort=Sort.NEWEST, # get the latest reviews
        count=count
    )

    scraped_reviews = []
    for r in result:
        scraped_reviews.append(
            Review(
                platform="Google Play",
                review_text=r['content'],
                rating=r['score'],
                username=r['userName'],
                country="us",
                review_date=r['at'], # datetime object
                review_url=None, # Google Play API doesn't return per-review URL in this function
                language="en"
            )
        )

    return scraped_reviews

if __name__ == "__main__":
    # Test the scraper
    test_reviews = scrape_google_play(count=5)
    for rev in test_reviews:
        print(rev.model_dump_json(indent=2))
