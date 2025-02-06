import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createExpense, updateExpense, getCategories, getCurrencies, getUsers, getExpenseById } from '../services/ExpenseService/expenseService';

const ExpenseForm = ({ onExpenseCreated, isDarkMode, showSharedExpense = false }) => {
    const { expenseId } = useParams();
    const navigate = useNavigate();
    const [alertMessage, setAlertMessage] = useState('');
    const [categories, setCategories] = useState([]);
    const [currencies, setCurrencies] = useState([]);
    const [users, setUsers] = useState([]);
    const [formData, setFormData] = useState({
        recording_user_id: null,
        credit_user_id: null,
        debit_user_id: null,
        other_party: '',
        heading: '',
        description: '',
        transaction_mode: '',
        shared_transaction: false,
        category: 0,
        amount: 0,
        currency_code: 0
    });

    const fetchExpense = async (id) => {
        try {
            const expense = await getExpenseById(id);
            setFormData({
                id: expense.id,
                timestamp: expense.timestamp,
                recording_user_id: expense.recording_user_id || null,
                credit_user_id: expense.credit_user_id || null,
                debit_user_id: expense.debit_user_id || null,
                other_party: expense.other_party || '',
                heading: expense.heading || '',
                description: expense.description || '',
                transaction_mode: expense.transaction_mode || '',
                shared_transaction: expense.shared_transaction || false,
                category: expense.category || 0,
                amount: expense.amount || 0,
                currency_code: expense.currency_code || 0
            });
        } catch (error) {
            console.error('Error fetching expense:', error);
        }
    };

    useEffect(() => {
        if (expenseId) {
            fetchExpense(expenseId);
        }
        fetchCategories();
        fetchCurrencies();
        fetchUsers();
    }, [expenseId]);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData({
            ...formData,
            [name]:
                type === 'checkbox'
                    ? checked
                    : name === 'category' || name === 'currency_code'
                    ? parseInt(value, 10)
                    : name === 'amount'
                    ? parseFloat(value)
                    : value
        });
    };

    const fetchCategories = async () => {
        try {
            const data = await getCategories();
            setCategories(data);
        } catch (error) {
            console.error('Error fetching categories:', error);
        }
    };

    const fetchCurrencies = async () => {
        try {
            const data = await getCurrencies();
            setCurrencies(data);
        } catch (error) {
            console.error('Error fetching currencies:', error);
        }
    };
    
    const fetchUsers = async () => {
        try {
            const data = await getUsers();
            setUsers(data);
        } catch (error) {
            console.error('Error fetching users:', error);
        }
    };
    
    const handleSubmit = async (e) => {
        e.preventDefault();

        const formattedData = {
            ...formData,
            timestamp: new Date().toISOString(),
            credit_user_id: formData.credit_user_id || null,
            debit_user_id: formData.debit_user_id || null,
            other_party: formData.other_party || null,
            description: formData.description || null
        };

        try {
            if (expenseId) {
                await updateExpense(expenseId, formattedData);
                setAlertMessage('Expense updated successfully!');
            } else {
                await createExpense(formattedData);
                setAlertMessage('Expense added successfully!');
            }
            onExpenseCreated();
            setTimeout(() => {
                setAlertMessage('');
                navigate('/expenses');
            }, 2000);
        } catch (error) {
            console.error('Error saving expense', error);
        }
    };

    return (
        <div className={`${isDarkMode ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-900'}`}>

            <button onClick={() => navigate('/ExpenseList')} className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">Back to Expense List</button>
            
            <div className={`min-h-screen flex items-center justify-center ${isDarkMode ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-900'}`}>
                <div className={`max-w-lg w-full mx-auto ${isDarkMode ? 'bg-gray-800' : 'bg-white'} rounded-lg shadow-md p-6`}>
                    
                    <h2 className={`text-2xl font-bold mb-6 text-center ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>{expenseId ? 'Edit Expense' : 'Add an Expense'}</h2>
                    
                    {alertMessage && (<div className={`mb-4 p-3 rounded-md ${isDarkMode? 'bg-green-900 text-green-300' : 'bg-green-100 text-green-700'}`}>
                        {alertMessage}
                    </div>
                    )}
                    
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Category
                            <span className="text-red-500">*</span>
                            </label>
                            <select name="category" value={formData.category} onChange={handleChange} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} required>
                                <option value="">Select a Category</option>
                                {categories.map((cat) => (
                                    <option key={cat.id} value={cat.id}>{cat.category}</option>
                                ))}
                            </select>
                        </div>      

                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Recording User<span className="text-red-500">*</span></label>
                            <select name="recording_user_id" value={formData.recording_user_id} onChange={handleChange} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100' : 'bg-white border-gray-300 text-gray-900'}`} required>
                                <option value="">Select a User</option>
                                {users.map((user) => (
                                    <option key={user.id} value={user.id}>{user.name}</option>
                                ))}
                            </select>
                        </div>

                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Credit User</label>
                            <select name="credit_user_id" value={formData.credit_user_id} onChange={handleChange} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`}>
                                <option value="">Select a User</option>
                                {users.map((user) => (
                                    <option key={user.id} value={user.id}>{user.name}</option>
                                ))}
                            </select>
                        </div>
                        
                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Debit User</label>
                            <select name="debit_user_id" value={formData.debit_user_id} onChange={handleChange} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`}>
                                <option value="">Select a User</option>
                                {users.map((user) => (
                                <option key={user.id} value={user.id}>{user.name}</option>
                                ))}
                            </select>
                        </div>

                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Other Party </label>
                            <input type="text" name="other_party" value={formData.other_party} onChange={handleChange} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`}/>
                        </div>

                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Heading<span className="text-red-500">*</span></label>
                            <input type="text" name="heading" value={formData.heading} onChange={handleChange} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} required />
                        </div>
        
                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Description</label>
                            <input type="text" name="description" value={formData.description} onChange={handleChange} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`}/>
                        </div>
                        
                        {showSharedExpense && (
                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                                Shared Expense
                            </label>
                            <input
                                type="checkbox"
                                name="shared_transaction"
                                checked={formData.shared_transaction}
                                onChange={handleChange}
                                className={`h-4 w-4 rounded focus:ring-indigo-500 ${isDarkMode ? "bg-gray-700 border-gray-600 text-indigo-400" : "bg-white border-gray-300 text-indigo-600"}`}
                            />
                        </div>
                    )}

                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Transaction Mode<span className="text-red-500">*</span></label>
                            <select name="transaction_mode" value={formData.transaction_mode} onChange={handleChange} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} required>
                                <option value="">Select Transaction Mode</option>
                                <option value="Cash">Cash</option>
                                <option value="Credit Card">Credit Card</option>
                                <option value="Debit Card">Debit Card</option>
                                <option value="Online">Online</option>
                            </select>
                        </div>
                    
                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Amount<span className="text-red-500">*</span></label> 
                            <input type="number" name="amount" value={formData.amount} onChange={handleChange} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} required />
                        </div>
                        
                        <div className="flex items-center">
                            <label className={`w-1/3 text-sm font-medium ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>Currency<span className="text-red-500">*</span></label>
                            <select name="currency_code" value={formData.currency_code} onChange={handleChange} className={`w-2/3 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${isDarkMode ? 'bg-gray-700 border-gray-600 text-gray-100': 'bg-white border-gray-300 text-gray-900'}`} required>
                                <option value="">Select Currency</option>
                                {currencies.map((currency) => (
                                    <option key={currency.id} value={currency.id}>{currency.currency}</option>
                                ))}
                            </select>
                        </div>

                        <div className="flex justify-end">
                            <button type="submit" className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                                {expenseId ? 'Update' : 'Add'} Expense
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
    );
};

export default ExpenseForm;
