import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Camera, TrendingUp, History, Award } from 'lucide-react';
import { userAPI, foodAPI } from '../services/api';
import './Dashboard.css';

function Dashboard({ user }) {
  const [stats, setStats] = useState(null);
  const [recentScans, setRecentScans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, historyRes] = await Promise.all([
        userAPI.getStats(),
        foodAPI.getHistory({ limit: 5 }),
      ]);

      setStats(statsRes.data);
      setRecentScans(historyRes.data.history);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getHealthBadge = (status) => {
    const badges = {
      healthy: { emoji: '✅', text: 'Healthy', class: 'healthy' },
      moderate: { emoji: '⚠️', text: 'Moderate', class: 'moderate' },
      unhealthy: { emoji: '❌', text: 'Unhealthy', class: 'unhealthy' },
    };
    return badges[status] || badges.moderate;
  };

  if (loading) {
    return (
      <div className="container">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="container">
        <div className="dashboard-header">
          <div>
            <h1>Welcome back, {user?.name}! 👋</h1>
            <p>Track your nutrition and make healthier choices</p>
          </div>
          <Link to="/scanner" className="btn btn-primary">
            <Camera size={20} />
            Scan Food
          </Link>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#dbeafe' }}>
              📊
            </div>
            <div className="stat-content">
              <h3>{stats?.total_scans || 0}</h3>
              <p>Total Scans</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#d1fae5' }}>
              ✅
            </div>
            <div className="stat-content">
              <h3>{stats?.healthy_count || 0}</h3>
              <p>Healthy Foods</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#fef3c7' }}>
              ⚠️
            </div>
            <div className="stat-content">
              <h3>{stats?.moderate_count || 0}</h3>
              <p>Moderate Foods</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{ background: '#fee2e2' }}>
              ❌
            </div>
            <div className="stat-content">
              <h3>{stats?.unhealthy_count || 0}</h3>
              <p>Unhealthy Foods</p>
            </div>
          </div>
        </div>

        <div className="dashboard-grid">
          <div className="card">
            <div className="card-header">
              <h2>Recent Scans</h2>
              <Link to="/history" className="view-all-link">
                View All →
              </Link>
            </div>
            <div className="card-body">
              {recentScans.length === 0 ? (
                <div className="empty-state">
                  <Camera size={48} color="#d1d5db" />
                  <p>No scans yet</p>
                  <Link to="/scanner" className="btn btn-secondary">
                    Scan Your First Food
                  </Link>
                </div>
              ) : (
                <div className="scans-list">
                  {recentScans.map((scan) => {
                    const badge = getHealthBadge(scan.health_score?.status);
                    return (
                      <div key={scan.id} className="scan-item">
                        <div className="scan-info">
                          <h4>{scan.food_name}</h4>
                          <p className="scan-date">
                            {new Date(scan.scanned_at).toLocaleDateString()}
                          </p>
                        </div>
                        <div className={`health-badge ${badge.class}`}>
                          <span>{badge.emoji}</span>
                          <span>{badge.text}</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          </div>

          <div className="card">
            <div className="card-header">
              <h2>Quick Actions</h2>
            </div>
            <div className="card-body">
              <div className="quick-actions">
                <Link to="/scanner" className="action-card">
                  <div className="action-icon" style={{ background: '#dbeafe' }}>
                    <Camera size={24} color="#3b82f6" />
                  </div>
                  <div>
                    <h4>Scan Food</h4>
                    <p>Analyze nutrition instantly</p>
                  </div>
                </Link>

                <Link to="/history" className="action-card">
                  <div className="action-icon" style={{ background: '#fef3c7' }}>
                    <History size={24} color="#f59e0b" />
                  </div>
                  <div>
                    <h4>View History</h4>
                    <p>Check past scans</p>
                  </div>
                </Link>

                <Link to="/insights" className="action-card">
                  <div className="action-icon" style={{ background: '#d1fae5' }}>
                    <TrendingUp size={24} color="#10b981" />
                  </div>
                  <div>
                    <h4>Insights</h4>
                    <p>Track your progress</p>
                  </div>
                </Link>
              </div>
            </div>
          </div>
        </div>

        {stats && stats.health_percentage >= 70 && (
          <div className="achievement-banner">
            <Award size={32} />
            <div>
              <h3>Great Job! 🎉</h3>
              <p>
                {stats.health_percentage}% of your scanned foods are healthy. Keep it up!
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
