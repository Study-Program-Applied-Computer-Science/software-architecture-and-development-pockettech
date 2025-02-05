import React from 'react';
import BudgetForm from '../components/BudgetForm';
import { useNavigate } from 'react-router-dom';

const CreateBudgetPage = ({isDarkMode}) => {
    const navigate = useNavigate();

    const containerClass = isDarkMode
        ? 'min-h-screen bg-gray-900 text-gray-100 p-6'
        : 'min-h-screen bg-gray-50 text-gray-900 p-6';
    
      return (
        <div className={containerClass}>
            <button onClick={() => navigate('/budget')} className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">Back to Budget List</button>
            <BudgetForm isDarkMode={isDarkMode} />
        </div>
      );
};

export default CreateBudgetPage;
