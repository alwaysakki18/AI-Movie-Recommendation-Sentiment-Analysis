import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ user }) => {
  return (
    <nav className="navbar">
      <h1>AI Movie Recommendation & Sentiment Analysis</h1>
      <div className="nav-links">
        <Link to="/">Dashboard</Link>
        <Link to="/recommendations">Recommendations</Link>
        <Link to="/search">Search</Link>
        <span>Welcome, {user.name}</span>
      </div>
    </nav>
  );
};

export default Navbar;