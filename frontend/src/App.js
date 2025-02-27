import React, { useState, useEffect } from "react";
import axios from "axios";
import Login from "./Login";

const App = () => {
    const [token, setToken] = useState(localStorage.getItem("token") || "");
    const [books, setBooks] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchBooks = async () => {
            try {
                const response = await axios.get("https://127.0.0.1:8000/api/books/", {
                    headers: { Authorization: `Bearer ${token}` },
                    withCredentials: false, // Nie przesyłamy cookies
                });
                setBooks(response.data);
                setError("");
            } catch (err) {
                setError("Failed to fetch books. Please log in again.");
                console.error("Error fetching books:", err);
            }
        };

        if (token) {
            fetchBooks();
        }
    }, [token]);

    const handleLogout = () => {
        setToken("");
        localStorage.removeItem("token");
    };

    return (
        <div>
            {!token ? (
                <Login setToken={setToken} />
            ) : (
                <div>
                    <h1>Library Management</h1>
                    {error && <p style={{ color: "red" }}>{error}</p>}
                    <ul>
                        {books.map((book) => (
                            <li key={book.id}>
                                {book.title} - {book.author}
                            </li>
                        ))}
                    </ul>
                    <button onClick={handleLogout}>Logout</button>
                </div>
            )}
        </div>
    );
};

export default App;
