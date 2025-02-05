import React, { useEffect, useState } from "react";
import { getUserDetails } from "../services/UserService/userService"; // Import the getUserDetails service
import { updateUser } from "../services/UserService/userService"; // Import the updateUser service

const UserProfile = () => {
  const [userDetails, setUserDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [isEditing, setIsEditing] = useState(false); // Track if user is editing the profile
  const [formData, setFormData] = useState({
    name: "",
    email_id: "",
    phone_number: "",
  });

  useEffect(() => {
    const fetchUserDetails = async () => {
      setError("");
      setLoading(true);

      try {
        const userId = localStorage.getItem("user_id");
        console.log("User identification:", userId);

        // Fetch user details using the service
        const data = await getUserDetails(userId);
        setUserDetails(data);
        setFormData({
          name: data.name,
          email_id: data.email_id,
          phone_number: data.phone_number,
        });
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUserDetails();
  }, []); // Only run once when the component mounts

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setFormData({
      name: userDetails.name,
      email_id: userDetails.email_id,
      phone_number: userDetails.phone_number,
    });
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const userId = localStorage.getItem("user_id");
      const updatedData = await updateUser(userId, formData); // Call updateUser service
      setUserDetails(updatedData); // Update state with new data
      setIsEditing(false); // Stop editing mode
    } catch (err) {
      setError(err.message || "Failed to update user details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <div className="flex items-center justify-center min-h-screen">
        <div className="bg-white shadow-lg rounded-lg p-8 max-w-lg w-full">
          <h1 className="text-2xl font-bold mb-6 text-center">User Profile</h1>

          {loading && <p className="text-center text-blue-600">Loading...</p>}

          {error && <p className="text-center text-red-500">{error}</p>}

          {userDetails && (
            <div className="space-y-4">
              {isEditing ? (
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <label className="block font-medium">First Name</label>
                    <input
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      className="w-full px-3 py-2 rounded"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block font-medium">Email</label>
                    <input
                      type="email"
                      name="email_id"
                      value={formData.email_id}
                      onChange={handleChange}
                      className="w-full px-3 py-2 rounded"
                      required
                    />
                  </div>
                  <div>
                    <label className="block font-medium">Phone Number</label>
                    <input
                      type="text"
                      name="phone_number"
                      value={formData.phone_number}
                      onChange={handleChange}
                      className="w-full px-3 py-2 rounded"
                      required
                    />
                  </div>
                  <div className="flex justify-between">
                    <button
                      type="button"
                      onClick={handleCancel}
                      className="bg-gray-500 text-white py-2 px-4 rounded"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      className="bg-blue-500 text-white py-2 px-4 rounded"
                    >
                      Save Changes
                    </button>
                  </div>
                </form>
              ) : (
                <div>
                  <p><strong>Full Name:</strong> {userDetails.name}</p>
                  <p><strong>Email:</strong> {userDetails.email_id}</p>
                  <p><strong>Phone Number:</strong> {userDetails.phone_number}</p>
                  <button
                    onClick={handleEdit}
                    className="mt-4 bg-blue-500 text-white py-2 px-4 rounded"
                  >
                    Edit Profile
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserProfile;