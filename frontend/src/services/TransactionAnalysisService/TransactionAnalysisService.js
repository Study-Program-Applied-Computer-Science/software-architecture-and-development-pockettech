import axios from "axios";

const BASE_URL = "http://127.0.0.1:8003/transaction-analysis/transactions";

/**
 * Fetch the last 10 transactions
 * @returns {Promise<Array>} - Array of last 10 transactions 
 */
export const fetchLastTransactions = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/last-10`);
    return response.data; // Return the transaction data
  } catch (error) {
    throw error.response?.data || error; // Forward the error for the component to handle
  }
};

/**
 * Fetch the last 10 transactions
 * @returns {Promise<Array>} - Array of transactions of last week
 */
export const fetchLastWeekTransactions = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/last-week`);
    return response.data; // Return the transaction data
  } catch (error) {
    throw error.response?.data || error; // Forward the error for the component to handle
  }
};

/**
 * Fetch the last 10 transactions
 * @returns {Promise<Array>} - Array of transactions by category
 */
export const fetchExpensesByCategory = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/expenses-by-category`);
    return response.data; // Return the transaction data
  } catch (error) {
    throw error.response?.data || error; // Forward the error for the component to handle
  }
};

