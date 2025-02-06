import React, { useState, useEffect } from 'react';
import { createBudget, updateBudget, getCategories, getCurrencies } from '../services/BudgetService/budgetService';

const BudgetForm = ({ initialData = null, onBudgetSaved, isDarkMode}) => {
  const [formData, setFormData] = useState({
    user_id: '',
    category_id: '',
    amount: '',
    start_date: '',
    end_date: '',
    currency_id: '',
    id: '',
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [categories, setCategories] = useState([]);
  const [currencies, setCurrencies] = useState([]);

  useEffect(() => {
    if (initialData) {
      setFormData({
        user_id: initialData.user_id,
        category_id: initialData.category_id,
        amount: initialData.amount,
        start_date: initialData.start_date,
        end_date: initialData.end_date,
        currency_id: initialData.currency_id,
        id: initialData.id,
      });
    }
    fetchCategories();
    fetchCurrencies();
  }, [initialData]);

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

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    try {
      const payload = {
        ...formData,
        amount: parseFloat(formData.amount),
      };

      let response;
      if (initialData) {
        response = await updateBudget(payload.id, payload);
        setSuccess('Budget updated successfully!');
      } else {
        response = await createBudget(payload);
        setSuccess('Budget created successfully!');
      }
      if (onBudgetSaved) {
        onBudgetSaved(response);
      }
    } catch (err) {
      console.error('Failed to save budget:', err);
      setError('Failed to save budget. Please try again.');
    }
  };

    const containerClass = isDarkMode
    ? 'min-h-screen bg-gray-900 text-gray-100 p-6 ml-64'
    : 'min-h-screen bg-gray-50 text-gray-900 p-6 ml-64';

    const labelClass = 'block text-sm font-medium mb-1';
    const inputClass =
    'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400';
    const buttonClass =
    'bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-400';

    return (
        <div className={containerClass}>
          <h2 className="text-2xl font-semibold mb-4 ">
            {initialData ? 'Edit Budget' : 'Create Budget'}
          </h2>
          {error && <div className="text-red-500 mb-2">{error}</div>}
          {success && <div className="text-green-500 mb-2">{success}</div>}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className={labelClass}>User ID</label>
              <input
                type="text"
                name="user_id"
                value={formData.user_id}
                onChange={handleChange}
                required
                className={inputClass}
              />
            </div>

            <div>
                <label className={labelClass}>Category</label>
                <select
                    name="category_id"
                    value={formData.category_id || ''}
                    onChange={handleChange}
                    className={inputClass}
                    disabled={!!initialData}
                    required
                >
                    <option value="">Select Category</option>
                    {categories &&
                    categories.map((category) => (
                        <option key={category.id} value={category.id}>
                        {category.category}
                        </option>
                    ))}
                </select>
            </div>

            <div>
              <label className={labelClass}>Amount</label>
              <input
                type="number"
                step="0.01"
                name="amount"
                value={formData.amount}
                onChange={handleChange}
                required
                className={inputClass}
              />
            </div>
            
            <div>
              <label className={labelClass}>Start Date</label>
              <input
                type="date"
                name="start_date"
                value={formData.start_date}
                onChange={handleChange}
                required
                className={inputClass}
              />
            </div>
           
            <div>
              <label className={labelClass}>End Date</label>
              <input
                type="date"
                name="end_date"
                value={formData.end_date}
                onChange={handleChange}
                required
                className={inputClass}
              />
            </div>
            
            <div>
                <label className={labelClass}>Currency</label>
                <select name="currency_id" value={formData.currency_code} onChange={handleChange} className={inputClass} required>
                    <option value="">Select Currency</option>
                        {currencies.map((currency) => (
                            <option key={currency.id} value={currency.id}>{currency.currency}</option>
                        ))}
                </select>
            </div>
            
            {initialData && (
              <input type="hidden" name="id" value={formData.id} />
            )}
           
            <button type="submit" className={buttonClass}>
              {initialData ? 'Update Budget' : 'Create Budget'}
            </button>
          </form>
        </div>
      );
};

export default BudgetForm;
