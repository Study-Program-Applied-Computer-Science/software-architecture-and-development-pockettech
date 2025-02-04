import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";
import Cookies from "js-cookie";

// API base URL
const API_URL = "http://localhost:8002"; // Replace with your actual FastAPI URL

// Async thunk for login
export const loginUser = createAsyncThunk(
  "auth/loginUser",
  async (credentials, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_URL}/login`, credentials, {
        withCredentials: true, // Allows cookies to be stored
      });

      return response.data; // { access_token, id }
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

// Async thunk for verifying token
export const verifyUser = createAsyncThunk(
  "auth/verifyUser",
  async (_, { rejectWithValue }) => {
    try {
      const token = Cookies.get("access_token");
      if (!token) throw new Error("No token found");

      const response = await axios.get(`${API_URL}/verifytoken`, {
        headers: { Authorization: `Bearer ${token}` },
        withCredentials: true,
      });

      return response.data; // { user_id, roles }
    } catch (error) {
      return rejectWithValue(error.response?.data || "Unauthorized");
    }
  }
);

// Async thunk for logout
export const logoutUser = createAsyncThunk("auth/logoutUser", async () => {
  Cookies.remove("access_token");
  sessionStorage.clear();
  localStorage.removeItem("persistedState");
});

const authSlice = createSlice({
  name: "auth",
  initialState: {
    user: null,
    token: Cookies.get("access_token") || null,
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.loading = false;
        state.user = { id: action.payload.id };
        state.token = action.payload.access_token;
        Cookies.set("access_token", action.payload.access_token, { expires: 1 }); // Expires in 1 day
        sessionStorage.setItem("user", JSON.stringify({ id: action.payload.id }));
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "Login failed";
      })
      .addCase(verifyUser.fulfilled, (state, action) => {
        state.user = { id: action.payload.user_id, roles: action.payload.roles };
      })
      .addCase(logoutUser.fulfilled, (state) => {
        state.user = null;
        state.token = null;
      });
  },
});

export default authSlice.reducer;
