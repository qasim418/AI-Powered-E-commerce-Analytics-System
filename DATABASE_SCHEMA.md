# Database Schema Documentation 🗄️

This document outlines the complete database schema for the AI-Powered eCommerce Database Assistant.

## 📋 Database Overview

**Database Name:** `online_store`  
**Engine:** MySQL 8.0+  
**Character Set:** utf8mb4  
**Collation:** utf8mb4_unicode_ci  

## 🏗️ Schema Architecture

The database follows a normalized eCommerce structure with the following key entities:

```
Users ────┐
          │
          ▼
       Orders ────┐
          │       │
          ▼       ▼
    Order Items   Payments
          │       
          ▼       
    Product Variants ────┐
          │             │
          ▼             ▼
      Products      Inventory
          │
          ▼
     Categories

Additional Tables:
- Reviews
- Shipping
```

## 📊 Table Definitions

### 1. Users Table
Stores customer information and authentication data.

```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
);
```

**Fields:**
- `user_id`: Unique identifier for each user
- `name`: Full name of the user
- `email`: Email address (unique)
- `password_hash`: Encrypted password
- `phone`: Contact number
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### 2. Categories Table
Product categorization system.

```sql
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    INDEX idx_name (name)
);
```

**Fields:**
- `category_id`: Unique identifier for each category
- `name`: Category name
- `description`: Category description

### 3. Products Table
Main product catalog.

```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    base_price DECIMAL(10,2) NOT NULL,
    brand VARCHAR(255),
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    INDEX idx_category (category_id),
    INDEX idx_brand (brand),
    INDEX idx_price (base_price),
    INDEX idx_created_at (created_at)
);
```

**Fields:**
- `product_id`: Unique identifier for each product
- `category_id`: Reference to categories table
- `name`: Product name
- `description`: Product description
- `base_price`: Base price of the product
- `brand`: Product brand
- `image_url`: Product image URL
- `created_at`: Product creation timestamp

### 4. Product Variants Table
Different variations of products (color, size, etc.).

```sql
CREATE TABLE product_variants (
    variant_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    color VARCHAR(50),
    size VARCHAR(50),
    additional_price DECIMAL(10,2) DEFAULT 0.00,
    
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    INDEX idx_product (product_id),
    INDEX idx_sku (sku)
);
```

**Fields:**
- `variant_id`: Unique identifier for each variant
- `product_id`: Reference to products table
- `sku`: Stock Keeping Unit (unique)
- `color`: Product color
- `size`: Product size
- `additional_price`: Additional price for this variant

### 5. Inventory Table
Stock management for product variants.

```sql
CREATE TABLE inventory (
    variant_id INT PRIMARY KEY,
    quantity INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id),
    INDEX idx_quantity (quantity),
    INDEX idx_last_updated (last_updated)
);
```

**Fields:**
- `variant_id`: Reference to product_variants table
- `quantity`: Available stock quantity
- `last_updated`: Last inventory update timestamp

### 6. Orders Table
Customer orders tracking.

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    total_amount DECIMAL(10,2) NOT NULL,
    shipping_address TEXT NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user (user_id),
    INDEX idx_status (status),
    INDEX idx_order_date (order_date),
    INDEX idx_total_amount (total_amount)
);
```

**Fields:**
- `order_id`: Unique identifier for each order
- `user_id`: Reference to users table
- `order_date`: Order placement timestamp
- `status`: Current order status
- `total_amount`: Total order amount
- `shipping_address`: Delivery address

### 7. Order Items Table
Individual items within orders.

```sql
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    variant_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id),
    INDEX idx_order (order_id),
    INDEX idx_variant (variant_id)
);
```

**Fields:**
- `order_item_id`: Unique identifier for each order item
- `order_id`: Reference to orders table
- `variant_id`: Reference to product_variants table
- `quantity`: Quantity ordered
- `price`: Price per item at time of order

### 8. Payments Table
Payment processing records.

```sql
CREATE TABLE payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    payment_method ENUM('credit_card', 'debit_card', 'paypal', 'bank_transfer', 'cash_on_delivery') NOT NULL,
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    paid_at TIMESTAMP NULL,
    
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    INDEX idx_order (order_id),
    INDEX idx_status (payment_status),
    INDEX idx_method (payment_method),
    INDEX idx_paid_at (paid_at)
);
```

**Fields:**
- `payment_id`: Unique identifier for each payment
- `order_id`: Reference to orders table
- `payment_method`: Method used for payment
- `payment_status`: Current payment status
- `paid_at`: Payment completion timestamp

### 9. Shipping Table
Delivery and tracking information.

```sql
CREATE TABLE shipping (
    shipping_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    carrier VARCHAR(255),
    tracking_number VARCHAR(255),
    status ENUM('preparing', 'shipped', 'in_transit', 'delivered', 'returned') DEFAULT 'preparing',
    estimated_delivery_date DATE,
    
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    INDEX idx_order (order_id),
    INDEX idx_status (status),
    INDEX idx_tracking (tracking_number),
    INDEX idx_delivery_date (estimated_delivery_date)
);
```

**Fields:**
- `shipping_id`: Unique identifier for each shipment
- `order_id`: Reference to orders table
- `carrier`: Shipping carrier name
- `tracking_number`: Package tracking number
- `status`: Current shipping status
- `estimated_delivery_date`: Expected delivery date

### 10. Reviews Table
Customer product reviews and ratings.

```sql
CREATE TABLE reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    INDEX idx_user (user_id),
    INDEX idx_product (product_id),
    INDEX idx_rating (rating),
    INDEX idx_created_at (created_at),
    UNIQUE KEY unique_user_product (user_id, product_id)
);
```

**Fields:**
- `review_id`: Unique identifier for each review
- `user_id`: Reference to users table
- `product_id`: Reference to products table
- `rating`: Product rating (1-5 stars)
- `comment`: Review comment
- `created_at`: Review creation timestamp

## 🔗 Relationships

### Primary Relationships
1. **Users → Orders**: One-to-Many
2. **Orders → Order Items**: One-to-Many
3. **Orders → Payments**: One-to-One
4. **Orders → Shipping**: One-to-One
5. **Categories → Products**: One-to-Many
6. **Products → Product Variants**: One-to-Many
7. **Product Variants → Inventory**: One-to-One
8. **Product Variants → Order Items**: One-to-Many
9. **Users → Reviews**: One-to-Many
10. **Products → Reviews**: One-to-Many

### Referential Integrity
All foreign key constraints are properly defined to maintain data integrity.

## 📈 Sample Data Insights

### Common Queries Supported

1. **Revenue Analysis**
   ```sql
   SELECT SUM(total_amount) as total_revenue 
   FROM orders 
   WHERE status = 'completed';
   ```

2. **Top Selling Products**
   ```sql
   SELECT p.name, SUM(oi.quantity) as total_sold
   FROM products p
   JOIN product_variants pv ON p.product_id = pv.product_id
   JOIN order_items oi ON pv.variant_id = oi.variant_id
   GROUP BY p.product_id
   ORDER BY total_sold DESC;
   ```

3. **Inventory Status**
   ```sql
   SELECT p.name, pv.sku, i.quantity
   FROM products p
   JOIN product_variants pv ON p.product_id = pv.product_id
   JOIN inventory i ON pv.variant_id = i.variant_id
   WHERE i.quantity < 10;
   ```

4. **Customer Insights**
   ```sql
   SELECT u.name, COUNT(o.order_id) as order_count, SUM(o.total_amount) as total_spent
   FROM users u
   JOIN orders o ON u.user_id = o.user_id
   GROUP BY u.user_id
   ORDER BY total_spent DESC;
   ```

## 🛡️ Security Considerations

### Data Protection
- **Password Hashing**: User passwords are stored as hashes
- **Data Validation**: All inputs are validated at application level
- **SQL Injection Prevention**: Parameterized queries used throughout

### Access Control
- **Read-Only Operations**: API only allows SELECT queries
- **Query Validation**: All SQL statements are parsed and validated
- **Result Limiting**: Automatic LIMIT clauses prevent large data dumps

## 🔧 Performance Optimizations

### Indexing Strategy
- **Primary Keys**: All tables have optimized primary keys
- **Foreign Keys**: Indexed for efficient joins
- **Search Fields**: Email, SKU, tracking numbers indexed
- **Date Fields**: Timestamp fields indexed for time-based queries
- **Composite Indexes**: For complex query patterns

### Query Optimization
- **Pagination**: LIMIT clauses automatically added
- **Selective Fields**: Avoid SELECT * in production queries
- **Join Optimization**: Proper foreign key relationships

## 📊 Data Types and Constraints

### Standard Data Types Used
- **INT**: For IDs and quantities
- **VARCHAR**: For text fields with length limits
- **TEXT**: For long text content
- **DECIMAL(10,2)**: For monetary values
- **TIMESTAMP**: For date/time tracking
- **ENUM**: For predefined options

### Constraints
- **NOT NULL**: Required fields
- **UNIQUE**: Email, SKU, user-product review combinations
- **CHECK**: Rating validation (1-5)
- **FOREIGN KEY**: Referential integrity
- **DEFAULT**: Default values for optional fields

## 🚀 Migration Scripts

### Initial Setup
```sql
-- Create database
CREATE DATABASE online_store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE online_store;

-- Run all table creation scripts in order:
-- 1. categories
-- 2. users
-- 3. products
-- 4. product_variants
-- 5. inventory
-- 6. orders
-- 7. order_items
-- 8. payments
-- 9. shipping
-- 10. reviews
```

### Sample Data Population
After creating tables, populate with sample data for testing:
```sql
-- Insert sample categories
INSERT INTO categories (name, description) VALUES 
('Electronics', 'Electronic devices and gadgets'),
('Clothing', 'Fashion and apparel'),
('Books', 'Books and literature');

-- Continue with other sample data...
```

---

*This schema documentation is designed to support the AI-Powered eCommerce Database Assistant. The structure allows for comprehensive eCommerce operations while maintaining data integrity and performance.*
