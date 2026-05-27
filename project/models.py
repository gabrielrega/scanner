from . import db
from datetime import datetime

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
