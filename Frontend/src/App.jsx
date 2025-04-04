import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar/Navbar';
import Home from './pages/Home';
import SafeZoneFinder from './pages/SafeZoneFinder';
// import Chatbot from './components/Chatbotfrontend/chatbot';/
import ChatBot from './components/Chatbot_frontend/chatbot';
import FindRoute from './pages/FindRoute';
// Import other pages as needed
// import About from './pages/About';
// import data from "./components/data/data.json"
import './App.css';

const App = () => {
  return (
    <Router>
      <Navbar/> 
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/safeZone" element={<SafeZoneFinder />} />
        <Route path='/findRoute' element={<FindRoute />} />
        <Route path='/chatbot' element={<ChatBot />} />
        {/* Add more routes as needed */}
      </Routes>
    </Router>
  );
};

export default App;