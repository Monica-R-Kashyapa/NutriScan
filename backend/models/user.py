from datetime import datetime
from bson import ObjectId
import bcrypt

class User:
    """User model for MongoDB"""
    
    def __init__(self, email, password, name=None):
        self.email = email
        self.password = self._hash_password(password)
        self.name = name or email.split('@')[0]
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def _hash_password(self, password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """Verify password against hash"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'email': self.email,
            'name': self.name,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        """Create user from dictionary"""
        user = User.__new__(User)
        user.email = data.get('email')
        user.name = data.get('name')
        user.password = data.get('password')
        user.created_at = data.get('created_at', datetime.utcnow())
        user.updated_at = data.get('updated_at', datetime.utcnow())
        return user
    
    @staticmethod
    def serialize(user_doc):
        """Serialize user document for JSON response"""
        return {
            'id': str(user_doc['_id']),
            'email': user_doc['email'],
            'name': user_doc['name'],
            'created_at': user_doc['created_at'].isoformat() if user_doc.get('created_at') else None
        }
