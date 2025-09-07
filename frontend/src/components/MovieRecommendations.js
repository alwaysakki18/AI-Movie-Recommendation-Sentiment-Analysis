import React, { useState } from 'react';

const MovieRecommendations = ({ recommendations, loading, onRefreshRecommendations }) => {
  const [recommendationType, setRecommendationType] = useState('hybrid');

  const handleTypeChange = (type) => {
    setRecommendationType(type);
    onRefreshRecommendations(type);
  };

  return (
    <div className="movie-recommendations">
      <div className="recommendations-header">
        <h1>AI-Powered Movie Recommendations</h1>
        <p className="subtitle">Our advanced algorithm analyzes your preferences to suggest movies you'll love</p>
        
        <div className="recommendation-types">
          <button 
            className={recommendationType === 'hybrid' ? 'active' : ''}
            onClick={() => handleTypeChange('hybrid')}
          >
            Hybrid Recommendations
          </button>
          <button 
            className={recommendationType === 'content' ? 'active' : ''}
            onClick={() => handleTypeChange('content')}
          >
            Content-Based
          </button>
          <button 
            className={recommendationType === 'collaborative' ? 'active' : ''}
            onClick={() => handleTypeChange('collaborative')}
          >
            Collaborative Filtering
          </button>
        </div>
      </div>

      {loading ? (
        <div className="loading">Loading recommendations...</div>
      ) : recommendations.length > 0 ? (
        <div className="recommendations-grid">
          {recommendations.map(movie => (
            <div key={movie.id || movie.movie_id} className="movie-card">
              <div className="movie-poster">
                <div className="poster-placeholder">
                  {movie.title?.charAt(0) || 'M'}
                </div>
              </div>
              <div className="movie-info">
                <h3>{movie.title}</h3>
                <p className="movie-year">{movie.release_date?.substring(0, 4) || 'Unknown year'}</p>
                <p className="movie-overview">
                  {movie.overview?.substring(0, 150) || 'No description available'}...
                </p>
                <div className="movie-rating">
                  ⭐ {movie.vote_average || 'N/A'}/10
                </div>
                <button className="view-details-btn">View Details</button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-recommendations">
          <p>No recommendations available. Try rating some movies first!</p>
        </div>
      )}
    </div>
  );
};

export default MovieRecommendations;