# Energy Horizon Scanner

## Overview
A web-based energy news monitoring tool that performs horizon scanning by fetching news from Google News RSS feeds and analyzing sentiment using TextBlob. Features historical tracking with database storage and trend visualization, with deeper sentiment analysis of both headlines and article summaries.

## Features
- Real-time news fetching for strategic energy-related search terms
- **Deeper Sentiment Analysis**: Analyzes both headlines AND article summaries for more accurate sentiment scores
- Sentiment analysis on headlines (Positive/Neutral/Negative)
- Visual sentiment overview by topic
- Filterable news feed by topic and sentiment
- **Historical Tracking**: All scans saved to PostgreSQL database with detailed sentiment breakdowns
- **Trend Charts**: View sentiment trends over time with Chart.js
- Modern dark-themed responsive UI with tabbed navigation

## Project Structure
```
.
├── app.py              # Flask web application with SQLAlchemy
├── templates/
│   └── index.html      # Main page template with tabs
├── static/
│   ├── style.css       # Styling with tabs and charts
│   └── script.js       # Frontend logic with Chart.js
├── pyproject.toml      # Python dependencies
└── .gitignore          # Git ignore rules
```

## Dependencies
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- psycopg2-binary: PostgreSQL driver
- feedparser: RSS feed parsing
- pandas: Data manipulation
- textblob: Sentiment analysis

## Sentiment Analysis
The app analyzes sentiment using TextBlob to extract polarity scores from:
1. **Headline sentiment**: Analyzed from article titles
2. **Summary sentiment**: Extracted from article descriptions/summaries when available
3. **Combined score**: Average of headline and summary sentiment for a more balanced analysis

When summaries are unavailable, the headline sentiment is used alone.

## Database Tables
- `scan_results`: Stores aggregated sentiment per keyword per scan
- `news_articles`: Stores individual article details including headline/summary sentiment breakdown

## Running
The app runs on port 5000. 
- **Live Scanner tab**: Click "Start Scan" to fetch and analyze latest news (saved to database)
- **Historical Trends tab**: View sentiment trends over time with charts

## API Endpoints
- `GET /` - Main web interface
- `GET /api/scan` - Fetch news, analyze sentiment, save to database
- `GET /api/history` - Get historical scan data for trend charts
- `GET /api/history/summary` - Get aggregated statistics
