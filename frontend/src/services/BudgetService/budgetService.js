import axios from "axios";

const BASE_URL = "http://localhost:8003";


// /**
//  * Login user
//  * @param {string} email - User's email
//  * @param {string} password - User's password
//  * @returns {Promise<Object>} - Response data from the API
//  */

// export const loginUser = async (email, password) => {
//   try {
//     const response = await axios.post(`${BASE_URL}/user/verifyuser`, {
//       email_id: email,
//       password: password,
//     });
//     return response.data; // Return the response data
//   } catch (error) {
//     throw error.response?.data || error; // Forward the error for the component to handle
//   }
// };

export const createBudget = async (budgetData) => {
  try {
    const response = await axios.post(`${BASE_URL}/budget/`, budgetData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
}

export const updateBudget = async (budgetId, budgetData) => {
  try {
    const response = await axios.put(`${BASE_URL}/budget/${budgetId}`, budgetData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
}

export const deleteBudget = async (budgetId) => {
  try {
    const response = await axios.delete(`${BASE_URL}/budget/${budgetId}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
}

export const getBudgets = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/budget/${userId}/${start_date}/${end_date}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
}

export const getBudgetsWithTransactions = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/budget/alltransactions/${userId}/${start_date}/${end_date}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
}

