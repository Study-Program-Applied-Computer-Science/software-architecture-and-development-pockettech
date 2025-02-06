import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import SharedTransactionsService from "../services/SharedExpensesService/SharedTransactionsService";

const CreateSharedTransactionPage = () => {
  const { groupId } = useParams();
  const navigate = useNavigate();

  const [recordingUserId, setRecordingUserId] = useState("");
  const [creditUserId, setCreditUserId] = useState("");
  const [debitUserId, setDebitUserId] = useState("");
  const [otherParty, setOtherParty] = useState("");
  const [heading, setHeading] = useState("");
  const [description, setDescription] = useState("");
  const [transactionMode, setTransactionMode] = useState("");
  const [sharedTransaction, setSharedTransaction] = useState(true);
  const [category, setCategory] = useState(1);
  const [amount, setAmount] = useState("");
  const [currencyCode, setCurrencyCode] = useState(1);

  // Hardcoded Categories
  const categories = [
    { id: 1, name: "Groceries" },
    { id: 2, name: "Clothes" },
    { id: 3, name: "Dining" },
  ];

  // Hardcoded Currencies
  const currencies = [
    { code: 1, name: "USD" },
    { code: 2, name: "INR" },
    { code: 3, name: "EUR" },
  ];

  const handleSubmit = async (event) => {
    event.preventDefault();

    const newSharedTransaction = {
      recording_user_id: recordingUserId,
      credit_user_id: creditUserId,
      debit_user_id: debitUserId,
      other_party: otherParty.trim(),
      heading: heading.trim(),
      description: description.trim(),
      transaction_mode: transactionMode.trim(),
      shared_transaction: sharedTransaction,
      category: parseInt(category),
      amount: parseFloat(amount),
      currency_code: parseInt(currencyCode),
      group_id: groupId,
    };

    try {
      const createdTransaction = await SharedTransactionsService.createSharedTransaction(newSharedTransaction);

      console.log("Transaction Response:", JSON.stringify(createdTransaction, null, 2));

      if (createdTransaction) {
        alert("Shared Transaction Created Successfully");
        navigate(`/SharedTransactionsPage/${groupId}`);
      }
    } catch (error) {
      console.error("Error creating shared transaction:", error);
      alert("Error creating shared transaction");
    }
  };

  return (
    <div className="container mx-auto px-4 py-6 bg-white dark:bg-gray-900 text-black dark:text-white">
      <h1 className="text-3xl font-bold mb-4">Create New Shared Transaction</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        
        {[
          { label: "Recording User ID", value: recordingUserId, setter: setRecordingUserId },
          { label: "Credit User ID", value: creditUserId, setter: setCreditUserId },
          { label: "Debit User ID", value: debitUserId, setter: setDebitUserId },
          { label: "Other Party", value: otherParty, setter: setOtherParty },
          { label: "Heading", value: heading, setter: setHeading },
          { label: "Description", value: description, setter: setDescription, isTextArea: true },
          { label: "Transaction Mode", value: transactionMode, setter: setTransactionMode },
          { label: "Amount", value: amount, setter: setAmount, type: "number" }
        ].map(({ label, value, setter, isTextArea, type = "text" }) => (
          <div key={label}>
            <label className="block text-lg font-medium">{label}</label>
            {isTextArea ? (
              <textarea
                value={value}
                onChange={(e) => setter(e.target.value)}
                required
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-black dark:text-white rounded-md"
              />
            ) : (
              <input
                type={type}
                value={value}
                onChange={(e) => setter(e.target.value)}
                required
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-black dark:text-white rounded-md"
              />
            )}
          </div>
        ))}

        <div>
          <label className="block text-lg font-medium">Shared Transaction</label>
          <select
            value={sharedTransaction}
            onChange={(e) => setSharedTransaction(e.target.value === "true")}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-black dark:text-white rounded-md"
          >
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        </div>

        <div>
          <label className="block text-lg font-medium">Category</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-black dark:text-white rounded-md"
          >
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-lg font-medium">Currency Code</label>
          <select
            value={currencyCode}
            onChange={(e) => setCurrencyCode(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-black dark:text-white rounded-md"
          >
            {currencies.map((currency) => (
              <option key={currency.code} value={currency.code}>
                {currency.name} ({currency.code})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-lg font-medium">Group ID</label>
          <input
            type="text"
            value={groupId}
            readOnly
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-gray-100 dark:bg-gray-800 text-black dark:text-white rounded-md"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-500 dark:bg-blue-700 text-white px-4 py-2 rounded-lg hover:bg-blue-600 dark:hover:bg-blue-800"
        >
          Create Shared Transaction
        </button>
      </form>
    </div>
  );
};

export default CreateSharedTransactionPage;
