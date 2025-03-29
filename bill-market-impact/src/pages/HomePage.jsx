import React from "react";
import "../styles/Home.css";
import { Link } from "react-router-dom";

function HomePage() {
  return (
    <main className="home-main">
      <section className="hero">
        <h2>Track Upcoming Bills & Their Market Impact</h2>
        <p>Get real-time predictions on how new bills could impact the stock market.</p>
        <Link to="/explore" className="cta-button">Explore Bills</Link>

      </section>
    </main>
  );
}

export default HomePage;
