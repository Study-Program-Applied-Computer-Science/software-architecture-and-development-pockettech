import React, { useEffect, useState } from "react";

import { Bar, Pie } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from "chart.js";
import {
  fetchLastTransactions,
  fetchLastWeekTransactions,
  fetchExpensesByCategory,
  fetchPredictedSavings,
  fetchCategorizeTransactions,
} from "../services/TransactionAnalysisService/TransactionAnalysisService";


// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

export default function Dashboard({ isDarkMode }) {
  const [transactions, setTransactions] = useState([]);
  const [weeklyData, setWeeklyData] = useState([]);

  const [categoryData, setCategoryData] = useState([]);
  const [predictedSavings, setPredictedSavings] = useState(null);
  const [categorizationResult, setCategorizationResult] = useState(null);

  const [loading, setLoading] = useState(true);

  // Fetch latest transactions
  useEffect(() => {
    const getTransactions = async () => {
      try {
        const data = await fetchLastTransactions();
        setTransactions(data);
      } catch (error) {
        console.error("Error fetching transactions:", error);
      }
    };
    getTransactions();
  }, []);

  // Fetch last week's transactions
  useEffect(() => {
    const fetchWeeklyTransactions = async () => {
      try {
        const data = await fetchLastWeekTransactions();
        setWeeklyData(data);
      } catch (error) {
        console.error("Error fetching weekly transactions:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchWeeklyTransactions();
  }, []);

  // Fetch expenses by category for the pie chart
  useEffect(() => {
    const fetchCategoryData = async () => {
      try {

        const data = await fetchExpensesByCategory();

        setCategoryData(data);
      } catch (error) {
        console.error("Error fetching category expenses:", error);
      }
    };

    fetchCategoryData();
  }, []);

  // Fetch predicted savings using the user ID from localStorage
  useEffect(() => {
    const getPredictedSavings = async () => {
      const userId = localStorage.getItem("user_id");
      if (!userId) {
        console.error("No user ID found in localStorage.");
        return;
      }
      try {
        const data = await fetchPredictedSavings(userId, 3);
        setPredictedSavings(data);
      } catch (error) {
        console.error("Error fetching predicted savings:", error);
      }
    };
    getPredictedSavings();
  }, []);

  // Fetch transaction categorization result
  useEffect(() => {
    const getCategorization = async () => {
      try {
        const data = await fetchCategorizeTransactions();
        setCategorizationResult(data);
      } catch (error) {
        console.error("Error fetching transaction categorization:", error);
      }
    };
    getCategorization();
  }, []);

  // Prepare chart data for the Bar chart (Weekly Spending)
  const barChartData = {

    labels: weeklyData.length
      ? weeklyData.map((txn) => new Date(txn.timestamp).toLocaleDateString())
      : [],
    datasets: [
      {
        label: "Weekly Spending ($)",
        data: weeklyData.length ? weeklyData.map((txn) => txn.amount) : [],

        backgroundColor: isDarkMode ? "rgba(255, 159, 64, 0.6)" : "rgba(70, 62, 238, 0.6)",
        borderColor: isDarkMode ? "#ffffff" : "#00000021",

        borderWidth: 1,
      },
    ],
  };


  const barChartOptions = {

    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true },
      tooltip: { enabled: true },
    },
    scales: {
      y: { beginAtZero: true },
    },
  };

  // Prepare data for Pie chart (Outcome Categories)
  const pieChartData = {

    labels: categoryData.length ? categoryData.map((cat) => cat.category) : [],
    datasets: [
      {
        data: categoryData.length ? categoryData.map((cat) => cat.total_amount) : [],

        backgroundColor: [
          "rgba(255, 99, 132, 0.6)",
          "rgba(54, 162, 235, 0.6)",
          "rgba(255, 206, 86, 0.6)",
          "rgba(75, 192, 192, 0.6)",
          "rgba(153, 102, 255, 0.6)",
          "rgba(255, 159, 64, 0.6)",

        ],

        borderColor: "#ffffff",
        borderWidth: 1,
      },
    ],
  };

  const pieChartOptions = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      tooltip: { enabled: true },
    },
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 ml-64">
      <header className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-semibold text-gray-800">Dashboard</h1>
        <input
          type="search"
          placeholder="Search..."
          className="rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring focus:ring-purple-300"
        />
      </header>


      {/* Charts and Overview */}
      <div className={`p-6 ${isDarkMode ? "bg-gray-800 text-white" : "bg-white text-gray-800"} rounded-lg shadow-lg mb-8`}>
        <div className="grid grid-cols-2 gap-6">
          {/* Bar Chart: Weekly Spending */}
          <div className="p-4">
            <h2 className="text-lg font-semibold">Weekly Spending</h2>
            <div className="mt-4 h-60">
              {loading ? (
                <p className="text-center">{isDarkMode ? "Loading data..." : "Loading data..."}</p>
              ) : weeklyData.length > 0 ? (
                <Bar data={barChartData} options={barChartOptions} />
              ) : (
                <p className="text-center">No transactions found for the last week.</p>
              )}
            </div>
          </div>

          {/* Pie Chart: Outcome Categories */}
          <div className="p-4">
            <h2 className="text-lg font-semibold">Outcome Categories</h2>
            <div className="mt-4 h-60">
              {loading ? (
                <p className="text-center">Loading data...</p>
              ) : categoryData.length > 0 ? (
                <Pie data={pieChartData} options={pieChartOptions} />
              ) : (
                <p className="text-center">No categories found.</p>
              )}
            </div>
          </div>
        </div>

        {/* Predicted Savings */}
        <div className="mt-8">
          <h2 className="text-lg font-semibold">Predicted Savings</h2>
          <div className="mt-4 p-4 bg-gray-50 rounded-lg shadow">
          {predictedSavings && predictedSavings.predicted_savings && Object.keys(predictedSavings.predicted_savings).length > 0 ? (
  <ul>
    {Object.entries(predictedSavings.predicted_savings).map(([month, amount]) => (
      <li key={month}>
        <strong>{month}:</strong> ${amount}
      </li>
    ))}
  </ul>
) : (
  <p className="text-gray-500">No savings prediction available.</p>
)}

          </div>
        </div>

        {/* Categorization Result */}
        <div className="mt-8">
          <h2 className="text-lg font-semibold">Categorization Result</h2>
          <div className="mt-4 p-4 bg-gray-50 rounded-lg shadow">
            {categorizationResult && categorizationResult.categorized_transactions ? (
              <ul>
                {categorizationResult.categorized_transactions.map((item) => (
                  <li key={item.id}>
                    Transaction {item.id} categorized as <strong>{item.category}</strong>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">
                {categorizationResult ? categorizationResult.error : "No categorization data available."}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Transactions Table */}
      <div className="mt-8">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Latest Transactions</h2>
        <div className={`${isDarkMode ? "bg-gray-800" : "bg-white"} rounded-lg shadow-lg p-4`}>
          <table className="table-auto w-full text-left">
            <thead>
              <tr className={`${isDarkMode ? "bg-gray-700 text-white" : "bg-gray-100 text-gray-600"}`}>
                <th className="px-4 py-2">Name</th>
                <th className="px-4 py-2">Amount</th>
                <th className="px-4 py-2">Date</th>
                <th className="px-4 py-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {transactions.length > 0 ? (
                transactions.map((transaction) => (
                  <tr key={transaction.id} className={`${isDarkMode ? "bg-gray-700 text-white" : "bg-gray-100 text-gray-600"}`}>
                    <td className="px-4 py-2">{transaction.heading}</td>
                    <td className="px-4 py-2">${transaction.amount.toFixed(2)}</td>
                    <td className="px-4 py-2">
                      {new Date(transaction.timestamp).toLocaleDateString()}
                    </td>
                    <td className="px-4 py-2">
                      {transaction.shared_transaction ? (
                        <span className="text-green-500">Shared</span>
                      ) : (
                        <span className="text-red-500">Personal</span>
                      )}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="4" className="text-center py-4 text-gray-500">
                    No recent transactions found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
