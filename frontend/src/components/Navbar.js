import React from "react";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";

const Navbar = () => {
  const token = useSelector((state) => state.auth.token);
  
  return (
    <nav>
      <ul style={{ listStyle: "none", display: "flex", gap: "1rem" }}>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/books">Books</Link>
        </li>
        {token ? (
          <>
            <li>
              <Link to="/user">Profile</Link>
            </li>
            <li>
              <Link to="/logout">Logout</Link>
            </li>
          </>
        ) : (
          <>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/register">Register</Link>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
