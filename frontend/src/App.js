import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import ChatbotPage from './components/ChatbotPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <div className="content-area">
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/chat" element={<ChatbotPage />} />
            <Route path="*" element={<Navigate to="/dashboard" />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
