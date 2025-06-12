import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-header">
        <h2>Admin Panel</h2>
      </div>
      <ul className="nav-links">
        <li>
          <NavLink 
            to="/dashboard" 
            className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}
          >
            <i className="nav-icon dashboard-icon"></i>
            <span>Dashboard</span>
          </NavLink>
        </li>
        <li>
          <NavLink 
            to="/chat" 
            className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}
          >
            <i className="nav-icon chat-icon"></i>
            <span>Chatbot</span>
          </NavLink>
        </li>
      </ul>
      <div className="navbar-footer">
        <div className="user-info">
          <div className="user-avatar">A</div>
          <div className="user-name">Admin</div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;