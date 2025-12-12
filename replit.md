# Energy Horizon Scanner

## Overview
A web-based energy news monitoring tool that performs horizon scanning by fetching news from Google News RSS feeds and analyzing sentiment using TextBlob.

## Features
- Real-time news fetching for strategic energy-related search terms
- Sentiment analysis on headlines (Positive/Neutral/Negative)
- Visual sentiment overview by topic
- Filterable news feed by topic and sentiment
- Modern dark-themed responsive UI

## Project Structure
```
.
├── app.py              # Flask web application
├── templates/
│   └── index.html      # Main page template
├── static/
│   ├── style.css       # Styling
│   └── script.js       # Frontend logic
├── pyproject.toml      # Python dependencies
└── .gitignore          # Git ignore rules
```

## Dependencies
- Flask: Web framework
- feedparser: RSS feed parsing
- pandas: Data manipulation
- textblob: Sentiment analysis

## Running
The app runs on port 5000. Click "Start Scan" to fetch and analyze the latest energy news.

## API Endpoints
- `GET /` - Main web interface
- `GET /api/scan` - Returns JSON with news data and sentiment summary
