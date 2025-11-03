import React, { useState, useEffect } from 'react';

const HomePage = () => {
  const [status, setStatus] = useState('loading');
  
  useEffect(() => {
    // Check API health
    fetch('/health')
      .then(res => res.json())
      .then(data => setStatus('connected'))
      .catch(err => setStatus('error'));
  }, []);
  
  return (
    <div className="home-page">
      <h2>Welcome to ToySoldiers</h2>
      <div className="status">
        API Status: <span className={`status-${status}`}>{status}</span>
      </div>
      <div className="features">
        <h3>Features (Generated from YAML)</h3>
        <ul>
          <li>✅ FastAPI Backend</li>
          <li>✅ React Frontend</li>
          <li>✅ Database Models</li>
          <li>✅ API Endpoints</li>
        </ul>
      </div>
    </div>
  );
};

export default HomePage;
