from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
import os

class SentimentAnalyzer:
    def __init__(self):
        self.model = self._load_model()
    
    def _load_model(self):
        # Try to load pre-trained model
        model_path = os.path.join('models', 'sentiment_model.pkl')
        
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            # Train a simple model (in real app, use a proper dataset)
            return self._train_default_model()
    
    def _train_default_model(self):
        # Sample training data (in real app, use IMDB dataset)
        texts = [
            "This movie is great", "Awesome film", "I loved it",
            "Terrible movie", "Boring film", "Waste of time",
            "It was okay", "Not bad", "Average movie"
        ]
        
        labels = [1, 1, 1, 0, 0, 0, 2, 2, 2]  # 1=positive, 0=negative, 2=neutral
        
        # Create and train model
        model = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', MultinomialNB())
        ])
        
        model.fit(texts, labels)
        
        # Save model
        os.makedirs('models', exist_ok=True)
        joblib.dump(model, os.path.join('models', 'sentiment_model.pkl'))
        
        return model
    
    def analyze_reviews(self, reviews):
        if not reviews:
            return {"positive": 0, "negative": 0, "neutral": 0, "average_score": 0}
        
        # Predict sentiment for each review
        predictions = self.model.predict(reviews)
        
        # Count sentiments
        positive = sum(1 for p in predictions if p == 1)
        negative = sum(1 for p in predictions if p == 0)
        neutral = sum(1 for p in predictions if p == 2)
        
        # Calculate average sentiment score using TextBlob as fallback
        scores = [TextBlob(review).sentiment.polarity for review in reviews]
        average_score = sum(scores) / len(scores) if scores else 0
        
        return {
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "average_score": average_score,
            "total_reviews": len(reviews)
        }