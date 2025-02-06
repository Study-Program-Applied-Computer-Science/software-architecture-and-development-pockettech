import React from 'react';
import BudgetList from '../components/BudgetList';

const BudgetOverviewPage = ({ isDarkMode }) => {
    const containerClass = isDarkMode
    ? 'min-h-screen bg-gray-900 text-gray-100 p-6'
    : 'min-h-screen bg-gray-50 text-gray-900 p-6';

  return (
    <div className={containerClass}>
      <h1 className="text-3xl font-bold mb-6">Budget Overview</h1>
      <BudgetList isDarkMode={isDarkMode} />
    </div>
  );
};


export default BudgetOverviewPage;
