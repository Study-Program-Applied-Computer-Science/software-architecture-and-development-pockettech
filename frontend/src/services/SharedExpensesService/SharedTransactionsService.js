import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8004/shared-transaction/";

const getSharedTransactions = async (userId, groupId) => {
  const response = await fetch(`${API_BASE_URL}shared-transactions/${userId}/${groupId}`);
  return response.json();
};

const getTransactionsWithNames = async (userId, groupId) => {
  const response = await fetch(`${API_BASE_URL}shared-transactions/named/${userId}/${groupId}`);
  return response.json();
};

export const getUsers = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8004/shared-users/users`);
    return response.data;
  } catch (error) {
    console.error('Error fetching users:', error);
    throw error;
  }
};

export const getCategories = async () => {
  try {
      const response = await axios.get(`${API_BASE_URL}/categories`);
      return response.data;
  } catch (error) {
      console.error('Error fetching categories:', error);
      throw error;
  }
};

export const getCurrencies = async () => {
  try {
      const response = await axios.get(`${API_BASE_URL}/currencies`);
      return response.data;
  } catch (error) {
      console.error('Error fetching currencies:', error);
      throw error;
  }
};

const createSharedTransaction = async (transactionData) => {
  const response = await fetch(`${API_BASE_URL}shared-transactions/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(transactionData),
  });
  return response.json();
};

const updateRepaymentTransaction = async (sharedTransactionId) => {
  const response = await fetch(`${API_BASE_URL}repay_shared_transaction/${sharedTransactionId}`, {
    method: "PUT",
  });
  return response.json();
};

export default {
  getSharedTransactions,
  createSharedTransaction,
  updateRepaymentTransaction,
  getTransactionsWithNames,
};