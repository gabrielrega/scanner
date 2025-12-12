let newsData = [];
let trendChart = null;

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab));
});

document.getElementById('scanBtn').addEventListener('click', startScan);
document.getElementById('topicFilter').addEventListener('change', filterNews);
document.getElementById('sentimentFilter').addEventListener('change', filterNews);
document.getElementById('refreshHistoryBtn').addEventListener('click', loadHistory);

function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
    document.getElementById(`${tabId}-tab`).classList.add('active');
    
    if (tabId === 'history') {
        loadHistory();
    }
}

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
        status.textContent = `${data.total_count} articles scanned at ${scanTime} (saved to history)`;
        
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

async function loadHistory() {
    const loading = document.getElementById('historyLoading');
    const status = document.getElementById('historyStatus');
    
    loading.classList.remove('hidden');
    status.textContent = 'Loading...';
    
    try {
        const [historyRes, summaryRes] = await Promise.all([
            fetch('/api/history'),
            fetch('/api/history/summary')
        ]);
        
        const historyData = await historyRes.json();
        const summaryData = await summaryRes.json();
        
        displayStats(summaryData);
        displayTrendChart(historyData);
        
        status.textContent = `Showing ${summaryData.total_scans} scans over ${historyData.days} days`;
        
    } catch (error) {
        status.textContent = 'Error loading history. Please try again.';
        console.error('History error:', error);
    } finally {
        loading.classList.add('hidden');
    }
}

function displayStats(data) {
    const container = document.getElementById('statsGrid');
    container.innerHTML = '';
    
    const totalScansCard = document.createElement('div');
    totalScansCard.className = 'stat-card';
    totalScansCard.innerHTML = `
        <h3>Total Scans</h3>
        <div class="stat-value">${data.total_scans}</div>
        <div class="stat-detail">Historical records</div>
    `;
    container.appendChild(totalScansCard);
    
    if (data.summary.length > 0) {
        const avgSentiments = data.summary.map(s => s.overall_avg);
        const overallAvg = avgSentiments.reduce((a, b) => a + b, 0) / avgSentiments.length;
        
        let sentimentClass = 'neutral';
        if (overallAvg > 0.1) sentimentClass = 'positive';
        else if (overallAvg < -0.1) sentimentClass = 'negative';
        
        const avgCard = document.createElement('div');
        avgCard.className = 'stat-card';
        avgCard.innerHTML = `
            <h3>Overall Avg Sentiment</h3>
            <div class="stat-value" style="color: ${sentimentClass === 'positive' ? '#00c853' : sentimentClass === 'negative' ? '#ff5252' : '#ffc107'}">${overallAvg > 0 ? '+' : ''}${overallAvg.toFixed(3)}</div>
            <div class="stat-detail">Across all topics</div>
        `;
        container.appendChild(avgCard);
        
        const topicsCard = document.createElement('div');
        topicsCard.className = 'stat-card';
        topicsCard.innerHTML = `
            <h3>Topics Tracked</h3>
            <div class="stat-value">${data.summary.length}</div>
            <div class="stat-detail">Energy keywords</div>
        `;
        container.appendChild(topicsCard);
    }
}

function displayTrendChart(data) {
    const ctx = document.getElementById('trendChart').getContext('2d');
    
    if (trendChart) {
        trendChart.destroy();
    }
    
    const colors = [
        '#4facfe', '#00f2fe', '#00c853', '#ffc107', '#ff5252', '#ab47bc'
    ];
    
    const datasets = data.keywords.map((keyword, index) => {
        const keywordData = data.history[keyword] || [];
        return {
            label: keyword,
            data: keywordData.map(d => ({
                x: new Date(d.scan_time),
                y: d.avg_sentiment
            })),
            borderColor: colors[index % colors.length],
            backgroundColor: colors[index % colors.length] + '20',
            fill: false,
            tension: 0.3,
            pointRadius: 4,
            pointHoverRadius: 6
        };
    });
    
    trendChart = new Chart(ctx, {
        type: 'line',
        data: { datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#888',
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 26, 46, 0.9)',
                    titleColor: '#e8e8e8',
                    bodyColor: '#e8e8e8',
                    borderColor: 'rgba(79, 172, 254, 0.3)',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'hour',
                        displayFormats: {
                            hour: 'MMM d, HH:mm'
                        }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#888'
                    }
                },
                y: {
                    min: -1,
                    max: 1,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#888',
                        callback: function(value) {
                            if (value === 0) return '0 (Neutral)';
                            if (value > 0) return '+' + value.toFixed(1) + ' (Positive)';
                            return value.toFixed(1) + ' (Negative)';
                        }
                    }
                }
            }
        }
    });
}
