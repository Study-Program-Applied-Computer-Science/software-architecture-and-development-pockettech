import React, { useState } from "react";
import { createUser } from "../services/UserService/userService"; // Import the createUser service
import { useNavigate } from "react-router-dom"; // Import the useNavigate hook

const CreateUserPage = () => {
  const [formData, setFormData] = useState({
    name: "",
    email_id: "",
    password: "",
    country_id: "",
    phone_number: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const navigate = useNavigate(); // Initialize useNavigate

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  // Handle country selection, update country_id
  const handleCountryChange = (e) => {
    const country = e.target.value;
    setFormData({
      ...formData,
      country_id: country, // Set country_id to the country name
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    const countryMapping = {
      India: 2,
      Germany: 3,
      USA: 1,
    };

    const formDataWithCountryId = {
      ...formData,
      country_id: countryMapping[formData.country_id] || "",
    };

    try {
      const newUser = await createUser(formDataWithCountryId); // Call createUser service
      setSuccess("User created successfully!");
      console.log("Response Data:", newUser);
      alert("User created successfully!");
      navigate("/"); // Redirect to login page after successful user creation
    } catch (err) {
      console.error("User creation failed:", err);
      setError(err.message || "Failed to create user. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 text-gray-900">
      <div className="w-full max-w-md p-8 rounded-lg shadow-lg bg-white">
        <h1 className="text-3xl font-bold text-center mb-6">Create a New Account</h1>
        
        {error && <div className="text-red-500 text-center mb-4">{error}</div>}
        {success && <div className="text-green-500 text-center mb-4">{success}</div>}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="name" className="block text-sm font-medium mb-1">Full Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="w-full px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Full Name"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="email_id" className="block text-sm font-medium mb-1">Email Address</label>
            <input
              type="email"
              id="email_id"
              name="email_id"
              value={formData.email_id}
              onChange={handleChange}
              className="w-full px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="you@example.com"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="password" className="block text-sm font-medium mb-1">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="w-full px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="*******"
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="country_id" className="block text-sm font-medium mb-1">Country</label>
            <select
              id="country_id"
              name="country_id"
              value={formData.country_id} // This will be one of "India", "Germany", or "USA"
              onChange={handleCountryChange}
              className="w-full px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="" disabled>Select Country</option>
              <option value="India">India</option>
              <option value="Germany">Germany</option>
              <option value="USA">USA</option>
            </select>
          </div>

          <div className="mb-4">
            <label htmlFor="phone_number" className="block text-sm font-medium mb-1">Phone Number</label>
            <input
              type="text"
              id="phone_number"
              name="phone_number"
              value={formData.phone_number}
              onChange={handleChange}
              className="w-full px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Phone Number"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full py-2 rounded-lg font-medium bg-blue-500 hover:bg-blue-600 text-white"
            disabled={loading}
          >
            {loading ? "Creating..." : "Create Account"}
          </button>
        </form>

        <p className="text-sm text-center mt-4">
          Already have an account?{" "}
          <a href="/login" className="text-blue-600 hover:underline">Login here</a>
        </p>
      </div>
    </div>
  );
};

export default CreateUserPage;