import React from "react";
import "../styles/SectorFilter.css"; // CSS Import

function SectorFilter({ sectors, selectedSector, onSelectSector }) {
  return (
    <div className="sector-filter">
      <label>Filter by Sector: </label>
      <select
        value={selectedSector}
        onChange={(e) => onSelectSector(e.target.value)}
      >
        <option value="">All</option>
        {sectors.map((sector, index) => (
          <option key={index} value={sector}>
            {sector}
          </option>
        ))}
      </select>
    </div>
  );
}

export default SectorFilter;
