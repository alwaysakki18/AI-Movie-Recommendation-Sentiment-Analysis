import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>Design & Developed By Akshay Pimpale</p>
        <p>AI Movie Recommender System © {new Date().getFullYear()}</p>
      </div>
    </footer>
  );
};

export default Footer;