import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import GroupParticipantsService from "../services/SharedExpensesService/GroupParticipantsService";

const GroupParticipantsPage = () => {
  const [groups, setGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [participants, setParticipants] = useState([]);
  const [selectedParticipants, setSelectedParticipants] = useState([]);
  const [allUsers, setAllUsers] = useState([]);
  const [newParticipant, setNewParticipant] = useState("");

  const navigate = useNavigate();
  const location = useLocation();
  const participantId = location.state?.userId; 
  const API_URL = "http://localhost:8004/shared-group";

  useEffect(() => {
    if (participantId) fetchGroups(participantId);
  }, [participantId]);

  const fetchGroups = async (participantId) => {
    try {
      const response = await fetch(`${API_URL}/shared_groups/${participantId}`);
      if (!response.ok) throw new Error("Error fetching groups");

      const data = await response.json();
      setGroups(data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleGroupChange = async (groupId) => {
    setSelectedGroup(groupId);
    fetchParticipants(groupId);
  };

  const fetchParticipants = async (groupId) => {
    try {
      const data = await GroupParticipantsService.getParticipants(groupId);
      setParticipants(data.participants || []);
    } catch (error) {
      console.error("Error fetching participants:", error);
    }
  };

  const handleCheckboxChange = (id) => {
    setSelectedParticipants((prev) =>
      prev.includes(id) ? prev.filter((pId) => pId !== id) : [...prev, id]
    );
  };

  const handleDeleteParticipants = async () => {
    if (!selectedGroup || selectedParticipants.length === 0) {
      alert("Please select a group and at least one participant to delete.");
      return;
    }

    try {
      await Promise.all(
        selectedParticipants.map((participantId) =>
          GroupParticipantsService.deleteParticipant(participantId)
        )
      );
      fetchParticipants(selectedGroup);
      setSelectedParticipants([]);
    } catch (error) {
      console.error("Error deleting participants:", error);
    }
  };

  const fetchAllUsers = async () => {
    if (!selectedGroup) {
      alert("Please select a group first.");
      return;
    }

    try {
      const data = await GroupParticipantsService.getAllUsers(selectedGroup);
      setAllUsers(data);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  const handleAddParticipant = async () => {
    if (!selectedGroup || !newParticipant) {
      alert("Please select a group and a participant.");
      return;
    }

    try {
      await GroupParticipantsService.addParticipant(selectedGroup, newParticipant);
      fetchParticipants(selectedGroup);
      setNewParticipant("");
    } catch (error) {
      console.error("Error adding participant:", error);
    }
  };

  const handleNavigate = () => {
    if (selectedGroup) {
      navigate(`/SharedTransactionsPage/${selectedGroup}`);
    } else {
      alert("Please select a group first.");
    }
  };

  return (
    <div className="flex flex-col items-center p-6 bg-white dark:bg-gray-800">
      <h1 className="text-3xl font-bold mb-4 text-black dark:text-white">Choose a Group</h1>

      <select
        className="p-2 border rounded-lg mb-4 bg-white dark:bg-gray-700 text-black dark:text-white"
        onChange={(e) => handleGroupChange(e.target.value)}
      >
        <option value="">Select a Group</option>
        {groups.map((group) => (
          <option key={group.id} value={group.id}>
            {group.group_name}
          </option>
        ))}
      </select>

      <h2 className="text-lg text-gray-600 mb-4 dark:text-gray-300">Group Participants</h2>

      <table className="w-full max-w-md border text-black dark:text-white">
        <thead>
          <tr>
            <th className="border p-2">Name</th>
            <th className="border p-2">Email</th>
            <th className="border p-2">Phone</th>
            <th className="border p-2">Select</th>
          </tr>
        </thead>
        <tbody>
          {participants.map((p) => (
            <tr key={p.id}>
              <td className="border p-2">{p.name}</td>
              <td className="border p-2">{p.email_id}</td>
              <td className="border p-2">{p.phone_number}</td>
              <td className="border p-2">
                <input
                  type="checkbox"
                  onChange={() => handleCheckboxChange(p.id)}
                  checked={selectedParticipants.includes(p.id)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="mt-4 flex flex-col items-center">
        <button
          className="bg-green-600 text-white p-2 rounded-lg mb-2 hover:bg-green-700"
          onClick={fetchAllUsers}
        >
          Add Participant
        </button>

        {allUsers.length > 0 && (
          <select
            className="p-2 border rounded-lg mb-2 bg-white dark:bg-gray-700 text-black dark:text-white"
            onChange={(e) => setNewParticipant(e.target.value)}
          >
            <option value="">Select a Participant</option>
            {allUsers.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name}
              </option>
            ))}
          </select>
        )}

        {newParticipant && (
          <button
            className="bg-blue-600 text-white p-2 rounded-lg mb-2 hover:bg-blue-700"
            onClick={handleAddParticipant}
          >
            Confirm Add
          </button>
        )}
      </div>

      <button
        className="bg-red-600 text-white p-2 rounded-lg mb-2 hover:bg-red-700"
        onClick={handleDeleteParticipants}
      >
        Delete Selected Participants
      </button>

      <button
        className="bg-gray-600 text-white p-2 rounded-lg hover:bg-gray-700"
        onClick={handleNavigate}
      >
        Go to Shared Transactions
      </button>
    </div>
  );
};

export default GroupParticipantsPage;
