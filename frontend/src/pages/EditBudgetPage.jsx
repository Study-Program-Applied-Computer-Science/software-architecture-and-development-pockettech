import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import BudgetForm from '../components/BudgetForm';
import BudgetService from '../services/BudgetService/budgetService';

const EditBudgetPage = () => {
  const { budgetId } = useParams();
  const navigate = useNavigate();
  const [budget, setBudget] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBudget = async () => {
      try {
        const fetchedBudget = await BudgetService.getBudgetById(budgetId);
        setBudget(fetchedBudget);
      } catch (err) {
        console.error('Error fetching budget:', err);
        setError('Error fetching budget data.');
      } finally {
        setLoading(false);
      }
    };

    fetchBudget();
  }, [budgetId]);

  if (loading) return <p>Loading budget data...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
        <button onClick={() => navigate('/budget')} className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">Back to Budget List</button>
        <BudgetForm initialData={budget}/>
    </div>
  );
};

export default EditBudgetPage;
