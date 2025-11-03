import React, { useState, useEffect } from 'react';

const Dashboard = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Fetch data from API
    const fetchData = async () => {
      try {
        // This would connect to actual API endpoints from YAML
        setData([
          { id: 1, name: 'Sample Data 1', status: 'active' },
          { id: 2, name: 'Sample Data 2', status: 'pending' }
        ]);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);
  
  if (loading) return <div>Loading...</div>;
  
  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <div className="data-grid">
        {data.map(item => (
          <div key={item.id} className="data-card">
            <h3>{item.name}</h3>
            <p>Status: {item.status}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
