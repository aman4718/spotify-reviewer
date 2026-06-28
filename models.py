from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Review(BaseModel):
    platform: str
    review_text: str
    rating: Optional[int] = Field(None, ge=1, le=5)
    username: Optional[str] = None
    country: Optional[str] = None
    review_date: Optional[datetime] = None
    review_url: Optional[str] = None
    language: str = "en"

class AIAnalysisResult(BaseModel):
    sentiment: str = Field(description="Positive, Negative, or Neutral")
    emotion: str = Field(description="The primary emotion expressed (e.g., Frustrated, Joyful, Apathetic)")
    pain_point: Optional[str] = Field(None, description="The main pain point mentioned, if any")
    root_cause: Optional[str] = Field(None, description="The root cause of the pain point")
    listening_goal: Optional[str] = Field(None, description="What the user is trying to achieve (e.g., Discover new music, Focus)")
    feature_request: Optional[str] = Field(None, description="Any specific feature requested by the user")
    discovery_barrier: Optional[str] = Field(None, description="Why the user fails to discover new music")
    user_segment: Optional[str] = Field(None, description="User persona (e.g., Commuter, Gym goer, Audiophile)")
    listening_behavior: Optional[str] = Field(None, description="How they listen (e.g., Repetitive, Shuffle, Curated playlists)")
    priority: str = Field(description="Priority for product managers to address: High, Medium, Low")

class BatchAIAnalysisResult(BaseModel):
    results: List[AIAnalysisResult]

class GlobalInsights(BaseModel):
    top_complaints: List[str]
    top_opportunities: List[str]
    top_feature_requests: List[str]
    user_personas: List[str]
    business_recommendations: List[str]
    root_causes: List[str]
