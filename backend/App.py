from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.json_util import dumps
import os
from dotenv import load_dotenv
import json
from datetime import datetime 

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB configuration
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/movie_recommender")
mongo = PyMongo(app)

# Import recommendation engine and sentiment analysis
from Recommendation_Engine import RecommendationEngine
from Sentiment_Analysis import SentimentAnalyzer
from imdb_scrapper import IMDBScraper

# Initialize components
recommendation_engine = RecommendationEngine()
sentiment_analyzer = SentimentAnalyzer()
imdb_scraper = IMDBScraper()

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Movie Recommender API"})

# Get movie recommendations for a user
@app.route('/api/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    try:
        # Get recommendation type from query params
        rec_type = request.args.get('type', 'hybrid')  # hybrid, content, collaborative
        
        # Get number of recommendations
        n_recs = int(request.args.get('n', 10))
        
        # Get recommendations
        if rec_type == 'content':
            recommendations = recommendation_engine.content_based_recommendations(user_id, n_recs)
        elif rec_type == 'collaborative':
            recommendations = recommendation_engine.collaborative_filtering_recommendations(user_id, n_recs)
        else:
            recommendations = recommendation_engine.hybrid_recommendations(user_id, n_recs)
        
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Search for movies
@app.route('/api/movies/search', methods=['GET'])
def search_movies():
    try:
        query = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        
        results = recommendation_engine.search_movies(query, page)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get movie details
@app.route('/api/movies/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    try:
        movie = recommendation_engine.get_movie_details(movie_id)
        return jsonify(movie)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Analyze sentiment for a movie
@app.route('/api/movies/<movie_id>/sentiment', methods=['GET'])
def analyze_sentiment(movie_id):
    try:
        # Get movie title for scraping
        movie = recommendation_engine.get_movie_details(movie_id)
        movie_title = movie.get('title')
        
        # Scrape IMDB reviews
        reviews = imdb_scraper.get_movie_reviews(movie_title)
        
        # Analyze sentiment
        sentiment_results = sentiment_analyzer.analyze_reviews(reviews)
        
        return jsonify({
            "movie_id": movie_id,
            "movie_title": movie_title,
            "sentiment": sentiment_results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rate a movie
@app.route('/api/ratings', methods=['POST'])
def add_rating():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        movie_id = data.get('movie_id')
        rating = data.get('rating')
        
        # Store rating in database
        rating_data = {
            "user_id": user_id,
            "movie_id": movie_id,
            "rating": rating,
            "timestamp": datetime.now()
        }
        
        result = mongo.db.ratings.insert_one(rating_data)
        
        return jsonify({
            "message": "Rating added successfully",
            "rating_id": str(result.inserted_id)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get user ratings
@app.route('/api/users/<user_id>/ratings', methods=['GET'])
def get_user_ratings(user_id):
    try:
        ratings = list(mongo.db.ratings.find({"user_id": user_id}))
        
        # Convert ObjectId to string
        for rating in ratings:
            rating['_id'] = str(rating['_id'])
        
        return jsonify(ratings)
        
        return dumps(ratings)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)