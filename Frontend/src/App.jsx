import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar/Navbar';
import Home from './pages/Home';
import SafeZoneFinder from './pages/SafeZoneFinder';
// Import other pages as needed
// import About from './pages/About';
import './App.css';

const App = () => {
  return (
    <Router>
      <Navbar /> {/* Navbar will be visible on all pages */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/safeZone" element={<SafeZoneFinder />} />
        {/* Add more routes as needed */}
      </Routes>
    </Router>
  );
};

export default App;