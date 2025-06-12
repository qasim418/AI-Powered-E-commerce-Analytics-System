import os
import re
import sqlparse
import mysql.connector
import pandas as pd
from tabulate import tabulate
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI")
if not GEMINI_API_KEY:
    raise Exception("❌ GEMINI_API_KEY not found. Please check your .env file or environment.")

# DB Config
DB_NAME = "online_store"
DB_USER = "root"
DB_PASS = ""
DB_HOST = "localhost"

# Step 1: Test DB Connection
def test_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
        )
        conn.close()
        print("✅ MySQL connection successful!")
    except Exception as e:
        print(f"❌ MySQL connection failed:\n{e}")

test_db_connection()

# Step 2: Run SQL Safely
def run_sql(sql):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        return f"❌ SQL Execution Error:\n{e}"

# Step 3: Ensure Safe SELECT Queries Only
def is_safe_select(sql):
    parsed = sqlparse.parse(sql)
    return all(stmt.get_type() == "SELECT" for stmt in parsed)

def add_limit(sql, limit=100):
    if re.search(r"\blimit\b", sql, re.IGNORECASE):
        return sql
    return sql.rstrip(";") + f" LIMIT {limit};"

# Step 4: Check if response is SQL or conversational text
def is_sql_response(response):
    # Check if response starts with SELECT and looks like SQL
    response_clean = response.strip().upper()
    return (response_clean.startswith('SELECT') and 
            any(keyword in response_clean for keyword in ['FROM', 'WHERE', 'JOIN']))

# Step 5: Updated Gemini Prompt Configuration
SYSTEM_PROMPT = """
You are an AI assistant for an eCommerce database system. You can handle both general conversation and database queries.

For DATABASE QUESTIONS:
- Return ONLY a valid MySQL SELECT query
- Do NOT include backticks, markdown, explanations, or natural language
- Do NOT prefix with "SQL:" or wrap with quotes or code blocks
- The entire output must be ONE LINE of raw SQL

For GENERAL CONVERSATION:
- Respond naturally and helpfully
- Be friendly and conversational
- If asked about your capabilities, mention you can help with both general questions and database queries

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

# Step 6: Gemini Integration
def get_response_from_gemini(user_question):
    client = genai.Client(api_key=GEMINI_API_KEY)
    model = "gemini-2.5-flash-preview-04-17"

    prompt = SYSTEM_PROMPT + f"\nUser Question: {user_question}\n"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain"
    )

    result = ""
    for chunk in client.models.generate_content_stream(
        model=model, contents=contents, config=generate_content_config
    ):
        result += chunk.text

    return result.strip()

# Step 7: Full Pipeline
def chat_with_db_gemini(user_question):
    print(f"\n🗨️ You: {user_question}\n")

    gemini_response = get_response_from_gemini(user_question)
    print(f"🤖 Gemini Response:\n{gemini_response}\n")

    # Check if response is SQL or conversational
    if is_sql_response(gemini_response):
        # Handle as SQL query
        sql_line = gemini_response.splitlines()[0]
        sql_clean = re.sub(r"[`;]", "", sql_line).strip()
        final_sql = sql_clean + ";"

        if not is_safe_select(final_sql):
            print("❌ Invalid SQL query generated.")
            return

        final_sql = add_limit(final_sql)
        print(f"📥 Running SQL:\n{final_sql}\n")
        
        result = run_sql(final_sql)

        if isinstance(result, pd.DataFrame) and not result.empty:
            print("📊 Result:\n")
            print(tabulate(result, headers='keys', tablefmt='fancy_grid', showindex=False))
            return result
        elif isinstance(result, pd.DataFrame):
            print("⚠️ No results found.")
        else:
            print(result)
    else:
        # Handle as conversational response
        print(f"💬 Gemini: {gemini_response}")
        return gemini_response

# Test with different types of questions
if __name__ == "__main__":
    # Test conversational
    chat_with_db_gemini("Hello, how are you?")
    
    # Test database query
    chat_with_db_gemini("Show me all product names and prices")
    
    # Test another conversation
    chat_with_db_gemini("What can you help me with?")
