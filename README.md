# AI-Powered eCommerce Database Assistant 🤖

A sophisticated Final Year Project (FYP) that combines artificial intelligence with database management to create an intelligent assistant for eCommerce operations. This application allows users to interact with an eCommerce database using natural language queries while providing comprehensive analytics and dashboard features.

## 🎯 Project Overview

This project demonstrates the integration of modern web technologies with AI capabilities to create a user-friendly interface for database operations. The system can:

- **Natural Language Processing**: Convert user questions into SQL queries using Google's Gemini AI
- **Database Operations**: Execute safe SELECT queries on a MySQL eCommerce database
- **Real-time Analytics**: Display comprehensive dashboard with sales metrics, trends, and insights
- **Interactive Chat Interface**: Modern chatbot interface for seamless user interaction
- **Data Visualization**: Present complex data in an intuitive and visually appealing format

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React.js      │────▶│   Flask API     │────▶│   MySQL DB      │
│   Frontend      │     │   Backend       │     │   eCommerce     │
│                 │     │                 │     │                 │
│ • Dashboard     │     │ • AI Processing │     │ • Products      │
│ • Chat Interface│     │ • Query Gen.    │     │ • Orders        │
│ • Analytics     │     │ • Safety Checks │     │ • Users         │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │
                                ▼
                        ┌─────────────────┐
                        │   Gemini AI     │
                        │   Google API    │
                        └─────────────────┘
```

## ✨ Key Features

### 🎨 Frontend (React.js)
- **Modern Dashboard**: Comprehensive analytics with real-time data visualization
- **Interactive Chatbot**: Natural language interface for database queries
- **Responsive Design**: Mobile-friendly UI with modern styling
- **Real-time Updates**: Dynamic data fetching and display
- **Professional Navigation**: Clean sidebar navigation with active states

### ⚡ Backend (Flask)
- **AI Integration**: Gemini AI for natural language to SQL conversion
- **Database Security**: Safe query execution with SQL injection protection
- **RESTful API**: Well-structured endpoints for data operations
- **Error Handling**: Comprehensive error management and logging
- **CORS Support**: Cross-origin resource sharing for frontend integration

### 🗄️ Database Features
- **Complete eCommerce Schema**: Users, products, orders, payments, shipping, reviews
- **Query Optimization**: Automatic LIMIT clauses for performance
- **Safe Operations**: Only SELECT queries allowed for security
- **Data Integrity**: Proper relationships and constraints

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v14 or higher)
- **Python** (v3.8 or higher)
- **MySQL** (v8.0 or higher)
- **Google Gemini API Key**

### 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/qasim418/AI-Powered-E-commerce-Analytics-System.git
   cd AI-Powered-E-commerce-Analytics-System
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   Create a `.env` file in the backend directory:
   ```env
   GEMINI=your_gemini_api_key_here
   ```

4. **Database Setup**
   - Create a MySQL database named `online_store`
   - Import your eCommerce schema
   - Update database credentials in `app.py` if needed

5. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

### 🎯 Running the Application

1. **Start the Backend Server**
   ```bash
   cd backend
   python app.py
   ```
   The Flask server will run on `http://localhost:5000`

2. **Start the Frontend Development Server**
   ```bash
   cd frontend
   npm start
   ```
   The React app will open at `http://localhost:3000`

## 📊 Database Schema

The application works with a comprehensive eCommerce database schema:

| Table | Description |
|-------|-------------|
| `users` | Customer information and authentication |
| `categories` | Product categorization |
| `products` | Product catalog with details |
| `product_variants` | Product variations (color, size, etc.) |
| `inventory` | Stock management |
| `orders` | Order tracking and management |
| `order_items` | Individual items within orders |
| `payments` | Payment processing records |
| `shipping` | Delivery and tracking information |
| `reviews` | Customer feedback and ratings |

## 🎮 Usage Examples

### Natural Language Queries
- "Show me all products in Electronics category"
- "What are the top 5 best-selling products?"
- "Find orders from last month"
- "Which users have spent the most money?"

### Dashboard Features
- **Sales Analytics**: Revenue trends, order statistics
- **Product Performance**: Top products, category insights
- **Inventory Management**: Stock levels, low stock alerts
- **Customer Insights**: User behavior and purchase patterns

## 🛠️ Technology Stack

### Frontend Technologies
- **React.js 19.1.0**: Modern JavaScript library for building user interfaces
- **React Router DOM**: Client-side routing
- **Chakra UI**: Modern component library
- **Framer Motion**: Animation library
- **React Icons**: Icon components

### Backend Technologies
- **Flask**: Lightweight Python web framework
- **MySQL Connector**: Database connectivity
- **Google Generative AI**: Gemini API integration
- **Pandas**: Data manipulation and analysis
- **SQLParse**: SQL parsing and validation
- **Flask-CORS**: Cross-origin resource sharing

### Development Tools
- **Create React App**: React application setup
- **dotenv**: Environment variable management
- **Tabulate**: Data presentation formatting

## 🔒 Security Features

- **SQL Injection Protection**: All queries are validated and sanitized
- **Safe Query Execution**: Only SELECT statements allowed
- **Input Validation**: User input is thoroughly validated
- **Error Handling**: Comprehensive error management
- **Environment Variables**: Sensitive data stored securely

## 📈 Performance Optimizations

- **Query Limiting**: Automatic LIMIT clauses to prevent large result sets
- **Connection Pooling**: Efficient database connection management
- **Caching**: Strategic caching for improved response times
- **Lazy Loading**: Components loaded on demand

## 🧪 Testing

### Backend Testing
```bash
cd backend
python test.py
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📝 API Documentation

### Chat Endpoint
- **POST** `/api/chat`
- Handles natural language queries and returns either SQL results or conversational responses

### Analytics Endpoints
- **GET** `/api/analytics/overview` - General dashboard statistics
- **GET** `/api/analytics/sales-trend` - Sales trend data
- **GET** `/api/analytics/top-products` - Best-selling products
- **GET** `/api/analytics/categories` - Category performance
- **GET** `/api/analytics/inventory` - Inventory status

## 🤝 Contributing

This is a Final Year Project for academic purposes. If you'd like to contribute or have suggestions:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is created for academic purposes as part of a Final Year Project at University of Agriculture, Faisalabad (UAF).

## 👨‍💻 Author

**[Your Name]**
- University: University of Agriculture, Faisalabad (UAF)
- Degree: BS Computer Science
- Project: Final Year Project (FYP)
- Year: 2025

## 🙏 Acknowledgments

- **University of Agriculture, Faisalabad** for providing the academic framework
- **Google Gemini AI** for natural language processing capabilities
- **React.js Community** for excellent documentation and resources
- **Flask Community** for the lightweight and flexible web framework

## 📞 Support

For any questions or support regarding this project, please feel free to reach out or create an issue in the repository.

---

*This project demonstrates the practical application of AI technologies in database management and showcases modern web development practices suitable for real-world eCommerce applications.*
