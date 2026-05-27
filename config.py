import os

# Flask secret key, loaded from environment variable or a default value
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or "energy-scanner-secret-key"

# List of keywords to scan for in the news
SEARCH_TERMS = [
    "Crude Oil Price",
    "OPEC+",
    "Offshore Wind Energy",
    "Carbon Capture",
    "Geopolitics Energy Middle East",
    "Petrobras"
]
# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
