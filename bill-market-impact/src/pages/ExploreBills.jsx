import React, { useState } from "react";
import { billsData } from "../api/Bills";
import BillCard from "../components/BillCard";
import SectorFilter from "../components/SectorFilter";
import "../styles/ExploreBills.css";

function ExploreBills() {
  const sectors = [...new Set(billsData.map((bill) => bill.sector))];
  const [selectedSector, setSelectedSector] = useState("");

  const filteredBills = selectedSector
    ? billsData.filter((bill) => bill.sector === selectedSector)
    : billsData;

  return (
    <main className="explore-main">
      <h2 className="explore-title">Explore Congressional Bills</h2>
      <SectorFilter
        sectors={sectors}
        selectedSector={selectedSector}
        onSelectSector={setSelectedSector}
      />
      <section className="bill-list">
        {filteredBills.map((bill) => (
          <BillCard key={bill.id} {...bill} />
        ))}
      </section>
    </main>
  );
}

export default ExploreBills;
