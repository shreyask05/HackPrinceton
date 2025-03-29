import React from 'react';
import './BillCard.css';

function BillCard({ title, summary, sector, sentiment, impact }) {
  return (
    <div className="bill-card">
      <h3>{title}</h3>
      <p className="summary">{summary}</p>
      <p><strong>Sector:</strong> {sector}</p>
      <p><strong>Sentiment:</strong> {sentiment}</p>
      <p><strong>Impact:</strong> {impact}</p>
    </div>
  );
}

export default BillCard;
