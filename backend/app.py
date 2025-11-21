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
    """Answer health questions using Q&A model"""
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
    
    if confidence > 0.1:  # Threshold
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
        return {
            'answer': "I'm not sure about that. Could you rephrase your question or ask about nutrition, fitness, BMI, blood pressure, pregnancy, or women's health?",
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
    """Main chatbot endpoint"""
    data = request.json
    
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    message = data['message']
    user_profile = data.get('profile', None)
    
    # Get answer
    result = answer_question(message, user_profile)
    
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
