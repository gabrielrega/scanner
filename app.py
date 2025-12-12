import feedparser
import pandas as pd
from textblob import TextBlob
from flask import Flask, render_template, jsonify, send_from_directory
from datetime import datetime
import json

app = Flask(__name__)

search_terms = [
    "Crude Oil Price",
    "OPEC+",
    "Offshore Wind Energy",
    "Carbon Capture",
    "Geopolitics Energy Middle East",
    "Petrobras"
]

def fetch_energy_news(term):
    url = f"https://news.google.com/rss/search?q={term.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    
    news_list = []
    
    for entry in feed.entries[:10]:
        analysis = TextBlob(entry.title)
        sentiment_score = analysis.sentiment.polarity
        
        if sentiment_score > 0.1:
            sentiment_label = "Positive"
        elif sentiment_score < -0.1:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        source_title = entry.source.title if hasattr(entry, 'source') and hasattr(entry.source, 'title') else 'Unknown'
        
        news_list.append({
            'keyword': term,
            'title': entry.title,
            'source': source_title,
            'published': entry.published if hasattr(entry, 'published') else '',
            'sentiment_score': round(sentiment_score, 3),
            'sentiment_label': sentiment_label,
            'link': entry.link
        })
            
    return news_list

def get_all_news():
    all_news = []
    for term in search_terms:
        try:
            data = fetch_energy_news(term)
            all_news.extend(data)
        except Exception as e:
            print(f"Error fetching {term}: {e}")
    return all_news

def calculate_sentiment_summary(news_data):
    df = pd.DataFrame(news_data)
    if df.empty:
        return []
    
    summary = df.groupby('keyword').agg({
        'sentiment_score': 'mean',
        'title': 'count'
    }).reset_index()
    summary.columns = ['keyword', 'avg_sentiment', 'count']
    summary['avg_sentiment'] = summary['avg_sentiment'].round(3)
    return summary.to_dict('records')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/')
def index():
    return render_template('index.html', search_terms=search_terms)

@app.route('/api/scan')
def scan():
    news_data = get_all_news()
    sentiment_summary = calculate_sentiment_summary(news_data)
    return jsonify({
        'news': news_data,
        'summary': sentiment_summary,
        'total_count': len(news_data),
        'scan_time': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
