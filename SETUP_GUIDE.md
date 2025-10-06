# 🚀 NutriScan Setup Guide

Complete step-by-step guide to get NutriScan running on your machine.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 14+** - [Download](https://nodejs.org/)
- **MongoDB** - [Download](https://www.mongodb.com/try/download/community) or use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- **Git** (optional) - For version control

## 🔧 Installation Steps

### Step 1: MongoDB Setup

#### Option A: Local MongoDB
1. Install MongoDB Community Edition
2. Start MongoDB service:
   ```bash
   # Windows
   net start MongoDB
   
   # macOS
   brew services start mongodb-community
   
   # Linux
   sudo systemctl start mongod
   ```

#### Option B: MongoDB Atlas (Cloud)
1. Create free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Get connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/nutriscan`)

### Step 2: Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd C:\Users\..\NutriScan\backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create .env file:**
   ```bash
   copy .env.example .env
   ```

6. **Edit .env file with your settings:**


7. **Run the backend:**
   ```bash
   python app.py
   ```

   You should see:
   ```
   ✅ Model loaded or using fallback mode
   * Running on http://0.0.0.0:5000
   ```

### Step 3: Frontend Setup

1. **Open new terminal and navigate to frontend:**
   ```bash
   cd C:\Users\..\NutriScan\frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The app will open at `http://localhost:3000`

## 🎯 First Run

1. **Register a new account:**
   - Go to `http://localhost:3000`
   - Click "Register here"
   - Fill in your details
   - Click "Register"

2. **Scan your first food:**
   - Click "Scan Food" in the navbar
   - Upload a food image
   - Click "Scan Food"
   - View nutrition analysis and health score

## 🔑 Optional: USDA API Key

For more accurate nutrition data:

1. Get free API key from [USDA FoodData Central](https://fdc.nal.usda.gov/api-key-signup.html)
2. Add to `.env` file:
   ```env
   USDA_API_KEY=your_actual_api_key_here
   ```
3. Restart backend server

## 🤖 Optional: ML Model Setup

The app works in fallback mode without a trained model. To add a real ML model:

### Option 1: Download Pre-trained Model
1. Download a Food-101 model from [Kaggle](https://www.kaggle.com/models)
2. Save as `backend/ml_models/food_classifier.h5`
3. Restart backend

### Option 2: Train Your Own Model
```python
# Example training script (train_model.py)
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

# Load base model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Add custom layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(30, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train with your dataset
# model.fit(train_data, epochs=10, validation_data=val_data)

# Save model
model.save('backend/ml_models/food_classifier.h5')
```

## 🧪 Testing the Application

### Test Backend API
```bash
# Health check
curl http://localhost:5000/api/health

# Should return: {"status":"healthy","database":"connected","environment":"development"}
```

### Test Frontend
1. Open browser to `http://localhost:3000`
2. Register/Login
3. Upload a food image
4. Verify results appear

## 📱 Features to Test

- ✅ User Registration & Login
- ✅ Food Image Upload & Scanning
- ✅ Nutrition Analysis Display
- ✅ Health Score Calculation
- ✅ Scan History
- ✅ Insights & Analytics
- ✅ Healthier Alternatives Suggestions

## 🐛 Troubleshooting

### Backend Issues

**MongoDB Connection Error:**
```
Solution: Ensure MongoDB is running
- Check: net start MongoDB (Windows)
- Or use MongoDB Atlas connection string
```

**Port 5000 already in use:**
```
Solution: Change PORT in .env file to 5001 or another port
```

**Module not found errors:**
```
Solution: Ensure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```

### Frontend Issues

**Port 3000 already in use:**
```
Solution: The app will prompt to use another port (3001)
Press 'Y' to continue
```

**API connection errors:**
```
Solution: Ensure backend is running on http://localhost:5000
Check proxy setting in package.json
```

**npm install fails:**
```
Solution: Clear npm cache and retry
npm cache clean --force
npm install
```

## 🔒 Security Notes

- Change `JWT_SECRET` in production
- Use strong passwords
- Enable HTTPS in production
- Keep API keys secure (never commit to Git)
- Use environment variables for sensitive data

## 📊 Database Structure

The app creates these MongoDB collections:
- `users` - User accounts
- `scan_history` - Food scan records

## 🚀 Production Deployment

### Backend (Flask)
- Use Gunicorn or uWSGI
- Set `FLASK_ENV=production`
- Use proper MongoDB Atlas cluster
- Enable CORS only for your domain

### Frontend (React)
- Build: `npm run build`
- Deploy to Vercel, Netlify, or AWS S3
- Update API URL in production

## 📞 Support

If you encounter issues:
1. Check this guide thoroughly
2. Review error messages in terminal
3. Check MongoDB connection
4. Ensure all dependencies are installed
5. Verify Python and Node.js versions

## 🎉 Success!

If everything is working:
- Backend: `http://localhost:5000` ✅
- Frontend: `http://localhost:3000` ✅
- MongoDB: Connected ✅

You're ready to scan and analyze food! 🍎
