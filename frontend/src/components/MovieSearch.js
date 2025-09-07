import React, { useState } from 'react';
import axios from 'axios';

const MovieSearch = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const searchMovies = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.get(`/api/movies/search?q=${encodeURIComponent(query)}`);
      setResults(response.data);
    } catch (error) {
      console.error('Error searching movies:', error);
      // Fallback data for demo
      setResults([
        {
          id: 1,
          title: 'Inception',
          release_date: '2010-07-16',
          overview: 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
          vote_average: 8.4
        },
        {
          id: 2,
          title: 'The Dark Knight',
          release_date: '2008-07-18',
          overview: 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
          vote_average: 9.0
        }
      ]);
    }
    setLoading(false);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    searchMovies();
  };

  return (
    <div className="movie-search">
      <h1>Search Movies</h1>
      
      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for movies..."
          className="search-input"
        />
        <button type="submit" disabled={loading} className="search-btn">
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {loading ? (
        <div className="loading">Searching movies...</div>
      ) : results.length > 0 ? (
        <div className="search-results">
          <h2>Search Results</h2>
          <div className="results-grid">
            {results.map(movie => (
              <div key={movie.id} className="movie-card">
                <div className="movie-poster">
                  <div className="poster-placeholder">
                    {movie.title.charAt(0)}
                  </div>
                </div>
                <div className="movie-info">
                  <h3>{movie.title}</h3>
                  <p className="movie-year">{movie.release_date?.substring(0, 4) || 'Unknown year'}</p>
                  <p className="movie-overview">
                    {movie.overview?.substring(0, 150)}...
                  </p>
                  <div className="movie-rating">
                    ⭐ {movie.vote_average || 'N/A'}/10
                  </div>
                  <button className="view-details-btn">View Details</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : query ? (
        <p>No results found for "{query}"</p>
      ) : null}
    </div>
  );
};

export default MovieSearch;