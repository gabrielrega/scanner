from celery import shared_task
import feedparser
import pandas as pd
from textblob import TextBlob
from datetime import datetime
import re
from collections import Counter
from . import db
from .models import ScanResult, NewsArticle
import config

@shared_task(ignore_result=False)
def run_scan_task():
    """Celery task to fetch, analyze, and save news articles."""
    
    def analyze_sentiment_deep(title, summary=None):
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
        if score > 0.1: return "Positive"
        elif score < -0.1: return "Negative"
        else: return "Neutral"

    def fetch_energy_news(term):
        url = f"https://news.google.com/rss/search?q={term.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        news_list = []
        for entry in feed.entries[:10]:
            summary = getattr(entry, 'summary', getattr(entry, 'description', None))
            headline_sent, summary_sent, combined_sentiment = analyze_sentiment_deep(entry.title, summary)
            sentiment_label = categorize_sentiment(combined_sentiment)
            source_title = getattr(entry.source, 'title', 'Unknown')
            news_list.append({
                'keyword': term, 'title': entry.title, 'summary': summary, 'source': source_title,
                'published': getattr(entry, 'published', ''), 'headline_sentiment': round(headline_sent, 3),
                'summary_sentiment': round(summary_sent, 3) if summary_sent is not None else None,
                'sentiment_score': round(combined_sentiment, 3), 'sentiment_label': sentiment_label, 'link': entry.link
            })
        return news_list

    def get_all_news():
        all_news = []
        for term in config.SEARCH_TERMS:
            try:
                all_news.extend(fetch_energy_news(term))
            except Exception as e:
                print(f"Error fetching {term}: {e}")
        return all_news

    def calculate_sentiment_summary(news_data):
        df = pd.DataFrame(news_data)
        if df.empty: return []
        summary = df.groupby('keyword').agg(
            avg_sentiment=('sentiment_score', 'mean'),
            count=('title', 'count')
        ).reset_index()
        summary['avg_sentiment'] = summary['avg_sentiment'].round(3)
        return summary.to_dict('records')

    def save_scan_to_db(news_data, sentiment_summary):
        scan_time = datetime.utcnow()
        for item in sentiment_summary:
            db.session.add(ScanResult(
                scan_time=scan_time, keyword=item['keyword'],
                avg_sentiment=item['avg_sentiment'], article_count=item['count']
            ))
        for article in news_data:
            db.session.add(NewsArticle(
                scan_time=scan_time, keyword=article['keyword'], title=article['title'],
                summary=article.get('summary'), source=article['source'], published=article['published'],
                headline_sentiment=article.get('headline_sentiment'), summary_sentiment=article.get('summary_sentiment'),
                sentiment_score=article['sentiment_score'], sentiment_label=article['sentiment_label'], link=article['link']
            ))
        db.session.commit()
        return scan_time

    def extract_keywords(headlines):
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer
        
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        
        # Add custom stop words if needed
        custom_stop_words = {'says', 'will', 'not', 'set', 'lower', 'asia', 'again', 'today'}
        stop_words.update(custom_stop_words)

        all_text = " ".join(headlines).lower()
        words = re.findall(r'\\b\\w+\\b', all_text)
        
        lemmatized_words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words and len(w) > 2]
        
        counts = Counter(lemmatized_words).most_common(50)
        return [{'text': word, 'size': count} for word, count in counts]

    news_data = get_all_news()
    sentiment_summary = calculate_sentiment_summary(news_data)
    headlines = [item['title'] for item in news_data]
    word_cloud_data = extract_keywords(headlines)
    scan_time = save_scan_to_db(news_data, sentiment_summary)
    
    return {
        'news': news_data,
        'summary': sentiment_summary,
        'word_cloud': word_cloud_data,
        'total_count': len(news_data),
        'scan_time': scan_time.isoformat()
    }
