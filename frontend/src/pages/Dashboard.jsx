import React, { useEffect, useState } from "react";
import { fetchLastTransactions, fetchLastWeekTransactions, fetchExpensesByCategory } from "../services/TransactionAnalysisService/TransactionAnalysisService"; // Assuming you have a function like this
import { Bar, Pie } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from "chart.js";

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

export default function Dashboard({ isDarkMode }) {
  const [transactions, setTransactions] = useState([]);
  const [weeklyData, setWeeklyData] = useState([]);
  const [categoryData, setCategoryData] = useState([]); // For storing category data
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
        const data = await fetchExpensesByCategory(); // Fetch category expenses from your API
        setCategoryData(data);
      } catch (error) {
        console.error("Error fetching category expenses:", error);
      }
    };

    fetchCategoryData();
  }, []);

  // Prepare chart data for the Bar chart (Weekly Spending)
  const chartData = {
    labels: weeklyData.length
      ? weeklyData.map((txn) => new Date(txn.timestamp).toLocaleDateString())
      : [],
    datasets: [
      {
        label: "Weekly Spending ($)",
        data: weeklyData.length ? weeklyData.map((txn) => txn.amount) : [],
        backgroundColor: "rgba(70, 62, 238, 0.6)",
        borderColor: "#00000021",
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
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
    labels: categoryData.length
      ? categoryData.map((category) => category.category)
      : [],
    datasets: [
      {
        data: categoryData.length ? categoryData.map((category) => category.total_amount) : [],
        backgroundColor: [
          "rgba(255, 99, 132, 0.6)",
          "rgba(54, 162, 235, 0.6)",
          "rgba(255, 206, 86, 0.6)",
          "rgba(75, 192, 192, 0.6)",
          "rgba(153, 102, 255, 0.6)",
          "rgba(255, 159, 64, 0.6)",
        ], // You can customize these colors
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
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="flex">
        {/* Sidebar */}
        <aside
          className={`${
            isDarkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-gray-900"
          } w-64 shadow-lg rounded-lg p-4`}
        >
          <div className="text-center text-2xl font-bold text-purple-600">
            Yobor
          </div>
          <nav className="mt-6">
            <ul className="space-y-4">
              {[
                ["dashboard", "Dashboard"],
                ["account_balance", "Balance"],
                ["receipt_long", "Invoices"],
                ["credit_card", "Cards"],
                ["attach_money", "Transactions"],
                ["settings", "Settings"],
              ].map(([icon, label]) => (
                <li key={label}>
                  <a
                    href="#"
                    className="flex items-center text-gray-700 hover:text-purple-600"
                  >
                    <span className="material-icons-outlined">{icon}</span>
                    <span className="ml-2">{label}</span>
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </aside>

        {/* Main Content */}
        <div className="flex-1 ml-8">
          <header className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-semibold text-gray-800">Dashboard</h1>
            <input
              type="search"
              placeholder="Search..."
              className="rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring focus:ring-purple-300"
            />
          </header>

          {/* Top Cards */}
          <div className="grid grid-cols-3 gap-6 mb-8">
            {[
              ["My Balance", "$12,345,789", "Card Holder: John Doe", "bg-purple-600"],
              ["Income", "$45,741", "+0.5% last month", "bg-green-500"],
              ["Expense", "$32,123", "-0.9% last month", "bg-red-500"],
            ].map(([title, amount, description, bgColor], index) => (
              <div key={index} className={`p-6 ${bgColor} text-white rounded-lg shadow-lg`}>
                <h2 className="text-xl font-semibold">{title}</h2>
                <p className="text-3xl font-bold mt-2">{amount}</p>
                <p className="mt-1 text-sm">{description}</p>
              </div>
            ))}
          </div>

          {/* Charts and Overview */}
          <div className="p-6 bg-white rounded-lg shadow-lg">
            <h2 className="text-lg font-semibold text-gray-800">Weekly Spending</h2>
            <div className="mt-4 h-60">
              {loading ? (
                <p className="text-gray-500 text-center">Loading data...</p>
              ) : weeklyData.length > 0 ? (
                <Bar data={chartData} options={chartOptions} />
              ) : (
                <p className="text-gray-500 text-center">No transactions found for the last week.</p>
              )}
            </div>

            <h2 className="text-lg font-semibold text-gray-800 mt-6">
              Outcome Categories
            </h2>
            <div className="mt-4 h-60">
              {categoryData.length > 0 ? (
                <Pie data={pieChartData} options={pieChartOptions} />
              ) : (
                <p className="text-gray-500 text-center">No category data available.</p>
              )}
            </div>
          </div>

          {/* Transactions Table */}
          <div className="mt-8">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">
              Latest Transactions
            </h2>
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
      </div>
    </div>
  );
}
