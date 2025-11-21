"""
HealthNest AI - Dataset Downloader
Downloads and organizes all required health datasets
"""

import os
import pandas as pd
from pathlib import Path

# Create directories
os.makedirs("raw", exist_ok=True)
os.makedirs("processed", exist_ok=True)

print("=" * 60)
print("HealthNest AI Dataset Downloader")
print("=" * 60)

# Note: Users need to manually download from Kaggle (requires API key)
# This script provides instructions and basic setup

DATASETS = {
    "nutrition": {
        "name": "Food Nutrition Dataset",
        "url": "https://www.kaggle.com/datasets/trolukovich/nutritional-values-for-common-foods-and-products",
        "file": "nutrition.csv"
    },
    "exercise": {
        "name": "Exercise Calories Dataset",
        "url": "https://www.kaggle.com/datasets/aadhavvignesh/calories-burned-during-exercise-and-activities",
        "file": "exercise.csv"
    },
    "health_metrics": {
        "name": "Health Metrics Dataset",
        "url": "https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database",
        "file": "diabetes.csv"
    },
    "medical_qa": {
        "name": "Medical Q&A Dataset",
        "url": "https://www.kaggle.com/datasets/pradeeppandey2000/medical-question-answer-datasets",
        "file": "medical_qa.csv"
    }
}

print("\n📥 Dataset Download Instructions:")
print("-" * 60)

for key, dataset in DATASETS.items():
    print(f"\n{dataset['name']}:")
    print(f"  URL: {dataset['url']}")
    print(f"  Save as: raw/{dataset['file']}")

print("\n" + "=" * 60)
print("💡 Alternative: Use Kaggle API")
print("=" * 60)
print("""
1. Install kaggle: pip install kaggle
2. Setup API key: https://www.kaggle.com/docs/api
3. Run commands:

kaggle datasets download -d trolukovich/nutritional-values-for-common-foods-and-products -p raw/
kaggle datasets download -d aadhavvignesh/calories-burned-during-exercise-and-activities -p raw/
kaggle datasets download -d uciml/pima-indians-diabetes-database -p raw/
kaggle datasets download -d pradeeppandey2000/medical-question-answer-datasets -p raw/

4. Unzip all files in raw/ folder
""")

# Create sample datasets for testing (small versions)
print("\n✅ Creating sample datasets for testing...")

# Sample Nutrition Data
nutrition_data = {
    'food_name': ['Rice', 'Chicken Breast', 'Apple', 'Egg', 'Banana', 'Milk', 'Bread', 'Fish'],
    'calories': [130, 165, 52, 68, 89, 42, 79, 206],
    'protein': [2.7, 31, 0.3, 6, 1.1, 3.4, 2.7, 22],
    'carbs': [28, 0, 14, 0.6, 23, 5, 15, 0],
    'fat': [0.3, 3.6, 0.2, 4.8, 0.3, 1, 1, 12],
    'category': ['grain', 'protein', 'fruit', 'protein', 'fruit', 'dairy', 'grain', 'protein']
}
df_nutrition = pd.DataFrame(nutrition_data)
df_nutrition.to_csv('raw/sample_nutrition.csv', index=False)
print("✓ Sample nutrition data created")

# Sample Exercise Data
exercise_data = {
    'exercise_name': ['Walking', 'Running', 'Cycling', 'Swimming', 'Yoga', 'Weight Lifting', 'Dancing'],
    'calories_per_hour': [200, 600, 400, 500, 180, 300, 350],
    'intensity': ['low', 'high', 'medium', 'high', 'low', 'medium', 'medium'],
    'type': ['cardio', 'cardio', 'cardio', 'cardio', 'flexibility', 'strength', 'cardio']
}
df_exercise = pd.DataFrame(exercise_data)
df_exercise.to_csv('raw/sample_exercise.csv', index=False)
print("✓ Sample exercise data created")

# Sample Medical Q&A
qa_data = {
    'question': [
        'How to improve health?',
        'What foods are good for heart?',
        'How much water should I drink daily?',
        'What is a healthy BMI range?',
        'How to reduce blood pressure?',
        'Best exercises for weight loss?',
        'How to improve sleep quality?',
        'What is healthy blood sugar level?'
    ],
    'answer': [
        'To improve health: eat balanced diet, exercise regularly, get 7-8 hours sleep, stay hydrated, manage stress, and have regular checkups.',
        'Heart-healthy foods include: salmon, walnuts, berries, oats, dark chocolate, leafy greens, avocado, and olive oil.',
        'Adults should drink 2-3 liters (8-10 glasses) of water daily. More if exercising or in hot weather.',
        'Healthy BMI range is 18.5-24.9. Below 18.5 is underweight, 25-29.9 is overweight, 30+ is obese.',
        'Reduce BP by: limiting salt, exercising regularly, maintaining healthy weight, limiting alcohol, managing stress, eating potassium-rich foods.',
        'Best exercises for weight loss: running, cycling, swimming, HIIT workouts, strength training, and walking 10,000+ steps daily.',
        'Improve sleep: maintain consistent schedule, avoid screens before bed, keep room dark and cool, avoid caffeine late, exercise regularly.',
        'Normal fasting blood sugar: 70-100 mg/dL. Prediabetes: 100-125. Diabetes: 126+. After meals: below 140 mg/dL is normal.'
    ],
    'category': ['general', 'nutrition', 'hydration', 'bmi', 'blood_pressure', 'fitness', 'sleep', 'diabetes']
}
df_qa = pd.DataFrame(qa_data)
df_qa.to_csv('raw/sample_medical_qa.csv', index=False)
print("✓ Sample medical Q&A data created")

# Pregnancy Data
pregnancy_data = []
weeks_data = {
    1: {"baby": "Conception occurs", "mother": "Preparing for pregnancy", "advice": "Start taking folic acid"},
    8: {"baby": "Size of a raspberry", "mother": "Morning sickness may begin", "advice": "Eat small frequent meals"},
    12: {"baby": "Size of a plum", "mother": "First trimester ending", "advice": "First ultrasound scan"},
    20: {"baby": "Size of a banana", "mother": "May feel baby movements", "advice": "Midpoint scan, eat iron-rich foods"},
    28: {"baby": "Size of an eggplant", "mother": "Third trimester begins", "advice": "Monitor baby kicks, prepare nursery"},
    40: {"baby": "Full term baby", "mother": "Ready for delivery", "advice": "Watch for labor signs, hospital bag ready"}
}

for week, data in weeks_data.items():
    pregnancy_data.append({
        'week': week,
        'baby_development': data['baby'],
        'mother_changes': data['mother'],
        'advice': data['advice'],
        'trimester': 1 if week <= 13 else (2 if week <= 27 else 3)
    })

df_pregnancy = pd.DataFrame(pregnancy_data)
df_pregnancy.to_csv('raw/sample_pregnancy.csv', index=False)
print("✓ Sample pregnancy data created")

# Women's Health Data
womens_health_data = {
    'symptom': ['Cramps', 'Bloating', 'Mood swings', 'Fatigue', 'Headache', 'Breast tenderness'],
    'phase': ['Menstrual', 'Luteal', 'Luteal', 'Menstrual', 'Menstrual', 'Luteal'],
    'advice': [
        'Use heating pad, take pain relief, rest',
        'Reduce salt intake, stay hydrated, gentle exercise',
        'Practice relaxation techniques, get adequate sleep',
        'Rest well, eat iron-rich foods, stay hydrated',
        'Stay hydrated, reduce stress, get enough sleep',
        'Wear comfortable bra, reduce caffeine'
    ],
    'severity': ['moderate', 'mild', 'moderate', 'moderate', 'mild', 'mild']
}
df_womens = pd.DataFrame(womens_health_data)
df_womens.to_csv('raw/sample_womens_health.csv', index=False)
print("✓ Sample women's health data created")

print("\n" + "=" * 60)
print("✅ Sample datasets created successfully!")
print("=" * 60)
print("\n📝 Next Steps:")
print("1. Download full datasets from Kaggle (optional)")
print("2. Run: python preprocess_datasets.py")
print("3. Train model: jupyter notebook ../notebooks/train_model.ipynb")
