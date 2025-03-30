import React, { useEffect, useState } from "react";
import BillCard from "../components/BillCard";
import SectorFilter from "../components/SectorFilter";
import StageFilter from "../components/StageFilter";
import "../styles/ExploreBills.css";
import { dummyBills } from "../data/dummyBills";

function ExploreBills() {
  const [bills, setBills] = useState([]);
  const [selectedSector, setSelectedSector] = useState("");
  const [selectedStage, setSelectedStage] = useState("all");

  useEffect(() => {
    setBills(dummyBills);
  }, []);

  const sectors = [...new Set(bills.map((bill) => bill.sector))];

  const filteredBills = bills.filter((bill) => {
    const sectorMatch = selectedSector ? bill.sector === selectedSector : true;
    const stageMatch =
      selectedStage === "all"
        ? true
        : selectedStage === "introduced"
        ? bill.stage === "Introduced"
        : bill.stage !== "Introduced";
    return sectorMatch && stageMatch;
  });

  return (
    <main className="explore-main">
      <div className="explore-header">
        <h2>Explore Bills</h2>
        <p>Browse bills by sector and learn their market impact analysis.</p>
      </div>

      <div className="explore-content">
        <div className="bill-list">
          {filteredBills.length === 0 ? (
            <p className="no-results">No bills found for this filter.</p>
          ) : (
            filteredBills.map((bill, index) => (
              <div
                key={bill.id}
                style={{ animationDelay: `${index * 0.2}s` }}
                className="fade-in"
              >
                <BillCard bill={bill} />
              </div>
            ))
          )}
        </div>

        <aside className="filter-sidebar">
          <SectorFilter
            sectors={sectors}
            selectedSector={selectedSector}
            onSelectSector={setSelectedSector}
          />
          <StageFilter selectedStage={selectedStage} onSelectStage={setSelectedStage} />
        </aside>
      </div>
    </main>
  );
}

export default ExploreBills;
