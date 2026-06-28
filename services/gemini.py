from google import genai
from google.genai import types
from models import Review, BatchAIAnalysisResult, GlobalInsights, AIAnalysisResult
from config import GEMINI_API_KEY
from typing import List
import json

def get_gemini_client():
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set.")
    return genai.Client(api_key=GEMINI_API_KEY)

def analyze_reviews_batch(reviews: List[Review]) -> List[AIAnalysisResult]:
    """
    Sends a batch of reviews to Gemini and returns structured AIAnalysisResult for each.
    Uses gemini-2.5-flash for speed and cost effectiveness.
    """
    if not reviews:
        return []

    client = get_gemini_client()
    model = "gemini-2.5-flash"
    
    # Prepare the input text
    reviews_text = "\n\n".join([f"Review {i+1}: {r.review_text}" for i, r in enumerate(reviews)])
    
    prompt = f"""
    You are a Senior Product Research Analyst working at Spotify.
    Analyze the following list of user reviews. For each review, extract the required fields as strictly defined in the JSON schema.
    
    Reviews to analyze:
    {reviews_text}
    """
    
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=BatchAIAnalysisResult,
                temperature=0.2, # Low temp for analytical consistency
            ),
        )
        
        # The response text should be a JSON matching BatchAIAnalysisResult
        result_dict = json.loads(response.text)
        batch_result = BatchAIAnalysisResult(**result_dict)
        return batch_result.results
    except Exception as e:
        print(f"Error in analyze_reviews_batch: {e}")
        return []

def generate_global_insights(all_analysis_results: List[AIAnalysisResult]) -> GlobalInsights:
    """
    Synthesizes aggregated insights from a large set of AIAnalysisResults.
    """
    client = get_gemini_client()
    model = "gemini-2.5-flash"
    
    # We might have too many results, so we'll sample or just summarize their text.
    # In a real scenario, we might want to batch this or use a larger context window.
    # For now, we'll convert the results back to a concise JSON string.
    summary_data = [
        {"pain_point": r.pain_point, "feature_request": r.feature_request, "user_segment": r.user_segment}
        for r in all_analysis_results if r.pain_point or r.feature_request or r.user_segment
    ]
    
    prompt = f"""
    You are a Senior Product Research Analyst for Spotify.
    Based on the following extracted pain points and feature requests from recent user reviews, 
    generate a global insights report.
    
    Extracted Data:
    {json.dumps(summary_data[:200])} # Limit to avoid token overflow in basic setup
    
    Provide the Top 10 complaints, Top 10 opportunities, Top feature requests, 
    User personas, Business recommendations, and Root causes.
    """
    
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GlobalInsights,
                temperature=0.5,
            ),
        )
        result_dict = json.loads(response.text)
        return GlobalInsights(**result_dict)
    except Exception as e:
        print(f"Error in generate_global_insights: {e}")
        return GlobalInsights(
            top_complaints=[], top_opportunities=[], top_feature_requests=[], 
            user_personas=[], business_recommendations=[], root_causes=[]
        )

if __name__ == "__main__":
    # Test script
    test_revs = [
        Review(platform="Play", review_text="The app crashes every time I try to open a playlist. Fix it!", rating=1),
        Review(platform="Reddit", review_text="I wish Spotify had a better way to organize my liked songs by mood. Also the new UI is confusing.", rating=None)
    ]
    results = analyze_reviews_batch(test_revs)
    for r in results:
        print(r.model_dump_json(indent=2))
