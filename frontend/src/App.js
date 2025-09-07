import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import Dashboard from './components/Dashboard';
import MovieRecommendations from './components/MovieRecommendations';
import MovieSearch from './components/MovieSearch';
import SentimentAnalysis from './components/SentimentAnalysis';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import './App.css';

// Set base URL for API calls
axios.defaults.baseURL = 'http://localhost:5000';

function App() {
  const [user, setUser] = useState({ id: 1, name: 'Demo User' });
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Load recommendations when app starts
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async (type = 'hybrid') => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/recommendations/${user.id}?type=${type}&n=10`);
      setRecommendations(response.data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      // Fallback data for demo
      setRecommendations([
        {
          id: 1,
          title: 'Inception',
          overview: 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
          vote_average: 8.4
        },
        {
          id: 2,
          title: 'The Dark Knight',
          overview: 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
          vote_average: 9.0
        },
        {
          id: 3,
          title: 'Interstellar',
          overview: 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
          vote_average: 8.6
        }
      ]);
    }
    setLoading(false);
  };

  return (
    <Router>
      <div className="App">
        <Navbar user={user} />
        <div className="main-content">
          <Routes>
            <Route path="/" element={
              <Dashboard 
                user={user} 
                recommendations={recommendations} 
                loading={loading}
                onRefreshRecommendations={fetchRecommendations}
              />
            } />
            <Route path="/recommendations" element={
              <MovieRecommendations 
                recommendations={recommendations} 
                loading={loading}
                onRefreshRecommendations={fetchRecommendations}
              />
            } />
            <Route path="/search" element={<MovieSearch />} />
            <Route path="/sentiment" element={<SentimentAnalysis />} />
          </Routes>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

export default App;