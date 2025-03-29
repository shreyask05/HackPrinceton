import React from 'react';
import './FeatureCards.css';

function FeatureCards() {
  return (
    <section className="features">
      <div className="feature-card">
        <h3>Real-Time Bill Tracking</h3>
        <p>We analyze prioritized bills in committees in real time.</p>
      </div>
      <div className="feature-card">
        <h3>Sector-Based Predictions</h3>
        <p>See how upcoming laws will impact different stock market sectors.</p>
      </div>
      <div className="feature-card">
        <h3>Investor-Friendly Summaries</h3>
        <p>Summaries that even non-policy experts can understand.</p>
      </div>
    </section>
  );
}

export default FeatureCards;
