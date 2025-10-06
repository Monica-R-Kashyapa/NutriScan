from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from bson import ObjectId
import os
from models.scan_history import ScanHistory
from services.ml_service import ml_service
from services.nutrition_service import nutrition_service
from services.health_scorer import health_scorer
from routes.auth import verify_token
from config import Config

bp = Blueprint('food', __name__)

def get_db():
    """Get database instance"""
    from app import mongo
    return mongo.db

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@bp.route('/scan', methods=['POST'])
def scan_food():
    """Scan food image and return nutrition analysis"""
    try:
        # Verify authentication
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Check if file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save file
        filename = secure_filename(f"{user_id}_{datetime.utcnow().timestamp()}_{file.filename}")
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Predict food item
        predictions = ml_service.predict(filepath)
        
        if not predictions:
            return jsonify({'error': 'Could not identify food'}), 400
        
        # Get top prediction
        top_prediction = predictions[0]
        food_name = top_prediction['food_name']
        confidence = top_prediction['confidence']
        
        # Get nutrition data
        nutrition_data = nutrition_service.get_nutrition_data(food_name)
        
        # Calculate health score
        health_score = health_scorer.calculate_score(nutrition_data)
        
        # Get alternatives
        alternatives = nutrition_service.get_healthier_alternatives(food_name)
        
        # Save to history
        db = get_db()
        scan = ScanHistory(
            user_id=user_id,
            food_name=food_name,
            image_path=filepath,
            nutrition_data=nutrition_data,
            health_score=health_score,
            alternatives=alternatives
        )
        result = db.scan_history.insert_one(scan.to_dict())
        
        return jsonify({
            'scan_id': str(result.inserted_id),
            'food_name': food_name,
            'confidence': confidence,
            'nutrition': nutrition_data,
            'health_score': health_score,
            'alternatives': alternatives,
            'all_predictions': predictions
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/history', methods=['GET'])
def get_history():
    """Get user's scan history"""
    try:
        # Verify authentication
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get query parameters
        limit = int(request.args.get('limit', 20))
        skip = int(request.args.get('skip', 0))
        
        # Get history
        db = get_db()
        scans = list(db.scan_history.find(
            {'user_id': ObjectId(user_id)}
        ).sort('scanned_at', -1).skip(skip).limit(limit))
        
        # Serialize scans
        history = [ScanHistory.serialize(scan) for scan in scans]
        
        return jsonify({
            'history': history,
            'total': db.scan_history.count_documents({'user_id': ObjectId(user_id)})
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/history/<scan_id>', methods=['GET'])
def get_scan_detail(scan_id):
    """Get detailed information about a specific scan"""
    try:
        # Verify authentication
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get scan
        db = get_db()
        scan = db.scan_history.find_one({
            '_id': ObjectId(scan_id),
            'user_id': ObjectId(user_id)
        })
        
        if not scan:
            return jsonify({'error': 'Scan not found'}), 404
        
        return jsonify({
            'scan': ScanHistory.serialize(scan)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/insights', methods=['GET'])
def get_insights():
    """Get nutrition insights and statistics"""
    try:
        # Verify authentication
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get time period
        period = request.args.get('period', 'week')  # week, month, all
        
        # Calculate date range
        if period == 'week':
            start_date = datetime.utcnow() - timedelta(days=7)
        elif period == 'month':
            start_date = datetime.utcnow() - timedelta(days=30)
        else:
            start_date = datetime.utcnow() - timedelta(days=365)
        
        # Get scans in period
        db = get_db()
        scans = list(db.scan_history.find({
            'user_id': ObjectId(user_id),
            'scanned_at': {'$gte': start_date}
        }).sort('scanned_at', 1))
        
        # Calculate statistics
        stats = ScanHistory.get_weekly_stats(scans)
        
        # Get daily breakdown
        daily_data = {}
        for scan in scans:
            date_key = scan['scanned_at'].strftime('%Y-%m-%d')
            if date_key not in daily_data:
                daily_data[date_key] = {
                    'date': date_key,
                    'scans': 0,
                    'calories': 0,
                    'healthy': 0,
                    'unhealthy': 0
                }
            
            daily_data[date_key]['scans'] += 1
            daily_data[date_key]['calories'] += scan['nutrition_data'].get('calories', 0)
            
            status = scan['health_score'].get('status', '')
            if status == 'healthy':
                daily_data[date_key]['healthy'] += 1
            elif status == 'unhealthy':
                daily_data[date_key]['unhealthy'] += 1
        
        # Convert to list
        daily_breakdown = list(daily_data.values())
        
        # Get most scanned foods
        food_counts = {}
        for scan in scans:
            food_name = scan['food_name']
            food_counts[food_name] = food_counts.get(food_name, 0) + 1
        
        top_foods = sorted(food_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return jsonify({
            'period': period,
            'statistics': stats,
            'daily_breakdown': daily_breakdown,
            'top_foods': [{'name': name, 'count': count} for name, count in top_foods]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/compare', methods=['POST'])
def compare_foods():
    """Compare two foods"""
    try:
        # Verify authentication
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        data = request.get_json()
        food1_name = data.get('food1')
        food2_name = data.get('food2')
        
        if not food1_name or not food2_name:
            return jsonify({'error': 'Both food names are required'}), 400
        
        # Get nutrition data
        nutrition1 = nutrition_service.get_nutrition_data(food1_name)
        nutrition2 = nutrition_service.get_nutrition_data(food2_name)
        
        # Calculate health scores
        score1 = health_scorer.calculate_score(nutrition1)
        score2 = health_scorer.calculate_score(nutrition2)
        
        # Compare
        comparison = health_scorer.compare_foods(nutrition1, nutrition2)
        
        return jsonify({
            'food1': {
                'name': food1_name,
                'nutrition': nutrition1,
                'health_score': score1
            },
            'food2': {
                'name': food2_name,
                'nutrition': nutrition2,
                'health_score': score2
            },
            'comparison': comparison
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(Config.UPLOAD_FOLDER, filename)
