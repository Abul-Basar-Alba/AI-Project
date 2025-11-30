"""
HealthNest AI Backend - Improved Version
Personalized health assistant with better Q&A
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

print("🔄 Loading HealthNest AI...")

# Comprehensive Health Knowledge Base
HEALTH_KB = {
    # BMI Information
    "bmi": {
        "what_is": "BMI (Body Mass Index) is a measure of body fat based on height and weight. Formula: weight(kg) / height(m)²",
        "ranges": {
            "underweight": {"range": [0, 18.5], "advice": "You may need to gain weight. Eat nutrient-rich foods, increase meal frequency, add healthy fats and proteins."},
            "normal": {"range": [18.5, 24.9], "advice": "Great! Maintain your healthy weight through balanced diet and regular exercise."},
            "overweight": {"range": [25, 29.9], "advice": "Focus on portion control, increase physical activity, and choose whole foods over processed ones."},
            "obese": {"range": [30, 50], "advice": "Consult a healthcare provider. Start with small dietary changes, aim for 150 min/week exercise, track your progress."}
        },
        "tips": [
            "BMI doesn't account for muscle mass - athletes may have high BMI but low body fat",
            "Track BMI monthly, not daily",
            "Combine BMI with waist measurement for better health assessment"
        ]
    },
    
    # Weight Loss
    "weight_loss": {
        "general": "Healthy weight loss is 0.5-1 kg per week. Create a calorie deficit through diet and exercise.",
        "tips": [
            "Drink 8-10 glasses of water daily",
            "Eat protein at every meal (eggs, chicken, fish, legumes)",
            "Fill half your plate with vegetables",
            "Avoid sugary drinks and processed foods",
            "Get 7-8 hours of sleep",
            "Do 30 minutes of cardio 5 days/week",
            "Strength train 2-3 times per week",
            "Track your food intake",
            "Meal prep on weekends",
            "Don't skip breakfast"
        ],
        "diet": "Focus on: Lean proteins, whole grains, fruits, vegetables, healthy fats. Avoid: Fried foods, sweets, soda, white bread/rice.",
        "exercise": "Combine cardio (walking, running, cycling) with strength training for best results."
    },
    
    # Nutrition
    "nutrition": {
        "balanced_diet": "Include all food groups: proteins, carbs, fats, vitamins, minerals",
        "macros": {
            "protein": "0.8-1g per kg body weight. Sources: chicken, fish, eggs, dal, paneer, tofu",
            "carbs": "45-65% of daily calories. Choose: brown rice, oats, quinoa, sweet potato",
            "fats": "20-35% of daily calories. Choose: nuts, seeds, avocado, olive oil, fish oil"
        },
        "meal_timing": [
            "Breakfast within 1 hour of waking",
            "Lunch 12-2pm",
            "Healthy snack 3-4pm",
            "Dinner before 8pm",
            "No eating 2 hours before sleep"
        ],
        "hydration": "Drink water = (Body weight in kg × 30-40) ml per day"
    },
    
    # Exercise & Fitness
    "fitness": {
        "types": {
            "cardio": "Running, cycling, swimming, brisk walking - Burns calories, improves heart health",
            "strength": "Weight lifting, resistance bands, bodyweight - Builds muscle, boosts metabolism",
            "flexibility": "Yoga, stretching - Prevents injury, improves mobility",
            "hiit": "High-intensity intervals - Maximum calorie burn in short time"
        },
        "beginner_plan": [
            "Week 1-2: 20 min walking daily",
            "Week 3-4: 30 min brisk walking + 10 min bodyweight exercises",
            "Week 5-6: Add light jogging intervals",
            "Week 7-8: 40 min cardio + 20 min strength training"
        ],
        "tips": [
            "Warm up 5-10 minutes before exercise",
            "Cool down and stretch after workout",
            "Rest days are important for recovery",
            "Stay consistent - exercise same time daily",
            "Track your progress weekly"
        ]
    },
    
    # Pregnancy
    "pregnancy": {
        "general": "Pregnancy lasts 40 weeks (9 months). Divided into 3 trimesters.",
        "nutrition": "Eat 300-500 extra calories daily. Take prenatal vitamins. Avoid alcohol, raw fish, unpasteurized dairy.",
        "exercise": "30 min moderate exercise daily. Try: walking, swimming, prenatal yoga. Avoid: contact sports, hot yoga.",
        "symptoms": {
            "trimester1": "Nausea, fatigue, breast tenderness, frequent urination",
            "trimester2": "Energy returns, baby movements, back pain, skin changes",
            "trimester3": "Weight gain, heartburn, shortness of breath, frequent bathroom trips"
        },
        "tips": [
            "Take folic acid 400mcg daily",
            "Stay hydrated - drink 10-12 glasses water",
            "Eat small frequent meals",
            "Get 8-9 hours sleep",
            "Avoid heavy lifting",
            "Attend all prenatal checkups",
            "Join prenatal classes"
        ]
    },
    
    # Women's Health
    "womens_health": {
        "period": {
            "normal": "Cycle: 21-35 days, Period: 3-7 days, Flow: 30-80ml total",
            "pain_relief": "Heat pad, gentle exercise, ibuprofen, ginger tea, proper rest",
            "diet": "Iron-rich foods (spinach, red meat, legumes), avoid caffeine and salt"
        },
        "pcos": "PCOS causes irregular periods, weight gain, acne. Manage with: low-carb diet, regular exercise, stress management.",
        "menopause": "Usually 45-55 years. Symptoms: hot flashes, mood changes, sleep issues. Treatment: healthy diet, exercise, hormone therapy if needed."
    },
    
    # General Health
    "health_tips": [
        "Sleep 7-8 hours daily",
        "Drink water first thing in morning",
        "Eat breakfast within 1 hour of waking",
        "Take 10,000 steps daily",
        "Limit screen time before bed",
        "Practice stress management (meditation, yoga)",
        "Get annual health checkups",
        "Maintain good posture",
        "Wash hands frequently",
        "Spend 15 min in sunlight daily for Vitamin D"
    ]
}


def calculate_bmr(age, gender, weight, height):
    """Calculate Basal Metabolic Rate"""
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return round(bmr)


def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure"""
    multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    multiplier = multipliers.get(activity_level, 1.55)
    return round(bmr * multiplier)


def get_personalized_response(message, profile):
    """Generate personalized response based on user profile"""
    message_lower = message.lower()
    
    # Extract user profile data
    age = profile.get('age', 25) if profile else 25
    gender = profile.get('gender', 'male') if profile else 'male'
    weight = profile.get('weight', 70) if profile else 70
    height = profile.get('height', 170) if profile else 170
    activity = profile.get('activity', 'moderate') if profile else 'moderate'
    
    # Calculate metrics
    bmi = round(weight / ((height/100) ** 2), 1)
    bmr = calculate_bmr(age, gender, weight, height)
    tdee = calculate_tdee(bmr, activity)
    water = round(weight * 0.033, 1)
    
    # Determine BMI category
    bmi_category = "normal"
    bmi_advice = ""
    for category, data in HEALTH_KB["bmi"]["ranges"].items():
        if data["range"][0] <= bmi < data["range"][1]:
            bmi_category = category
            bmi_advice = data["advice"]
            break
    
    response = {
        "metrics": {
            "bmi": bmi,
            "bmi_category": bmi_category,
            "bmr": bmr,
            "tdee": tdee,
            "water_liters": water
        },
        "advice": []
    }
    
    # BMI Questions
    if any(word in message_lower for word in ['bmi', 'body mass', 'index']):
        response["answer"] = f"📊 **Your BMI Analysis:**\n\n" \
                           f"Your BMI: **{bmi}** ({bmi_category.title()})\n\n" \
                           f"**What this means:**\n{bmi_advice}\n\n" \
                           f"**General BMI Info:**\n{HEALTH_KB['bmi']['what_is']}\n\n" \
                           f"**Healthy Range:** 18.5-24.9"
        return response
    
    # Weight Loss
    if any(word in message_lower for word in ['weight loss', 'lose weight', '減weight', 'diet plan']):
        deficit = 500 if bmi > 25 else 300
        target_calories = tdee - deficit
        
        tips_text = "\n".join([f"• {tip}" for tip in HEALTH_KB['weight_loss']['tips'][:8]])
        
        response["answer"] = f"🎯 **Personalized Weight Loss Plan:**\n\n" \
                           f"Current Weight: {weight}kg\n" \
                           f"BMI: {bmi} ({bmi_category})\n" \
                           f"Daily Calories: {tdee} kcal\n" \
                           f"**Target for weight loss:** {target_calories} kcal/day\n\n" \
                           f"**Action Plan:**\n{tips_text}\n\n" \
                           f"**Diet Focus:**\n{HEALTH_KB['weight_loss']['diet']}\n\n" \
                           f"**Exercise:**\n{HEALTH_KB['weight_loss']['exercise']}"
        return response
    
    # Nutrition Advice
    if any(word in message_lower for word in ['nutrition', 'diet', 'food', 'eat', 'meal', 'calories', 'calorie']):
        protein_need = round(weight * 0.8)
        
        response["answer"] = f"🥗 **Your Nutrition Plan:**\n\n" \
                           f"**Daily Needs:**\n" \
                           f"• Calories: {tdee} kcal\n" \
                           f"• Protein: {protein_need}g\n" \
                           f"• Water: {water}L\n\n" \
                           f"**Macros:**\n" \
                           f"• Protein: {HEALTH_KB['nutrition']['macros']['protein']}\n" \
                           f"• Carbs: {HEALTH_KB['nutrition']['macros']['carbs']}\n" \
                           f"• Fats: {HEALTH_KB['nutrition']['macros']['fats']}\n\n" \
                           f"**Meal Timing:**\n" + "\n".join([f"• {t}" for t in HEALTH_KB['nutrition']['meal_timing']])
        return response
    
    # Exercise & Fitness
    if any(word in message_lower for word in ['exercise', 'workout', 'fitness', 'gym', 'training']):
        response["answer"] = f"💪 **Your Fitness Plan:**\n\n" \
                           f"**Exercise Types:**\n" \
                           f"• Cardio: {HEALTH_KB['fitness']['types']['cardio']}\n" \
                           f"• Strength: {HEALTH_KB['fitness']['types']['strength']}\n" \
                           f"• Flexibility: {HEALTH_KB['fitness']['types']['flexibility']}\n\n" \
                           f"**Beginner Plan:**\n" + "\n".join([f"• {p}" for p in HEALTH_KB['fitness']['beginner_plan']]) + "\n\n" \
                           f"**Tips:**\n" + "\n".join([f"• {t}" for t in HEALTH_KB['fitness']['tips']])
        return response
    
    # Pregnancy
    if any(word in message_lower for word in ['pregnancy', 'pregnant', 'baby', 'trimester', 'prenatal']):
        response["answer"] = f"🤰 **Pregnancy Information:**\n\n" \
                           f"**Overview:**\n{HEALTH_KB['pregnancy']['general']}\n\n" \
                           f"**Nutrition:**\n{HEALTH_KB['pregnancy']['nutrition']}\n\n" \
                           f"**Exercise:**\n{HEALTH_KB['pregnancy']['exercise']}\n\n" \
                           f"**Important Tips:**\n" + "\n".join([f"• {t}" for t in HEALTH_KB['pregnancy']['tips'][:6]])
        return response
    
    # Women's Health
    if any(word in message_lower for word in ['period', 'menstrual', 'cramps', 'pcos', 'menopause']):
        response["answer"] = f"👩 **Women's Health:**\n\n" \
                           f"**Menstrual Cycle:**\n{HEALTH_KB['womens_health']['period']['normal']}\n\n" \
                           f"**Pain Relief:**\n{HEALTH_KB['womens_health']['period']['pain_relief']}\n\n" \
                           f"**Diet During Period:**\n{HEALTH_KB['womens_health']['period']['diet']}"
        return response
    
    # General Health Tips
    if any(word in message_lower for word in ['health tips', 'healthy', 'wellness', 'tips']):
        tips_text = "\n".join([f"• {tip}" for tip in HEALTH_KB['health_tips'][:10]])
        response["answer"] = f"💡 **Health Tips for You:**\n\n" \
                           f"**Your Stats:**\n" \
                           f"• BMI: {bmi} ({bmi_category})\n" \
                           f"• Daily Calories: {tdee} kcal\n" \
                           f"• Water Intake: {water}L\n\n" \
                           f"**Top 10 Health Tips:**\n{tips_text}"
        return response
    
    # Default response with user info
    response["answer"] = f"👋 Hello! I'm HealthNest AI, your personal health assistant.\n\n" \
                       f"**Your Profile:**\n" \
                       f"• Age: {age} years\n" \
                       f"• BMI: {bmi} ({bmi_category})\n" \
                       f"• Daily Calorie Needs: {tdee} kcal\n" \
                       f"• Recommended Water: {water}L\n\n" \
                       f"I can help you with:\n" \
                       f"🥗 Nutrition & diet advice\n" \
                       f"💪 Fitness & exercise recommendations\n" \
                       f"📊 BMI, calorie calculations\n" \
                       f"🤰 Pregnancy information\n" \
                       f"👩 Women's health questions\n" \
                       f"🏥 General health tips\n\n" \
                       f"Just ask me anything!"
    
    return response


@app.route('/')
def home():
    return jsonify({
        'message': 'HealthNest AI Backend API',
        'version': '2.0.0',
        'status': 'running',
        'features': ['BMI Calculator', 'Calorie Calculator', 'Personalized Health Tips', 'Q&A System']
    })


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': True
    })


@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint with personalized responses"""
    try:
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        message = data['message'].strip()
        profile = data.get('profile', None)
        
        # Get personalized response
        result = get_personalized_response(message, profile)
        
        return jsonify({
            'message': message,
            'response': result.get('answer', 'I can help with health questions!'),
            'metrics': result.get('metrics', {}),
            'category': 'health_advice',
            'confidence': 0.95
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Error processing request'
        }), 500


if __name__ == '__main__':
    print("✅ HealthNest AI Backend Ready!")
    print("📡 Server: http://0.0.0.0:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
