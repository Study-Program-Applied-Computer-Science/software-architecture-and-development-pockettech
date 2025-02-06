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
  const [category, setCategory] = useState(0);
  const [amount, setAmount] = useState("");
  const [currencyCode, setCurrencyCode] = useState(0);

  useEffect(() => {
    fetchCategories();
    fetchUsers();
    fetchCurrencies();
  }, []);

  

  const fetchCategories = async () => {
    try {
        const data = await getCategories();
        setCategories(data);
    } catch (error) {
        console.error('Failed to fetch categories');
    }
  };

const fetchCurrencies = async () => {
    try {
        const data = await getCurrencies();
        setCurrencies(data);
    } catch (error) {
        console.error('Failed to fetch currencies');
    }
  };

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
      group_id: groupId, // ✅ Use the groupId from the URL
    };

    try {
      const createdTransaction = await SharedTransactionsService.createSharedTransaction(newSharedTransaction);

      // ✅ Log response in the expected JSON format
      console.log("Transaction Response:", JSON.stringify(createdTransaction, null, 2));

      if (createdTransaction) {
        alert("Shared Transaction Created Successfully");
        navigate(`/SharedTransactionsPage/${groupId}`); // ✅ Redirect back with groupId
      }
    } catch (error) {
      console.error("Error creating shared transaction:", error);
      alert("Error creating shared transaction");
    }
  };

  return (
    <div className="container mx-auto px-4 py-6">
      <h1 className="text-3xl font-bold mb-4">Create New Shared Transaction</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        
        <div>
          <label className="block text-lg font-medium">Recording User ID</label>
          <input
            type="text"
            value={recordingUserId}
            onChange={(e) => setRecordingUserId(e.target.value)}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-lg font-medium">Credit User ID</label>
          <input
            type="text"
            value={creditUserId}
            onChange={(e) => setCreditUserId(e.target.value)}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-lg font-medium">Debit User ID</label>
          <input
            type="text"
            value={debitUserId}
            onChange={(e) => setDebitUserId(e.target.value)}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-lg font-medium">Other Party</label>
          <input
            type="text"
            value={otherParty}
            onChange={(e) => setOtherParty(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-lg font-medium">Heading</label>
          <input
            type="text"
            value={heading}
            onChange={(e) => setHeading(e.target.value)}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-lg font-medium">Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-lg font-medium">Transaction Mode</label>
          <input
            type="text"
            value={transactionMode}
            onChange={(e) => setTransactionMode(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-lg font-medium">Shared Transaction</label>
          <select
            value={sharedTransaction}
            onChange={(e) => setSharedTransaction(e.target.value === "true")}
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          >
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        </div>

        <div>
          <label className="block text-lg font-medium">Category</label>
          <input
            type="number"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-lg font-medium">Amount</label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-lg font-medium">Currency Code</label>
          <input
            type="number"
            value={currencyCode}
            onChange={(e) => setCurrencyCode(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>

        <div>
          <label className="block text-lg font-medium">Group ID</label>
          <input
            type="text"
            value={groupId} // ✅ Auto-fill from URL
            readOnly // Prevent user from changing it
            className="w-full px-4 py-2 border border-gray-300 rounded-md bg-gray-100"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
        >
          Create Shared Transaction
        </button>
      </form>
    </div>
  );
};

export default CreateSharedTransactionPage;