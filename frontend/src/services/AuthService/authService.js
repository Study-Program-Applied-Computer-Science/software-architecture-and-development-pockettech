import axios from "axios";

const BASE_URL = "http://localhost:8002";

/**
 * Login user
 * @param {string} email - User's email
 * @param {string} password - User's password
 * @returns {Promise<Object>} - Response data from the API
 */

export const loginUser = async (email, password) => {
  try {
    const response = await axios.post(`${BASE_URL}/user/verifyuser`, {
      email_id: email,
      password: password,
    });
    return response.data; // Return the response data
  } catch (error) {
    throw error.response?.data || error; // Forward the error for the component to handle
  }
};

