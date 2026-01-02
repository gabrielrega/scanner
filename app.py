import os
import feedparser
import pandas as pd
from textblob import TextBlob
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timedelta

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "energy-scanner-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

search_terms = [
    "Crude Oil Price",
    "OPEC+",
    "Offshore Wind Energy",
    "Carbon Capture",
    "Geopolitics Energy Middle East",
    "Petrobras"
]

class ScanResult(db.Model):
    __tablename__ = 'scan_results'
    
    id = db.Column(db.Integer, primary_key=True)
    scan_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    keyword = db.Column(db.String(100), nullable=False)
    avg_sentiment = db.Column(db.Float, nullable=False)
    article_count = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'scan_time': self.scan_time.isoformat(),
            'keyword': self.keyword,
            'avg_sentiment': round(self.avg_sentiment, 3),
            'article_count': self.article_count
        }

class NewsArticle(db.Model):
    __tablename__ = 'news_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    scan_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    keyword = db.Column(db.String(100), nullable=False)
    title = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(200))
    published = db.Column(db.String(100))
    headline_sentiment = db.Column(db.Float, nullable=True)
    summary_sentiment = db.Column(db.Float, nullable=True)
    sentiment_score = db.Column(db.Float, nullable=False)
    sentiment_label = db.Column(db.String(20), nullable=False)
    link = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'scan_time': self.scan_time.isoformat(),
            'keyword': self.keyword,
            'title': self.title,
            'summary': self.summary,
            'source': self.source,
            'published': self.published,
            'headline_sentiment': self.headline_sentiment,
            'summary_sentiment': self.summary_sentiment,
            'sentiment_score': self.sentiment_score,
            'sentiment_label': self.sentiment_label,
            'link': self.link
        }

with app.app_context():
    db.create_all()

def analyze_sentiment_deep(title, summary=None):
    """Analyze sentiment from both headline and summary for deeper accuracy"""
    headline_analysis = TextBlob(title)
    headline_sentiment = headline_analysis.sentiment.polarity
    
    summary_sentiment = None
    combined_sentiment = headline_sentiment
    
    if summary:
        summary_analysis = TextBlob(summary)
        summary_sentiment = summary_analysis.sentiment.polarity
        combined_sentiment = (headline_sentiment + summary_sentiment) / 2
    
    return headline_sentiment, summary_sentiment, combined_sentiment

def categorize_sentiment(score):
    """Categorize sentiment score into label"""
    if score > 0.1:
        return "Positive"
    elif score < -0.1:
        return "Negative"
    else:
        return "Neutral"

def fetch_energy_news(term):
    url = f"https://news.google.com/rss/search?q={term.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    
    news_list = []
    
    for entry in feed.entries[:10]:
        summary = None
        if hasattr(entry, 'summary') and entry.summary:
            summary = entry.summary
        elif hasattr(entry, 'description') and entry.description:
            summary = entry.description
        
        headline_sent, summary_sent, combined_sentiment = analyze_sentiment_deep(entry.title, summary)
        sentiment_label = categorize_sentiment(combined_sentiment)
        
        source_title = entry.source.title if hasattr(entry, 'source') and hasattr(entry.source, 'title') else 'Unknown'
        
        news_list.append({
            'keyword': term,
            'title': entry.title,
            'summary': summary,
            'source': source_title,
            'published': entry.published if hasattr(entry, 'published') else '',
            'headline_sentiment': round(headline_sent, 3),
            'summary_sentiment': round(summary_sent, 3) if summary_sent is not None else None,
            'sentiment_score': round(combined_sentiment, 3),
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

def save_scan_to_db(news_data, sentiment_summary):
    scan_time = datetime.utcnow()
    
    for item in sentiment_summary:
        scan_result = ScanResult(
            scan_time=scan_time,
            keyword=item['keyword'],
            avg_sentiment=item['avg_sentiment'],
            article_count=item['count']
        )
        db.session.add(scan_result)
    
    for article in news_data:
        news_article = NewsArticle(
            scan_time=scan_time,
            keyword=article['keyword'],
            title=article['title'],
            summary=article.get('summary'),
            source=article['source'],
            published=article['published'],
            headline_sentiment=article.get('headline_sentiment'),
            summary_sentiment=article.get('summary_sentiment'),
            sentiment_score=article['sentiment_score'],
            sentiment_label=article['sentiment_label'],
            link=article['link']
        )
        db.session.add(news_article)
    
    db.session.commit()
    return scan_time

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/')
def index():
    return render_template('index.html', search_terms=search_terms)

from collections import Counter
import re

def extract_keywords(headlines):
    """Extract most common meaningful words from headlines"""
    # Simple stop words list
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'of', 'from', 'up', 'down', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'as', 'at', 'if', 'has', 'have', 'had', 'do', 'does', 'did', 'set', 'set', 'lower', 'Asia', 'again', 'today', 'says', 'will', 'not'}
    
    all_text = " ".join(headlines).lower()
    # Remove special characters and keep only words
    words = re.findall(r'\w+', all_text)
    
    # Filter out stop words and short words
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Count occurrences
    counts = Counter(keywords).most_common(50)
    
    # Format for word cloud (label, value)
    return [{'text': word, 'size': count} for word, count in counts]

@app.route('/api/scan')
def scan():
    news_data = get_all_news()
    sentiment_summary = calculate_sentiment_summary(news_data)
    
    headlines = [item['title'] for item in news_data]
    word_cloud_data = extract_keywords(headlines)
    
    scan_time = save_scan_to_db(news_data, sentiment_summary)
    
    return jsonify({
        'news': news_data,
        'summary': sentiment_summary,
        'word_cloud': word_cloud_data,
        'total_count': len(news_data),
        'scan_time': scan_time.isoformat()
    })

@app.route('/api/history')
def get_history():
    days = 7
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    results = ScanResult.query.filter(
        ScanResult.scan_time >= cutoff
    ).order_by(ScanResult.scan_time.asc()).all()
    
    history_data = {}
    for result in results:
        if result.keyword not in history_data:
            history_data[result.keyword] = []
        history_data[result.keyword].append({
            'scan_time': result.scan_time.isoformat(),
            'avg_sentiment': result.avg_sentiment,
            'article_count': result.article_count
        })
    
    return jsonify({
        'history': history_data,
        'keywords': list(history_data.keys()),
        'days': days
    })

@app.route('/api/history/summary')
def get_history_summary():
    results = db.session.query(
        ScanResult.keyword,
        db.func.count(ScanResult.id).label('scan_count'),
        db.func.avg(ScanResult.avg_sentiment).label('overall_avg'),
        db.func.min(ScanResult.scan_time).label('first_scan'),
        db.func.max(ScanResult.scan_time).label('last_scan')
    ).group_by(ScanResult.keyword).all()
    
    summary = []
    for r in results:
        summary.append({
            'keyword': r.keyword,
            'scan_count': r.scan_count,
            'overall_avg': round(r.overall_avg, 3) if r.overall_avg else 0,
            'first_scan': r.first_scan.isoformat() if r.first_scan else None,
            'last_scan': r.last_scan.isoformat() if r.last_scan else None
        })
    
    total_scans = db.session.query(
        db.func.count(db.func.distinct(ScanResult.scan_time))
    ).scalar() or 0
    
    return jsonify({
        'summary': summary,
        'total_scans': total_scans
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
