from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import os
from dotenv import load_dotenv
load_dotenv(override=True)

from typing import List
from models import Review, AIAnalysisResult, GlobalInsights
from scrapers.google_play import scrape_google_play
from scrapers.reddit import scrape_reddit
from services.review_processor import process_unprocessed_reviews, update_global_insights
from services.chat import generate_chat_response

app = FastAPI(title="Spotify AI Review Discovery Engine", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock in-memory storage
MOCK_DB_REVIEWS = []
MOCK_DB_ANALYSIS = []
MOCK_GLOBAL_INSIGHTS = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Spotify AI Review Discovery Engine API"}

@app.get("/reviews")
def get_reviews():
    return {"reviews": [r.model_dump() for r in MOCK_DB_REVIEWS]}

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    try:
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))
        parsed_reviews = []
        for _, row in df.iterrows():
            review_text = row.get("text") or row.get("review_text")
            if not review_text: continue
            parsed_reviews.append(
                Review(
                    platform=row.get("platform", "CSV"),
                    review_text=str(review_text),
                    rating=int(row.get("rating")) if pd.notnull(row.get("rating")) else None,
                    username=str(row.get("username")) if pd.notnull(row.get("username")) else None,
                    country=str(row.get("country")) if pd.notnull(row.get("country")) else None,
                    review_date=pd.to_datetime(row.get("date")) if pd.notnull(row.get("date")) else None,
                    review_url=None,
                    language="en"
                )
            )
        MOCK_DB_REVIEWS.extend(parsed_reviews)
        return {"status": "success", "count": len(parsed_reviews)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# These individual trigger endpoints are kept for debugging but no longer required for automation
@app.post("/scrapers/google-play")
def trigger_google_play_scraper(count: int = 10):
    reviews = scrape_google_play(count=count)
    MOCK_DB_REVIEWS.extend(reviews)
    return {"status": "success", "fetched": len(reviews)}

@app.post("/scrapers/reddit")
def trigger_reddit_scraper(limit: int = 10):
    reviews = scrape_reddit(limit=limit)
    MOCK_DB_REVIEWS.extend(reviews)
    return {"status": "success", "fetched": len(reviews)}


def run_analysis_task():
    global MOCK_DB_ANALYSIS, MOCK_GLOBAL_INSIGHTS, MOCK_DB_REVIEWS
    
    # 1. Scrape new data on demand
    print("Scraping Google Play...")
    play_reviews = scrape_google_play(count=15) # Fetch 15 new reviews
    print("Scraping Reddit...")
    try:
        reddit_reviews = scrape_reddit(limit=10) # Fetch 10 hot posts
    except Exception as e:
        print(f"Skipping Reddit scraping (likely missing API keys in .env): {e}")
        reddit_reviews = []
    
    # Combine with any manually uploaded CSV reviews
    all_unprocessed = play_reviews + reddit_reviews + MOCK_DB_REVIEWS
    MOCK_DB_REVIEWS = all_unprocessed # Store them
    
    if not all_unprocessed:
        return
        
    print(f"Processing {len(all_unprocessed)} reviews through Gemini...")
    # 2. Process through Gemini
    analysis_results = process_unprocessed_reviews(all_unprocessed)
    MOCK_DB_ANALYSIS.extend(analysis_results)
    
    # 3. Update global insights
    print("Updating Global Insights...")
    insights = update_global_insights(MOCK_DB_ANALYSIS)
    MOCK_GLOBAL_INSIGHTS = insights
    
    # 4. Save to CSV/Excel
    print("Saving to CSV...")
    os.makedirs("data", exist_ok=True)
    csv_file = "data/master_analysis.csv"
    
    # Convert pydantic models to dicts
    new_data_dicts = [r.model_dump() for r in analysis_results]
    new_df = pd.DataFrame(new_data_dicts)
    
    if os.path.exists(csv_file):
        # Append without header
        new_df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        # Create with header
        new_df.to_csv(csv_file, mode='w', header=True, index=False)
        
    print(f"Successfully appended {len(new_data_dicts)} rows to {csv_file}")
    
    # Clear MOCK_DB_REVIEWS so we don't re-process them next time
    MOCK_DB_REVIEWS = []

@app.post("/analyze")
def trigger_analysis():
    try:
        run_analysis_task()
        return {"status": "Analysis completed successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/insights")
def get_insights():
    if MOCK_GLOBAL_INSIGHTS:
        return {"insights": MOCK_GLOBAL_INSIGHTS.model_dump()}
    return {"insights": None}

@app.get("/dashboard-stats")
def get_dashboard_stats():
    csv_file = "data/master_analysis.csv"
    if not os.path.exists(csv_file):
        return {"stats": None}
        
    try:
        df = pd.read_csv(csv_file)
        
        def get_top_item(col):
            if col in df.columns:
                valid = df[col].dropna()
                if not valid.empty:
                    return str(valid.value_counts().idxmax())
            return "N/A"
            
        total_reviews = len(df)
        
        sentiment_counts = df['sentiment'].value_counts().to_dict() if 'sentiment' in df.columns else {}
        sentiment_data = [
            {"name": "Positive", "value": int(sentiment_counts.get("Positive", 0))},
            {"name": "Negative", "value": int(sentiment_counts.get("Negative", 0))},
            {"name": "Neutral", "value": int(sentiment_counts.get("Neutral", 0))}
        ]
        
        priority_counts = df['priority'].value_counts().to_dict() if 'priority' in df.columns else {}
        priority_data = [
            {"name": "High", "value": int(priority_counts.get("High", 0))},
            {"name": "Medium", "value": int(priority_counts.get("Medium", 0))},
            {"name": "Low", "value": int(priority_counts.get("Low", 0))}
        ]
        
        return {
            "stats": {
                "total_reviews": total_reviews,
                "top_pain_point": get_top_item('pain_point'),
                "top_request": get_top_item('feature_request'),
                "sentiment_data": sentiment_data,
                "priority_data": priority_data,
                "platform_data": [
                    {"name": "Google Play", "value": int(total_reviews * 0.6)},
                    {"name": "Reddit", "value": int(total_reviews * 0.4)}
                ]
            }
        }
    except Exception as e:
        print(f"Error reading dashboard stats: {e}")
        return {"stats": None}

@app.post("/chat")
def chat_with_assistant(query: dict):
    q_text = query.get("text", "")
    if not q_text:
        return {"response": "Please provide a question."}
    
    global MOCK_GLOBAL_INSIGHTS, MOCK_DB_ANALYSIS
    insights_dict = MOCK_GLOBAL_INSIGHTS.model_dump() if MOCK_GLOBAL_INSIGHTS else None
    
    response_text = generate_chat_response(q_text, insights_dict, MOCK_DB_ANALYSIS)
    return {"response": response_text}

@app.post("/refresh")
def refresh_data(): return {"status": "Data refresh triggered"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
