import React, {useState, useEffect} from "react";
import "../styles/SectorFilter.css";
import axios from "axios";

const SectorFilter = ({ sectors, selectedSector, onSelectSector }) => {
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
      <label htmlFor="sector-select">Filter by Sector:</label>
      <select
        id="sector-select"
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
};

export default SectorFilter;
