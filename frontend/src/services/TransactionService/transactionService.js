import axios from 'axios';

const API_URL = 'http://localhost:8000/transactions';

export const getTransactions = async () => {
    try {
        const response = await axios.get(API_URL);
        return response.data;
    } catch (error) {
        console.error('Error fetching transactions:', error);
        throw error;
    }
};

export const createTransaction = async (transactionData) => {
    try {
        const response = await axios.post(API_URL, transactionData);
        return response.data;
    } catch (error) {
        console.error('Error creating transaction:', error);
        throw error;
    }
};

export const updateTransaction = async (transactionId, transactionData) => {
    try {
        const response = await axios.put(`${API_URL}/${transactionId}`, transactionData);
        return response.data;
    } catch (error) {
        console.error('Error updating transaction:', error);
        throw error;
    }
};

export const deleteTransaction = async (transactionId) => {
    try {
        const response = await axios.delete(`${API_URL}/${transactionId}`);
        return response.data;
    } catch (error) {
        console.error('Error deleting transaction:', error);
        throw error;
    }
};