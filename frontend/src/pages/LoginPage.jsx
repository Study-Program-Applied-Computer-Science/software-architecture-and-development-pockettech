import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; 
import { loginUser } from "../services/AuthService/authService"; 

export default function LoginPage({ isDarkMode }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const navigate = useNavigate(); 

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const data = await loginUser(email, password);
      setSuccess("Login successful!");
      console.log("Response Data:", data);
      localStorage.setItem("user_id", data.id);
      navigate("/dashboard"); 
    } catch (err) {
      console.error("Login failed:", err);
      setError(err.message || "Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className={`min-h-screen flex items-center justify-center ${
        isDarkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-gray-900"
      }`}
    >
      <div
        className={`w-full max-w-md p-8 rounded-lg shadow-lg ${
          isDarkMode ? "bg-gray-800 text-white" : "bg-white text-gray-900"
        }`}
      >
        <h1 className="text-3xl font-bold text-center mb-6">
          Login to Your Account
        </h1>
        {error && (
          <div className="text-red-500 text-center mb-4">{error}</div>
        )}
        {success && (
          <div className="text-green-500 text-center mb-4">{success}</div>
        )}
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <label
              htmlFor="email"
              className="block text-sm font-medium mb-1"
            >
              Email Address
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={`w-full px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                isDarkMode ? "bg-gray-700 text-white" : "bg-gray-100 text-gray-900"
              }`}
              placeholder="you@example.com"
              required
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="password"
              className="block text-sm font-medium mb-1"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={`w-full px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                isDarkMode ? "bg-gray-700 text-white" : "bg-gray-100 text-gray-900"
              }`}
              placeholder="*******"
              required
            />
          </div>
          <button
            type="submit"
            className={`w-full py-2 rounded-lg font-medium ${
              isDarkMode
                ? "bg-blue-600 hover:bg-blue-700 text-white"
                : "bg-blue-500 hover:bg-blue-600 text-white"
            }`}
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
        <p className="text-sm text-center mt-4">
          Don’t have an account?{" "}
          <a
            href="/create-user"
            className={`${
              isDarkMode
                ? "text-blue-400 hover:underline"
                : "text-blue-600 hover:underline"
            }`}
          >
            Sign up
          </a>
        </p>
      </div>
    </div>
  );
}
