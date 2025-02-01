import React, { useEffect, useState } from "react";
import { fetchLastTransactions } from "../services/TransactionAnalysisService/TransactionAnalysisService"; // Import the service


export default function Dashboard({ isDarkMode }) {
  const [transactions, setTransactions] = useState([]);

  // Fetch the transactions data on component mount
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

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* Sidebar */}
      <div className="flex">
        <aside className={`${isDarkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-gray-900"} w-64 shadow-lg rounded-lg p-4`}>
          <div className="text-center text-2xl font-bold text-purple-600">Yobor</div>
          <nav className="mt-6">
            <ul className="space-y-4">
              <li>
                <a href="#" className="flex items-center text-gray-700 hover:text-purple-600">
                  <span className="material-icons-outlined">dashboard</span>
                  <span className="ml-2">Dashboard</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center text-gray-700 hover:text-purple-600">
                  <span className="material-icons-outlined">account_balance</span>
                  <span className="ml-2">Balance</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center text-gray-700 hover:text-purple-600">
                  <span className="material-icons-outlined">receipt_long</span>
                  <span className="ml-2">Invoices</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center text-gray-700 hover:text-purple-600">
                  <span className="material-icons-outlined">credit_card</span>
                  <span className="ml-2">Cards</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center text-gray-700 hover:text-purple-600">
                  <span className="material-icons-outlined">attach_money</span>
                  <span className="ml-2">Transactions</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center text-gray-700 hover:text-purple-600">
                  <span className="material-icons-outlined">settings</span>
                  <span className="ml-2">Settings</span>
                </a>
              </li>
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
            <div className="p-6 bg-purple-600 text-white rounded-lg shadow-lg">
              <h2 className="text-xl font-semibold">My Balance</h2>
              <p className="text-3xl font-bold mt-2">$12,345,789</p>
              <p className="mt-1 text-sm">Card Holder: John Doe</p>
            </div>
            <div className="p-6 bg-green-500 text-white rounded-lg shadow-lg">
              <h2 className="text-xl font-semibold">Income</h2>
              <p className="text-3xl font-bold mt-2">$45,741</p>
              <p className="mt-1 text-sm">+0.5% last month</p>
            </div>
            <div className="p-6 bg-red-500 text-white rounded-lg shadow-lg">
              <h2 className="text-xl font-semibold">Expense</h2>
              <p className="text-3xl font-bold mt-2">$32,123</p>
              <p className="mt-1 text-sm">-0.9% last month</p>
            </div>
          </div>

          {/* Charts and Overview */}
          <div className="grid grid-cols-2 gap-6">
            <div className="p-6 bg-white rounded-lg shadow-lg">
              <h2 className="text-lg font-semibold text-gray-800">Weekly Spending</h2>
              <div className="mt-4">
                {/* Placeholder for Chart */}
                <div className="h-40 bg-gray-200 rounded-lg flex items-center justify-center">
                  <p className="text-gray-500">Chart Placeholder</p>
                </div>
              </div>
            </div>
            <div className="p-6 bg-white rounded-lg shadow-lg">
              <h2 className="text-lg font-semibold text-gray-800">Outcome Categories</h2>
              <div className="mt-4">
                {/* Placeholder for Pie Chart */}
                <div className="h-40 bg-gray-200 rounded-lg flex items-center justify-center">
                  <p className="text-gray-500">Pie Chart Placeholder</p>
                </div>
              </div>
            </div>
          </div>

          {/* Transactions */}
          <div
  className={` mt-8`}
>
  <h2
    className={`text-lg font-semibold text-gray-800 mb-4`}
  >
    Latest Transactions
  </h2>
  <div
    className={`${
      isDarkMode ? "bg-gray-800" : "bg-white"
    } rounded-lg shadow-lg p-4`}
  >
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
        {/* Loop through the transactions and render them */}
        {transactions.map((transaction) => (
          <tr
            key={transaction.id}
            className={`${isDarkMode ? "bg-gray-700 text-white" : "bg-gray-100 text-gray-600"} `}
          >
            <td className="px-4 py-2">{transaction.heading}</td>
            <td className="px-4 py-2">
              ${transaction.amount.toFixed(2)}
            </td>
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
        ))}
                  {/* Add more rows as needed */}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
