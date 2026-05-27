# GEMINI.md: Project Context

This document provides a comprehensive overview of the "Energy Horizon Scanner" project to guide future development and interaction.

## Project Overview

This project is a Python-based web application designed to monitor and analyze sentiment in news articles related to the energy sector.

- **Purpose**: To provide a real-time dashboard that tracks sentiment trends for specific energy-related keywords (e.g., "Crude Oil Price", "Offshore Wind Energy").
- **Backend**: The backend is built with **Flask**, a Python web framework. It serves a REST API to the frontend and handles the core logic.
- **Data Persistence**: **SQLAlchemy** is used as the ORM to interact with a SQL database (configured via the `DATABASE_URL` environment variable). It stores historical sentiment data and scanned articles.
- **Core Logic**:
    - The application fetches news articles from the Google News RSS feed using the `feedparser` library.
    - It performs sentiment analysis on article headlines and summaries using `textblob`.
    - It aggregates sentiment scores and saves them to the database for historical trend analysis.
- **Frontend**: The frontend is built with vanilla **HTML**, **CSS**, and **JavaScript**.
    - It provides a user interface with two main tabs: a "Live Scanner" and "Historical Trends".
    - It uses **Chart.js** to visualize sentiment data, including bar charts for current sentiment and line charts for historical trends.
    - It also generates a "Key Topics Cloud" from the headlines of the scanned articles.

## Building and Running the Project

### 1. Installation

The project's Python dependencies are listed in `requirements.txt`. You will need Python 3.11+ installed.

**Step 1: Install Python Packages**

First, ensure you have `uv` or `pip` installed. Then, install the required packages:

```bash
# Using uv (recommended, based on uv.lock)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

**Step 2: Download NLP Data**

The application uses the NLTK library for natural language processing. Run the following script to download the necessary data corpora (stopwords, wordnet, etc.):

```bash
python download_nltk_data.py
```

### 2. Database Setup

The application uses Flask-Migrate to manage the database schema. After the initial setup, run the following command to apply the migrations:

```bash
flask db upgrade
```

### 2. Configuration

The application requires the following environment variables to be set:

- `DATABASE_URL`: The connection string for the PostgreSQL database (e.g., `postgresql://user:password@host:port/dbname`).
- `FLASK_SECRET_KEY` (Optional): A secret key for Flask sessions. Defaults to a placeholder if not set.

You can set these in your shell before running the application:

```bash
export DATABASE_URL="your_database_connection_string"
export FLASK_SECRET_KEY="a-very-secret-key"
```

### 3. Running the Application

**For Development:**

To run the application, you need two terminals.

**Terminal 1: Start the Celery Worker**

This application uses Celery for asynchronous task processing, which requires a running Redis server. Ensure Redis is installed and running on its default port. Then, start the Celery worker:

```bash
# Activate the virtual environment
.venv/Scripts/activate

# Start the worker
celery -A celery_worker.celery_app worker --loglevel=info
```

**Terminal 2: Start the Flask Application**

Once the Celery worker is running, start the Flask development server:

```bash
# Activate the virtual environment
.venv/Scripts/activate

# Run the app
python run.py
```

The application will be available at `http://0.0.0.0:5000`.

**For Production:**

The project is configured to be run with a production-grade WSGI server like Gunicorn. You will also need a production-ready way to run the Celery worker, such as using a process manager like `supervisor`.

```bash
# Run the web server
gunicorn "project:create_app()"

# Run the Celery worker (in a separate process)
celery -A celery_worker.celery_app worker --loglevel=info
```


## Development Conventions

- **Project Structure**: The project follows a modular structure using an application factory pattern.
    - `run.py`: The main entry point to start the application.
    - `config.py`: Contains application configuration, such as the list of search terms.
    - `project/`: The main application package.
        - `__init__.py`: The application factory (`create_app`) where the app is configured and blueprints are registered.
        - `models.py`: Defines the SQLAlchemy database models.
        - `main/`: A blueprint for the core UI routes.
        - `api/`: A blueprint for the backend API routes.
        - `templates/`: Contains the `index.html` Jinja2 template.
        - `static/`: Contains the frontend CSS (`style.css`) and JavaScript (`script.js`).
- **API Endpoints**: The backend exposes a simple REST API under the `/api/` prefix for the frontend to consume (e.g., `/api/scan`, `/api/history`).
- **Styling**: The project uses a custom stylesheet located at `project/static/style.css`.
- **Database**: The database schema is defined in `project/models.py`. The database file (`scanner.db`) is created in the `instance` folder at the project root.
