from config import Config

class NutritionService:
    """Service for nutrition data - uses custom database for your foods"""
    
    def __init__(self):
        self.fallback_data = self._load_fallback_data()
    
    def _load_fallback_data(self):
        """Load fallback nutrition data for common foods"""
        return {
            'pizza': {
                'calories': 266,
                'protein': 11,
                'carbs': 33,
                'fat': 10,
                'sugar': 3.8,
                'fiber': 2.5,
                'sodium': 598,
                'serving_size': '100g'
            },
            'hamburger': {
                'calories': 295,
                'protein': 17,
                'carbs': 24,
                'fat': 14,
                'sugar': 5,
                'fiber': 1.5,
                'sodium': 497,
                'serving_size': '100g'
            },
            'french fries': {
                'calories': 312,
                'protein': 3.4,
                'carbs': 41,
                'fat': 15,
                'sugar': 0.2,
                'fiber': 3.8,
                'sodium': 210,
                'serving_size': '100g'
            },
            'salad': {
                'calories': 33,
                'protein': 2.5,
                'carbs': 6.3,
                'fat': 0.3,
                'sugar': 2.3,
                'fiber': 2.1,
                'sodium': 28,
                'serving_size': '100g'
            },
            'sushi': {
                'calories': 143,
                'protein': 6,
                'carbs': 21,
                'fat': 3.7,
                'sugar': 3,
                'fiber': 0.5,
                'sodium': 428,
                'serving_size': '100g'
            },
            'ice cream': {
                'calories': 207,
                'protein': 3.5,
                'carbs': 24,
                'fat': 11,
                'sugar': 21,
                'fiber': 0.7,
                'sodium': 80,
                'serving_size': '100g'
            },
            'donut': {
                'calories': 452,
                'protein': 5,
                'carbs': 51,
                'fat': 25,
                'sugar': 27,
                'fiber': 1.4,
                'sodium': 326,
                'serving_size': '100g'
            },
            'grilled salmon': {
                'calories': 206,
                'protein': 22,
                'carbs': 0,
                'fat': 12,
                'sugar': 0,
                'fiber': 0,
                'sodium': 59,
                'serving_size': '100g'
            },
            'chicken wings': {
                'calories': 203,
                'protein': 30,
                'carbs': 0,
                'fat': 8.1,
                'sugar': 0,
                'fiber': 0,
                'sodium': 82,
                'serving_size': '100g'
            },
            'apple pie': {
                'calories': 237,
                'protein': 2,
                'carbs': 34,
                'fat': 11,
                'sugar': 16,
                'fiber': 1.6,
                'sodium': 266,
                'serving_size': '100g'
            },
            'hot dog': {
                'calories': 290,
                'protein': 10,
                'carbs': 24,
                'fat': 17,
                'sugar': 4,
                'fiber': 1,
                'sodium': 810,
                'serving_size': '100g'
            },
            'sandwich': {
                'calories': 250,
                'protein': 12,
                'carbs': 30,
                'fat': 9,
                'sugar': 4,
                'fiber': 2,
                'sodium': 520,
                'serving_size': '100g'
            },
            'fried rice': {
                'calories': 163,
                'protein': 4.2,
                'carbs': 26,
                'fat': 4.6,
                'sugar': 0.5,
                'fiber': 1.2,
                'sodium': 380,
                'serving_size': '100g'
            },
            'tacos': {
                'calories': 226,
                'protein': 9,
                'carbs': 20,
                'fat': 13,
                'sugar': 2,
                'fiber': 3,
                'sodium': 367,
                'serving_size': '100g'
            },
            'spaghetti': {
                'calories': 158,
                'protein': 5.8,
                'carbs': 31,
                'fat': 0.9,
                'sugar': 2.7,
                'fiber': 1.8,
                'sodium': 6,
                'serving_size': '100g'
            },
            'cake': {
                'calories': 257,
                'protein': 2.9,
                'carbs': 42,
                'fat': 9.3,
                'sugar': 28,
                'fiber': 0.8,
                'sodium': 242,
                'serving_size': '100g'
            },
            'burrito': {
                'calories': 206,
                'protein': 8,
                'carbs': 28,
                'fat': 7,
                'sugar': 2,
                'fiber': 3,
                'sodium': 495,
                'serving_size': '100g'
            },
            'steak': {
                'calories': 271,
                'protein': 25,
                'carbs': 0,
                'fat': 19,
                'sugar': 0,
                'fiber': 0,
                'sodium': 54,
                'serving_size': '100g'
            },
            'pancakes': {
                'calories': 227,
                'protein': 6,
                'carbs': 28,
                'fat': 10,
                'sugar': 6,
                'fiber': 1,
                'sodium': 439,
                'serving_size': '100g'
            },
            'waffles': {
                'calories': 291,
                'protein': 7,
                'carbs': 33,
                'fat': 14,
                'sugar': 10,
                'fiber': 1.7,
                'sodium': 511,
                'serving_size': '100g'
            }
        }
    
    def get_nutrition_data(self, food_name):
        """Get nutrition data for a food item"""
        # Normalize food name
        food_key = food_name.lower().strip()
        
        # PRIORITY 1: Try exact match in your custom database
        if food_key in self.fallback_data:
            print(f"✅ Found nutrition data for: {food_name}")
            return self.fallback_data[food_key]
        
        # PRIORITY 2: Try partial match
        for key, data in self.fallback_data.items():
            if key in food_key or food_key in key:
                print(f"✅ Found partial match: {key}")
                return data
        
        # PRIORITY 3: Return generic data as last resort
        print(f"⚠️ No nutrition data found for '{food_name}', using generic values")
        print(f"💡 Run 'python auto_nutrition.py' to add nutrition data for your foods")
        return {
            'calories': 200,
            'protein': 8,
            'carbs': 25,
            'fat': 8,
            'sugar': 5,
            'fiber': 2,
            'sodium': 300,
            'serving_size': '100g'
        }
    
    
    def get_healthier_alternatives(self, food_name):
        """Get healthier alternatives for a food item"""
        alternatives_map = {
            'pizza': ['Whole wheat veggie pizza', 'Cauliflower crust pizza', 'Grilled chicken salad'],
            'hamburger': ['Turkey burger', 'Veggie burger', 'Grilled chicken sandwich'],
            'french fries': ['Baked sweet potato fries', 'Air-fried vegetables', 'Roasted chickpeas'],
            'ice cream': ['Greek yogurt with berries', 'Frozen banana nice cream', 'Sorbet'],
            'donut': ['Whole grain muffin', 'Oatmeal with fruit', 'Greek yogurt parfait'],
            'hot dog': ['Grilled chicken breast', 'Turkey sausage', 'Veggie dog'],
            'cake': ['Angel food cake', 'Fruit salad', 'Dark chocolate'],
            'soda': ['Sparkling water with lemon', 'Herbal tea', 'Infused water'],
            'fried rice': ['Brown rice with vegetables', 'Quinoa bowl', 'Cauliflower rice'],
            'chicken wings': ['Grilled chicken breast', 'Baked chicken tenders', 'Grilled chicken skewers'],
            'pancakes': ['Whole wheat pancakes', 'Oatmeal pancakes', 'Protein pancakes'],
            'waffles': ['Whole grain waffles', 'Oat waffles with fruit', 'Protein waffles']
        }
        
        food_key = food_name.lower().strip()
        
        # Try exact match
        if food_key in alternatives_map:
            return alternatives_map[food_key]
        
        # Try partial match
        for key, alternatives in alternatives_map.items():
            if key in food_key or food_key in key:
                return alternatives
        
        # Default alternatives
        return ['Grilled vegetables', 'Fresh salad', 'Lean protein with quinoa']

# Global instance
nutrition_service = NutritionService()
