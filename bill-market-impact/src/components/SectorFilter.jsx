import React, { useState, useEffect } from "react";
import "../styles/SectorFilter.css"; // CSS Import
import axios from "axios";
import BillCard from "./BillCard";

function SectorFilter({ sectors, selectedSector, onSelectSector }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get('http://localhost:8000/all_bills');
        setData(res.data)

      } catch (err) {
        console.log(err.message)
      }
    }
    fetchData();
  }, []);

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
      <div>
        {data.map((item, index) => (
          <div key={index} className="data-item">
            <BillCard 
            sector={item.sector}  // Passing the sector
            // title={item.title}    // Passing the title
            billType={item.bill_type} // Passing the bill type
            confidenceScore={item.confidence_score} // Passing the confidence score
            />
          </div>
        ))}
      </div>
    </div>

  );
}

export default SectorFilter;
