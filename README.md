📊 YouTube Sentiment & Engagement Analyzer
An end-to-end data analysis web application that fetches real-time YouTube data, performs sentiment analysis on comments, and visualizes audience engagement.

🚀 Key Features
Real-time Data Ingestion: Uses YouTube Data API v3 to fetch the latest videos based on user search queries.

Sentiment Analysis: Analyzes audience mood (Positive, Negative, Neutral) using TextBlob (NLP) on the top 50-100 comments per video.

Engagement Metrics: Calculates custom metrics like Like-to-View ratio to measure video quality beyond just view counts.

Interactive Dashboard: Built with Streamlit for a seamless user experience.

Data Visualization: Uses Plotly to create interactive scatter plots comparing Views vs. Public Sentiment.

🛠️ Tech Stack
Language: Python

Framework: Streamlit

Data Handling: Pandas, NumPy

Natural Language Processing: TextBlob

Visualization: Plotly, Seaborn, Matplotlib

API: Google API Client Library

📋 Project Setup (Local)
Clone the repository:

Bash
git clone https://github.com/your-username/youtube-sentiment-analyzer.git
Install dependencies:

Bash
pip install -r requirements.txt
Run the application:

Bash
streamlit run app.py
💡 How It Works
The user enters a search topic in the sidebar.

The app calls the YouTube Search API to retrieve video metadata.

For each video, a secondary API call fetches the statistics (likes, views) and comment threads.

The NLP engine processes the comments to generate a Sentiment Score.

A final consolidated report and interactive bubble chart are displayed to the user.

🛡️ Security & Secrets
This project follows best practices by using Streamlit Secrets Management. The API_KEY is never hardcoded in the source code, ensuring that sensitive credentials are protected during deployment.
