import axios from "axios";

const BASE_URL = "http://127.0.0.1:8006/transaction-analysis/transactions";

/**
 * Fetch the last 10 transactions
 * @returns {Promise<Array>} - Array of last 10 transactions 
 */
export const fetchLastTransactions = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/last-10`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};

/**
 * Fetch transactions from the last week
 * @returns {Promise<Array>} - Array of transactions from the last week
 */
export const fetchLastWeekTransactions = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/last-week`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};

/**
 * Fetch expenses grouped by category
 * @returns {Promise<Array>} - Array of category expenses
 */
export const fetchExpensesByCategory = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/expenses-by-category`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};

/**
 * Predict future savings for a user
 * @param {string} userId - The user ID for which to predict savings
 * @param {number} monthsToPredict - Number of months to predict (default: 3)
 * @returns {Promise<Object>} - Predicted savings data
 */
export const fetchPredictedSavings = async (userId, monthsToPredict = 3) => {
  try {
    const response = await axios.post(
      `${BASE_URL}/predict-savings/${userId}`,
      { months_to_predict: monthsToPredict }
    );
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};

/**
 * Categorize uncategorized transactions
 * @returns {Promise<Object>} - Categorization result
 */
export const fetchCategorizeTransactions = async () => {
  try {
    const response = await axios.post(`${BASE_URL}/categorize-transactions`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
};
