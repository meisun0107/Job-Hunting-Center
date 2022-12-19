import React from "react";
import './App.css';
import Header from './components/Header/Header';
import Footer from "./components/Footer/Footer";
import Discover from "./components/Discover/Discover";
import Homepage from './components/Homepage/Homepage';
import Login from './components/Login/Login';
import Register from "./components/Register/Register";
import UserProfile from "./components/Profile/UserProfile";
import CompanyProfile from "./components/Profile/CompanyProfile";
import ExactMatch from "./components/Match/ExactMatch";
import QuickMatch from "./components/Match/QuickMatch";
import MarketAnalysis from "./components/MarketAnalysis/MarketAnalysis";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Header />
      </header>
        <Routes>
          <Route exact path="/" element={<Homepage />} />
          <Route path="/home" element={<Homepage />} />
          <Route path="/discover" element={<Discover />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/user-profile" element={<UserProfile />} />
          <Route path="/company-profile" element={<CompanyProfile />} />
          <Route path="/exact-match" element={<ExactMatch />} />
          <Route path="/quick-match" element={<QuickMatch />} />
          <Route path="/market-analysis" element={<MarketAnalysis />} />
        </Routes>
      <Footer />
      

    </div>
  );
}

export default App;
