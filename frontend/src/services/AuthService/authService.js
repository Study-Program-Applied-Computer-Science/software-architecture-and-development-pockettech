import axios from "axios";

const BASE_URL = "http://localhost:8001";


const axiosInstance = axios.create({
  baseURL: BASE_URL,
  withCredentials: true, // Include credentials (cookies)
});

/**
 * Login user
 * @param {string} email - User's email
 * @param {string} password - User's password
 * @returns {Promise<Object>} - Response data from the API
 */

export const loginUser = async (email, password) => {
  try {
    const response = await axiosInstance.post(`${BASE_URL}/api/v1/auth/login`, {
      email_id: email,
      password: password,
    });
    return response.data; // Return the response data
  } catch (error) {
    throw error.response?.data || error; // Forward the error for the component to handle
  }
};

