"""
AI-Powered eCommerce Database Assistant - Backend Server
Final Year Project (FYP)

Author: Muhammad Qasim
Registration: 2021-ag-7873
University: University of Agriculture, Faisalabad (UAF)
Degree: BS Computer Science
Batch: 2021-2025
Email: qasimvirk90@gmail.com

Description: Flask backend server for AI-powered eCommerce analytics system
that converts natural language queries to SQL using Google's Gemini AI.
"""

from flask import Flask, request, jsonify
import os
import mysql.connector
import pandas as pd
from tabulate import tabulate
from dotenv import load_dotenv
import re
import sqlparse
from google import genai
from google.genai import types
from decimal import Decimal
from flask_cors import CORS
from collections import defaultdict
import decimal
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI")
if not GEMINI_API_KEY:
    raise Exception("❌ GEMINI_API_KEY not found. Please check your .env file or environment.")

DB_NAME = "online_store"
DB_USER = "root"
DB_PASS = ""
DB_HOST = "localhost"

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

# Helper function to execute queries
def execute_query(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def test_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        conn.close()
        print("✅ MySQL connection successful!")
    except Exception as e:
        print(f"❌ MySQL connection failed:\n{e}")

# Test the DB connection
# test_db_connection()  # Commented out to avoid running on every API call

def run_sql(sql):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        return f"❌ SQL Execution Error:\n{e}"

def is_safe_select(sql):
    parsed = sqlparse.parse(sql)
    for stmt in parsed:
        if stmt.get_type() != 'SELECT':
            return False
    return True

def add_limit(sql, limit=100):
    # Check for existing LIMIT clause (case-insensitive, word boundary)
    if re.search(r'\bLIMIT\s+\d+', sql, re.IGNORECASE):
        return sql
    sql = sql.rstrip(';')
    return f"{sql} LIMIT {limit};"

# Step 4: Check if response is SQL or conversational text
def is_sql_response(response):
    # Check if response starts with SELECT and looks like SQL
    response_clean = response.strip().upper()
    return (response_clean.startswith('SELECT') and 
            any(keyword in response_clean for keyword in ['FROM', 'WHERE', 'JOIN']))

# Updated Gemini Prompt Configuration
SYSTEM_PROMPT = """
You are an AI assistant for an eCommerce database system. You can handle both general conversation and database queries.

For DATABASE QUESTIONS:
- Return ONLY a valid MySQL SELECT query
- Do NOT include backticks, markdown, explanations, or natural language
- Do NOT prefix with "SQL:" or wrap with quotes or code blocks
- The entire output must be ONE LINE of raw SQL

For GENERAL CONVERSATION:
- Respond naturally and helpfully in complete, grammatically correct English sentences
- Use proper sentence structure and avoid mixing technical terms with casual language
- Be friendly, professional, and conversational
- Provide clear and easy-to-understand explanations
- Use proper punctuation and capitalization
- If asked about your capabilities, mention you can help with both general questions and database queries

IMPORTANT RESPONSE GUIDELINES:
- Always respond in complete, well-formed English sentences
- Use natural language that sounds human and professional
- Avoid technical jargon unless necessary and always explain it
- Structure your responses logically with proper grammar
- Be concise but complete in your explanations

SCHEMA (for database queries):
- users(user_id, name, email, password_hash, phone, created_at, updated_at)
- categories(category_id, name, description)
- products(product_id, category_id, name, description, base_price, brand, image_url, created_at)
- product_variants(variant_id, product_id, sku, color, size, additional_price)
- inventory(variant_id, quantity, last_updated)
- orders(order_id, user_id, order_date, status, total_amount, shipping_address)
- order_items(order_item_id, order_id, variant_id, quantity, price)
- payments(payment_id, order_id, payment_method, payment_status, paid_at)
- shipping(shipping_id, order_id, carrier, tracking_number, status, estimated_delivery_date)
- reviews(review_id, user_id, product_id, rating, comment, created_at)
"""

def get_sql_from_gemini(user_question):
    client = genai.Client(api_key=GEMINI_API_KEY)
    model = "gemini-2.5-flash-preview-04-17"

    prompt = SYSTEM_PROMPT + f"\nUser Question: {user_question}\n"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    sql_result = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        sql_result += chunk.text
    return sql_result.strip()

def format_natural_response(columns, rows, user_question):
    """Format database results into natural English responses"""
    if not rows:
        return "No results found for your query."
    
    # Convert column names to more readable format
    def humanize_column(col):
        # Handle SQL aggregate functions
        if '(' in col and ')' in col:
            # Extract function name and field
            if col.upper().startswith('SUM('):
                if 'quantity' in col.lower():
                    return "total quantity sold"
                elif 'amount' in col.lower() or 'price' in col.lower():
                    return "total amount"
                else:
                    return "total"
            elif col.upper().startswith('COUNT('):
                return "count"
            elif col.upper().startswith('AVG('):
                return "average"
            elif col.upper().startswith('MAX('):
                return "maximum"
            elif col.upper().startswith('MIN('):
                return "minimum"
            else:
                # Remove function wrapper and process the inner field
                inner = col[col.find('(')+1:col.rfind(')')]
                return inner.replace('_', ' ').title()
        
        # Regular column name processing
        return col.replace('_', ' ').title()
    
    if len(columns) == 1:
        # Single column results
        col_name = humanize_column(columns[0])
        if len(rows) == 1:
            return f"The {col_name.lower()} is {rows[0][0]}."
        else:
            values = [str(row[0]) for row in rows[:10]]  # Limit to first 10
            if len(rows) > 10:
                return f"Here are the top 10 {col_name.lower()}s: {', '.join(values)}."
            else:
                return f"The {col_name.lower()}s are: {', '.join(values)}."
    
    elif len(columns) == 2:
        # Two column results - create natural sentences
        col1_name = humanize_column(columns[0])
        col2_name = humanize_column(columns[1])
        
        sentences = []
        for i, row in enumerate(rows[:10]):  # Limit to first 10
            # Create more natural sentences based on context
            if 'quantity' in col2_name.lower() or 'total' in col2_name.lower():
                sentences.append(f"{row[0]} has sold {row[1]} units")
            elif 'amount' in col2_name.lower() or 'price' in col2_name.lower():
                sentences.append(f"{row[0]} has a {col2_name.lower()} of ${row[1]}")
            elif 'count' in col2_name.lower():
                sentences.append(f"{row[0]} has {row[1]} items")
            elif 'name' in columns[0].lower():
                sentences.append(f"The {col1_name.lower()} '{row[0]}' has {col2_name.lower()} of {row[1]}")
            else:
                sentences.append(f"{row[0]} - {col2_name.lower()}: {row[1]}")
        
        if len(rows) > 10:
            result = ". ".join(sentences) + f". (Showing top 10 of {len(rows)} results)"
        else:
            result = ". ".join(sentences) + "."
        return result
    
    else:
        # Multiple columns - create structured sentences
        sentences = []
        for i, row in enumerate(rows[:5]):  # Limit to first 5 for readability
            pairs = []
            for col, val in zip(columns, row):
                human_col = humanize_column(col)
                pairs.append(f"{human_col}: {val}")
            sentences.append("Record " + str(i+1) + " - " + ", ".join(pairs))
        
        if len(rows) > 5:
            result = ". ".join(sentences) + f". (Showing 5 of {len(rows)} total records)"
        else:
            result = ". ".join(sentences) + "."
        return result

def chat_with_db_gemini(user_question):
    print(f"[DEBUG] User question: {user_question}")
    gemini_response = get_sql_from_gemini(user_question)
    print(f"[DEBUG] Gemini response: {gemini_response}")

    # Check if response is SQL or conversational
    if is_sql_response(gemini_response):
        # Handle as SQL query
        sql_line = gemini_response.splitlines()[0]
        sql_clean = re.sub(r"[`;]", "", sql_line).strip()
        final_sql = sql_clean + ";"
        print(f"[DEBUG] Cleaned SQL: {final_sql}")

        # Validate it's a SELECT query
        if not is_safe_select(final_sql):
            print(f"[DEBUG] Not a valid SELECT query: {final_sql}")
            return {"text": "Sorry, I could not generate a valid SELECT SQL query for your question.", "sql": None}

        # Add LIMIT
        final_sql_with_limit = add_limit(final_sql)
        print(f"[DEBUG] Final SQL with LIMIT: {final_sql_with_limit}")

        result = run_sql(final_sql_with_limit)
        print(f"[DEBUG] SQL execution result: {result}")

        if isinstance(result, pd.DataFrame) and not result.empty:
            result = result.replace({Decimal: float})
            columns = list(result.columns)
            rows = result.values.tolist()
            
            # Use the new natural response formatter
            text = format_natural_response(columns, rows, user_question)
            print(f"[DEBUG] Response text: {text}")
            return {"text": text, "sql": final_sql.rstrip(';')}
        elif isinstance(result, pd.DataFrame):
            print("[DEBUG] No results found.")
            return {"text": "No results found.", "sql": final_sql.rstrip(';')}
        else:
            print(f"[DEBUG] Error or non-DataFrame result: {result}")
            return {"text": str(result), "sql": final_sql.rstrip(';')}
    else:
        # Handle as conversational response
        print(f"[DEBUG] Conversational response: {gemini_response}")
        return {"text": gemini_response, "sql": None}

# Analytics API Endpoints

def convert_decimals_to_float(obj):
    """Recursively convert Decimal objects to float for JSON serialization"""
    if isinstance(obj, list):
        return [convert_decimals_to_float(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_decimals_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

@app.route('/api/analytics/overview', methods=['GET'])
def get_overview_stats():
    """Get key metrics for dashboard overview"""
    try:
        # Total users
        total_users = execute_query("SELECT COUNT(*) as count FROM users")[0]['count']
        
        # Users this month vs last month
        this_month = execute_query("""
            SELECT COUNT(*) as count FROM users 
            WHERE created_at >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
        """)[0]['count']
        
        last_month = execute_query("""
            SELECT COUNT(*) as count FROM users 
            WHERE created_at >= DATE_FORMAT(CURDATE() - INTERVAL 1 MONTH, '%Y-%m-01')
            AND created_at < DATE_FORMAT(CURDATE(), '%Y-%m-01')
        """)[0]['count']
        
        user_growth = ((this_month - last_month) / max(last_month, 1)) * 100 if last_month > 0 else 0
        
        # Total orders
        total_orders = execute_query("SELECT COUNT(*) as count FROM orders")[0]['count']
        
        # Orders this month vs last month
        orders_this_month = execute_query("""
            SELECT COUNT(*) as count FROM orders 
            WHERE order_date >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
        """)[0]['count']
        
        orders_last_month = execute_query("""
            SELECT COUNT(*) as count FROM orders 
            WHERE order_date >= DATE_FORMAT(CURDATE() - INTERVAL 1 MONTH, '%Y-%m-01')
            AND order_date < DATE_FORMAT(CURDATE(), '%Y-%m-01')
        """)[0]['count']
        
        order_growth = ((orders_this_month - orders_last_month) / max(orders_last_month, 1)) * 100 if orders_last_month > 0 else 0
        
        # Total revenue
        total_revenue = execute_query("SELECT SUM(total_amount) as total FROM orders WHERE status != 'Cancelled'")[0]['total'] or 0
        
        # Revenue this month vs last month
        revenue_this_month = execute_query("""
            SELECT SUM(total_amount) as total FROM orders 
            WHERE order_date >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
            AND status != 'Cancelled'
        """)[0]['total'] or 0
        
        revenue_last_month = execute_query("""
            SELECT SUM(total_amount) as total FROM orders 
            WHERE order_date >= DATE_FORMAT(CURDATE() - INTERVAL 1 MONTH, '%Y-%m-01')
            AND order_date < DATE_FORMAT(CURDATE(), '%Y-%m-01')
            AND status != 'Cancelled'
        """)[0]['total'] or 0
        
        revenue_growth = ((revenue_this_month - revenue_last_month) / max(revenue_last_month, 1)) * 100 if revenue_last_month > 0 else 0
        
        # Total products
        total_products = execute_query("SELECT COUNT(*) as count FROM products")[0]['count']
        
        # Average order value
        avg_order_value = execute_query("""
            SELECT AVG(total_amount) as avg_value FROM orders 
            WHERE status != 'Cancelled'
        """)[0]['avg_value'] or 0
        
        data = {
            'total_users': total_users,
            'user_growth': round(user_growth, 1),
            'total_orders': total_orders,
            'order_growth': round(order_growth, 1),
            'total_revenue': float(total_revenue),
            'revenue_growth': round(revenue_growth, 1),
            'total_products': total_products,
            'avg_order_value': float(avg_order_value)
        }
        
        return jsonify({
            'success': True,
            'data': convert_decimals_to_float(data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytics/sales-trend', methods=['GET'])
def get_sales_trend():
    """Get sales trend for the last 30 days"""
    try:
        sales_data = execute_query("""
            SELECT 
                DATE(order_date) as date,
                COUNT(*) as orders,
                SUM(total_amount) as revenue
            FROM orders 
            WHERE order_date >= CURDATE() - INTERVAL 30 DAY
            AND status != 'Cancelled'
            GROUP BY DATE(order_date)
            ORDER BY date
        """)
        
        return jsonify({
            'success': True,
            'data': convert_decimals_to_float(sales_data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytics/order-status', methods=['GET'])
def get_order_status_distribution():
    """Get order status distribution"""
    try:
        status_data = execute_query("""
            SELECT 
                status,
                COUNT(*) as count,
                SUM(total_amount) as revenue
            FROM orders 
            GROUP BY status
            ORDER BY count DESC
        """)
        
        return jsonify({
            'success': True,
            'data': convert_decimals_to_float(status_data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytics/top-products', methods=['GET'])
def get_top_products():
    """Get top selling products"""
    try:
        top_products = execute_query("""
            SELECT 
                p.name,
                p.brand,
                SUM(oi.quantity) as total_sold,
                SUM(oi.quantity * oi.price) as revenue
            FROM products p
            JOIN product_variants pv ON p.product_id = pv.product_id
            JOIN order_items oi ON pv.variant_id = oi.variant_id
            JOIN orders o ON oi.order_id = o.order_id
            WHERE o.status != 'Cancelled'
            GROUP BY p.product_id, p.name, p.brand
            ORDER BY total_sold DESC
            LIMIT 10
        """)
        
        return jsonify({
            'success': True,
            'data': convert_decimals_to_float(top_products)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytics/categories', methods=['GET'])
def get_category_performance():
    """Get category performance data"""
    try:
        category_data = execute_query("""
            SELECT 
                c.name as category,
                COUNT(DISTINCT p.product_id) as product_count,
                COALESCE(SUM(oi.quantity), 0) as total_sold,
                COALESCE(SUM(oi.quantity * oi.price), 0) as revenue
            FROM categories c
            LEFT JOIN products p ON c.category_id = p.category_id
            LEFT JOIN product_variants pv ON p.product_id = pv.product_id
            LEFT JOIN order_items oi ON pv.variant_id = oi.variant_id
            LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status != 'Cancelled'
            GROUP BY c.category_id, c.name
            ORDER BY revenue DESC
        """)
        
        return jsonify({
            'success': True,
            'data': convert_decimals_to_float(category_data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytics/customer-insights', methods=['GET'])
def get_customer_insights():
    """Get customer behavior insights"""
    try:
        # Top customers by revenue
        top_customers = execute_query("""
            SELECT 
                u.name,
                u.email,
                COUNT(o.order_id) as total_orders,
                SUM(o.total_amount) as total_spent
            FROM users u
            JOIN orders o ON u.user_id = o.user_id
            WHERE o.status != 'Cancelled'
            GROUP BY u.user_id, u.name, u.email
            ORDER BY total_spent DESC
            LIMIT 10
        """)
        
        # Customer acquisition by month
        customer_acquisition = execute_query("""
            SELECT 
                DATE_FORMAT(created_at, '%Y-%m') as month,
                COUNT(*) as new_customers
            FROM users
            WHERE created_at >= CURDATE() - INTERVAL 12 MONTH
            GROUP BY DATE_FORMAT(created_at, '%Y-%m')
            ORDER BY month
        """)
        
        data = {
            'top_customers': top_customers,
            'customer_acquisition': customer_acquisition
        }
        
        return jsonify({
            'success': True,
            'data': convert_decimals_to_float(data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytics/inventory', methods=['GET'])
def get_inventory_status():
    """Get inventory status and low stock alerts"""
    try:
        low_stock = execute_query("""
            SELECT 
                p.name as product_name,
                pv.color,
                pv.size,
                pv.sku,
                i.quantity
            FROM products p
            JOIN product_variants pv ON p.product_id = pv.product_id
            JOIN inventory i ON pv.variant_id = i.variant_id
            WHERE i.quantity < 10
            ORDER BY i.quantity ASC
            LIMIT 20
        """)
        
        # Inventory summary
        inventory_summary = execute_query("""
            SELECT 
                COUNT(*) as total_variants,
                SUM(i.quantity) as total_stock,
                AVG(i.quantity) as avg_stock,
                COUNT(CASE WHEN i.quantity = 0 THEN 1 END) as out_of_stock,
                COUNT(CASE WHEN i.quantity < 10 THEN 1 END) as low_stock
            FROM inventory i
        """)[0]
        
        data = {
            'low_stock_items': low_stock,
            'summary': inventory_summary
        }
        
        return jsonify({
            'success': True,
            'data': convert_decimals_to_float(data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/analytics/reviews', methods=['GET'])
def get_review_analytics():
    """Get review and rating analytics"""
    try:
        # Average rating by product
        product_ratings = execute_query("""
            SELECT 
                p.name,
                AVG(r.rating) as avg_rating,
                COUNT(r.review_id) as review_count
            FROM products p
            LEFT JOIN reviews r ON p.product_id = r.product_id
            GROUP BY p.product_id, p.name
            HAVING review_count > 0
            ORDER BY avg_rating DESC, review_count DESC
            LIMIT 10
        """)
        
        # Rating distribution
        rating_distribution = execute_query("""
            SELECT 
                rating,
                COUNT(*) as count
            FROM reviews
            GROUP BY rating
            ORDER BY rating DESC
        """)
        
        data = {
            'product_ratings': product_ratings,
            'rating_distribution': rating_distribution
        }
        
        return jsonify({
            'success': True,
            'data': convert_decimals_to_float(data)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/')
def hello_world():
    return {'message': 'Hello, World! Flask app is running successfully!'}

@app.route('/test')
def test_route():
    return {'status': 'success', 'data': 'This is a dummy test route'}

@app.route('/ask', methods=['GET', 'POST'])
def ask_gemini():
    if request.method == 'GET':
        # For testing: get message from query param
        user_message = "what is sum of all orders"
        if not user_message:
            return jsonify({'error': 'Missing "message" in query params.'}), 400
    else:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Missing "message" in request body.'}), 400
        user_message = data['message']
    response = chat_with_db_gemini(user_message)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
