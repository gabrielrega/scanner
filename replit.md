# Energy Horizon Scanner

## Overview
A Python-based energy news monitoring tool that performs horizon scanning by fetching news from Google News RSS feeds and analyzing sentiment using TextBlob.

## Features
- Fetches news for strategic energy-related search terms
- Performs sentiment analysis on headlines
- Generates visualizations of sentiment by topic
- Outputs results as a pandas DataFrame

## Project Structure
```
.
├── app.py          # Main application script
├── pyproject.toml  # Python dependencies
└── .gitignore      # Git ignore rules
```

## Dependencies
- feedparser: RSS feed parsing
- pandas: Data manipulation
- textblob: Sentiment analysis
- matplotlib: Visualization

## Running
Execute with `python app.py` to scan for energy news and display sentiment analysis.

## Notes
- The script is a console application, not a web server
- Matplotlib charts may not display in headless environments
- Results can be saved to CSV by uncommenting the final line
