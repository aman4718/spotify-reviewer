from typing import List
from models import Review, AIAnalysisResult, GlobalInsights
from services.gemini import analyze_reviews_batch, generate_global_insights

def process_unprocessed_reviews(reviews: List[Review]) -> List[AIAnalysisResult]:
    """
    Takes raw reviews, batches them, and gets AI analysis.
    In the real app, this will fetch from Supabase `reviews` table 
    where they don't have an entry in `ai_analysis`.
    """
    # Batch processing to optimize Gemini API calls
    BATCH_SIZE = 10
    all_results = []
    
    for i in range(0, len(reviews), BATCH_SIZE):
        batch = reviews[i:i + BATCH_SIZE]
        print(f"Processing batch of {len(batch)} reviews...")
        results = analyze_reviews_batch(batch)
        all_results.extend(results)
        
    # Later: Save all_results to Supabase ai_analysis table
    return all_results

def update_global_insights(all_analysis: List[AIAnalysisResult]) -> GlobalInsights:
    """
    Updates the global insights by running them through Gemini.
    """
    insights = generate_global_insights(all_analysis)
    # Later: Save insights to Supabase dashboard_stats or similar
    return insights
