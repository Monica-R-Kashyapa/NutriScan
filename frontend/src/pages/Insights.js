import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, Calendar, Award } from 'lucide-react';
import { foodAPI } from '../services/api';
import './Insights.css';

function Insights() {
  const [insights, setInsights] = useState(null);
  const [period, setPeriod] = useState('week');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInsights();
  }, [period]);

  const fetchInsights = async () => {
    setLoading(true);
    try {
      const response = await foodAPI.getInsights(period);
      setInsights(response.data);
    } catch (error) {
      console.error('Error fetching insights:', error);
    } finally {
      setLoading(false);
    }
  };

  const COLORS = {
    healthy: '#10b981',
    moderate: '#f59e0b',
    unhealthy: '#ef4444',
  };

  if (loading) {
    return (
      <div className="container">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!insights) {
    return (
      <div className="container">
        <div className="card">
          <p>No insights available</p>
        </div>
      </div>
    );
  }

  const pieData = [
    { name: 'Healthy', value: insights.statistics.healthy_count, color: COLORS.healthy },
    { name: 'Moderate', value: insights.statistics.moderate_count, color: COLORS.moderate },
    { name: 'Unhealthy', value: insights.statistics.unhealthy_count, color: COLORS.unhealthy },
  ];

  return (
    <div className="insights">
      <div className="container">
        <div className="insights-header">
          <div>
            <h1>📊 Nutrition Insights</h1>
            <p>Track your eating habits and progress</p>
          </div>
          <div className="period-selector">
            <button
              className={`period-btn ${period === 'week' ? 'active' : ''}`}
              onClick={() => setPeriod('week')}
            >
              Week
            </button>
            <button
              className={`period-btn ${period === 'month' ? 'active' : ''}`}
              onClick={() => setPeriod('month')}
            >
              Month
            </button>
            <button
              className={`period-btn ${period === 'all' ? 'active' : ''}`}
              onClick={() => setPeriod('all')}
            >
              All Time
            </button>
          </div>
        </div>

        {/* Summary Stats */}
        <div className="insights-stats">
          <div className="insight-stat-card">
            <div className="stat-icon" style={{ background: '#dbeafe' }}>
              <TrendingUp size={24} color="#3b82f6" />
            </div>
            <div>
              <h3>{insights.statistics.total_scans}</h3>
              <p>Total Scans</p>
            </div>
          </div>
          <div className="insight-stat-card">
            <div className="stat-icon" style={{ background: '#d1fae5' }}>
              <Award size={24} color="#10b981" />
            </div>
            <div>
              <h3>{insights.statistics.avg_calories}</h3>
              <p>Avg Calories</p>
            </div>
          </div>
          <div className="insight-stat-card">
            <div className="stat-icon" style={{ background: '#fef3c7' }}>
              <Calendar size={24} color="#f59e0b" />
            </div>
            <div>
              <h3>{period === 'week' ? '7' : period === 'month' ? '30' : 'All'}</h3>
              <p>Days Period</p>
            </div>
          </div>
        </div>

        {/* Charts Grid */}
        <div className="charts-grid">
          {/* Health Distribution Pie Chart */}
          <div className="card chart-card">
            <h2>Health Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="chart-legend">
              <div className="legend-item">
                <span className="legend-dot" style={{ background: COLORS.healthy }}></span>
                <span>Healthy: {insights.statistics.healthy_count}</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot" style={{ background: COLORS.moderate }}></span>
                <span>Moderate: {insights.statistics.moderate_count}</span>
              </div>
              <div className="legend-item">
                <span className="legend-dot" style={{ background: COLORS.unhealthy }}></span>
                <span>Unhealthy: {insights.statistics.unhealthy_count}</span>
              </div>
            </div>
          </div>

          {/* Daily Scans Bar Chart */}
          <div className="card chart-card">
            <h2>Daily Scans</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={insights.daily_breakdown}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="scans" fill="#667eea" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Daily Calories Line Chart */}
          <div className="card chart-card">
            <h2>Daily Calories</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={insights.daily_breakdown}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="calories" stroke="#f59e0b" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Top Foods */}
          <div className="card chart-card">
            <h2>Most Scanned Foods</h2>
            {insights.top_foods.length === 0 ? (
              <div className="empty-chart">
                <p>No data available</p>
              </div>
            ) : (
              <div className="top-foods-list">
                {insights.top_foods.map((food, index) => (
                  <div key={index} className="top-food-item">
                    <div className="food-rank">#{index + 1}</div>
                    <div className="food-info">
                      <span className="food-name">{food.name}</span>
                      <div className="food-bar">
                        <div
                          className="food-bar-fill"
                          style={{
                            width: `${(food.count / insights.top_foods[0].count) * 100}%`,
                          }}
                        ></div>
                      </div>
                    </div>
                    <div className="food-count">{food.count}x</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Recommendations */}
        <div className="card recommendations-card">
          <h2>💡 Personalized Recommendations</h2>
          <div className="recommendations-grid">
            {insights.statistics.healthy_count > insights.statistics.unhealthy_count ? (
              <div className="recommendation-item success">
                <span className="rec-icon">🎉</span>
                <div>
                  <h4>Great Job!</h4>
                  <p>You're making healthy choices. Keep up the good work!</p>
                </div>
              </div>
            ) : (
              <div className="recommendation-item warning">
                <span className="rec-icon">⚠️</span>
                <div>
                  <h4>Room for Improvement</h4>
                  <p>Try to include more healthy options in your diet.</p>
                </div>
              </div>
            )}

            {insights.statistics.avg_calories > 500 && (
              <div className="recommendation-item info">
                <span className="rec-icon">🍽️</span>
                <div>
                  <h4>Watch Your Portions</h4>
                  <p>Your average calorie intake is high. Consider portion control.</p>
                </div>
              </div>
            )}

            <div className="recommendation-item info">
              <span className="rec-icon">📈</span>
              <div>
                <h4>Stay Consistent</h4>
                <p>Regular tracking helps you make better food choices over time.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Insights;
