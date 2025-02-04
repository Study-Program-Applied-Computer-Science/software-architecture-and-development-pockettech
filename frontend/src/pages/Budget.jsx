import React from "react";

export default function Budget({ isDarkMode }) {
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
              <div className="mt-8">
                <h2 className="text-lg font-semibold text-gray-800 mb-4">Latest Transactions</h2>
                <div className="bg-white rounded-lg shadow-lg p-4">
                  <table className="table-auto w-full text-left">
                    <thead>
                      <tr className="bg-gray-100 text-gray-600">
                        <th className="px-4 py-2">Name</th>
                        <th className="px-4 py-2">Amount</th>
                        <th className="px-4 py-2">Date</th>
                        <th className="px-4 py-2">Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr className="border-t">
                        <td className="px-4 py-2">Samantha W.</td>
                        <td className="px-4 py-2">$50,036</td>
                        <td className="px-4 py-2">Jan 25, 2021</td>
                        <td className="px-4 py-2 text-green-500">Completed</td>
                      </tr>
                      <tr className="border-t">
                        <td className="px-4 py-2">Karen Hope</td>
                        <td className="px-4 py-2">$10,500</td>
                        <td className="px-4 py-2">Jan 22, 2021</td>
                        <td className="px-4 py-2 text-red-500">Canceled</td>
                      </tr>
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
    