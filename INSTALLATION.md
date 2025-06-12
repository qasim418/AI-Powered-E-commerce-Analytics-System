# Installation Guide 🚀

This guide will help you set up the AI-Powered eCommerce Database Assistant on your local machine.

## 📋 System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Ubuntu 18.04+
- **Node.js**: Version 14.0.0 or higher
- **Python**: Version 3.8.0 or higher
- **MySQL**: Version 8.0 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 2GB free space

## 🔧 Prerequisites Installation

### 1. Install Node.js
- Download from [nodejs.org](https://nodejs.org/)
- Verify installation:
  ```bash
  node --version
  npm --version
  ```

### 2. Install Python
- Download from [python.org](https://python.org/)
- Verify installation:
  ```bash
  python --version
  pip --version
  ```

### 3. Install MySQL
- Download from [mysql.com](https://dev.mysql.com/downloads/)
- Create a database named `online_store`
- Note your MySQL root credentials

### 4. Get Google Gemini API Key
- Visit [Google AI Studio](https://aistudio.google.com/)
- Create an account and generate an API key
- Keep this key secure for environment configuration

## 📥 Project Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/qasim418/AI-Powered-E-commerce-Analytics-System.git
cd AI-Powered-E-commerce-Analytics-System
```

### Step 2: Backend Configuration

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   Create a `.env` file in the backend directory:
   ```env
   GEMINI=your_gemini_api_key_here
   ```

5. **Configure database connection**
   Edit `app.py` if your MySQL settings differ:
   ```python
   DB_NAME = "online_store"  # Your database name
   DB_USER = "root"          # Your MySQL username
   DB_PASS = ""              # Your MySQL password
   DB_HOST = "localhost"     # Your MySQL host
   ```

### Step 3: Database Setup

1. **Start MySQL service**
   ```bash
   # On Windows (if MySQL is in PATH)
   net start mysql
   
   # On macOS
   brew services start mysql
   
   # On Ubuntu
   sudo systemctl start mysql
   ```

2. **Create database**
   ```sql
   CREATE DATABASE online_store;
   USE online_store;
   ```

3. **Import sample schema** (if you have one)
   ```bash
   mysql -u root -p online_store < database_schema.sql
   ```

### Step 4: Frontend Configuration

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

## 🚀 Running the Application

### Start Backend Server

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Activate virtual environment** (if using)
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Start Flask server**
   ```bash
   python app.py
   ```
   
   You should see:
   ```
   * Running on http://127.0.0.1:5000
   * Debug mode: on
   ```

### Start Frontend Server

1. **Open a new terminal**
   ```bash
   cd frontend
   ```

2. **Start React development server**
   ```bash
   npm start
   ```
   
   The application will automatically open at `http://localhost:3000`

## 🧪 Testing the Installation

### 1. Test Database Connection
- Visit the chatbot page
- Try asking: "Show me all users"
- You should see either data or a "no results" message

### 2. Test AI Integration
- Ask a conversational question: "Hello, how are you?"
- The bot should respond naturally

### 3. Test Dashboard
- Visit the dashboard page
- Check if analytics data loads properly

## 🔧 Troubleshooting

### Common Issues

**1. MySQL Connection Error**
```
❌ MySQL connection failed: Access denied for user 'root'@'localhost'
```
- **Solution**: Check your MySQL credentials in `app.py`
- Ensure MySQL service is running

**2. Gemini API Error**
```
❌ GEMINI_API_KEY not found
```
- **Solution**: Check your `.env` file in the backend directory
- Ensure the API key is correct

**3. Port Already in Use**
```
Port 5000 is already in use
```
- **Solution**: Kill the process using port 5000 or change the port in `app.py`

**4. Module Not Found Error**
```
ModuleNotFoundError: No module named 'flask'
```
- **Solution**: Ensure you're in the correct virtual environment and ran `pip install -r requirements.txt`

**5. Frontend Not Loading**
```
npm ERR! code EADDRINUSE
```
- **Solution**: Change the port by setting `PORT=3001` in your environment or kill the process on port 3000

### Getting Help

If you encounter issues:

1. **Check the console logs** for detailed error messages
2. **Verify all prerequisites** are properly installed
3. **Ensure all services are running** (MySQL, etc.)
4. **Check file paths** and permissions
5. **Verify API keys** and credentials

## 🎯 Next Steps

After successful installation:

1. **Explore the Dashboard** - Check out various analytics features
2. **Test the Chatbot** - Try different types of queries
3. **Review the Code** - Understand the implementation
4. **Customize** - Modify styling or add features
5. **Deploy** - Consider deployment options for production

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Google Gemini AI Documentation](https://ai.google.dev/)

---

*If you encounter any issues not covered in this guide, please create an issue in the repository with detailed error messages and your system configuration.*
