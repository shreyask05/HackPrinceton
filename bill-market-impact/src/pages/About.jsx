import React from "react";
import "../styles/About.css";

function About() {
  return (
    <main className="about-main">
      <div className="about-content">
        <h2>About Bill Market Tracker</h2>
        <p>
          This project predicts how upcoming congressional bills will impact different sectors in the stock market. 
          We use AI models to analyze bills and provide real-time sentiment analysis so that investors can stay informed.
        </p>
      </div>
    </main>
  );
}

export default About;
