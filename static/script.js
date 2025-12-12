let newsData = [];

document.getElementById('scanBtn').addEventListener('click', startScan);
document.getElementById('topicFilter').addEventListener('change', filterNews);
document.getElementById('sentimentFilter').addEventListener('change', filterNews);

async function startScan() {
    const btn = document.getElementById('scanBtn');
    const loading = document.getElementById('loading');
    const status = document.getElementById('status');
    
    btn.disabled = true;
    btn.textContent = 'Scanning...';
    loading.classList.remove('hidden');
    status.textContent = '';
    
    try {
        const response = await fetch('/api/scan');
        const data = await response.json();
        
        newsData = data.news;
        
        displaySummary(data.summary);
        displayNews(newsData);
        
        document.getElementById('summary').classList.remove('hidden');
        document.getElementById('newsSection').classList.remove('hidden');
        
        const scanTime = new Date(data.scan_time).toLocaleTimeString();
        status.textContent = `${data.total_count} articles scanned at ${scanTime}`;
        
    } catch (error) {
        status.textContent = 'Error scanning news. Please try again.';
        console.error('Scan error:', error);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Refresh Scan';
        loading.classList.add('hidden');
    }
}

function displaySummary(summary) {
    const container = document.getElementById('summaryChart');
    container.innerHTML = '';
    
    summary.sort((a, b) => b.avg_sentiment - a.avg_sentiment);
    
    summary.forEach(item => {
        let sentimentClass = 'neutral';
        if (item.avg_sentiment > 0.1) sentimentClass = 'positive';
        else if (item.avg_sentiment < -0.1) sentimentClass = 'negative';
        
        const barWidth = Math.abs(item.avg_sentiment) * 100 + 50;
        let barColor = '#ffc107';
        if (sentimentClass === 'positive') barColor = '#00c853';
        else if (sentimentClass === 'negative') barColor = '#ff5252';
        
        const card = document.createElement('div');
        card.className = 'sentiment-card';
        card.innerHTML = `
            <h3>${item.keyword}</h3>
            <div class="sentiment-score ${sentimentClass}">${item.avg_sentiment > 0 ? '+' : ''}${item.avg_sentiment.toFixed(2)}</div>
            <div class="sentiment-bar">
                <div class="sentiment-bar-fill" style="width: ${barWidth}%; background: ${barColor}"></div>
            </div>
            <div class="article-count">${item.count} articles</div>
        `;
        container.appendChild(card);
    });
}

function displayNews(news) {
    const container = document.getElementById('newsGrid');
    container.innerHTML = '';
    
    if (news.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #888;">No news found matching your filters.</p>';
        return;
    }
    
    news.forEach(item => {
        let sentimentClass = 'neutral';
        if (item.sentiment_label === 'Positive') sentimentClass = 'positive';
        else if (item.sentiment_label === 'Negative') sentimentClass = 'negative';
        
        const newsItem = document.createElement('article');
        newsItem.className = `news-item ${sentimentClass}`;
        newsItem.innerHTML = `
            <div class="news-header">
                <span class="news-keyword">${item.keyword}</span>
                <span class="sentiment-badge ${sentimentClass}">${item.sentiment_label} (${item.sentiment_score})</span>
            </div>
            <h3 class="news-title"><a href="${item.link}" target="_blank" rel="noopener">${item.title}</a></h3>
            <div class="news-meta">
                <span>${item.source}</span>
                <span>${item.published}</span>
            </div>
        `;
        container.appendChild(newsItem);
    });
}

function filterNews() {
    const topicFilter = document.getElementById('topicFilter').value;
    const sentimentFilter = document.getElementById('sentimentFilter').value;
    
    let filtered = newsData;
    
    if (topicFilter !== 'all') {
        filtered = filtered.filter(item => item.keyword === topicFilter);
    }
    
    if (sentimentFilter !== 'all') {
        filtered = filtered.filter(item => item.sentiment_label === sentimentFilter);
    }
    
    displayNews(filtered);
}
