import React from "react";
import { useParams } from "react-router-dom";
import { billsData } from "../api/Bills";
import "../styles/BillDetail.css";
import { motion } from "framer-motion";

function BillDetail() {
  const { id } = useParams();
  const bill = billsData.find((b) => b.id === parseInt(id));

  if (!bill) {
    return <p>Bill not found.</p>;
  }

  const stages = ["Introduced", "Passed House", "Passed Senate", "Became Law"];
  const currentStageIndex = stages.indexOf(bill.stage);

  return (
    <main className="bill-detail">
      <motion.h2
        className="bill-title"
        initial={{ y: -30, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.7 }}
      >
        {bill.title}
      </motion.h2>

      <motion.div
        className={`sentiment-box ${bill.sentiment.toLowerCase()}`}
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <p>Effect: {bill.sentiment}</p>
        {bill.sentiment === "Positive" && <span>😊</span>}
        {bill.sentiment === "Neutral" && <span>😐</span>}
        {bill.sentiment === "Negative" && <span>😡</span>}
      </motion.div>

      <motion.section
        className="justification"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        <h3>Justification</h3>
        <p>{bill.justification || "GPT analysis will appear here."}</p>
      </motion.section>

      <section className="confidence-score">
        <h3>Confidence Score: {(bill.confidence * 100).toFixed(0)}%</h3>
        <motion.div
          className="progress-bar"
          initial={{ width: 0 }}
          animate={{ width: "100%" }}
          transition={{ duration: 1 }}
        >
          <div
            className="progress-fill"
            style={{ width: `${(bill.confidence * 100).toFixed(0)}%` }}
          ></div>
        </motion.div>
      </section>

      <motion.section
        className="sector"
        initial={{ x: -30, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ delay: 0.8 }}
      >
        <h3>Sector</h3>
        <p>{bill.sector}</p>
      </motion.section>

      <motion.section
        className="stage-progress"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
      >
        <h3>Bill Progress</h3>
        <div className="progress-container">
          {stages.map((stage, index) => (
            <div
              key={index}
              className={`progress-step ${
                index === currentStageIndex
                  ? "current-stage"
                  : index < currentStageIndex
                  ? "completed-stage"
                  : "pending-stage"
              }`}
            >
              <div className="circle">{index + 1}</div>
              <p>{stage}</p>
            </div>
          ))}
        </div>
      </motion.section>
    </main>
  );
}

export default BillDetail;
