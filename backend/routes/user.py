from flask import Blueprint, request, jsonify
from bson import ObjectId
from routes.auth import verify_token

bp = Blueprint('user', __name__)

def get_db():
    """Get database instance"""
    from app import mongo
    return mongo.db

@bp.route('/stats', methods=['GET'])
def get_user_stats():
    """Get user statistics"""
    try:
        # Verify authentication
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        db = get_db()
        
        # Get total scans
        total_scans = db.scan_history.count_documents({'user_id': ObjectId(user_id)})
        
        # Get health status breakdown
        scans = list(db.scan_history.find({'user_id': ObjectId(user_id)}))
        
        healthy_count = 0
        moderate_count = 0
        unhealthy_count = 0
        
        for scan in scans:
            status = scan.get('health_score', {}).get('status', '')
            if status == 'healthy':
                healthy_count += 1
            elif status == 'moderate':
                moderate_count += 1
            elif status == 'unhealthy':
                unhealthy_count += 1
        
        return jsonify({
            'total_scans': total_scans,
            'healthy_count': healthy_count,
            'moderate_count': moderate_count,
            'unhealthy_count': unhealthy_count,
            'health_percentage': round((healthy_count / total_scans * 100), 1) if total_scans > 0 else 0
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
