import React, { useState, useEffect } from 'react';
import { Link, useNavigate} from 'react-router-dom';
import BudgetService from '../services/BudgetService/budgetService';

const BudgetList = ({ isDarkMode }) => {
  const [userId, setUserId] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [budgets, setBudgets] = useState([]);
  const [error, setError] = useState(null);
  const [currencies, setCurrencies] = useState([]);

  const navigate = useNavigate();

  const containerClass = isDarkMode
    ? 'min-h-screen bg-gray-900 text-gray-100 p-4 ml-64'
    : 'min-h-screen bg-gray-100 text-gray-900 p-4 ml-64';

  const inputClass =
    'w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400';
  const buttonClass =
    'bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-400';
  const errorClass = 'text-red-500 mt-2';
  const cardClass = isDarkMode
    ? 'bg-gray-800 border-gray-700'
    : 'bg-white border-gray-300';

    const fetchBudgets = async () => {
        if (!userId || !startDate || !endDate) {
        setError('Please fill in all fields.');
        return;
        }
        setError(null);
        try {
        const data = await BudgetService.getAllTransactions(userId, startDate, endDate);
        setBudgets(data);
        } catch (err) {
        console.error('Error fetching budgets:', err);
        setError('Error fetching budgets. Please check the input values and try again.');
        setBudgets([]);
        }
    };

    const getCurrencies = async () => {
        const data = await BudgetService.getCurrencies();
        setCurrencies(data);
    };

    useEffect(() => {
        getCurrencies();
      }, []);

    const handleDelete = async (budgetId) => {
    try {
      await BudgetService.deleteBudget(budgetId);
      setBudgets(budgets.filter((budget) => budget.id !== budgetId));
    } catch (err) {
      console.error('Error deleting budget:', err);
      setError('Error deleting budget.');
    }
  };

  return (
    <div className={containerClass}>
      <div className="flex justify-between items-center mb-4">
        <button
          onClick={() => navigate('/budget/create')}
          className={buttonClass}
        >
          Create New Budget
        </button>
      </div>
      <h2 className="text-2xl font-semibold mb-4">Budget List</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div>
          <label className="block mb-1">User ID:</label>
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="Enter user ID"
            className={inputClass}
          />
        </div>
        <div>
          <label className="block mb-1">Start Date:</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className={inputClass}
          />
        </div>
        <div>
          <label className="block mb-1">End Date:</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className={inputClass}
          />
        </div>
      </div>
      <div className="mb-6">
        <button onClick={fetchBudgets} className={buttonClass}>
          Fetch Budgets
        </button>
      </div>
      {error && <p className={errorClass}>{error}</p>}
      <hr className="mb-6 border-t border-gray-300" />
      {budgets.length > 0 ? (
        budgets.map((budget) => {
          const money = currencies.find((c) => c.id === budget.currency_id);
          return (
            <div
              key={budget.id}
              className={`mb-6 p-4 border rounded shadow-sm ${cardClass}`}
            >
              <h3 className="text-xl font-bold mb-2">
                Category: {budget.category}
              </h3>
              <p className="mb-1">
                <span className="font-semibold">Amount:</span> {budget.amount}
              </p>
              <p className="mb-1">
                <span className="font-semibold">Start Date:</span> {budget.start_date}
              </p>
              <p className="mb-1">
                <span className="font-semibold">End Date:</span> {budget.end_date}
              </p>
              <p className="mb-1">
                <span className="font-semibold">Currency:</span>{' '}
                {money ? money.currency : 'Unknown'}
              </p>
              <p className="mb-2">
                <span className="font-semibold">Total Transactions Amount:</span>{' '}
                {budget.total_amount}
              </p>
              <h4 className="font-semibold mb-1">Transactions:</h4>
              {budget.transactions && budget.transactions.length > 0 ? (
                <ul className="list-disc list-inside mb-2">
                  {budget.transactions.map((transaction) => (
                    <li key={transaction.transaction_id}>
                      <span className="font-medium">{transaction.heading}</span>:{' '}
                      {transaction.amount} on {transaction.timestamp}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No transactions available.</p>
              )}
              <div className="mt-4 flex space-x-4">
                <Link to={`/budget/edit/${budget.id}`}>
                  <button className={`${buttonClass} bg-green-500 hover:bg-green-600`}>
                    Edit
                  </button>
                </Link>
                <button
                  onClick={() => handleDelete(budget.id)}
                  className={`${buttonClass} bg-red-500 hover:bg-red-600`}
                >
                  Delete
                </button>
              </div>
            </div>
          );
        })
      ) : (
        <p>No budgets found for the given criteria.</p>
      )}
    </div>
  );

};

export default BudgetList;
