import axios from 'axios';

const API_URL = 'http://localhost:8005/transactions';
const CATEGORY_API_URL = 'http://localhost:8005/transactions/category';
const CURRENCY_API_URL = 'http://localhost:8005/transactions/country';
const USERS_API_URL = 'http://localhost:8005/transactions/users';

export const getUsers = async () => {
    try {
        const response = await axios.get(USERS_API_URL);
        return response.data;
    } catch (error) {
        console.error('Error fetching users:', error);
        throw error;
    }
};

export const getCurrencies = async () => {
    try {
        const response = await axios.get(CURRENCY_API_URL);
        return response.data;
    } catch (error) {
        console.error('Error fetching currencies:', error);
        throw error;
    }
};

export const getExpenses = async () => {
    try {
        const response = await axios.get(API_URL);
        return response.data;
    } catch (error) {
        console.error('Error fetching expenses:', error);
        throw error;
    }
};

export const getExpenseById = async (expenseId) => {
    try {
        const response = await axios.get(`${API_URL}/${expenseId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching expense:', error);
        throw error;
    }
};

export const getCategories = async () => {
    try {
        const response = await axios.get(CATEGORY_API_URL);
        return response.data;
    } catch (error) {
        console.error('Error fetching categories:', error);
        throw error;
    }
};

export const createExpense = async (expenseData) => {
    try {
        const response = await axios.post(API_URL, expenseData);
        return response.data;
    } catch (error) {
        console.error("Error creating expense:", error.response?.data || error);
        throw error;
    }
};

export const updateExpense = async (expenseId, expenseData) => {
    try {
        const response = await axios.put(`${API_URL}/${expenseId}`, expenseData);
        return response.data;
    } catch (error) {
        console.error('Error updating expense:', error);
        throw error;
    }
};

export const deleteExpense = async (expenseId) => {
    try {
        const response = await axios.delete(`${API_URL}/${expenseId}`);
        return response.data;
    } catch (error) {
        console.error('Error deleting expense:', error);
        throw error;
    }
};