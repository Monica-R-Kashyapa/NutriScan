from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import jwt
from bson import ObjectId
from models.user import User
from config import Config

bp = Blueprint('auth', __name__)

def get_db():
    """Get database instance"""
    from app import mongo
    return mongo.db

def create_token(user_id):
    """Create JWT token"""
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        print(f"📝 Registration request received: {data.get('email') if data else 'No data'}")
        
        # Validate input
        if not data or not data.get('email') or not data.get('password'):
            print("❌ Validation failed: Missing email or password")
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        name = data.get('name', email.split('@')[0])
        
        print(f"📧 Checking if user exists: {email}")
        
        # Check if user already exists
        db = get_db()
        existing_user = db.users.find_one({'email': email})
        if existing_user:
            print(f"⚠️ User already exists: {email}")
            return jsonify({'error': 'User already exists'}), 400
        
        print(f"👤 Creating new user: {email}")
        
        # Create new user
        user = User(email=email, password=password, name=name)
        result = db.users.insert_one(user.to_dict())
        
        print(f"✅ User created with ID: {result.inserted_id}")
        
        # Create token
        token = create_token(result.inserted_id)
        
        print(f"🎫 Token created for user: {email}")
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': str(result.inserted_id),
                'email': email,
                'name': name
            }
        }), 201
        
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Find user
        db = get_db()
        user = db.users.find_one({'email': email})
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not User.verify_password(password, user['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Create token
        token = create_token(user['_id'])
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': User.serialize(user)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get user
        db = get_db()
        user = db.users.find_one({'_id': ObjectId(user_id)})
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': User.serialize(user)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/profile', methods=['PUT'])
def update_profile():
    """Update user profile"""
    try:
        # Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Get update data
        data = request.get_json()
        update_fields = {}
        
        if data.get('name'):
            update_fields['name'] = data['name']
        
        if not update_fields:
            return jsonify({'error': 'No fields to update'}), 400
        
        update_fields['updated_at'] = datetime.utcnow()
        
        # Update user
        db = get_db()
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_fields}
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'No changes made'}), 400
        
        # Get updated user
        user = db.users.find_one({'_id': ObjectId(user_id)})
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': User.serialize(user)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
