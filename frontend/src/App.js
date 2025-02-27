import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [books, setBooks] = useState([]);
  const [isLibrarian, setIsLibrarian] = useState(false);
  const [newBook, setNewBook] = useState({ title: '', author: '', year: '', genre: '' });

  // Fetch the list of books from the API
  useEffect(() => {
    axios.get('http://localhost:5000/api/books') // Ensure this endpoint matches your API
      .then(response => setBooks(response.data))
      .catch(error => console.error('Error fetching books:', error));
  }, []);

  // Function to add a new book
  const addBook = () => {
    axios.post('http://localhost:5000/api/books', newBook)
      .then(response => {
        setBooks([...books, response.data]);
        setNewBook({ title: '', author: '', year: '', genre: '' });
      })
      .catch(error => console.error('Error adding book:', error));
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Library</h1>
      <button onClick={() => setIsLibrarian(!isLibrarian)}>
        Switch Mode: {isLibrarian ? 'User' : 'Librarian'}
      </button>
      
      {isLibrarian && (
        <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ccc' }}>
          <h2>Add Book</h2>
          <div>
            <input
              type="text"
              placeholder="Title"
              value={newBook.title}
              onChange={(e) => setNewBook({ ...newBook, title: e.target.value })}
            />
          </div>
          <div>
            <input
              type="text"
              placeholder="Author"
              value={newBook.author}
              onChange={(e) => setNewBook({ ...newBook, author: e.target.value })}
            />
          </div>
          <div>
            <input
              type="number"
              placeholder="Year"
              value={newBook.year}
              onChange={(e) => setNewBook({ ...newBook, year: e.target.value })}
            />
          </div>
          <div>
            <input
              type="text"
              placeholder="Genre"
              value={newBook.genre}
              onChange={(e) => setNewBook({ ...newBook, genre: e.target.value })}
            />
          </div>
          <button onClick={addBook}>Add</button>
        </div>
      )}

      <h2 style={{ marginTop: '30px' }}>Books List</h2>
      <ul>
        {books.map(book => (
          <li key={book.id}>
            <strong>{book.title}</strong> – {book.author} ({book.year}) [{book.genre}]
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
