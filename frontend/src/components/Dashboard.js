import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import axios from 'axios';

const Dashboard = ({ user, recommendations, loading, onRefreshRecommendations }) => {
  const [stats, setStats] = useState({
    totalUsers: 1250,
    totalMovies: 5800,
    activeSessions: 342,
    positiveSentiments: 68
  });

  const [popularMovies, setPopularMovies] = useState([]);

  useEffect(() => {
    // Fetch popular movies
    const fetchPopularMovies = async () => {
      try {
        const response = await axios.get('/api/movies/popular');
        setPopularMovies(response.data.slice(0, 5));
      } catch (error) {
        console.error('Error fetching popular movies:', error);
        // Fallback data
        setPopularMovies([
          { title: 'Inception', views: 12500 },
          { title: 'The Dark Knight', views: 11800 },
          { title: 'Interstellar', views: 9800 },
          { title: 'The Shawshank Redemption', views: 9200 },
          { title: 'Pulp Fiction', views: 8700 }
        ]);
      }
    };

    fetchPopularMovies();
  }, []);

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Movie Recommender Dashboard</h1>
        <button 
          className="refresh-btn"
          onClick={() => onRefreshRecommendations('hybrid')}
          disabled={loading}
        >
          {loading ? 'Refreshing...' : 'Refresh Recommendations'}
        </button>
      </div>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Users</h3>
          <p className="stat-number">{stats.totalUsers}</p>
        </div>
        <div className="stat-card">
          <h3>Movies in Database</h3>
          <p className="stat-number">{stats.totalMovies}</p>
        </div>
        <div className="stat-card">
          <h3>Active Sessions</h3>
          <p className="stat-number">{stats.activeSessions}</p>
        </div>
        <div className="stat-card">
          <h3>Positive Sentiments</h3>
          <p className="stat-number">{stats.positiveSentiments}%</p>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="recommendations-preview">
          <h2>Your Recommendations</h2>
          {loading ? (
            <div className="loading">Loading recommendations...</div>
          ) : recommendations.length > 0 ? (
            <div className="recommendations-list">
              {recommendations.slice(0, 5).map(movie => (
                <div key={movie.id || movie.movie_id} className="movie-preview">
                  <h4>{movie.title}</h4>
                  <p>{movie.overview?.substring(0, 100)}...</p>
                </div>
              ))}
            </div>
          ) : (
            <p>No recommendations yet. Rate some movies to get personalized recommendations!</p>
          )}
        </div>

        <div className="popular-movies">
          <h2>Most Popular Movies</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={popularMovies}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="title" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="views" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;