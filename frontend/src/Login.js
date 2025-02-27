import React, { useState } from "react";
import axios from "axios";

const Login = ({ setToken }) => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();
        
        if (!username || !password) {
            setError("Username and password cannot be empty.");
            return;
        }

        try {
            const response = await axios.post(
                "https://127.0.0.1:8000/api/token/",
                { username, password },
                {
                    headers: { "Content-Type": "application/json" },
                    withCredentials: false, // Nie przesyłamy cookies
                }
            );

            if (response.data && response.data.access) {
                const token = response.data.access;
                localStorage.setItem("token", token);
                setToken(token);
                setError(""); // Czyszczenie błędu po udanym logowaniu
                console.log("Login successful, token saved.");
            } else {
                setError("Invalid login response.");
            }
        } catch (err) {
            setError("Login failed. Check your credentials.");
            console.error("Login error:", err.response?.data || err.message);
        }
    };

    return (
        <div>
            <h2>Login</h2>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <form onSubmit={handleLogin}>
                <div>
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;
