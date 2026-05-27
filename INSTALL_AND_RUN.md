# Installation and Running Guide

This guide provides two methods for running the Energy Horizon Scanner application. The recommended method is using Docker, as it automatically handles all dependencies and services.

---

## Method 1: Running with Docker (Recommended)

This method uses Docker and Docker Compose to build the application and run all its components (web server, background worker, and Redis) in isolated containers.

### 1. Prerequisites

-   **Docker**: Install Docker Desktop from the official [Docker website](https://www.docker.com/products/docker-desktop/).

### 2. Running the Application

1.  **Clone the Repository (if you haven't already)**
    If you are using Git, clone the repository and navigate into the directory:
    ```bash
    git clone <repository-url>
    cd scanner
    ```

2.  **Build and Run with Docker Compose**
    Open a terminal in the project's root directory (the one containing `docker-compose.yml`) and run the following command:
    ```bash
    docker-compose up --build
    ```
    This command will:
    -   Build the Docker image for the application, installing all Python and NLP dependencies.
    -   Start the Flask web server, the Celery background worker, and the Redis service.
    -   Apply any pending database migrations.

### 3. Accessing the Application

Once the containers are running, you can access the Energy Horizon Scanner in your web browser at:

**http://127.0.0.1:5000**

To stop the application, press `Ctrl+C` in the terminal where `docker-compose` is running.

---

## Method 2: Running Locally

This method involves setting up a local Python environment and manually running the required services.

### 1. Prerequisites

-   **Python 3.11+**
-   **Redis**: The application uses Redis as a message broker. Ensure a Redis server is running on its default port (6379).

### 2. Installation Steps

1.  **Clone the Repository** (if applicable)

2.  **Create a Virtual Environment**
    ```bash
    python -m venv .venv
    # Activate it (Windows)
    .venv\\Scripts\\activate
    # Or for macOS/Linux: source .venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download NLP Data**
    ```bash
    python download_nltk_data.py
    ```

5.  **Set up the Database**
    ```bash
    # For Windows
    .venv\\Scripts\\flask db upgrade
    # Or for macOS/Linux: flask db upgrade
    ```

### 3. Running the Application

You need to start two separate processes in two different terminals.

-   **Terminal 1: Start the Celery Worker**
    ```bash
    celery -A celery_worker.celery_app worker --loglevel=info
    ```

-   **Terminal 2: Start the Flask Application**
    ```bash
    python run.py
    ```

### 4. Accessing the Application

Access the application in your web browser at: **http://127.0.0.1:5000**
