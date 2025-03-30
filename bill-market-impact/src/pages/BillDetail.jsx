import React, { useEffect, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import "../styles/BillDetail.css";

const stageLabels = ["Introduced", "Passed House", "Passed Senate", "Enacted"];

const BillDetail = () => {
  const { billId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();

  // If bill data is passed via navigation state, use it instead of fetching
  const [bill, setBill] = useState(location.state?.bill || null);
  const [loading, setLoading] = useState(!bill); // Skip loading if data is already passed
  const [confidenceWidth, setConfidenceWidth] = useState(0);

  useEffect(() => {
    console.log("Extracted billId:", billId);

    // If bill data already exists (from navigation state), no need to fetch
    if (bill) {
      setLoading(false);
      setTimeout(() => {
        setConfidenceWidth(bill.confidence_score);
      }, 300);
      return;
    }

    // Ensure billId is defined before making the request
    if (!billId) {
      console.error("No billId provided in URL.");
      return;
    }

    // Fetch bill details from API
    const fetchBillDetails = async () => {
      try {
        console.log("Fetching bill details for ID:", billId);
        const response = await axios.get(`http://localhost:8000/all_bills/${billId}`);
        console.log("API Response:", response.data);

        if (response.data) {
          setBill(response.data);
          setTimeout(() => {
            setConfidenceWidth(response.data.confidence_score);
          }, 300);
        } else {
          console.log("No bill data found in response.");
          setBill(null);
        }
      } catch (error) {
        console.error("Error fetching bill details:", error);
        setBill(null);
      } finally {
        setLoading(false);
      }
    };

    fetchBillDetails();
  }, [billId, bill]);

  if (loading) {
    return <div className="bill-detail-container">Loading Bill Details...</div>;
  }

  if (!bill) {
    return (
      <div className="bill-detail-container">
        <p className="error-text">No Bill Data Found.</p>
        <button className="back-button" onClick={() => navigate(-1)}>
          ← Back
        </button>
      </div>
    );
  }

  const currentStageIndex = stageLabels.indexOf(bill.stage);

  return (
    <div className="bill-detail-container">
      <button
        className="back-button fade-slide-up"
        style={{ animationDelay: "0.1s" }}
        onClick={() => navigate(-1)}
      >
        ← Back to Explore Bills
      </button>

      <h1 className="bill-title fade-slide-up" style={{ animationDelay: "0.2s" }}>
        {bill.title}
      </h1>

      <div className="bill-sector fade-slide-up" style={{ animationDelay: "0.3s" }}>
        <strong>Sector:</strong> <span>{bill.sectors?.join(", ") || "N/A"}</span>
      </div>

      <div className="bill-effect fade-slide-up" style={{ animationDelay: "0.4s" }}>
        <strong>Effect:</strong>
        <div className={`effect-block ${bill.effect >= 0 ? "positive" : "negative"}`}>
          {bill.effect}
        </div>
      </div>

      <div className="bill-justification fade-slide-up" style={{ animationDelay: "0.5s" }}>
        <strong>Justification:</strong>
        <p>{bill.justification || "No justification provided."}</p>
      </div>

      <div className="bill-confidence fade-slide-up" style={{ animationDelay: "0.6s" }}>
        <strong>Confidence:</strong>
        <div className="confidence-bar">
          <div className="confidence-fill" style={{ width: `${confidenceWidth}%` }}></div>
        </div>
        <p className="confidence-score">{bill.confidence_score?.toFixed(0) || 0}%</p>
      </div>

      <div className="bill-stage fade-slide-up" style={{ animationDelay: "0.7s" }}>
        <strong>Stage:</strong>
        <div className="stage-progress-container">
          <div className="stage-line-full"></div>
          <div className="stage-progress">
            {stageLabels.map((stage, index) => (
              <div key={index} className="stage-item-horizontal">
                <div className={`stage-circle-horizontal ${index === currentStageIndex ? "current" : ""}`}></div>
                <p>{stage}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bill-companies fade-slide-up" style={{ animationDelay: "0.8s" }}>
        <strong>Affected Companies:</strong>
        <div className="companies-list">
          {bill.companies?.length > 0 ? (
            bill.companies.map((company, index) => (
              <div key={index} className="company-card">
                {company}
              </div>
            ))
          ) : (
            <p>No specific companies listed.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default BillDetail;
