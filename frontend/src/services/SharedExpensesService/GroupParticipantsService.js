import axios from "axios";

const API_URL = "http://127.0.0.1:8004/shared-group";
//const API_URL = "http://127.0.0.1:8004";


const GroupParticipantsService = {
    getGroups: async (participantId) => {
        try {
          const response = await axios.get(`${API_URL}/shared_groups/${participantId}`);
          return response.data;
        } catch (error) {
          console.error("Error fetching groups:", error);
          throw error;
        }
      },
      
    getParticipants: async (groupId) => {
        const response = await axios.get(`${API_URL}/participants/${groupId}`);
        return response.data;
      },
      
    addParticipant: async (groupId, participantUserId) => {
        const response = await axios.post(`${API_URL}/`, {
          group_id: groupId,
          participant_user_id: participantUserId,
        });
        return response.data;
      },
      
      // deleteParticipant: async (participantId, groupId) => {
      //   console.log(`Deleting participant ${participantId} from group ${groupId}`);
      //   await axios.delete(`${API_URL}/participants/${participantId}/${groupId}`);
      // },

    deleteParticipant: async (participantId) => {
        const response = await axios.delete(`${API_URL}/${participantId}`);
        return response.data;
      },
      
      
      
      
      // getAllUsers: async (groupId) => {
      //   const response = await axios.get(`${API_URL}/participants/${groupId}`);
      //   return response.data;
      // },


    getAllUsers: async () => {
        const response = await axios.get(`${API_URL}/users/`);
        return response.data;
      },
    
  };

export default GroupParticipantsService;
