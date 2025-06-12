# Project Structure 📁

This document outlines the complete file structure and organization of the AI-Powered eCommerce Database Assistant project.

## 🏗️ Project Overview

```
ai-ecommerce-assistant/
├── backend/                 # Flask API server
├── frontend/               # React.js application
├── docs/                   # Additional documentation
├── README.md              # Main project documentation
├── INSTALLATION.md        # Setup and installation guide
├── API_DOCUMENTATION.md   # API endpoints documentation
├── DATABASE_SCHEMA.md     # Database structure documentation
├── .gitignore            # Git ignore rules
└── LICENSE               # Project license
```

## 🔧 Backend Structure

```
backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (not in git)
├── test.py               # Backend testing script
├── test.ipynb           # Jupyter notebook for testing
├── models/               # Database models (if applicable)
├── utils/                # Utility functions
├── config/               # Configuration files
└── static/               # Static files (if any)
```

### 📄 Key Backend Files

#### `app.py` - Main Application
- **Flask app initialization** with CORS support
- **Database connection management** with MySQL
- **AI integration** with Google Gemini API
- **API endpoints** for chat and analytics
- **Security features** including SQL injection protection
- **Error handling** and logging

**Key Functions:**
- `get_db_connection()` - Database connection handler
- `execute_query()` - Safe query execution
- `run_sql()` - SQL query runner with DataFrame output
- `is_safe_select()` - SQL query validation
- `get_sql_from_gemini()` - AI query generation
- `chat_with_db_gemini()` - Main chat interface

#### `requirements.txt` - Dependencies
```
flask                    # Web framework
flask-cors              # Cross-origin resource sharing
pandas                  # Data manipulation
tabulate                # Data presentation
python-dotenv           # Environment variable management
mysql-connector-python  # MySQL database driver
sqlparse                # SQL parsing and validation
google-generativeai     # Google Gemini AI integration
requests                # HTTP client library
sqlalchemy              # SQL toolkit (if used)
pymysql                 # Alternative MySQL driver
```

#### `.env` - Environment Configuration
```env
GEMINI=your_gemini_api_key_here
```

#### `test.py` - Testing Script
- Database connection testing
- API endpoint testing
- AI integration verification
- Query execution testing

## ⚛️ Frontend Structure

```
frontend/
├── public/                # Static public files
│   ├── index.html        # Main HTML template
│   ├── favicon.ico       # Site icon
│   ├── logo192.png       # PWA icon (192x192)
│   ├── logo512.png       # PWA icon (512x512)
│   ├── manifest.json     # PWA manifest
│   └── robots.txt        # Search engine directives
├── src/                  # React source code
│   ├── components/       # React components
│   │   ├── Navbar.js     # Navigation sidebar
│   │   ├── Navbar.css    # Navbar styling
│   │   ├── Dashboard.js  # Analytics dashboard
│   │   ├── Dashboard.css # Dashboard styling
│   │   ├── ChatbotPage.js # Chat interface
│   │   └── ChatbotPage.css # Chat styling
│   ├── App.js           # Main application component
│   ├── App.css          # Global application styles
│   ├── App.test.js      # Application tests
│   ├── index.js         # React application entry point
│   ├── index.css        # Global styles
│   ├── logo.svg         # React logo
│   ├── reportWebVitals.js # Performance monitoring
│   └── setupTests.js    # Test configuration
├── package.json         # Node.js dependencies and scripts
├── package-lock.json    # Dependency lock file
├── .gitignore          # Frontend-specific git ignore
└── README.md           # Create React App documentation
```

### 🎨 Frontend Components

#### `App.js` - Main Application
- **React Router** setup for navigation
- **Layout structure** with sidebar and content area
- **Route definitions** for different pages
- **Global state management** (if applicable)

#### `Navbar.js` - Navigation Component
- **Sidebar navigation** with modern design
- **Active route highlighting**
- **User information display**
- **Responsive design** for mobile devices

#### `Dashboard.js` - Analytics Dashboard
- **Real-time data fetching** from backend API
- **Statistical cards** showing key metrics
- **Charts and visualizations** for data insights
- **Performance indicators** and trends
- **Error handling** and loading states

**Key Features:**
- Revenue and sales analytics
- Order status distribution
- Top-selling products
- Category performance
- Inventory status and alerts
- Sales trend visualization

#### `ChatbotPage.js` - AI Chat Interface
- **Message handling** with user and bot responses
- **Real-time typing indicators**
- **Auto-scroll** to latest messages
- **Message formatting** and timestamp display
- **Quick action buttons** for common queries
- **Copy-to-clipboard** functionality

**Key Features:**
- Natural language processing
- SQL query execution and display
- Conversational AI responses
- Modern chat UI with animations
- Message history management
- Error handling and user feedback

### 📦 Frontend Dependencies

```json
{
  "dependencies": {
    "@chakra-ui/react": "^3.19.1",      // UI component library
    "@emotion/react": "^11.14.0",       // CSS-in-JS library
    "@emotion/styled": "^11.14.0",      // Styled components
    "@testing-library/dom": "^10.4.0",  // DOM testing utilities
    "@testing-library/jest-dom": "^6.6.3", // Jest DOM matchers
    "@testing-library/react": "^16.3.0", // React testing utilities
    "@testing-library/user-event": "^13.5.0", // User interaction testing
    "framer-motion": "^12.12.1",        // Animation library
    "next-themes": "^0.4.6",            // Theme management
    "react": "^19.1.0",                 // React library
    "react-dom": "^19.1.0",             // React DOM rendering
    "react-icons": "^5.5.0",            // Icon components
    "react-router-dom": "^7.6.0",       // Client-side routing
    "react-scripts": "5.0.1",           // Build tools and configuration
    "web-vitals": "^2.1.4"              // Performance metrics
  }
}
```

## 📚 Documentation Structure

```
docs/ (if created)
├── api/                  # API-specific documentation
│   ├── endpoints.md     # Detailed endpoint documentation
│   ├── examples.md      # Request/response examples
│   └── authentication.md # Auth documentation (future)
├── deployment/          # Deployment guides
│   ├── docker.md       # Docker containerization
│   ├── aws.md          # AWS deployment
│   └── heroku.md       # Heroku deployment
├── development/         # Development guides
│   ├── setup.md        # Development environment setup
│   ├── testing.md      # Testing guidelines
│   └── contributing.md # Contribution guidelines
└── troubleshooting/     # Common issues and solutions
    ├── common-errors.md # Frequently encountered errors
    └── faq.md          # Frequently asked questions
```

## 🎯 Configuration Files

### Frontend Configuration

#### `package.json` - Project Metadata
```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "start": "react-scripts start",    // Development server
    "build": "react-scripts build",   // Production build
    "test": "react-scripts test",     // Test runner
    "eject": "react-scripts eject"    // Eject from CRA
  }
}
```

#### `public/manifest.json` - PWA Configuration
```json
{
  "short_name": "React App",
  "name": "Create React App Sample",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}
```

### Root Configuration

#### `.gitignore` - Version Control
```gitignore
# Dependencies
node_modules/
*/node_modules/

# Environment Variables
.env
*.env

# Python
__pycache__/
*.py[cod]
venv/

# IDE
.vscode/
.idea/

# Operating System
.DS_Store
Thumbs.db

# Logs
*.log

# Build outputs
frontend/build/
backend/dist/
```

## 🔄 Data Flow

```
User Interface (React) 
    ↓ HTTP Requests
Flask API Server
    ↓ SQL Queries
MySQL Database
    ↓ Raw Data
Pandas Processing
    ↓ Formatted Data
AI Processing (Gemini)
    ↓ Intelligent Responses
User Interface Display
```

## 🧩 Component Architecture

### Frontend Component Hierarchy
```
App
├── Router
│   ├── Navbar (persistent)
│   └── Routes
│       ├── Dashboard
│       │   ├── StatCard (multiple)
│       │   ├── ChartCard (multiple)
│       │   └── DataTable (multiple)
│       └── ChatbotPage
│           ├── MessageList
│           │   └── Message (multiple)
│           ├── InputArea
│           └── QuickActions
```

### Backend Module Organization
```
Flask App
├── Database Layer
│   ├── Connection Management
│   ├── Query Execution
│   └── Data Validation
├── AI Integration Layer
│   ├── Gemini API Client
│   ├── Prompt Engineering
│   └── Response Processing
├── API Layer
│   ├── Chat Endpoints
│   ├── Analytics Endpoints
│   └── Error Handling
└── Security Layer
    ├── SQL Injection Prevention
    ├── Query Validation
    └── Input Sanitization
```

## 🚀 Build Process

### Development Workflow
1. **Backend Development**: Python Flask with hot reload
2. **Frontend Development**: React with fast refresh
3. **Database Updates**: MySQL schema migrations
4. **API Testing**: Postman or curl commands
5. **Integration Testing**: Frontend + Backend testing

### Production Build
1. **Frontend Build**: `npm run build` creates optimized bundle
2. **Backend Preparation**: Environment configuration
3. **Database Setup**: Production schema deployment
4. **Static Asset Serving**: Flask serves React build
5. **Environment Configuration**: Production environment variables

## 📈 Scalability Considerations

### Horizontal Scaling
- **API Server**: Multiple Flask instances behind load balancer
- **Database**: MySQL replication and sharding
- **Frontend**: CDN deployment for static assets

### Performance Optimization
- **Database Indexing**: Optimized queries with proper indexes
- **Caching**: Redis for frequent queries
- **Code Splitting**: React lazy loading for components
- **Asset Optimization**: Minification and compression

---

*This project structure is designed for maintainability, scalability, and ease of development while following modern web application best practices.*
