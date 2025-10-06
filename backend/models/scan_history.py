from datetime import datetime
from bson import ObjectId

class ScanHistory:
    """Scan history model for MongoDB"""
    
    def __init__(self, user_id, food_name, image_path, nutrition_data, health_score, alternatives=None):
        self.user_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
        self.food_name = food_name
        self.image_path = image_path
        self.nutrition_data = nutrition_data
        self.health_score = health_score
        self.alternatives = alternatives or []
        self.scanned_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert scan history to dictionary"""
        return {
            'user_id': self.user_id,
            'food_name': self.food_name,
            'image_path': self.image_path,
            'nutrition_data': self.nutrition_data,
            'health_score': self.health_score,
            'alternatives': self.alternatives,
            'scanned_at': self.scanned_at
        }
    
    @staticmethod
    def serialize(scan_doc):
        """Serialize scan document for JSON response"""
        return {
            'id': str(scan_doc['_id']),
            'user_id': str(scan_doc['user_id']),
            'food_name': scan_doc['food_name'],
            'image_path': scan_doc.get('image_path'),
            'nutrition_data': scan_doc['nutrition_data'],
            'health_score': scan_doc['health_score'],
            'alternatives': scan_doc.get('alternatives', []),
            'scanned_at': scan_doc['scanned_at'].isoformat() if scan_doc.get('scanned_at') else None
        }
    
    @staticmethod
    def get_weekly_stats(scans):
        """Calculate weekly nutrition statistics"""
        if not scans:
            return {
                'total_scans': 0,
                'avg_calories': 0,
                'healthy_count': 0,
                'unhealthy_count': 0
            }
        
        total_calories = 0
        healthy_count = 0
        unhealthy_count = 0
        
        for scan in scans:
            nutrition = scan.get('nutrition_data', {})
            total_calories += nutrition.get('calories', 0)
            
            health_status = scan.get('health_score', {}).get('status', '')
            if health_status == 'healthy':
                healthy_count += 1
            elif health_status == 'unhealthy':
                unhealthy_count += 1
        
        return {
            'total_scans': len(scans),
            'avg_calories': round(total_calories / len(scans), 2) if scans else 0,
            'healthy_count': healthy_count,
            'unhealthy_count': unhealthy_count,
            'moderate_count': len(scans) - healthy_count - unhealthy_count
        }
