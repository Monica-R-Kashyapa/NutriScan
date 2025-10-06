import React, { useState, useEffect } from 'react';
import { Calendar, Search, Filter } from 'lucide-react';
import { foodAPI } from '../services/api';
import './History.css';

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await foodAPI.getHistory({ limit: 50 });
      setHistory(response.data.history);
    } catch (error) {
      console.error('Error fetching history:', error);
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

  const filteredHistory = history.filter((scan) => {
    const matchesSearch = scan.food_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || scan.health_score?.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  if (loading) {
    return (
      <div className="container">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="history">
      <div className="container">
        <div className="history-header">
          <div>
            <h1>📋 Scan History</h1>
            <p>View all your scanned foods and nutrition data</p>
          </div>
        </div>

        <div className="card">
          <div className="filters-section">
            <div className="search-box">
              <Search size={20} color="#9ca3af" />
              <input
                type="text"
                placeholder="Search foods..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>

            <div className="filter-buttons">
              <button
                className={`filter-btn ${filterStatus === 'all' ? 'active' : ''}`}
                onClick={() => setFilterStatus('all')}
              >
                All
              </button>
              <button
                className={`filter-btn ${filterStatus === 'healthy' ? 'active' : ''}`}
                onClick={() => setFilterStatus('healthy')}
              >
                ✅ Healthy
              </button>
              <button
                className={`filter-btn ${filterStatus === 'moderate' ? 'active' : ''}`}
                onClick={() => setFilterStatus('moderate')}
              >
                ⚠️ Moderate
              </button>
              <button
                className={`filter-btn ${filterStatus === 'unhealthy' ? 'active' : ''}`}
                onClick={() => setFilterStatus('unhealthy')}
              >
                ❌ Unhealthy
              </button>
            </div>
          </div>

          {filteredHistory.length === 0 ? (
            <div className="empty-state">
              <Calendar size={64} color="#d1d5db" />
              <p>
                {searchTerm || filterStatus !== 'all'
                  ? 'No results found'
                  : 'No scan history yet'}
              </p>
            </div>
          ) : (
            <div className="history-list">
              {filteredHistory.map((scan) => {
                const badge = getHealthBadge(scan.health_score?.status);
                return (
                  <div key={scan.id} className="history-item">
                    <div className="history-item-header">
                      <div className="history-item-info">
                        <h3>{scan.food_name}</h3>
                        <div className="history-item-meta">
                          <Calendar size={14} />
                          <span>
                            {new Date(scan.scanned_at).toLocaleDateString('en-US', {
                              year: 'numeric',
                              month: 'short',
                              day: 'numeric',
                              hour: '2-digit',
                              minute: '2-digit',
                            })}
                          </span>
                        </div>
                      </div>
                      <div className={`health-badge ${badge.class}`}>
                        <span>{badge.emoji}</span>
                        <span>{badge.text}</span>
                      </div>
                    </div>

                    <div className="history-item-nutrition">
                      <div className="nutrition-mini-item">
                        <span className="label">Calories</span>
                        <span className="value">{scan.nutrition_data?.calories || 0} kcal</span>
                      </div>
                      <div className="nutrition-mini-item">
                        <span className="label">Protein</span>
                        <span className="value">{scan.nutrition_data?.protein || 0}g</span>
                      </div>
                      <div className="nutrition-mini-item">
                        <span className="label">Carbs</span>
                        <span className="value">{scan.nutrition_data?.carbs || 0}g</span>
                      </div>
                      <div className="nutrition-mini-item">
                        <span className="label">Fat</span>
                        <span className="value">{scan.nutrition_data?.fat || 0}g</span>
                      </div>
                      <div className="nutrition-mini-item">
                        <span className="label">Score</span>
                        <span className="value score">{scan.health_score?.score || 0}/100</span>
                      </div>
                    </div>

                    {scan.health_score?.reasons && scan.health_score.reasons.length > 0 && (
                      <div className="history-item-reasons">
                        <strong>Analysis:</strong>{' '}
                        {scan.health_score.reasons.slice(0, 2).join(', ')}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <div className="history-stats">
          <div className="stat-box">
            <h4>Total Scans</h4>
            <p className="stat-number">{history.length}</p>
          </div>
          <div className="stat-box">
            <h4>Healthy Foods</h4>
            <p className="stat-number healthy">
              {history.filter((s) => s.health_score?.status === 'healthy').length}
            </p>
          </div>
          <div className="stat-box">
            <h4>Moderate Foods</h4>
            <p className="stat-number moderate">
              {history.filter((s) => s.health_score?.status === 'moderate').length}
            </p>
          </div>
          <div className="stat-box">
            <h4>Unhealthy Foods</h4>
            <p className="stat-number unhealthy">
              {history.filter((s) => s.health_score?.status === 'unhealthy').length}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default History;
