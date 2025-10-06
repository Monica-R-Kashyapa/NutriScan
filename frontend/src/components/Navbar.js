import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Camera, History, BarChart3, LogOut, User } from 'lucide-react';
import './Navbar.css';

function Navbar({ user, onLogout }) {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/dashboard" className="navbar-brand">
          <span className="brand-icon">🍎</span>
          <span className="brand-text">NutriScan</span>
        </Link>

        <div className="navbar-menu">
          <Link to="/dashboard" className={`nav-link ${isActive('/dashboard')}`}>
            <Home size={20} />
            <span>Dashboard</span>
          </Link>
          <Link to="/scanner" className={`nav-link ${isActive('/scanner')}`}>
            <Camera size={20} />
            <span>Scan Food</span>
          </Link>
          <Link to="/history" className={`nav-link ${isActive('/history')}`}>
            <History size={20} />
            <span>History</span>
          </Link>
          <Link to="/insights" className={`nav-link ${isActive('/insights')}`}>
            <BarChart3 size={20} />
            <span>Insights</span>
          </Link>
        </div>

        <div className="navbar-user">
          <div className="user-info">
            <User size={20} />
            <span>{user?.name || user?.email}</span>
          </div>
          <button onClick={onLogout} className="logout-btn">
            <LogOut size={20} />
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
