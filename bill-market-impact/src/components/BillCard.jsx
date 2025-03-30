import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/BillCard.css";

function BillCard({ bill }) {
  const navigate = useNavigate();

  const handleViewDetail = () => {
    navigate(`/bill/${bill.id}`, { state: { bill } });
  };

  return (
    <div className="bill-card fade-in">
      <h3 className="bill-title">{bill.title}</h3>
      <p className="bill-summary">{bill.summary}</p>
      <p className="bill-sector">Sector: {bill.sector}</p>
      <button className="view-detail-button" onClick={handleViewDetail}>
        View Detail
      </button>
    </div>
  );
}

export default BillCard;
