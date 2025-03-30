import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "../styles/BillDetail.css";

const stageLabels = ["Introduced", "Passed House", "Passed Senate", "Enacted"];

const BillDetail = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const bill = location.state?.bill;
  const [loading, setLoading] = useState(true);
  const [confidenceWidth, setConfidenceWidth] = useState(0);

  useEffect(() => {
    if (bill) {
      setTimeout(() => {
        setLoading(false);
        setTimeout(() => {
          setConfidenceWidth(bill.confidence * 100);
        }, 300); // slight delay for smoothness
      }, 500);
    }
  }, [bill]);

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
      {loading ? (
        <div className="skeleton-loader">Loading Bill Details...</div>
      ) : (
        <>
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
            <strong>Sector:</strong> <span>{bill.sector}</span>
          </div>

          <div className="bill-effect fade-slide-up" style={{ animationDelay: "0.4s" }}>
            <strong>Effect:</strong>
            <div className={`effect-block ${bill.sentiment.toLowerCase()}`}>
              {bill.sentiment}
            </div>
          </div>

          <div className="bill-justification fade-slide-up" style={{ animationDelay: "0.5s" }}>
            <strong>Justification:</strong>
            <p>{bill.justification}</p>
          </div>

          <div className="bill-confidence fade-slide-up" style={{ animationDelay: "0.6s" }}>
            <strong>Confidence:</strong>
            <div className="confidence-bar">
              <div
                className="confidence-fill"
                style={{ width: `${confidenceWidth}%` }}
              ></div>
            </div>
            <p className="confidence-score">{(bill.confidence * 100).toFixed(0)}%</p>
          </div>

          <div className="bill-stage fade-slide-up" style={{ animationDelay: "0.7s" }}>
            <strong>Stage:</strong>
            <div className="stage-progress-container">
              <div className="stage-line-full"></div>
              <div className="stage-progress">
                {stageLabels.map((stage, index) => (
                  <div key={index} className="stage-item-horizontal">
                    <div
                      className={`stage-circle-horizontal ${
                        index === currentStageIndex ? "current" : ""
                      }`}
                    ></div>
                    <p>{stage}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="bill-companies fade-slide-up" style={{ animationDelay: "0.8s" }}>
            <strong>Affected Companies:</strong>
            <div className="companies-list">
              {bill.companies.map((company, index) => (
                <div key={index} className="company-card">
                  {company}
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default BillDetail;
