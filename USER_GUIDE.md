# Energy Horizon Scanner - User Guide

Welcome to the Energy Horizon Scanner! This guide will walk you through the features of the application and how to use them to monitor and analyze sentiment in energy-sector news.

## 1. Introduction

The Energy Horizon Scanner is a dashboard designed to give you a real-time view of news sentiment for key topics in the energy industry. It automatically scans news sources for a predefined list of keywords (like "Crude Oil Price," "Offshore Wind Energy," etc.) and analyzes the tone of each article.

This helps you quickly understand the prevailing sentiment—positive, negative, or neutral—for important topics and track how these trends evolve over time.

## 2. The Interface

The application has two main sections, accessible via tabs at the top of the page:

-   **Live Scanner**: This is where you can initiate a new, real-time scan of news sources.
-   **Historical Trends**: This is where you can view aggregated data and trends from all scans performed over the last 7 days.

---

## 3. Using the Live Scanner

The Live Scanner tab is the default view and allows you to get an up-to-the-minute sentiment analysis.

### How to Start a Scan

1.  Click the **"Start Scan"** button at the top left.
2.  The scan will begin in the background. You can monitor its progress via the status message next to the button (e.g., "Initializing scan...", "Processing...", "X articles scanned...").
3.  Because the scan runs asynchronously, you can continue to interact with the application while it's in progress.

### Understanding the Results

Once the scan is complete, three new sections will appear with the results:

#### a. Sentiment Overview

This section shows a high-level summary of the sentiment for each keyword. Each topic has a card displaying:
-   **Sentiment Score**: A number between -1.0 (very negative) and +1.0 (very positive). Scores near 0 are neutral.
-   **Color Coding**: The score is color-coded for quick interpretation:
    -   **Green**: Positive sentiment
    -   **Yellow**: Neutral sentiment
    -   **Red**: Negative sentiment
-   **Article Count**: The number of articles found and analyzed for that keyword.

#### b. Key Topics Cloud

This is a word cloud generated from the headlines of all scanned articles. **The larger a word appears, the more frequently it was mentioned**, helping you identify key topics and buzzwords at a glance.

#### c. Latest Headlines

This section displays a grid of the individual news articles that were analyzed. Each article card shows:
-   The keyword it was found under.
-   The headline, which is a clickable link to the original article.
-   The source of the article (e.g., "Reuters", "Bloomberg").
-   The sentiment label ("Positive", "Neutral", "Negative") and its score.

You can **filter the articles** using the dropdown menus at the top of this section to narrow down the view by a specific **topic** or **sentiment**.

---

## 4. Viewing Historical Trends

Click the **"Historical Trends"** tab to see how sentiment has evolved over time. This data is automatically saved from every scan you perform.

### a. Scan Statistics

This provides a quick summary of the historical data collected:
-   **Total Scans**: The total number of scans recorded in the database.
-   **Overall Avg Sentiment**: The average sentiment score across all keywords and all scans.
-   **Topics Tracked**: The number of unique keywords being monitored.

### b. Sentiment Trends Over Time

This is an interactive line chart that plots the average sentiment score for each keyword over the last 7 days.
-   **Hover over a point** on the chart to see the exact sentiment score for a specific scan time.
-   **Click on a keyword in the legend** at the top to toggle its visibility on the chart, allowing you to focus on the topics you care about most.

This chart is invaluable for identifying shifts in news sentiment in response to real-world events.
