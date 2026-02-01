# ⚡ Quick Start Guide

Get NutriScan running in 5 minutes!

## 🎯 Prerequisites

- Python 3.8+
- Node.js 14+
- MongoDB (local or Atlas)

## 🚀 Quick Setup

### 1️⃣ Backend (2 minutes)

```bash
# Navigate to backend
cd C:\Users\...\NutriScan\backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env and set MongoDB URI (use default for local MongoDB)
# MONGODB_URI=mongodb://localhost:27017/nutriscan

# Run backend
python run.py
```

✅ Backend running at `http://localhost:5000`

### 2️⃣ Frontend (2 minutes)

Open **new terminal**:

```bash
# Navigate to frontend
cd C:\Users\...\NutriScan\frontend

# Install dependencies
npm install

# Start development server
npm start
```

✅ Frontend running at `http://localhost:3000`

### 3️⃣ Start Using (1 minute)

1. **Register**: Create account 
2. **Scan**: Click "Scan Food" → Upload image → Get results!
3. **Explore**: Check Dashboard, History, and Insights

## 🎉 That's It!

You're now running NutriScan locally!

## 📚 Next Steps

- Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup
- See [README.md](README.md) for project overview

Happy scanning! 🍎
