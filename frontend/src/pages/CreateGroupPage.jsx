import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; 
import { createSharedGroup } from "../services/SharedExpensesService/SharedExpensesServices";

const CreateGroupPage = () => {
  const [userId, setUserId] = useState("");
  const [groupName, setGroupName] = useState("");
  const [message, setMessage] = useState({ text: "", type: "" });

  const navigate = useNavigate();

  const handleCreateGroup = async () => {
    if (!userId || !groupName) {
      setMessage({ text: "Both fields are required!", type: "error" });
      return;
    }

    try {
      const response = await createSharedGroup({ user_id: userId, group_name: groupName });
      setMessage({ text: `Group "${response.group_name}" created successfully!`, type: "success" });
      setUserId("");
      setGroupName("");
      // Navigate only after successful creation
      navigate("/GroupParticipantsPage");
    } catch (error) {
      setMessage({ text: "Error creating group. Please try again.", type: "error" });
      console.error("Error:", error);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <div className="bg-white p-6 rounded-lg shadow-lg w-96">
        <h2 className="text-2xl font-semibold text-center mb-4">Create Shared Group</h2>

        {message.text && (
          <div
            className={`text-sm text-center p-2 rounded-md mb-4 ${
              message.type === "success" ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
            }`}
          >
            {message.text}
          </div>
        )}

        <input
          type="text"
          placeholder="Enter User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="w-full border p-2 rounded-md mb-3 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <input
          type="text"
          placeholder="Enter Group Name"
          value={groupName}
          onChange={(e) => setGroupName(e.target.value)}
          className="w-full border p-2 rounded-md mb-3 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        <button
          onClick={handleCreateGroup}
          className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition"
        >
          Create Group
        </button>
      </div>
    </div>
  );
};

export default CreateGroupPage;
