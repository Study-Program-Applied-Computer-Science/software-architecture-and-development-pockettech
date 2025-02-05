import axios from "axios";


const userAxiosInstance = axios.create({
  baseURL: "http://localhost:8002", // Base URL for user-related operations
  withCredentials: true, // Include credentials (cookies)
});

// Create New User
/**
 * Create a new user
 * @param {Object} userData - The user data (e.g., name, email, password, etc.)
 * @returns {Promise<Object>} - Response data from the API
 */
export const createUser = async (userData) => {
  try {
    console.log("userData", userData);
    const response = await userAxiosInstance.post(`/api/v1/user`, userData);
    return response.data; 
  } catch (error) {
    throw error.response?.data || error; 
  }
};

export const updateUser = async (userId, userData) => {
  try {
    console.log("userData", userData);
    const response = await userAxiosInstance.put(`/api/v1/user/${userId}`, userData);
    return response.data; 
  } catch (error) {
    throw error.response?.data || error; 
  }
};






// Get User Details
export const getUserDetails = async (userId) => {
  try {
    const response = await userAxiosInstance.get(`/api/v1/user/${userId}`);
    return response.data; // Return the response data
  } catch (error) {
    throw error.response?.data || error; // Forward the error for the component to handle
  }
};