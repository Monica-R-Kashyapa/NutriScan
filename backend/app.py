from flask import Flask, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from config import Config
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config["MONGO_URI"] = app.config["MONGODB_URI"]

# Initialize MongoDB
mongo = PyMongo(app)

# Create upload folder if it doesn't exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Import routes
from routes import auth, food, user

# Register blueprints
app.register_blueprint(auth.bp, url_prefix='/api/auth')
app.register_blueprint(food.bp, url_prefix='/api/food')
app.register_blueprint(user.bp, url_prefix='/api/user')

@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'NutriScan API is running',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    """API health check"""
    try:
        # Test MongoDB connection
        mongo.db.command('ping')
        db_status = 'connected'
    except Exception as e:
        db_status = f'disconnected: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'environment': Config.FLASK_ENV
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )
