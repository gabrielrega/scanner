# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
# (Add any your project may need, e.g., build-essential for C extensions)
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Copy the requirements file
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Download NLTK data
RUN python download_nltk_data.py

# The command to run the app will be specified in the docker-compose.yml
