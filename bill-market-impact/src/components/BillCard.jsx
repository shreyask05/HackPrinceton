import React from "react";
import { Link } from "react-router-dom";
import "../components/BillCard.css";

function BillCard({ id, title, summary, sector, sentiment, impact }) {
  return (
    <div className="bill-card">
      <h3>{title}</h3>
      <p>{summary}</p>
      <p><strong>Sector:</strong> {sector}</p>
      <p><strong>Sentiment:</strong> {sentiment}</p>
      <p><strong>Impact:</strong> {impact}</p>
      <Link to={`/bill/${id}`} className="detail-button">
        View Details
      </Link>
    </div>
  );
}

export default BillCard;
