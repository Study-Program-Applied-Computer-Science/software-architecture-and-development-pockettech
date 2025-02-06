import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getExpenseById, getCategories, getCurrencies, getUsers } from '../services/ExpenseService/expenseService';

const ExpenseView = ({ isDarkMode }) => {
    const { expenseId } = useParams();
    const [expense, setExpense] = useState({});
    const [categories, setCategories] = useState([]);
    const [currencies, setCurrencies] = useState([]);
    const [users, setUsers] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchExpense();
        fetchCategories();
        fetchUsers();
        fetchCurrencies();
    }, []);

    const fetchExpense = async () => {
        try {
            const data = await getExpenseById(expenseId);
            setExpense(data);
        } catch (error) {
            console.error('Failed to fetch expense');
        }
    };

    const fetchCategories = async () => {
        try {
            const data = await getCategories();
            setCategories(data);
        } catch (error) {
            console.error('Failed to fetch categories');
        }
    };
    
    const fetchCurrencies = async () => {
        try {
            const data = await getCurrencies();
            setCurrencies(data);
        } catch (error) {
            console.error('Failed to fetch currencies');
        }
    };

    const fetchUsers = async () => {
        try {
            const data = await getUsers();
            setUsers(data);
        } catch (error) {
            console.error('Failed to fetch users');
        }
    };

    const recordingUser = users.find(user => user.id === expense.recording_user_id);
    const creditUser = users.find(user => user.id === expense.credit_user_id);
    const debitUser = users.find(user => user.id === expense.debit_user_id);
    const expenseCategory = categories.find(cat => cat.id === expense.category);
    const money = currencies.find(curr => curr.id === expense.currency_code);

    return (
        <div className={`${isDarkMode ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-900'}`}>
            <button onClick={() => navigate('/expenses')} className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">Back to Expense List</button>
            
            <div className={`min-h-screen flex items-center justify-center ${isDarkMode ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-900'}`}>
                <div className={`max-w-lg w-full mx-auto ${isDarkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-md p-6`}>
                    
                    <h2 className={`text-2xl font-bold mb-6 text-center ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>Expense Details</h2>
                    
                    <h3 className={`text-2xl font-bold mb-6 text-center ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>{expense.heading}</h3>

                    <form className="space-y-4">
                        
                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Category</label>
                            <input type="text" name="heading" value={expenseCategory ? expenseCategory.category : 'Unknown'} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} disabled />
                        </div>
                    
                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Recording User</label>
                            <input type="text" name="heading" value={recordingUser ? recordingUser.name : 'Unknown'} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} disabled />
                        </div>

                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Credit User</label>
                            <input type="text" name="heading" value={creditUser ? creditUser.name : 'Unknown'} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} disabled />
                        </div>

                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Debit User</label>
                            <input type="text" name="heading" value={debitUser ? debitUser.name : 'Unknown'} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} disabled />
                        </div>

                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Other Party</label>
                            <input type="text" name="heading" value={expense.other_party} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} disabled />
                        </div>

                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Description</label>
                            <input type="text" name="heading" value={expense.description} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} disabled />
                        </div>

                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Shared Expense</label>
                            <input type="text" name="heading" value={expense.shared_transaction ? 'Yes' : 'No'} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} disabled />
                        </div>

                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Transaction Mode</label>
                            <input type="text" name="heading" value={expense.transaction_mode} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} disabled />
                        </div>

                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Amount</label>
                            <input type="number" name="heading" value={expense.amount} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} disabled />
                        </div>

                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Currency</label>
                            <input type="text" name="heading" value={money ? money.currency : 'Unknown'} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} disabled />
                        </div>

                        <div className="flex justify-end">
                            <button onClick={() => navigate(`/expenses/edit/${expenseId}`)} className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                                Edit
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        );
    };

export default ExpenseView;