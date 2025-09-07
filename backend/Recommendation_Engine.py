import pandas as pd
import numpy as np
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import MinMaxScaler
import tmdbsimple as tmdb
import os
from datetime import datetime
import joblib

class RecommendationEngine:
    def __init__(self):
        # Set TMDB API key
        tmdb.API_KEY = os.getenv('TMDB_API_KEY')
        
        # Load or create movie dataset
        self.movies_df = self._load_movie_data()
        
        # Initialize TF-IDF Vectorizer
        self.tfidf = TfidfVectorizer(stop_words='english')
        
        # Prepare content-based features
        self._prepare_content_based_features()
        
        # Load or train collaborative filtering model
        self.cf_model = self._load_collaborative_model()
    
    def _load_movie_data(self):
        # In a real application, this would load from MongoDB
        # For demo purposes, we'll create a sample dataset
        movies = [
            {'movie_id': 1, 'title': 'The Shawshank Redemption', 'genres': 'Drama', 'overview': 'Two imprisoned men bond over a number of years...'},
            {'movie_id': 2, 'title': 'The Godfather', 'genres': 'Crime, Drama', 'overview': 'The aging patriarch of an organized crime dynasty...'},
            {'movie_id': 3, 'title': 'The Dark Knight', 'genres': 'Action, Crime, Drama', 'overview': 'When the menace known as the Joker wreaks havoc...'},
            # Add more movies as needed
        ]
        
        return pd.DataFrame(movies)
    
    def _prepare_content_based_features(self):
        # Fill NaN values
        self.movies_df['overview'] = self.movies_df['overview'].fillna('')
        
        # Create content matrix
        self.movies_df['content'] = self.movies_df['overview'] + ' ' + self.movies_df['genres']
        
        # Compute TF-IDF matrix
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies_df['content'])
        
        # Compute cosine similarity matrix
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)
        
        # Create mapping between movie title and index
        self.indices = pd.Series(self.movies_df.index, index=self.movies_df['title']).drop_duplicates()
    
    def _load_collaborative_model(self):
        # In a real application, this would load from a trained model file
        # For demo, we'll create a simple model
        
        # Sample ratings data
        ratings_dict = {
            'item_id': [1, 1, 2, 2, 3, 3],
            'user_id': [1, 2, 1, 3, 2, 3],
            'rating': [5, 4, 4, 5, 3, 4]
        }
        
        df = pd.DataFrame(ratings_dict)
        
        # Define reader
        reader = Reader(rating_scale=(1, 5))
        
        # Load dataset
        data = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)
        
        # Train test split
        trainset, testset = train_test_split(data, test_size=0.2)
        
        # Train model
        model = SVD()
        model.fit(trainset)
        
        return model
    
    def content_based_recommendations(self, user_id, n=10):
        # Get user's rated movies
        user_ratings = self._get_user_ratings(user_id)
        
        if not user_ratings:
            # Return popular movies if no ratings
            return self._get_popular_movies(n)
        
        # Calculate weighted average of similar movies
        sim_scores = np.zeros(len(self.movies_df))
        
        for movie_id, rating in user_ratings:
            if movie_id in self.indices:
                idx = self.indices[movie_id]
                sim_scores += rating * self.cosine_sim[idx]
        
        # Get top N recommendations
        movie_indices = sim_scores.argsort()[::-1][:n]
        
        # Return recommendations
        return self.movies_df.iloc[movie_indices].to_dict('records')
    
    def collaborative_filtering_recommendations(self, user_id, n=10):
        # Get all movie IDs
        all_movie_ids = self.movies_df['movie_id'].tolist()
        
        # Predict ratings for all movies
        predictions = []
        for movie_id in all_movie_ids:
            pred = self.cf_model.predict(user_id, movie_id)
            predictions.append((movie_id, pred.est))
        
        # Sort by predicted rating
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        # Get top N recommendations
        top_movie_ids = [x[0] for x in predictions[:n]]
        
        # Return movie details
        return self.movies_df[self.movies_df['movie_id'].isin(top_movie_ids)].to_dict('records')
    
    def hybrid_recommendations(self, user_id, n=10):
        # Get content-based recommendations
        cb_recs = self.content_based_recommendations(user_id, n*2)
        
        # Get collaborative filtering recommendations
        cf_recs = self.collaborative_filtering_recommendations(user_id, n*2)
        
        # Combine and rank
        all_recs = {}
        
        for rec in cb_recs:
            movie_id = rec['movie_id']
            if movie_id not in all_recs:
                all_recs[movie_id] = {'movie': rec, 'score': 0}
            all_recs[movie_id]['score'] += 0.5  # Weight for content-based
        
        for rec in cf_recs:
            movie_id = rec['movie_id']
            if movie_id not in all_recs:
                all_recs[movie_id] = {'movie': rec, 'score': 0}
            all_recs[movie_id]['score'] += 0.5  # Weight for collaborative
        
        # Sort by combined score
        sorted_recs = sorted(all_recs.values(), key=lambda x: x['score'], reverse=True)
        
        # Return top N
        return [rec['movie'] for rec in sorted_recs[:n]]
    
    def search_movies(self, query, page=1):
        # Use TMDB API to search movies
        search = tmdb.Search()
        search.movie(query=query, page=page)
        
        return search.results
    
    def get_movie_details(self, movie_id):
        # Use TMDB API to get movie details
        movie = tmdb.Movies(movie_id)
        response = movie.info()
        
        # Add credits information
        response['credits'] = movie.credits()
        
        return response
    
    def _get_user_ratings(self, user_id):
        # In a real application, this would query the database
        # For demo, return sample ratings
        user_ratings = {
            1: [(1, 5), (2, 4)],
            2: [(1, 4), (3, 3)],
            3: [(2, 5), (3, 4)]
        }
        
        return user_ratings.get(user_id, [])
    
    def _get_popular_movies(self, n=10):
        # Get popular movies from TMDB
        movie = tmdb.Movies()
        popular = movie.popular(page=1)
        
        return popular['results'][:n]