import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";

const BookDetails = () => {
  const { id } = useParams();
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBook = async () => {
      try {
        const response = await api.get(`/books/${id}`);
        setBook(response.data);
      } catch (err) {
        setError("Error fetching book details");
      } finally {
        setLoading(false);
      }
    };

    fetchBook();
  }, [id]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!book) return <p>No book found</p>;

  return (
    <div>
      <h2>{book.title}</h2>
      <p>{book.description}</p>
      {/* Możesz dodać więcej szczegółów, np. autora, datę wydania itp. */}
    </div>
  );
};

export default BookDetails;
