import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Provider } from "react-redux";
import store from "./store/store";
import HomePage from "./pages/HomePage";
import BooksPage from "./pages/BooksPage";
import UserPage from "./pages/UserPage";
import AdminPage from "./pages/AdminPage";
import LoginForm from "./components/LoginForm";
import RegistrationForm from "./components/RegistrationForm";
import Navbar from "./components/Navbar";
import BookDetails from "./components/BookDetails";
import ReviewForm from "./components/ReviewForm";
import api from "./services/api";

function App() {
  return (
    <Provider store={store}>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/books" element={<BooksPage />} />
          <Route path="/books/:id" element={<BookDetails />} />
          <Route path="/user" element={<UserPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/register" element={<RegistrationForm />} />
          <Route path="/review" element={<ReviewForm />} />
        </Routes>
      </Router>
    </Provider>
  );
}

export default App;
