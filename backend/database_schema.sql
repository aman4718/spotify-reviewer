-- Database Schema for Spotify AI Review Discovery Engine

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table: reviews (Stores the raw review data from all platforms)
CREATE TABLE IF NOT EXISTS reviews (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    platform VARCHAR(50) NOT NULL, -- e.g., 'Google Play', 'Reddit', 'Spotify Community', 'CSV'
    review_text TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    username VARCHAR(255),
    country VARCHAR(100),
    review_date TIMESTAMP WITH TIME ZONE,
    review_url TEXT,
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: ai_analysis (Stores the Gemini analysis results for each review)
CREATE TABLE IF NOT EXISTS ai_analysis (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    review_id UUID REFERENCES reviews(id) ON DELETE CASCADE,
    sentiment VARCHAR(20), -- Positive, Negative, Neutral
    emotion VARCHAR(50),
    pain_point TEXT,
    root_cause TEXT,
    listening_goal TEXT,
    feature_request TEXT,
    discovery_barrier TEXT,
    user_segment VARCHAR(100),
    listening_behavior TEXT,
    priority VARCHAR(20), -- High, Medium, Low
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: segments (Pre-aggregated segments)
CREATE TABLE IF NOT EXISTS segments (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    segment_name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: pain_points (Aggregated pain points)
CREATE TABLE IF NOT EXISTS pain_points (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    pain_point_name VARCHAR(255) NOT NULL,
    frequency INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: feature_requests (Aggregated feature requests)
CREATE TABLE IF NOT EXISTS feature_requests (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    feature_name VARCHAR(255) NOT NULL,
    frequency INTEGER DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: dashboard_stats (Snapshots for quick dashboard loading)
CREATE TABLE IF NOT EXISTS dashboard_stats (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    total_reviews INTEGER DEFAULT 0,
    positive_reviews INTEGER DEFAULT 0,
    negative_reviews INTEGER DEFAULT 0,
    neutral_reviews INTEGER DEFAULT 0,
    average_rating NUMERIC(3, 2),
    snapshot_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
