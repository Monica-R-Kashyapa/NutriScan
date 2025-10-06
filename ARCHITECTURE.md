# 🏗️ NutriScan Architecture

Technical architecture and design decisions for the NutriScan application.

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                      (React.js App)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │ Scanner  │  │ History  │  │ Insights │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Service Layer (Axios)                │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST API
                       │ (JSON)
┌──────────────────────▼──────────────────────────────────────┐
│                      Backend API                             │
│                    (Flask REST API)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Auth   │  │   Food   │  │   User   │  │  System  │   │
│  │  Routes  │  │  Routes  │  │  Routes  │  │  Routes  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 Service Layer                         │  │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐       │  │
│  │  │ ML Service │ │  Nutrition │ │   Health   │       │  │
│  │  │            │ │  Service   │ │   Scorer   │       │  │
│  │  └────────────┘ └────────────┘ └────────────┘       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  Data Models                          │  │
│  │  ┌────────────┐ ┌────────────┐                       │  │
│  │  │    User    │ │   Scan     │                       │  │
│  │  │   Model    │ │  History   │                       │  │
│  │  └────────────┘ └────────────┘                       │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                     Database                                 │
│                   (MongoDB)                                  │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │    users     │  │ scan_history │                        │
│  │  collection  │  │  collection  │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   External Services                          │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │  TensorFlow  │  │     USDA     │                        │
│  │  ML Model    │  │  FoodData    │                        │
│  │              │  │     API      │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Design Patterns

### Frontend

#### Component Architecture
- **Container/Presentational Pattern**: Separation of logic and UI
- **Hooks Pattern**: State management with React hooks
- **Service Layer**: API calls abstracted in service files

#### State Management
- **Local State**: Component-level state with useState
- **Context API**: User authentication state
- **LocalStorage**: Persistent token storage

### Backend

#### Layered Architecture
1. **Route Layer**: HTTP request handling
2. **Service Layer**: Business logic
3. **Model Layer**: Data structures
4. **Database Layer**: Data persistence

#### Design Patterns Used
- **Blueprint Pattern**: Modular route organization
- **Service Pattern**: Reusable business logic
- **Factory Pattern**: Model creation
- **Singleton Pattern**: Service instances

## 📦 Project Structure

```
NutriScan/
├── backend/                    # Flask backend
│   ├── app.py                 # Application entry point
│   ├── config.py              # Configuration
│   ├── run.py                 # Development runner
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment template
│   │
│   ├── models/                # Data models
│   │   ├── user.py           # User model
│   │   └── scan_history.py   # Scan history model
│   │
│   ├── routes/                # API routes
│   │   ├── auth.py           # Authentication routes
│   │   ├── food.py           # Food scanning routes
│   │   └── user.py           # User routes
│   │
│   ├── services/              # Business logic
│   │   ├── ml_service.py     # ML predictions
│   │   ├── nutrition_service.py  # Nutrition data
│   │   └── health_scorer.py  # Health scoring
│   │
│   └── ml_models/             # ML models
│       ├── food_classifier.h5 # Trained model
│       └── food_labels.txt    # Food labels
│
├── frontend/                   # React frontend
│   ├── public/                # Static files
│   │   └── index.html
│   │
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   │   └── Navbar.js
│   │   │
│   │   ├── pages/             # Page components
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Dashboard.js
│   │   │   ├── Scanner.js
│   │   │   ├── History.js
│   │   │   └── Insights.js
│   │   │
│   │   ├── services/          # API services
│   │   │   └── api.js
│   │   │
│   │   ├── App.js             # Main app component
│   │   ├── App.css            # Global styles
│   │   ├── index.js           # Entry point
│   │   └── index.css          # Base styles
│   │
│   ├── package.json           # Dependencies
│   └── .env.example           # Environment template
│
└── Documentation/
    ├── README.md              # Project overview
    ├── SETUP_GUIDE.md         # Setup instructions
    ├── QUICK_START.md         # Quick start guide
    ├── FEATURES.md            # Feature list
    ├── ARCHITECTURE.md        # This file
    └── CONTRIBUTING.md        # Contribution guide
```

## 🔄 Data Flow

### Food Scanning Flow

```
1. User uploads image
   ↓
2. Frontend validates file
   ↓
3. FormData sent to /api/food/scan
   ↓
4. Backend receives image
   ↓
5. ML Service predicts food
   ↓
6. Nutrition Service fetches data
   ↓
7. Health Scorer calculates score
   ↓
8. Data saved to MongoDB
   ↓
9. Response sent to frontend
   ↓
10. UI displays results
```

### Authentication Flow

```
1. User enters credentials
   ↓
2. Frontend sends to /api/auth/login
   ↓
3. Backend verifies password
   ↓
4. JWT token generated
   ↓
5. Token sent to frontend
   ↓
6. Token stored in localStorage
   ↓
7. Token added to all API requests
   ↓
8. Backend verifies token
   ↓
9. Protected routes accessible
```

## 🗄️ Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  email: String (unique, indexed),
  password: String (hashed),
  name: String,
  created_at: DateTime,
  updated_at: DateTime
}
```

### Scan History Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId (indexed),
  food_name: String,
  image_path: String,
  nutrition_data: {
    calories: Number,
    protein: Number,
    carbs: Number,
    fat: Number,
    sugar: Number,
    fiber: Number,
    sodium: Number,
    serving_size: String
  },
  health_score: {
    status: String,
    score: Number,
    detailed_scores: Object,
    reasons: Array,
    recommendations: Array,
    emoji: String
  },
  alternatives: Array,
  scanned_at: DateTime (indexed)
}
```

## 🔐 Security Architecture

### Authentication
- **JWT Tokens**: Stateless authentication
- **Password Hashing**: bcrypt with salt
- **Token Expiration**: 24-hour validity
- **Secure Storage**: HttpOnly cookies (recommended for production)

### API Security
- **CORS**: Configured for specific origins
- **Input Validation**: All inputs validated
- **Error Handling**: Generic error messages
- **Rate Limiting**: (Recommended for production)

### Data Security
- **Environment Variables**: Sensitive data in .env
- **No Hardcoded Secrets**: All secrets configurable
- **File Upload Validation**: Type and size checks
- **SQL Injection Prevention**: MongoDB parameterized queries

## 🚀 Performance Optimizations

### Frontend
- **Code Splitting**: Route-based splitting
- **Lazy Loading**: Components loaded on demand
- **Image Optimization**: Compression before upload
- **Caching**: API response caching
- **Memoization**: React.memo for expensive components

### Backend
- **Database Indexing**: Indexed queries
- **Connection Pooling**: MongoDB connection pool
- **Caching**: (Can add Redis for production)
- **Async Operations**: Non-blocking I/O
- **Batch Processing**: Bulk operations where possible

## 📊 Scalability Considerations

### Horizontal Scaling
- **Stateless API**: Can run multiple instances
- **Load Balancer**: Distribute traffic
- **Database Sharding**: Scale MongoDB
- **CDN**: Serve static assets

### Vertical Scaling
- **Resource Optimization**: Efficient algorithms
- **Database Optimization**: Query optimization
- **Caching Layer**: Redis/Memcached
- **Background Jobs**: Celery for heavy tasks

## 🧪 Testing Strategy

### Frontend Testing
- **Unit Tests**: Component testing with Jest
- **Integration Tests**: API integration tests
- **E2E Tests**: Cypress for user flows
- **Visual Tests**: Storybook for components

### Backend Testing
- **Unit Tests**: Function-level tests
- **Integration Tests**: API endpoint tests
- **Load Tests**: Performance testing
- **Security Tests**: Vulnerability scanning

## 🔄 CI/CD Pipeline

### Recommended Pipeline
```
1. Code Push
   ↓
2. Linting & Formatting
   ↓
3. Unit Tests
   ↓
4. Integration Tests
   ↓
5. Build
   ↓
6. Security Scan
   ↓
7. Deploy to Staging
   ↓
8. E2E Tests
   ↓
9. Deploy to Production
```

## 🌐 Deployment Architecture

### Production Setup
```
┌─────────────┐
│   Cloudflare│  CDN & DDoS Protection
└──────┬──────┘
       │
┌──────▼──────┐
│Load Balancer│  Nginx/AWS ALB
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼──┐ ┌──▼──┐
│API  │ │API  │  Multiple instances
│ #1  │ │ #2  │
└──┬──┘ └──┬──┘
   │       │
   └───┬───┘
       │
┌──────▼──────┐
│  MongoDB    │  Replica Set
│  Cluster    │
└─────────────┘
```

## 🔮 Future Enhancements

### Architecture Improvements
- **Microservices**: Split into smaller services
- **Message Queue**: RabbitMQ/Kafka for async tasks
- **Caching Layer**: Redis for performance
- **API Gateway**: Centralized API management
- **Service Mesh**: Istio for microservices
- **GraphQL**: Alternative to REST API
- **WebSockets**: Real-time features
- **Serverless**: AWS Lambda functions

### Technology Stack Evolution
- **TypeScript**: Type safety
- **Next.js**: SSR for React
- **FastAPI**: Alternative to Flask
- **PostgreSQL**: Relational data needs
- **Docker**: Containerization
- **Kubernetes**: Orchestration
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack

## 📚 Technology Choices

### Why React?
- Component-based architecture
- Large ecosystem
- Virtual DOM performance
- Hooks for state management
- Strong community support

### Why Flask?
- Lightweight and flexible
- Easy to learn
- Great for APIs
- Extensive libraries
- Python ecosystem

### Why MongoDB?
- Flexible schema
- JSON-like documents
- Horizontal scaling
- Good for rapid development
- Rich query language

### Why JWT?
- Stateless authentication
- Scalable
- Cross-domain support
- Mobile-friendly
- Industry standard

## 🎓 Learning Resources

- [React Documentation](https://react.dev)
- [Flask Documentation](https://flask.palletsprojects.com)
- [MongoDB Documentation](https://docs.mongodb.com)
- [TensorFlow Documentation](https://www.tensorflow.org)
- [REST API Best Practices](https://restfulapi.net)

---

This architecture is designed to be:
- ✅ Scalable
- ✅ Maintainable
- ✅ Secure
- ✅ Performant
- ✅ Testable
- ✅ Extensible
