import React, { useState, useEffect } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import SharedTransactionsService from "../services/SharedExpensesService/SharedTransactionsService";

const SharedTransactionsPage = () => {
  const { groupId } = useParams(); // ✅ Get groupId from URL
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const userId = "afa42e1a-628f-4a06-9771-47e85344ca85"; // Replace with dynamic user ID if needed

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const data = await SharedTransactionsService.getTransactionsWithNames(userId, groupId);
        console.log("Fetched transactions:", data);
        setTransactions(data);
      } catch (error) {
        console.error("Error fetching transactions:", error);
      }
      setLoading(false);
    };

    if (groupId) fetchTransactions();
  }, [userId, groupId]);

  const handleRepaymentUpdate = async (sharedTransactionId) => {
    const updatedTransaction = await SharedTransactionsService.updateRepaymentTransaction(sharedTransactionId);
    if (updatedTransaction) {
      alert("Repayment updated successfully");
      window.location.reload();
    }
  };

  if (loading) return <div className="text-center py-4">Loading...</div>;

  return (
    <div className="container mx-auto px-4 py-6 bg-white dark:bg-gray-800">
      <h1 className="text-3xl font-bold mb-4 text-black dark:text-white">
        Shared Transactions for Group ID: {groupId}
      </h1>

      <table className="min-w-full bg-white dark:bg-gray-700 border border-gray-200 rounded-lg shadow-md">
        <thead>
          <tr className="bg-gray-100 dark:bg-gray-600">
            <th className="px-4 py-2 border-b text-left text-black dark:text-white">Transaction ID</th>
            <th className="px-4 py-2 border-b text-left text-black dark:text-white">Group User Main</th>
            <th className="px-4 py-2 border-b text-left text-black dark:text-white">Group User Sub</th>
            <th className="px-4 py-2 border-b text-left text-black dark:text-white">Share Value</th>
            <th className="px-4 py-2 border-b text-left text-black dark:text-white">Payment Status</th>
            <th className="px-4 py-2 border-b text-left text-black dark:text-white">Repayment Status</th>
          </tr>
        </thead>
        <tbody>
          {Array.isArray(transactions) && transactions.length > 0 ? (
            transactions.map((transaction) => (
              <tr key={transaction.id} className="border-b dark:border-gray-600">
                <td className="px-4 py-2 text-black dark:text-white">{transaction.transaction_id}</td>
                <td className="px-4 py-2 text-black dark:text-white">{transaction.group_user_name_main}</td>
                <td className="px-4 py-2 text-black dark:text-white">{transaction.group_user_name_sub}</td>
                <td className="px-4 py-2 text-black dark:text-white">{transaction.share_value}</td>
                <td className="px-4 py-2 text-black dark:text-white">{transaction.payment_status}</td>
                <td className="px-4 py-2 text-black dark:text-white">
                  {transaction.repayment_transaction_id ? (
                    "Paid"
                  ) : (
                    <button
                      onClick={() => handleRepaymentUpdate(transaction.id)}
                      className="text-blue-500 dark:text-blue-300 hover:text-blue-700"
                    >
                      Update Repayment
                    </button>
                  )}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="7" className="text-center py-4 text-black dark:text-white">
                No transactions found.
              </td>
            </tr>
          )}
        </tbody>
      </table>

      <div className="mt-4">
        <Link
          to={`/CreateSharedTransactionPage/${groupId}`}  // Pass groupId in the URL
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 dark:bg-blue-700 dark:hover:bg-blue-600"
        >
          Create New Shared Transaction
        </Link>
      </div>
    </div>
  );
};

export default SharedTransactionsPage;
