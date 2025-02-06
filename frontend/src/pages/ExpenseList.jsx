import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getExpenses, deleteExpense, getCategories } from '../services/ExpenseService/expenseService';

const ExpenseList = ({ isDarkMode }) => {
    const [expenses, setExpenses] = useState([]);
    const [categories, setCategories] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchExpenses();
        fetchCategories();
    }, []);

    const fetchExpenses = async () => {
        try {
            const data = await getExpenses();
            setExpenses(data);
        } catch (error) {
            console.error('Failed to fetch expenses');
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

    const handleDelete = async (id) => {
        try {
            await deleteExpense(id);
            fetchExpenses();
        } catch (error) {
            console.error('Failed to delete expense');
        }
    };

    return (
        <div className={`${isDarkMode ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-900'} p-4 min-h-screen`}>
          <h2 className="text-2xl font-bold mb-4">Expenses</h2>
          <button
            onClick={() => navigate('/expenses/new')}
            className="mb-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md"
          >
            Add New Expense
          </button>
    
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className={`${isDarkMode ? 'bg-gray-800' : 'bg-gray-200'}`}>
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
                    Title
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
                    Description
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
                    Transaction Mode
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
                    Category
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
                    Amount
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className={`${isDarkMode ? 'bg-gray-900' : 'bg-white'} divide-y divide-gray-200`}>
                {expenses.map((expense) => {
                  const expenseCategory = categories.find(
                    (cat) => cat.id === expense.category
                  );
                  return (
                    <tr
                      key={expense.id}
                      className={`${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'}`}
                    >
                      <td className="px-6 py-4 whitespace-nowrap">{expense.heading}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{expense.description}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{expense.transaction_mode}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {new Date(expense.timestamp).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {expenseCategory ? expenseCategory.category : 'Unknown'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">{expense.amount}</td>
                      <td className="px-6 py-4 whitespace-nowrap space-x-2">
                        <button
                          onClick={() => navigate(`/expenses/${expense.id}`)}
                          className="px-2 py-1 bg-blue-500 hover:bg-blue-600 text-white rounded"
                        >
                          View
                        </button>
                        <button
                          onClick={() => navigate(`/expenses/edit/${expense.id}`)}
                          className="px-2 py-1 bg-green-500 hover:bg-green-600 text-white rounded"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDelete(expense.id)}
                          className="px-2 py-1 bg-red-500 hover:bg-red-600 text-white rounded"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      );
    
};

export default ExpenseList;