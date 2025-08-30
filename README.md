Project Title:
AI-Powered Movie Recommendation System with Sentiment Analysis

Project Description:
Developed a comprehensive AI-driven movie recommendation system that combines content-based filtering, collaborative filtering, and advanced sentiment analysis to provide personalised movie suggestions. The system features a responsive web interface with real-time analytics and integrates multiple data sources, including TMDB API and IMDB web scraping.

Technical Stack:
Frontend: React.js, Recharts, Axios, CSS3
Backend: Python, Flask, RESTful APIs
Database: MongoDB with PyMongo
Machine Learning: Scikit-learn, Surprise (SVD), TextBlob, Custom Sentiment Analysis Model
APIs & Web Services: TMDB API, YouTube API, Custom Web Scraping

Key Features & Responsibilities:
Engineered a hybrid recommendation algorithm combining content-based filtering (TF-IDF, cosine similarity) and collaborative filtering (SVD matrix factorisation).
Implemented sentiment analysis pipeline using machine learning (Naive Bayes classifier) trained on IMDB dataset to analyse YouTube movie reviews.
Developed a web scraping module using BeautifulSoup to extract and process movie reviews from IMDB.
Designed and built a RESTful API with Flask, handling user management, movie data, recommendations, and sentiment analysis.
Created an interactive dashboard with React featuring data visualisations of recommendation metrics and sentiment analysis results.
Integrated TMDB API for comprehensive movie metadata, including cast, crew, ratings, and descriptions.
Implemented a user rating system and preference tracking to improve recommendation accuracy continuously.
Optimised MongoDB database schema for efficient querying of user preferences, movie data, and recommendation history.

Technical Highlights:
Content-Based Filtering: Used TF-IDF vectorisation and cosine similarity on movie metadata
Collaborative Filtering: Implemented Singular Value Decomposition (SVD) for user-item matrix factorisation
Hybrid Approach: Combined both methods with weighted scoring for optimal recommendations
Sentiment Analysis: Custom ML model trained on IMDB dataset with TextBlob fallback
Web Scraping: Robust IMDB review extraction with error handling and rate limiting
Data Visualisation: Interactive charts showing recommendation metrics and sentiment distribution
