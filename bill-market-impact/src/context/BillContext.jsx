import React, { createContext, useState, useEffect } from 'react';
import { fetchBills } from '../api/billAPI';

export const BillContext = createContext();

export const BillProvider = ({ children }) => {
  const [bills, setBills] = useState([]);

  useEffect(() => {
    const loadBills = async () => {
      const data = await fetchBills();
      setBills(data);
    };
    loadBills();
  }, []);

  return (
    <BillContext.Provider value={{ bills }}>
      {children}
    </BillContext.Provider>
  );
};
