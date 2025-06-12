# API Documentation 📚

This document provides comprehensive information about the backend API endpoints for the AI-Powered eCommerce Database Assistant.

## 🌐 Base URL

```
http://localhost:5000
```

## 🔐 Authentication

Currently, the API doesn't require authentication. In a production environment, consider implementing proper authentication mechanisms.

## 📋 Content Type

All requests should include:
```
Content-Type: application/json
```

## 🚀 API Endpoints

### 1. Chat Interface

#### Send Message to AI Assistant
**POST** `/api/chat`

Processes user messages and returns either conversational responses or database query results.

**Request Body:**
```json
{
  "message": "string"
}
```

**Example Requests:**

1. **Natural Language Query:**
```json
{
  "message": "Show me all products in Electronics category"
}
```

2. **Conversational Message:**
```json
{
  "message": "Hello, how are you today?"
}
```

**Response Format:**

For **Database Queries:**
```json
{
  "type": "data",
  "data": [
    {
      "column1": "value1",
      "column2": "value2",
      ...
    }
  ],
  "sql_query": "SELECT * FROM products WHERE category = 'Electronics' LIMIT 100",
  "row_count": 15
}
```

For **Conversational Responses:**
```json
{
  "type": "message",
  "response": "Hello! I'm doing great, thank you for asking. How can I assist you today?"
}
```

**Error Response:**
```json
{
  "type": "error",
  "error": "Error message description"
}
```

### 2. Analytics Dashboard

#### Get Overview Statistics
**GET** `/api/analytics/overview`

Returns general dashboard statistics including revenue, orders, users, and products.

**Response:**
```json
{
  "total_revenue": 125430.50,
  "total_orders": 1247,
  "total_users": 892,
  "total_products": 156,
  "revenue_change": "+12.5%",
  "orders_change": "+8.3%",
  "users_change": "+15.2%",
  "products_change": "+5.1%"
}
```

#### Get Sales Trend Data
**GET** `/api/analytics/sales-trend`

Returns daily sales data for the last 7 days.

**Response:**
```json
[
  {
    "date": "2025-06-06",
    "orders": 45,
    "revenue": 3450.00
  },
  {
    "date": "2025-06-07",
    "orders": 52,
    "revenue": 4120.50
  }
]
```

#### Get Top Products
**GET** `/api/analytics/top-products`

Returns the best-selling products with sales statistics.

**Response:**
```json
[
  {
    "product_id": 1,
    "name": "iPhone 15 Pro",
    "brand": "Apple",
    "total_sold": 145,
    "total_revenue": 145000.00,
    "category": "Electronics"
  },
  {
    "product_id": 2,
    "name": "MacBook Air M2",
    "brand": "Apple",
    "total_sold": 89,
    "total_revenue": 123500.00,
    "category": "Computers"
  }
]
```

#### Get Category Performance
**GET** `/api/analytics/categories`

Returns performance statistics for each product category.

**Response:**
```json
[
  {
    "category_id": 1,
    "name": "Electronics",
    "total_products": 45,
    "total_revenue": 85420.50,
    "total_orders": 324,
    "avg_order_value": 263.70
  },
  {
    "category_id": 2,
    "name": "Clothing",
    "total_products": 78,
    "total_revenue": 32150.00,
    "total_orders": 567,
    "avg_order_value": 56.70
  }
]
```

#### Get Inventory Status
**GET** `/api/analytics/inventory`

Returns inventory statistics and low stock alerts.

**Response:**
```json
{
  "total_variants": 342,
  "in_stock": 298,
  "low_stock": 32,
  "out_of_stock": 12,
  "low_stock_threshold": 10,
  "alerts": [
    {
      "variant_id": 15,
      "product_name": "iPhone 15 Pro",
      "sku": "IPH15P-BLK-256",
      "color": "Black",
      "size": "256GB",
      "quantity": 5
    }
  ]
}
```

#### Get Order Status Distribution
**GET** `/api/analytics/order-status`

Returns the distribution of orders by status.

**Response:**
```json
[
  {
    "status": "completed",
    "count": 892,
    "revenue": 85420.50,
    "percentage": 71.5
  },
  {
    "status": "processing",
    "count": 156,
    "revenue": 15230.00,
    "percentage": 12.5
  },
  {
    "status": "shipped",
    "count": 134,
    "revenue": 12890.00,
    "percentage": 10.7
  },
  {
    "status": "pending",
    "count": 65,
    "revenue": 6120.50,
    "percentage": 5.2
  }
]
```

## 🔍 Database Query Examples

The chat endpoint accepts natural language queries that are converted to SQL. Here are some examples:

### Product Queries
- "Show me all products"
- "Find products in Electronics category"
- "What are the most expensive products?"
- "Show products with low stock"

### Order Queries
- "Show me recent orders"
- "Find orders from last month"
- "What are the largest orders?"
- "Show pending orders"

### User Queries
- "List all users"
- "Find users who registered this month"
- "Show top customers by spending"

### Sales Queries
- "Show sales by category"
- "What's the revenue for last week?"
- "Find best-selling products"

## ⚠️ Safety and Limitations

### Security Measures
- **SQL Injection Protection**: All queries are parsed and validated
- **Read-Only Operations**: Only SELECT queries are allowed
- **Query Limits**: Automatic LIMIT clauses prevent large result sets
- **Input Validation**: User input is sanitized before processing

### Limitations
- Maximum 100 rows per query result
- Only SELECT statements are supported
- No data modification operations (INSERT, UPDATE, DELETE)
- No schema modification operations (CREATE, ALTER, DROP)

## 🚨 Error Handling

### Common Error Codes

**400 Bad Request**
```json
{
  "type": "error",
  "error": "Invalid request format"
}
```

**500 Internal Server Error**
```json
{
  "type": "error",
  "error": "Database connection failed"
}
```

**503 Service Unavailable**
```json
{
  "type": "error",
  "error": "AI service temporarily unavailable"
}
```

## 📊 Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing:
- Request rate limiting per IP
- API key-based quotas
- Concurrent request limitations

## 🔄 CORS Configuration

The API includes CORS headers to allow requests from the frontend:
```python
CORS(app)  # Allows all origins
```

For production, configure specific origins:
```python
CORS(app, origins=['http://localhost:3000', 'https://yourdomain.com'])
```

## 📝 Request/Response Examples

### Complete Chat Example

**Request:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me top 5 products by revenue"}'
```

**Response:**
```json
{
  "type": "data",
  "data": [
    {
      "product_id": 1,
      "name": "iPhone 15 Pro",
      "total_revenue": 145000.00,
      "total_sold": 145
    },
    {
      "product_id": 2,
      "name": "MacBook Air M2",
      "total_revenue": 123500.00,
      "total_sold": 89
    }
  ],
  "sql_query": "SELECT product_id, name, SUM(price * quantity) as total_revenue, SUM(quantity) as total_sold FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY product_id ORDER BY total_revenue DESC LIMIT 5",
  "row_count": 5
}
```

## 🛠️ Development Notes

### Environment Variables
```env
GEMINI=your_google_gemini_api_key
```

### Database Configuration
```python
DB_NAME = "online_store"
DB_USER = "root"
DB_PASS = ""
DB_HOST = "localhost"
```

### Testing Endpoints
You can test all endpoints using tools like:
- **Postman**: Import the provided collection
- **curl**: Use command line examples
- **Browser**: For GET endpoints
- **Frontend**: Through the React application

---

*This API documentation is part of the AI-Powered eCommerce Database Assistant project. For additional information, refer to the main README.md file.*
