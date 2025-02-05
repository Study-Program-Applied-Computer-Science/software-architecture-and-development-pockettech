import axios from 'axios';

const API_URL = 'http://127.0.0.1:8003';

export const createBudget = async (budget) => {
  const response = await axios.post(`${API_URL}/budget/`, budget);
  return response.data;
};

export const getCategories = async () => {
  const response = await axios.get(`${API_URL}/budget/categories`);
  return response.data;
};

export const getCurrencies = async () => {
    const response = await axios.get(`${API_URL}/budget/currencies`);
    return response.data;
};

export const updateBudget = async (budgetId, budget) => {
  const response = await axios.put(`${API_URL}/budget/${budgetId}`, budget);
  return response.data;
};

export const deleteBudget = async (budgetId) => {
  const response = await axios.delete(`${API_URL}/budget/${budgetId}`);
  return response.data;
};

export const getAllTransactions = async (userId, startDate, endDate) => {
  const response = await axios.get(
    `${API_URL}/budget/alltransactions/${userId}/${startDate}/${endDate}`
  );
  return response.data;
};

export const getBudgetById = async (budgetId) => {
  const response = await axios.get(`${API_URL}/budget/getbudget/${budgetId}`);
  return response.data;
};

export default {
  createBudget,
  updateBudget,
  deleteBudget,
  getAllTransactions,
  getBudgetById,
  getCurrencies, 
  getCategories
};
