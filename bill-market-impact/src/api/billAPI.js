import axios from 'axios';

const API_URL = 'http://localhost:5000/api'; // Replace with backend later

export const fetchBills = async () => {
  const res = await axios.get(`${API_URL}/bills`);
  return res.data;
};

export const fetchBillDetails = async (id) => {
  const res = await axios.get(`${API_URL}/bills/${id}`);
  return res.data;
};
