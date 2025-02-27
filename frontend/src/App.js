import React, { useState, useEffect } from "react";
import axios from "axios";
import Login from "./Login";

const App = () => {
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [books, setBooks] = useState([]);
  const [error, setError] = useState("");
  // Nowe książki – operujemy tylko na polach: title, author, category
  const [newBook, setNewBook] = useState({
    title: "",
    author: "",
    category: "",
  });
  // Edytowana książka – również tylko title, author, category (pozostałe pola są read-only)
  const [editingBook, setEditingBook] = useState(null);

  useEffect(() => {
    if (token) {
      fetchBooks();
    }
  }, [token]);

  const fetchBooks = async () => {
    try {
      const response = await axios.get("https://127.0.0.1:8000/api/books/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setBooks(response.data);
      setError("");
    } catch (err) {
      setError("Failed to fetch books. Please log in again.");
      console.error("Error fetching books:", err);
    }
  };

  const handleLogout = () => {
    setToken("");
    localStorage.removeItem("token");
  };

  const addBook = async (e) => {
    e.preventDefault();
    // Przyjmujemy, że backend tworzy pola "added_by" oraz "created_at" automatycznie
    const payload = {
      title: newBook.title,
      author: newBook.author,
      category: newBook.category,
    };

    try {
      const response = await axios.post(
        "https://127.0.0.1:8000/api/books/",
        payload,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      // Aktualizujemy listę książek – API powinno zwrócić pełny obiekt
      setBooks([...books, response.data]);
      setNewBook({ title: "", author: "", category: "" });
      setError("");
    } catch (err) {
      setError("Failed to add book.");
      console.error("Error adding book:", err.response?.data || err);
    }
  };

  const deleteBook = async (bookId) => {
    try {
      await axios.delete(`https://127.0.0.1:8000/api/books/${bookId}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setBooks(books.filter((book) => book.id !== bookId));
      setError("");
    } catch (err) {
      setError("Failed to delete book.");
      console.error("Error deleting book:", err);
    }
  };

  // Ustawiamy pola edycji na wartości książki; tylko title, author, category będą edytowalne
  const startEditing = (book) => {
    setEditingBook({
      id: book.id,
      title: book.title || "",
      author: book.author || "",
      category: book.category || "",
    });
  };

  const updateBook = async (e) => {
    e.preventDefault();
    const payload = {
      title: editingBook.title,
      author: editingBook.author,
      category: editingBook.category,
    };
    try {
      const response = await axios.put(
        `https://127.0.0.1:8000/api/books/${editingBook.id}/`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      setBooks(
        books.map((book) =>
          book.id === editingBook.id ? response.data : book
        )
      );
      setEditingBook(null);
      setError("");
    } catch (err) {
      setError("Failed to update book.");
      console.error("Error updating book:", err.response?.data || err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      {!token ? (
        <Login setToken={setToken} />
      ) : (
        <div>
          <h1>Library Management</h1>
          {error && <p style={{ color: "red" }}>{error}</p>}
          <button onClick={handleLogout}>Logout</button>

          <h2>Books List</h2>
          <ul>
            {books.map((book) => (
              <li key={book.id}>
                <strong>{book.title}</strong> - {book.author} - {book.category}{" "}
                - <em>{book.added_by}</em> - {book.created_at}
                <button onClick={() => startEditing(book)}>Edit</button>
                <button onClick={() => deleteBook(book.id)}>Delete</button>
              </li>
            ))}
          </ul>

          <h2>Add New Book</h2>
          <form onSubmit={addBook}>
            <input
              type="text"
              placeholder="Title"
              value={newBook.title}
              onChange={(e) =>
                setNewBook({ ...newBook, title: e.target.value })
              }
              required
            />
            <input
              type="text"
              placeholder="Author"
              value={newBook.author}
              onChange={(e) =>
                setNewBook({ ...newBook, author: e.target.value })
              }
              required
            />
            <input
              type="text"
              placeholder="Category"
              value={newBook.category}
              onChange={(e) =>
                setNewBook({ ...newBook, category: e.target.value })
              }
              required
            />
            <button type="submit">Add Book</button>
          </form>

          {editingBook && (
            <div>
              <h2>Edit Book</h2>
              <form onSubmit={updateBook}>
                <input
                  type="text"
                  placeholder="Title"
                  value={editingBook.title || ""}
                  onChange={(e) =>
                    setEditingBook({
                      ...editingBook,
                      title: e.target.value,
                    })
                  }
                  required
                />
                <input
                  type="text"
                  placeholder="Author"
                  value={editingBook.author || ""}
                  onChange={(e) =>
                    setEditingBook({
                      ...editingBook,
                      author: e.target.value,
                    })
                  }
                  required
                />
                <input
                  type="text"
                  placeholder="Category"
                  value={editingBook.category || ""}
                  onChange={(e) =>
                    setEditingBook({
                      ...editingBook,
                      category: e.target.value,
                    })
                  }
                  required
                />
                <button type="submit">Update Book</button>
                <button onClick={() => setEditingBook(null)}>Cancel</button>
              </form>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default App;
