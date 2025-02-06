import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8004/shared-group"; // Update with your actual backend URL

export const createSharedGroup = async (groupData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/shared_groups`, groupData);
    return response.data;
  } catch (error) {
    console.error("Error creating shared group:", error);
    throw error;
  }
};

export const getSharedGroups = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/shared_groups/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching shared groups:", error);
    throw error;
  }
};

export const deleteSharedGroup = async (groupId) => {
  try {
    await axios.delete(`${API_BASE_URL}/shared_groups/${groupId}`);
  } catch (error) {
    console.error("Error deleting shared group:", error);
    throw error;
  }
};
