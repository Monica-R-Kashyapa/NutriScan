from config import Config

class HealthScorer:
    """Service for calculating health scores"""
    
    def __init__(self):
        self.healthy_thresholds = Config.HEALTHY_THRESHOLDS
        self.moderate_thresholds = Config.MODERATE_THRESHOLDS
    
    def calculate_score(self, nutrition_data):
        """
        Calculate health score based on nutrition data
        Returns: dict with status, score, and reasons
        """
        calories = nutrition_data.get('calories', 0)
        sugar = nutrition_data.get('sugar', 0)
        fat = nutrition_data.get('fat', 0)
        sodium = nutrition_data.get('sodium', 0)
        protein = nutrition_data.get('protein', 0)
        fiber = nutrition_data.get('fiber', 0)
        
        # Calculate individual scores
        scores = {
            'calories': self._score_calories(calories),
            'sugar': self._score_sugar(sugar),
            'fat': self._score_fat(fat),
            'sodium': self._score_sodium(sodium),
            'protein': self._score_protein(protein),
            'fiber': self._score_fiber(fiber)
        }
        
        # Calculate overall score (0-100)
        overall_score = sum(scores.values()) / len(scores)
        
        # Determine status
        status = self._determine_status(scores, nutrition_data)
        
        # Generate reasons
        reasons = self._generate_reasons(nutrition_data, scores)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(nutrition_data, scores)
        
        return {
            'status': status,
            'score': round(overall_score, 1),
            'detailed_scores': scores,
            'reasons': reasons,
            'recommendations': recommendations,
            'emoji': self._get_emoji(status)
        }
    
    def _score_calories(self, calories):
        """Score calories (0-100)"""
        if calories <= self.healthy_thresholds['calories']:
            return 100
        elif calories <= self.moderate_thresholds['calories']:
            return 60
        else:
            # Decrease score as calories increase
            return max(0, 60 - (calories - self.moderate_thresholds['calories']) / 10)
    
    def _score_sugar(self, sugar):
        """Score sugar content (0-100)"""
        if sugar <= self.healthy_thresholds['sugar']:
            return 100
        elif sugar <= self.moderate_thresholds['sugar']:
            return 60
        else:
            return max(0, 60 - (sugar - self.moderate_thresholds['sugar']) * 2)
    
    def _score_fat(self, fat):
        """Score fat content (0-100)"""
        if fat <= self.healthy_thresholds['fat']:
            return 100
        elif fat <= self.moderate_thresholds['fat']:
            return 60
        else:
            return max(0, 60 - (fat - self.moderate_thresholds['fat']) * 2)
    
    def _score_sodium(self, sodium):
        """Score sodium content (0-100)"""
        if sodium <= self.healthy_thresholds['sodium']:
            return 100
        elif sodium <= self.moderate_thresholds['sodium']:
            return 60
        else:
            return max(0, 60 - (sodium - self.moderate_thresholds['sodium']) / 20)
    
    def _score_protein(self, protein):
        """Score protein content (0-100) - higher is better"""
        if protein >= 20:
            return 100
        elif protein >= 10:
            return 80
        elif protein >= 5:
            return 60
        else:
            return 40
    
    def _score_fiber(self, fiber):
        """Score fiber content (0-100) - higher is better"""
        if fiber >= 5:
            return 100
        elif fiber >= 3:
            return 80
        elif fiber >= 1:
            return 60
        else:
            return 40
    
    def _determine_status(self, scores, nutrition_data):
        """Determine overall health status"""
        avg_score = sum(scores.values()) / len(scores)
        
        # Check critical thresholds
        calories = nutrition_data.get('calories', 0)
        sugar = nutrition_data.get('sugar', 0)
        fat = nutrition_data.get('fat', 0)
        
        # Unhealthy if any critical metric is too high
        if (calories > self.moderate_thresholds['calories'] or
            sugar > self.moderate_thresholds['sugar'] or
            fat > self.moderate_thresholds['fat']):
            return 'unhealthy'
        
        # Healthy if score is high and all metrics are good
        if avg_score >= 80:
            return 'healthy'
        elif avg_score >= 60:
            return 'moderate'
        else:
            return 'unhealthy'
    
    def _generate_reasons(self, nutrition_data, scores):
        """Generate reasons for the health score"""
        reasons = []
        
        calories = nutrition_data.get('calories', 0)
        sugar = nutrition_data.get('sugar', 0)
        fat = nutrition_data.get('fat', 0)
        sodium = nutrition_data.get('sodium', 0)
        protein = nutrition_data.get('protein', 0)
        fiber = nutrition_data.get('fiber', 0)
        
        # Negative factors
        if calories > self.moderate_thresholds['calories']:
            reasons.append(f"High calories ({calories} kcal)")
        if sugar > self.moderate_thresholds['sugar']:
            reasons.append(f"High sugar content ({sugar}g)")
        if fat > self.moderate_thresholds['fat']:
            reasons.append(f"High fat content ({fat}g)")
        if sodium > self.moderate_thresholds['sodium']:
            reasons.append(f"High sodium ({sodium}mg)")
        
        # Positive factors
        if protein >= 15:
            reasons.append(f"Good protein content ({protein}g)")
        if fiber >= 3:
            reasons.append(f"Good fiber content ({fiber}g)")
        if calories <= self.healthy_thresholds['calories']:
            reasons.append(f"Low calorie ({calories} kcal)")
        
        return reasons if reasons else ["Moderate nutritional value"]
    
    def _generate_recommendations(self, nutrition_data, scores):
        """Generate personalized recommendations"""
        recommendations = []
        
        calories = nutrition_data.get('calories', 0)
        sugar = nutrition_data.get('sugar', 0)
        fat = nutrition_data.get('fat', 0)
        protein = nutrition_data.get('protein', 0)
        fiber = nutrition_data.get('fiber', 0)
        
        if calories > self.moderate_thresholds['calories']:
            recommendations.append("Consider portion control or choose lower-calorie alternatives")
        
        if sugar > self.moderate_thresholds['sugar']:
            recommendations.append("Reduce sugar intake by choosing unsweetened options")
        
        if fat > self.moderate_thresholds['fat']:
            recommendations.append("Opt for grilled or baked versions instead of fried")
        
        if protein < 10:
            recommendations.append("Add lean protein sources to make it more balanced")
        
        if fiber < 3:
            recommendations.append("Include more vegetables or whole grains for fiber")
        
        if not recommendations:
            recommendations.append("This is a balanced choice! Maintain portion control.")
        
        return recommendations
    
    def _get_emoji(self, status):
        """Get emoji for health status"""
        emoji_map = {
            'healthy': '✅',
            'moderate': '⚠️',
            'unhealthy': '❌'
        }
        return emoji_map.get(status, '❓')
    
    def compare_foods(self, food1_nutrition, food2_nutrition):
        """Compare two foods and return which is healthier"""
        score1 = self.calculate_score(food1_nutrition)
        score2 = self.calculate_score(food2_nutrition)
        
        return {
            'food1_score': score1['score'],
            'food2_score': score2['score'],
            'healthier': 'food1' if score1['score'] > score2['score'] else 'food2',
            'difference': abs(score1['score'] - score2['score'])
        }

# Global instance
health_scorer = HealthScorer()
