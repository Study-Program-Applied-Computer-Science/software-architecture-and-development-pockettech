import React, { useState, useEffect } from "react";
import GroupParticipantsService from "../services/SharedExpensesService/GroupParticipantsService";
import { useNavigate } from "react-router-dom";

const GroupParticipantsPage = () => {
  const [groups, setGroups] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [participants, setParticipants] = useState([]);
  const [selectedParticipants, setSelectedParticipants] = useState([]);
  const [allUsers, setAllUsers] = useState([]);
  const [newParticipant, setNewParticipant] = useState("");


  
  const handleNavigate = () => {
    if (selectedGroup) {
      navigate(`/SharedTransactionsPage/${selectedGroup}`);
    } else {
      alert("Please select a group first.");
    }
  };

  const API_URL = "http://127.0.0.1:8004/shared-group";


//TODO at session management
  const participantId = "afa42e1a-628f-4a06-9771-47e85344ca85"; 

  useEffect(() => {
    fetchGroups(participantId);
  }, []);

  const fetchGroups = async (participantId) => {
    try {
      const data = await GroupParticipantsService.getGroups(participantId);
      setGroups(data);
    } catch (error) {
      console.error("Error fetching groups:", error);
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

  const handleCheckboxChange = (participantId) => {
    setSelectedParticipants((prev) =>
      prev.includes(participantId)
        ? prev.filter((id) => id !== participantId)
        : [...prev, participantId]
    );
  };

  const handleDeleteParticipants = async () => {
    if (!selectedGroup) {
      console.error("No group selected.");
      return;
    }
  
    if (selectedParticipants.length === 0) {
      console.error("No participants selected.");
      return;
    }
  
    try {
      for (const participantId of selectedParticipants) {
        const deleteUrl = `${API_URL}/${participantId}`;
        console.log(`Attempting DELETE: ${deleteUrl}`);
  
        console.log('participantId:', participantId);
        await GroupParticipantsService.deleteParticipant(participantId);
      }
    try {
      const participants = await fetchParticipants(selectedGroup); // Refresh list
      console.log(participants)
      setSelectedParticipants([]); // Clear selection
      } catch (error) {
        console.log("Error updating list")
      }
    } catch (error) {
      console.error("Error deleting participants:", error);
    }
  };
  



  const fetchAllUsers = async () => {
    if (!selectedGroup) {
      console.error("Please select a group first.");
      return;
    }
  
    try {
      const data = await GroupParticipantsService.getAllUsers(selectedGroup); // Pass the selectedGroup
      setAllUsers(data);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };


   // Add Participant: First fetch the list of all users
//    const handleAddParticipant = async () => {
//     if (!newParticipant) return;

//     try {
//       // Fetch all users before adding the participant
//       const users = await GroupParticipantsService.getAllUsers();
//       setAllUsers(users);  // Set the list of all users
//       // Now perform the add operation after users are fetched
//       await GroupParticipantsService.addParticipant(selectedGroup, newParticipant);
//       fetchParticipants(selectedGroup);  // Refresh the participants list
//       setNewParticipant(""); // Clear the selected participant
//     } catch (error) {
//       console.error("Error adding participant:", error);
//     }
//   };


const handleAddParticipant = async () => {
  if (!selectedGroup) {
    console.error("No group selected.");
    return;
  }
  if (!newParticipant) {
    console.error("No participant selected.");
    return;
  }

  const payload = {
    group_id: selectedGroup,
    participant_user_id: newParticipant,
  };

  console.log("Adding participant:", payload);

  try {
    await GroupParticipantsService.addParticipant(selectedGroup, newParticipant);
    await fetchParticipants(selectedGroup); // Refresh the participants list
    setNewParticipant(""); // Clear the selected participant
  } catch (error) {
    console.error("Error adding participant:", error);
  }
};



  return (
    <div className="flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold mb-4">Choose the Group</h1>
      <select
        className="p-2 border rounded-lg mb-4"
        onChange={(e) => handleGroupChange(e.target.value)}
      >
        <option key="default-group" value="">Select a Group</option>
        {groups.map((group) => (
          <option key={group.id} value={group.id}>
            {group.group_name}
          </option>
        ))}
      </select>

      <h2 className="text-lg text-gray-600 mb-4">Below are the participants of the Group</h2>

      <table className="w-full max-w-md border">
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
          onClick={() => fetchAllUsers()}
        >
          ADD
        </button>
        {allUsers.length > 0 && (
          <select
            className="p-2 border rounded-lg mb-2"
            onChange={(e) => setNewParticipant(e.target.value)}
          >
            <option key="default-participant" value="">
              Select a participant
            </option>
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
            Add Participant
          </button>
        )}
      </div>

      <button
        className="bg-red-600 text-white p-2 rounded-lg mb-2 hover:bg-red-700"
        onClick={handleDeleteParticipants}
      >
        DELETE
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
