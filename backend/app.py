"""
HealthNest AI Backend API
Flask REST API for health assistant chatbot
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Load models on startup
print("🔄 Loading AI models...")

try:
    qa_vectorizer = joblib.load('../models/qa_vectorizer.pkl')
    qa_database = joblib.load('../models/qa_database.pkl')
    print("✓ Q&A Model loaded")
except:
    print("⚠ Q&A Model not found")
    qa_vectorizer = None
    qa_database = None

try:
    calorie_predictor = joblib.load('../models/calorie_predictor.pkl')
    print("✓ Calorie Predictor loaded")
except:
    print("⚠ Calorie Predictor not found")
    calorie_predictor = None

try:
    exercise_recommender = joblib.load('../models/exercise_recommender.pkl')
    exercise_encoder = joblib.load('../models/exercise_encoder.pkl')
    print("✓ Exercise Recommender loaded")
except:
    print("⚠ Exercise Recommender not found")
    exercise_recommender = None
    exercise_encoder = None

try:
    with open('../models/health_knowledge.json', 'r') as f:
        health_knowledge = json.load(f)
    print("✓ Health Knowledge Base loaded")
except:
    print("⚠ Health Knowledge Base not found")
    health_knowledge = {}

print("✅ Models loaded successfully!\n")


# Helper Functions

def get_bmi(weight_kg, height_m):
    """Calculate BMI"""
    return weight_kg / (height_m ** 2)


def get_bmi_category(bmi):
    """Get BMI category and advice"""
    if 'bmi_ranges' not in health_knowledge:
        return None
    
    for category, data in health_knowledge['bmi_ranges'].items():
        if data['range'][0] <= bmi < data['range'][1]:
            return {
                'category': category,
                'advice': data['advice']
            }
    return None


def handle_pregnancy_query(message, user_profile):
    """Handle pregnancy-related queries"""
    if 'pregnancy' not in health_knowledge:
        return None
    
    # Extract week number if mentioned
    import re
    week_match = re.search(r'week\s*(\d+)', message)
    
    if week_match:
        week = int(week_match.group(1))
        week_key = f"week_{week}"
        
        if week_key in health_knowledge['pregnancy']:
            info = health_knowledge['pregnancy'][week_key]
            answer = f"🤰 **Pregnancy Week {week}:**\n\n" \
                    f"**Baby Development:** {info['baby_development']}\n\n" \
                    f"**Mother's Body:** {info['mother_changes']}\n\n" \
                    f"**Advice:** {info['advice']}"
            
            return {
                'answer': answer,
                'confidence': 0.95,
                'category': 'pregnancy'
            }
    
    # General pregnancy advice
    answer = "🤰 **Pregnancy Health Tips:**\n\n" \
            "• Take prenatal vitamins (especially folic acid)\n" \
            "• Eat a balanced diet rich in nutrients\n" \
            "• Stay hydrated (8-10 glasses of water)\n" \
            "• Exercise moderately (walking, prenatal yoga)\n" \
            "• Get adequate rest and sleep\n" \
            "• Attend all prenatal checkups\n" \
            "• Avoid alcohol, smoking, and raw foods\n\n" \
            "💡 Mention a specific week (e.g., 'week 20') for detailed information!"
    
    return {
        'answer': answer,
        'confidence': 0.85,
        'category': 'pregnancy'
    }


def handle_womens_health_query(message, user_profile):
    """Handle women's health queries"""
    if 'womens_health' not in health_knowledge:
        return None
    
    # Check for specific symptoms
    for symptom, info in health_knowledge['womens_health'].items():
        if symptom.replace('_', ' ') in message:
            answer = f"👩 **{symptom.replace('_', ' ').title()}:**\n\n" \
                    f"**Symptoms:** {info['symptoms']}\n\n" \
                    f"**Advice:** {info['advice']}"
            
            return {
                'answer': answer,
                'confidence': 0.9,
                'category': 'womens_health'
            }
    
    # General women's health advice
    answer = "👩 **Women's Health Tips:**\n\n" \
            "• Maintain regular menstrual cycle tracking\n" \
            "• Practice good hygiene\n" \
            "• Eat iron-rich foods (spinach, lentils, red meat)\n" \
            "• Exercise regularly\n" \
            "• Get annual checkups and screenings\n" \
            "• Manage stress through yoga or meditation\n" \
            "• Stay hydrated\n\n" \
            "💡 Ask about specific symptoms like cramps, PCOS, or fertility for detailed advice!"
    
    return {
        'answer': answer,
        'confidence': 0.8,
        'category': 'womens_health'
    }


def get_daily_water(weight_kg):
    """Calculate daily water intake"""
    if 'daily_water' not in health_knowledge:
        return 2.5
    
    water = weight_kg * 0.033
    water = max(health_knowledge['daily_water']['min'], 
                min(water, health_knowledge['daily_water']['max']))
    return round(water, 1)


def get_calorie_needs(age, gender, weight_kg, height_cm, activity_level):
    """Calculate daily calorie needs (Harris-Benedict Equation)"""
    # BMR calculation
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    
    # Activity multiplier
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    multiplier = activity_multipliers.get(activity_level.lower(), 1.55)
    tdee = bmr * multiplier
    
    return round(tdee)


def answer_question(question, user_profile=None):
    """Answer health questions using Q&A model with improved flexibility"""
    if qa_vectorizer is None or qa_database is None:
        return {
            'answer': "Sorry, the Q&A model is not available at the moment.",
            'confidence': 0.0,
            'category': 'error'
        }
    
    # Vectorize question
    question_vec = qa_vectorizer.transform([question])
    
    # Get all question vectors
    all_questions = qa_database['questions']
    all_question_vecs = qa_vectorizer.transform(all_questions)
    
    # Calculate similarities
    similarities = cosine_similarity(question_vec, all_question_vecs)[0]
    
    # Get best match
    best_match_idx = similarities.argmax()
    confidence = similarities[best_match_idx]
    
    # Lower threshold for more flexible matching
    if confidence > 0.15:  # Lowered from 0.1 for better matching
        answer = qa_database['answers'][best_match_idx]
        category = qa_database['categories'][best_match_idx]
        
        # Personalize answer if user profile provided
        if user_profile:
            answer = personalize_answer(answer, user_profile)
        
        return {
            'answer': answer,
            'confidence': float(confidence),
            'category': category
        }
    else:
        # Provide helpful fallback with examples
        return {
            'answer': "🏥 I'm here to help with health questions! I can assist with:\n\n" +
                     "• **Nutrition:** 'What foods are healthy?', 'How many calories do I need?'\n" +
                     "• **Fitness:** 'What exercises should I do?', 'How to lose weight?'\n" +
                     "• **Health Metrics:** 'What is a healthy BMI?', 'Normal blood pressure?'\n" +
                     "• **Pregnancy:** 'Pregnancy week 20 info', 'Prenatal care tips'\n" +
                     "• **Women's Health:** 'Period cramps relief', 'PCOS symptoms'\n\n" +
                     "💡 Try rephrasing your question or ask about a specific health topic!",
            'confidence': 0.0,
            'category': 'unknown'
        }


def personalize_answer(answer, profile):
    """Add personalized recommendations based on user profile"""
    personalized = answer
    
    # Add BMI-specific advice
    if 'weight' in profile and 'height' in profile:
        bmi = get_bmi(profile['weight'], profile['height'] / 100)
        bmi_info = get_bmi_category(bmi)
        if bmi_info:
            personalized += f"\n\n💡 Your BMI ({bmi:.1f}) is {bmi_info['category']}. {bmi_info['advice']}"
    
    # Add calorie advice
    if all(k in profile for k in ['age', 'gender', 'weight', 'height', 'activity']):
        calories = get_calorie_needs(
            profile['age'], 
            profile['gender'], 
            profile['weight'],
            profile['height'],
            profile['activity']
        )
        personalized += f"\n\n🔥 Your daily calorie needs: approximately {calories} kcal"
    
    return personalized


# API Routes

@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        'message': 'HealthNest AI Backend API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            '/chat': 'POST - Chat with health assistant',
            '/health-check': 'POST - Get personalized health analysis',
            '/predict-calories': 'POST - Predict food calories',
            '/recommend-exercise': 'POST - Get exercise recommendations',
            '/pregnancy-info': 'GET - Get pregnancy week info',
            '/health': 'GET - API health status'
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Check API health"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': {
            'qa_model': qa_vectorizer is not None,
            'calorie_predictor': calorie_predictor is not None,
            'exercise_recommender': exercise_recommender is not None,
            'knowledge_base': bool(health_knowledge)
        }
    })


@app.route('/chat', methods=['POST'])
def chat():
    """Main chatbot endpoint with improved understanding"""
    data = request.json
    
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    message = data['message'].strip()
    message_lower = message.lower()
    user_profile = data.get('profile', None)
    
    # Handle greetings and casual conversation
    greetings = ['hi', 'hello', 'hey', 'hola', 'namaste', 'assalamu alaikum', 
                 'good morning', 'good afternoon', 'good evening', 'salam', 'kon khabar']
    
    if any(greeting in message_lower for greeting in greetings) or len(message.split()) <= 2:
        return jsonify({
            'message': message,
            'response': "Hello! 👋 I'm HealthNest AI, your personal health assistant. I can help you with:\n\n" +
                       "🥗 Nutrition & diet advice\n" +
                       "💪 Fitness & exercise recommendations\n" +
                       "🤰 Pregnancy information\n" +
                       "👩 Women's health questions\n" +
                       "📊 BMI, blood pressure, and health metrics\n" +
                       "🏥 General health advice\n\n" +
                       "Just ask me anything about your health!",
            'confidence': 1.0,
            'category': 'greeting'
        })
    
    # Check for specific health domains with more keywords
    pregnancy_keywords = ['pregnancy', 'pregnant', 'week', 'trimester', 'baby', 'fetal', 'prenatal', 'gorbhoboti']
    womens_health_keywords = ['period', 'menstrual', 'cramp', 'pcos', 'ovulation', 'fertility', 
                               'menopause', 'endometriosis', 'masik', 'menses']
    nutrition_keywords = ['calorie', 'calories', 'food', 'nutrition', 'diet', 'eat', 'meal', 
                          'protein', 'carb', 'fat', 'vitamin', 'khabar', 'khaddo']
    exercise_keywords = ['exercise', 'workout', 'fitness', 'gym', 'running', 'weight loss', 
                         'cardio', 'strength', 'yoga', 'kashrot', 'byayam']
    
    # Pregnancy queries
    if any(word in message_lower for word in pregnancy_keywords):
        pregnancy_info = handle_pregnancy_query(message_lower, user_profile)
        if pregnancy_info:
            return jsonify({
                'message': message,
                'response': pregnancy_info['answer'],
                'confidence': pregnancy_info['confidence'],
                'category': 'pregnancy'
            })
    
    # Women's health queries
    if any(word in message_lower for word in womens_health_keywords):
        womens_info = handle_womens_health_query(message_lower, user_profile)
        if womens_info:
            return jsonify({
                'message': message,
                'response': womens_info['answer'],
                'confidence': womens_info['confidence'],
                'category': 'womens_health'
            })
    
    # Nutrition queries
    if any(word in message_lower for word in nutrition_keywords):
        if user_profile:
            age = user_profile.get('age', 25)
            gender = user_profile.get('gender', 'male')
            weight = user_profile.get('weight', 70)
            height = user_profile.get('height', 170)
            activity = user_profile.get('activity_level', 'moderate')
            
            calories = get_calorie_needs(age, gender, weight, height, activity)
            water = get_daily_water(weight)
            
            response_text = f"🥗 **Nutrition Advice:**\n\n" \
                          f"📊 Daily calorie needs: {calories} kcal\n" \
                          f"💧 Daily water intake: {water} liters\n\n" \
                          f"**Balanced Diet Tips:**\n" \
                          f"• Eat 5-6 small meals throughout the day\n" \
                          f"• Include lean proteins (chicken, fish, legumes)\n" \
                          f"• Choose complex carbs (brown rice, oats, quinoa)\n" \
                          f"• Add healthy fats (nuts, avocado, olive oil)\n" \
                          f"• Eat plenty of fruits & vegetables (5+ servings daily)\n" \
                          f"• Limit processed foods, sugar, and salt\n" \
                          f"• Stay hydrated throughout the day"
        else:
            response_text = "🥗 **General Nutrition Advice:**\n\n" \
                          "A healthy diet includes:\n" \
                          "• Proteins: Eggs, chicken, fish, legumes, dairy\n" \
                          "• Carbohydrates: Whole grains, fruits, vegetables\n" \
                          "• Fats: Nuts, seeds, olive oil, avocado\n" \
                          "• Hydration: 8-10 glasses of water daily\n\n" \
                          "💡 Update your profile for personalized recommendations!"
        
        return jsonify({
            'message': message,
            'response': response_text,
            'confidence': 0.85,
            'category': 'nutrition'
        })
    
    # Exercise queries
    if any(word in message_lower for word in exercise_keywords):
        if user_profile and user_profile.get('activity_level'):
            activity = user_profile.get('activity_level', 'moderate')
            response_text = f"💪 **Exercise Recommendations:**\n\n" \
                          f"Based on your {activity} activity level:\n\n" \
                          f"**Cardio (3-5 times/week):**\n" \
                          f"• Walking: 30-45 minutes\n" \
                          f"• Jogging/Running: 20-30 minutes\n" \
                          f"• Cycling: 30-45 minutes\n" \
                          f"• Swimming: 30 minutes\n\n" \
                          f"**Strength Training (2-3 times/week):**\n" \
                          f"• Bodyweight exercises (push-ups, squats)\n" \
                          f"• Weight lifting\n" \
                          f"• Resistance bands\n\n" \
                          f"**Flexibility (daily):**\n" \
                          f"• Yoga or stretching: 10-15 minutes\n\n" \
                          f"⚡ Start slowly and gradually increase intensity!"
        else:
            response_text = "💪 **Exercise Guidelines:**\n\n" \
                          "**Weekly Goals:**\n" \
                          "• 150 minutes moderate cardio OR 75 minutes vigorous cardio\n" \
                          "• Strength training 2-3 times per week\n" \
                          "• Flexibility exercises daily\n\n" \
                          "**Popular Exercises:**\n" \
                          "• Walking, jogging, cycling, swimming (cardio)\n" \
                          "• Push-ups, squats, lunges (strength)\n" \
                          "• Yoga, stretching (flexibility)\n\n" \
                          "💡 Update your profile for personalized plans!"
        
        return jsonify({
            'message': message,
            'response': response_text,
            'confidence': 0.85,
            'category': 'exercise'
        })
    
    # General health questions - use Q&A model
    result = answer_question(message, user_profile)
    
    # Add BMI info if profile available and relevant
    if user_profile and user_profile.get('weight') and user_profile.get('height'):
        if any(word in message_lower for word in ['bmi', 'weight', 'healthy', 'swasthyo']):
            bmi = get_bmi(user_profile['weight'], user_profile['height'] / 100)
            bmi_info = get_bmi_category(bmi)
            if bmi_info:
                result['answer'] += f"\n\n📊 Your BMI: {bmi:.1f} ({bmi_info['category']}) - {bmi_info['advice']}"
    
    return jsonify({
        'message': message,
        'response': result['answer'],
        'confidence': result['confidence'],
        'category': result['category']
    })


@app.route('/health-check', methods=['POST'])
def complete_health_check():
    """Complete health analysis"""
    data = request.json
    
    required_fields = ['age', 'gender', 'weight', 'height']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    age = data['age']
    gender = data['gender']
    weight = data['weight']  # kg
    height = data['height']  # cm
    activity = data.get('activity', 'moderate')
    
    # Calculate metrics
    bmi = get_bmi(weight, height / 100)
    bmi_info = get_bmi_category(bmi)
    water = get_daily_water(weight)
    calories = get_calorie_needs(age, gender, weight, height, activity)
    
    # Determine step goal
    step_goal = 10000 if activity in ['active', 'very_active'] else 7500
    
    # Generate recommendations
    recommendations = []
    
    if bmi_info:
        recommendations.append({
            'type': 'BMI',
            'message': f"Your BMI is {bmi:.1f} ({bmi_info['category']}). {bmi_info['advice']}"
        })
    
    recommendations.append({
        'type': 'Hydration',
        'message': f"Drink at least {water} liters of water daily."
    })
    
    recommendations.append({
        'type': 'Calories',
        'message': f"Your daily calorie target: {calories} kcal (based on {activity} activity level)."
    })
    
    recommendations.append({
        'type': 'Steps',
        'message': f"Aim for {step_goal} steps per day to stay healthy."
    })
    
    return jsonify({
        'metrics': {
            'bmi': round(bmi, 1),
            'bmi_category': bmi_info['category'] if bmi_info else 'unknown',
            'daily_water_liters': water,
            'daily_calories': calories,
            'step_goal': step_goal
        },
        'recommendations': recommendations
    })


@app.route('/predict-calories', methods=['POST'])
def predict_calories():
    """Predict calories from macros"""
    data = request.json
    
    if not data or not all(k in data for k in ['protein', 'carbs', 'fat']):
        return jsonify({'error': 'Missing protein, carbs, or fat values'}), 400
    
    if calorie_predictor is None:
        return jsonify({'error': 'Calorie predictor not available'}), 503
    
    protein = data['protein']
    carbs = data['carbs']
    fat = data['fat']
    
    # Predict
    X = np.array([[protein, carbs, fat]])
    predicted_calories = calorie_predictor.predict(X)[0]
    
    return jsonify({
        'protein_g': protein,
        'carbs_g': carbs,
        'fat_g': fat,
        'predicted_calories': round(predicted_calories)
    })


@app.route('/recommend-exercise', methods=['POST'])
def recommend_exercise():
    """Recommend exercises based on user data"""
    data = request.json
    
    if not data or 'weight' not in data:
        return jsonify({'error': 'Weight is required'}), 400
    
    weight = data['weight']
    goal = data.get('goal', 'general')  # weight_loss, muscle_gain, general
    
    # Basic exercise recommendations (rule-based)
    exercises = []
    
    if goal == 'weight_loss':
        exercises = [
            {'name': 'Running', 'duration': '30 min', 'calories': round(600 * (weight/70) * 0.5)},
            {'name': 'Cycling', 'duration': '45 min', 'calories': round(400 * (weight/70) * 0.75)},
            {'name': 'Swimming', 'duration': '30 min', 'calories': round(500 * (weight/70) * 0.5)}
        ]
    elif goal == 'muscle_gain':
        exercises = [
            {'name': 'Weight Lifting', 'duration': '45 min', 'calories': round(300 * (weight/70) * 0.75)},
            {'name': 'Push-ups', 'sets': '3x15', 'calories': 100},
            {'name': 'Squats', 'sets': '3x20', 'calories': 150}
        ]
    else:
        exercises = [
            {'name': 'Walking', 'duration': '30 min', 'calories': round(200 * (weight/70) * 0.5)},
            {'name': 'Yoga', 'duration': '30 min', 'calories': round(180 * (weight/70) * 0.5)},
            {'name': 'Dancing', 'duration': '30 min', 'calories': round(350 * (weight/70) * 0.5)}
        ]
    
    return jsonify({
        'goal': goal,
        'recommended_exercises': exercises,
        'total_calories': sum(ex.get('calories', 0) for ex in exercises)
    })


@app.route('/pregnancy-info', methods=['GET'])
def pregnancy_info():
    """Get pregnancy week information"""
    week = request.args.get('week', type=int)
    
    if not week or week < 1 or week > 42:
        return jsonify({'error': 'Invalid week number (1-42)'}), 400
    
    if 'pregnancy' not in health_knowledge:
        return jsonify({'error': 'Pregnancy data not available'}), 503
    
    week_str = str(week)
    if week_str in health_knowledge['pregnancy']:
        info = health_knowledge['pregnancy'][week_str]
        return jsonify({
            'week': week,
            'baby_development': info.get('baby_development', ''),
            'mother_changes': info.get('mother_changes', ''),
            'advice': info.get('advice', ''),
            'trimester': info.get('trimester', 1)
        })
    else:
        return jsonify({'error': 'Week data not found'}), 404


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 HealthNest AI Backend API Starting...")
    print("="*60)
    print("\n📡 Server: http://localhost:5000")
    print("📖 Docs: http://localhost:5000/\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
