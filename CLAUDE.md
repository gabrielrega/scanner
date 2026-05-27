# scanner — Energy Horizon Scanner

Dashboard web para monitoramento de sentimento em notícias do setor de energia. Busca artigos via Google News RSS, analisa o sentimento com TextBlob e exibe tendências históricas em gráficos interativos.

## Stack

- **Backend**: Flask + SQLAlchemy + Flask-Migrate
- **Tarefas assíncronas**: Celery + Redis
- **NLP**: TextBlob + NLTK
- **Frontend**: HTML/CSS/JS vanilla + Chart.js
- **Deploy**: Docker Compose (recomendado)

## Como rodar

### Docker (recomendado)

```bash
docker-compose up --build
```

Sobe automaticamente: Flask, Celery worker e Redis. App em `http://127.0.0.1:5000`.

### Local

```bash
# 1. Instalar dependências
pip install -r requirements.txt
python download_nltk_data.py

# 2. Banco de dados
flask db upgrade

# 3. Terminal 1 — Celery worker (requer Redis rodando na porta 6379)
celery -A celery_worker.celery_app worker --loglevel=info

# 4. Terminal 2 — Flask
python run.py
```

**Variáveis de ambiente necessárias:**
- `DATABASE_URL` — string de conexão PostgreSQL (ex: `postgresql://user:pass@host/db`)
- `FLASK_SECRET_KEY` — chave secreta do Flask (opcional, tem default)

## Estrutura

```
run.py                   — entrypoint Flask
config.py                — lista de keywords monitoradas e configurações
celery_worker.py         — definição do app Celery
project/
  __init__.py            — application factory (create_app)
  models.py              — modelos SQLAlchemy (SentimentResult, etc.)
  main/                  — blueprint de UI (rota /)
  api/                   — blueprint de API REST (/api/scan, /api/history)
  templates/index.html   — template Jinja2
  static/
    style.css            — estilos
    script.js            — lógica do frontend (Chart.js, word cloud, polling)
migrations/              — scripts Flask-Migrate
```

## API

| Endpoint | Método | Descrição |
|---|---|---|
| `/api/scan` | POST | Dispara novo scan (assíncrono via Celery) |
| `/api/scan/<task_id>` | GET | Consulta status/resultado do scan |
| `/api/history` | GET | Retorna histórico dos últimos 7 dias |

## Keywords monitoradas

Definidas em `config.py`. Exemplos: "Crude Oil Price", "Offshore Wind Energy", etc.

## Adicionar keyword

Editar a lista em `config.py` e reiniciar a aplicação.
