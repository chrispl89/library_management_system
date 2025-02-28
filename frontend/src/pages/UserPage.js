import React, { useEffect, useState } from "react";
import api from "../services/api";

const UserPage = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get("/user/profile");
        setUser(response.data);
      } catch (err) {
        setError("Error fetching user profile");
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  if (loading) return <p>Loading user information...</p>;
  if (error) return <p>{error}</p>;
  if (!user) return <p>No user data available</p>;

  return (
    <div>
      <h1>User Profile</h1>
      <p>Username: {user.username}</p>
      <p>Email: {user.email}</p>
      {/* Dodaj inne informacje o użytkowniku */}
    </div>
  );
};

export default UserPage;
