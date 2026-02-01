# 🍎 NutriScan – AI-powered Food Health Scanner

An intelligent food recognition and nutrition analysis application that helps users make healthier food choices.

## 🔹 Features

- **Food Recognition**: Upload or scan food images using AI-powered image classification
- **Real-Time Camera Scanning**: Capture food photos directly from your camera (NEW!)
- **Nutrition Analysis**: Get detailed nutritional information (calories, sugar, fat, protein, etc.)
- **Health Score**: Automatic classification as Healthy/Moderately Healthy/Unhealthy
- **User Dashboard**: Track scanned foods, view history, and nutrition insights
- **Smart Suggestions**: Get healthier food alternatives
- **Visual Analytics**: Weekly/monthly nutrition charts and trends

## 🔹 Tech Stack

### Frontend
- React.js with modern hooks
- CSS3 for styling
- Recharts for data visualization
- Axios for API calls

### Backend
- Python Flask REST API
- TensorFlow/Keras for ML model
- JWT authentication
- CORS enabled

### Database
- MongoDB for flexible data storage
- User profiles, scan history, and food data

### AI/ML
- Pre-trained CNN model (Food-101 dataset)
- USDA FoodData Central API integration
- Custom health scoring algorithm

## 🚀 Quick Start

### Prerequisites
- Node.js (v14+)
- Python (v3.8+)
- MongoDB (local or Atlas)

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

### Environment Variables

Create `.env` file in backend directory:
```
MONGODB_URI=mongodb://localhost:27017/nutriscan
JWT_SECRET=your_secret_key_here
USDA_API_KEY=your_usda_api_key_here
```

## 🔄 User Flow

1. User opens app → uploads/scans food image 📸
2. ML model predicts food item (e.g., "Pizza")
3. Backend fetches nutrition data from API
4. Health scoring engine evaluates the food
5. Frontend displays results with health status
6. Data saved to user's history for tracking

## 🎯 Health Scoring Rules

- **Healthy** ✅: Calories < 400, Sugar < 15g, Fat < 10g
- **Moderately Healthy** ⚠️: Calories < 600, Sugar < 25g, Fat < 20g
- **Unhealthy** ❌: Above moderate thresholds
