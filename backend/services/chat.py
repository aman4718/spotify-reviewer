from groq import Groq
import json
import os

def generate_chat_response(query: str, insights: dict, recent_analysis: list) -> str:
    """
    Generates a conversational response using Groq (Llama 3), grounded in the provided review insights.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "I'm sorry, the Groq API key is not configured. Please add GROQ_API_KEY to your .env file."
        
    client = Groq(api_key=api_key)
    model = "llama-3.3-70b-versatile"
    
    # Safely truncate data to prevent token limit issues
    safe_insights = json.dumps(insights) if insights else "No global insights available yet."
    safe_analysis = json.dumps([r.model_dump() for r in recent_analysis[-20:]]) if recent_analysis else "No recent analysis available."

    prompt = f"""
    You are the Spotify AI Product Assistant. Your job is to answer the Product Manager's questions based ONLY on the provided review data and insights.
    Do not invent data. If the answer is not in the provided data, politely say so.

    CONTEXT DATA:
    Global Insights:
    {safe_insights}

    Recent Reviews Analysis (Sample):
    {safe_analysis}

    USER QUERY:
    {query}

    Answer strictly based on the context above. Be professional, concise, and helpful.
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful Spotify AI Assistant."},
                {"role": "user", "content": prompt}
            ],
            model=model,
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in generate_chat_response (Groq): {e}")
        return f"I'm sorry, I encountered an error connecting to Groq: {str(e)}"
