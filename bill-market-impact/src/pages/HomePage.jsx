import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Home.css";

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <main className="home-container">
      <section className="home-content">
        <h1 className="home-title">BillPulse AI</h1>
        <p className="home-subtitle">Predict & Track Congressional Bills' Market Impact</p>
        <p className="home-description">
          Stay informed with real-time predictions on how new U.S. bills could affect the stock market.
        </p>
        <button className="explore-button" onClick={() => navigate("/explore")}>
          Explore Bills
        </button>
      </section>
    </main>
  );
};

export default HomePage;
