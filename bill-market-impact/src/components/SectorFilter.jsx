import React, { useState, useEffect } from "react";
import "../styles/SectorFilter.css"; // CSS Import
import axios from "axios";

function SectorFilter({ sectors, selectedSector, onSelectSector }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.post('http://localhost:5432/all_bills');
        setData(res.data)

      } catch (err) {
        console.log(err.message)
      }
    }
    fetchData();
    console.log(data);
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
            <p>{item.title}</p>
          </div>
        ))}
      </div>
    </div>

  );
}

export default SectorFilter;
