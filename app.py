import feedparser
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from datetime import datetime

# --- CONFIGURAÇÃO ---
# Termos estratégicos para monitorar (Horizon Scanning)
search_terms = [
    "Crude Oil Price",
    "OPEC+",
    "Offshore Wind Energy",
    "Carbon Capture",
    "Geopolitics Energy Middle East",
    "Petrobras"
]

def fetch_energy_news(term):
    """
    Busca notícias recentes no Google News via RSS.
    """
    # URL formatada para o Google News RSS
    url = f"https://news.google.com/rss/search?q={term.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    
    news_list = []
    
    for entry in feed.entries[:10]: # Limitando a 10 notícias por termo para o teste
        # Análise de Sentimento Básica (TextBlob)
        # Polarity: -1 (Muito Negativo) a +1 (Muito Positivo)
        analysis = TextBlob(entry.title)
        sentiment_score = analysis.sentiment.polarity
        
        # Categorização simples
        if sentiment_score > 0.1:
            sentiment_label = "Positivo"
        elif sentiment_score < -0.1:
            sentiment_label = "Negativo"
        else:
            sentiment_label = "Neutro"

        news_list.append({
            'keyword': term,
            'title': entry.title,
            'source': entry.source.title,
            'published': entry.published,
            'sentiment_score': sentiment_score,
            'sentiment_label': sentiment_label,
            'link': entry.link
        })
            
    return news_list

# --- EXECUÇÃO DO PIPELINE ---
print("🚀 Iniciando Energy Horizon Scanner...")
all_news = []

for term in search_terms:
    print(f"Scanning: {term}...")
    try:
        data = fetch_energy_news(term)
        all_news.extend(data)
    except Exception as e:
        print(f"Erro ao buscar {term}: {e}")

# Transformando em DataFrame (formato tabular familiar para economistas)
df = pd.read_csv('energy_news_poc.csv') if False else pd.DataFrame(all_news)

# Convertendo data para datetime
df['published'] = pd.to_datetime(df['published'], errors='coerce')

# --- VISUALIZAÇÃO RÁPIDA ---
print(f"\nColeta finalizada: {len(df)} manchetes processadas.")
print("-" * 30)
print(df[['keyword', 'sentiment_label', 'title']].head())

# Criando um gráfico simples de Sentimento Médio por Tópico
plt.figure(figsize=(10, 6))
avg_sentiment = df.groupby('keyword')['sentiment_score'].mean().sort_values()
colors = ['red' if x < 0 else 'green' for x in avg_sentiment]
avg_sentiment.plot(kind='barh', color=colors)
plt.title('Sentimento Médio do Mercado por Tópico (Tempo Real)')
plt.xlabel('Score de Sentimento (Negativo < 0 < Positivo)')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Opcional: Salvar para abrir no Excel/R depois
# df.to_csv("energy_scan_results.csv", index=False)
