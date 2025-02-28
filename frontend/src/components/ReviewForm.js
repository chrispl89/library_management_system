import React, { useState } from "react";
import api from "../services/api";

const ReviewForm = ({ bookId }) => {
  const [review, setReview] = useState("");
  const [rating, setRating] = useState(1);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Zakładamy, że endpoint do dodawania recenzji to: /books/:bookId/reviews
      await api.post(`/books/${bookId}/reviews`, { review, rating });
      setMessage("Review added successfully!");
    } catch (err) {
      setMessage("Failed to add review");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Add Review</h2>
      <div>
        <label>Rating (1-5):</label>
        <input
          type="number"
          value={rating}
          onChange={(e) => setRating(Number(e.target.value))}
          min="1"
          max="5"
          required
        />
      </div>
      <div>
        <label>Review:</label>
        <textarea
          value={review}
          onChange={(e) => setReview(e.target.value)}
          required
        />
      </div>
      <button type="submit">Submit</button>
      {message && <p>{message}</p>}
    </form>
  );
};

export default ReviewForm;
