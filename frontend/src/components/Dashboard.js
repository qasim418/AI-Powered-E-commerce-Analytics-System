import React, { useState, useEffect } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [overviewData, setOverviewData] = useState(null);
  const [salesTrend, setSalesTrend] = useState([]);
  const [orderStatus, setOrderStatus] = useState([]);
  const [topProducts, setTopProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [inventory, setInventory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE = 'http://localhost:5000/api/analytics';

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      const [overview, sales, status, products, cats, inv] = await Promise.all([
        fetch(`${API_BASE}/overview`).then(res => res.json()),
        fetch(`${API_BASE}/sales-trend`).then(res => res.json()),
        fetch(`${API_BASE}/order-status`).then(res => res.json()),
        fetch(`${API_BASE}/top-products`).then(res => res.json()),
        fetch(`${API_BASE}/categories`).then(res => res.json()),
        fetch(`${API_BASE}/inventory`).then(res => res.json())
      ]);

      if (overview.success) setOverviewData(overview.data);
      if (sales.success) setSalesTrend(sales.data);
      if (status.success) setOrderStatus(status.data);
      if (products.success) setTopProducts(products.data);
      if (cats.success) setCategories(cats.data);
      if (inv.success) setInventory(inv.data);
    } catch (err) {
      setError('Failed to fetch analytics data');
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatNumber = (num) => {
    return new Intl.NumberFormat('en-US').format(num);
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading">Loading analytics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="error">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Online Store Analytics Dashboard</h1>
        <button onClick={fetchAllData} className="refresh-btn">
          Refresh Data
        </button>
      </div>
      
      {/* Overview Stats */}
      <div className="dashboard-stats">
        <div className="stat-card">
          <div className="stat-icon revenue-icon">💰</div>
          <div className="stat-content">
            <h3>Total Revenue</h3>
            <p className="stat-value">{formatCurrency(overviewData?.total_revenue || 0)}</p>
            <p className={`stat-delta ${overviewData?.revenue_growth >= 0 ? 'positive' : 'negative'}`}>
              {overviewData?.revenue_growth >= 0 ? '+' : ''}{overviewData?.revenue_growth}% from last month
            </p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon orders-icon">📦</div>
          <div className="stat-content">
            <h3>Total Orders</h3>
            <p className="stat-value">{formatNumber(overviewData?.total_orders || 0)}</p>
            <p className={`stat-delta ${overviewData?.order_growth >= 0 ? 'positive' : 'negative'}`}>
              {overviewData?.order_growth >= 0 ? '+' : ''}{overviewData?.order_growth}% from last month
            </p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon users-icon">👥</div>
          <div className="stat-content">
            <h3>Total Customers</h3>
            <p className="stat-value">{formatNumber(overviewData?.total_users || 0)}</p>
            <p className={`stat-delta ${overviewData?.user_growth >= 0 ? 'positive' : 'negative'}`}>
              {overviewData?.user_growth >= 0 ? '+' : ''}{overviewData?.user_growth}% from last month
            </p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon products-icon">🛍️</div>
          <div className="stat-content">
            <h3>Total Products</h3>
            <p className="stat-value">{formatNumber(overviewData?.total_products || 0)}</p>
            <p className="stat-info">Average Order: {formatCurrency(overviewData?.avg_order_value || 0)}</p>
          </div>
        </div>
      </div>

      {/* Charts and Data */}
      <div className="dashboard-charts">
        {/* Order Status Distribution */}
        <div className="chart-card">
          <h3>Order Status Distribution</h3>
          <div className="order-status-chart">
            {orderStatus.map((status, index) => (
              <div key={index} className="status-item">
                <div className="status-info">
                  <span className="status-name">{status.status}</span>
                  <span className="status-count">{formatNumber(status.count)} orders</span>
                </div>
                <div className="status-revenue">{formatCurrency(status.revenue || 0)}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Products */}
        <div className="chart-card">
          <h3>Top Selling Products</h3>
          <div className="top-products-list">
            {topProducts.slice(0, 5).map((product, index) => (
              <div key={index} className="product-item">
                <div className="product-rank">#{index + 1}</div>
                <div className="product-info">
                  <div className="product-name">{product.name}</div>
                  <div className="product-brand">{product.brand}</div>
                </div>
                <div className="product-stats">
                  <div className="product-sold">{formatNumber(product.total_sold)} sold</div>
                  <div className="product-revenue">{formatCurrency(product.revenue)}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Category Performance */}
        <div className="chart-card full-width">
          <h3>Category Performance</h3>
          <div className="category-grid">
            {categories.map((category, index) => (
              <div key={index} className="category-card">
                <h4>{category.category}</h4>
                <div className="category-stats">
                  <div className="category-stat">
                    <span className="stat-label">Products:</span>
                    <span className="stat-value">{category.product_count}</span>
                  </div>
                  <div className="category-stat">
                    <span className="stat-label">Sold:</span>
                    <span className="stat-value">{formatNumber(category.total_sold)}</span>
                  </div>
                  <div className="category-stat">
                    <span className="stat-label">Revenue:</span>
                    <span className="stat-value">{formatCurrency(category.revenue)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Inventory Status */}
        {inventory && (
          <div className="chart-card">
            <h3>Inventory Status</h3>
            <div className="inventory-summary">
              <div className="inventory-stat">
                <span className="stat-label">Total Variants:</span>
                <span className="stat-value">{formatNumber(inventory.summary.total_variants)}</span>
              </div>
              <div className="inventory-stat">
                <span className="stat-label">Total Stock:</span>
                <span className="stat-value">{formatNumber(inventory.summary.total_stock)}</span>
              </div>
              <div className="inventory-stat alert">
                <span className="stat-label">Low Stock:</span>
                <span className="stat-value">{inventory.summary.low_stock}</span>
              </div>
              <div className="inventory-stat critical">
                <span className="stat-label">Out of Stock:</span>
                <span className="stat-value">{inventory.summary.out_of_stock}</span>
              </div>
            </div>
            
            {inventory.low_stock_items.length > 0 && (
              <div className="low-stock-alerts">
                <h4>Low Stock Alerts</h4>
                {inventory.low_stock_items.slice(0, 5).map((item, index) => (
                  <div key={index} className="stock-alert">
                    <span className="product-name">{item.product_name}</span>
                    <span className="variant-info">
                      {item.color && `${item.color} `}
                      {item.size && `/ ${item.size}`}
                    </span>
                    <span className={`stock-quantity ${item.quantity === 0 ? 'critical' : 'warning'}`}>
                      {item.quantity} left
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Sales Trend */}
        <div className="chart-card">
          <h3>Sales Trend (Last 30 Days)</h3>
          <div className="sales-trend">
            {salesTrend.slice(-7).map((day, index) => (
              <div key={index} className="trend-day">
                <div className="trend-date">{new Date(day.date).toLocaleDateString()}</div>
                <div className="trend-orders">{day.orders} orders</div>
                <div className="trend-revenue">{formatCurrency(day.revenue)}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;