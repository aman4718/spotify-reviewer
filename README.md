# Spotify AI Review Discovery Engine

![Spotify AI Engine](https://upload.wikimedia.org/wikipedia/commons/2/26/Spotify_logo_with_text.svg)

## Overview
The **Spotify AI Review Discovery Engine** is an advanced, production-ready full-stack application designed specifically for Product Managers. It completely automates the tedious process of collecting, analyzing, and synthesizing user feedback from multiple platforms (Google Play, Reddit, CSVs).

By leveraging Google's **Gemini AI**, this engine reads raw user complaints, automatically categorizes them by sentiment and priority, and extracts actionable product insights—such as top requested features and major pain points.

This project was built as a capstone for a Product Manager Fellowship.

## Features
- 🚀 **Automated Data Scrapers**: Custom built Python scrapers for Google Play and Reddit.
- 🧠 **Gemini AI Integration**: Uses `gemini-2.5-flash` with strict JSON schema forcing to structure unstructured reviews into actionable Pydantic schemas.
- 💬 **AI Product Assistant**: A built-in RAG-lite Chat UI that allows PMs to query the review database using natural language (e.g., "What are users complaining about today?").
- 📊 **Beautiful Next.js Dashboard**: Glassmorphic, dark-mode specialized dashboard using Recharts and shadcn/ui.
- 💾 **CSV Export**: Click a single button on the frontend to run the scrapers, process the data via Gemini, and automatically append the structured insights into a master local `.csv` file!

## Tech Stack
- **Frontend**: Next.js 15, React, Tailwind CSS v4, shadcn/ui, Recharts.
- **Backend**: Python 3.12, FastAPI, Pandas.
- **AI**: Google GenAI SDK (Gemini API Free Tier).
- **Automation Engine**: Seamless unified FastAPI background task processing.

## Getting Started (Local Development)

### Prerequisites
- Python 3.12+
- Node.js 18+
- A Google Gemini API Key

### Backend Setup
1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend` folder and add your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   GROQ_API_KEY=your_groq_key_here
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn api:app --reload
   ```
   *The backend will run on http://localhost:8000*

### Frontend Setup
1. Navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Create a `.env.local` file and link the backend:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```
   *The frontend will run on http://localhost:3000 (or 3001)*

## Deployment Architecture
- **Frontend**: Designed to be deployed on **Vercel** with zero-config (using Next.js defaults).
- **Backend**: Configured for deployment on **Render** (using the included `render.yaml` file).

## How it works (The "Run AI Analysis" Button)
When a Product Manager clicks **Run AI Analysis** on the dashboard:
1. The frontend hits the `POST /analyze` FastAPI endpoint.
2. FastAPI triggers a `BackgroundTask` to avoid timeout.
3. The background task runs the Google Play scraper (`google-play-scraper`) and Reddit API (`praw`).
4. The collected reviews are batched and sent to Gemini with a strict schema requirement.
5. Gemini returns a structured analysis (Sentiment, Pain Points, Features).
6. The backend appends these results via Pandas to `backend/data/master_analysis.csv` for the PM to download!
