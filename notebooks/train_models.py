"""
HealthNest AI - Model Training Script
Direct Python execution (no Jupyter needed)
"""

import pandas as pd
import numpy as np
import json
import joblib
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from sklearn.preprocessing import LabelEncoder
import os

print("=" * 60)
print("🧠 HealthNest AI - Model Training")
print("=" * 60)
print()

# Create models directory
os.makedirs('../models', exist_ok=True)

# Download NLTK data
try:
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    print("✓ NLTK data downloaded")
except:
    print("⚠ NLTK download skipped")

# Load datasets
print("\n📂 Loading datasets...")

df_nutrition = pd.read_csv('../datasets/processed/nutrition_processed.csv')
df_exercise = pd.read_csv('../datasets/processed/exercise_processed.csv')
df_qa = pd.read_csv('../datasets/processed/medical_qa_processed.csv')
df_pregnancy = pd.read_csv('../datasets/processed/pregnancy_processed.csv')
df_womens = pd.read_csv('../datasets/processed/womens_health_processed.csv')
knowledge_base = pd.read_csv('../datasets/processed/knowledge_base.csv')

print(f"✓ Nutrition: {len(df_nutrition)} records")
print(f"✓ Exercise: {len(df_exercise)} records")
print(f"✓ Medical Q&A: {len(df_qa)} records")
print(f"✓ Pregnancy: {len(df_pregnancy)} records")
print(f"✓ Women's Health: {len(df_womens)} records")
print(f"✓ Knowledge Base: {len(knowledge_base)} entries")

# 1. Train Q&A Model
print("\n🤖 Training Q&A Model...")

questions = knowledge_base['question'].fillna('').tolist()
answers = knowledge_base['answer'].fillna('').tolist()
categories = knowledge_base['category'].fillna('general').tolist()

vectorizer = TfidfVectorizer(
    max_features=500,
    stop_words='english',
    ngram_range=(1, 2),
    min_df=1
)

question_vectors = vectorizer.fit_transform(questions)

print(f"✓ Vectorizer trained on {len(questions)} questions")
print(f"✓ Vocabulary size: {len(vectorizer.vocabulary_)}")

# Save Q&A model
joblib.dump(vectorizer, '../models/qa_vectorizer.pkl')
qa_db = {
    'questions': questions,
    'answers': answers,
    'categories': categories
}
joblib.dump(qa_db, '../models/qa_database.pkl')
print("✓ Q&A Model saved!")

# 2. Train Calorie Predictor
print("\n🍽 Training Calorie Prediction Model...")

X = df_nutrition[['protein', 'carbs', 'fat']]
y = df_nutrition['calories']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

calorie_model = RandomForestRegressor(n_estimators=100, random_state=42)
calorie_model.fit(X_train, y_train)

y_pred = calorie_model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"✓ Model trained on {len(X_train)} samples")
print(f"✓ R² Score: {r2:.4f}")
print(f"✓ RMSE: {rmse:.2f} calories")

joblib.dump(calorie_model, '../models/calorie_predictor.pkl')
print("✓ Calorie Predictor saved!")

# 3. Train Exercise Recommender
print("\n🏃 Training Exercise Recommendation Model...")

X_ex = df_exercise[['body_weight', 'calories_per_hour']]
le_exercise = LabelEncoder()
y_ex = le_exercise.fit_transform(df_exercise['exercise_name'])

X_train_ex, X_test_ex, y_train_ex, y_test_ex = train_test_split(X_ex, y_ex, test_size=0.2, random_state=42)

exercise_model = RandomForestClassifier(n_estimators=100, random_state=42)
exercise_model.fit(X_train_ex, y_train_ex)

y_pred_ex = exercise_model.predict(X_test_ex)
accuracy = accuracy_score(y_test_ex, y_pred_ex)

print(f"✓ Model trained on {len(X_train_ex)} samples")
print(f"✓ Accuracy: {accuracy:.4f}")

joblib.dump(exercise_model, '../models/exercise_recommender.pkl')
joblib.dump(le_exercise, '../models/exercise_encoder.pkl')
print("✓ Exercise Recommender saved!")

# 4. Create Health Knowledge Base
print("\n🏥 Creating Health Advisor Knowledge Base...")

health_knowledge = {
    'bmi_ranges': {
        'underweight': {'range': [0, 18.5], 'advice': 'Increase calorie intake with nutritious foods. Consult a nutritionist.'},
        'normal': {'range': [18.5, 24.9], 'advice': 'Maintain current healthy lifestyle and balanced diet.'},
        'overweight': {'range': [25, 29.9], 'advice': 'Reduce calorie intake, increase physical activity. Consider portion control.'},
        'obese': {'range': [30, 100], 'advice': 'Consult healthcare provider. Focus on gradual weight loss through diet and exercise.'}
    },
    'blood_pressure': {
        'normal': {'range': {'systolic': [90, 120], 'diastolic': [60, 80]}, 'advice': 'Maintain healthy lifestyle'},
        'elevated': {'range': {'systolic': [120, 129], 'diastolic': [60, 80]}, 'advice': 'Reduce salt, exercise regularly'},
        'high': {'range': {'systolic': [130, 200], 'diastolic': [80, 120]}, 'advice': 'Consult doctor, medication may be needed'}
    },
    'blood_glucose': {
        'normal': {'range': [70, 100], 'advice': 'Maintain balanced diet and regular exercise'},
        'prediabetes': {'range': [100, 125], 'advice': 'Reduce sugar intake, increase physical activity, monitor regularly'},
        'diabetes': {'range': [126, 500], 'advice': 'Consult doctor immediately, medication and diet control essential'}
    },
    'daily_water': {
        'formula': 'body_weight_kg * 0.033',
        'min': 2.0,
        'max': 4.0
    },
    'daily_steps': {
        'sedentary': 5000,
        'moderate': 7500,
        'active': 10000,
        'very_active': 12500
    },
    'sleep_hours': {
        'adult': [7, 9],
        'teenager': [8, 10],
        'child': [9, 12]
    }
}

# Add pregnancy knowledge
pregnancy_dict = {}
for _, row in df_pregnancy.iterrows():
    pregnancy_dict[str(row['week'])] = {
        'baby_development': row['baby_development'],
        'mother_changes': row['mother_changes'],
        'advice': row['advice'],
        'trimester': int(row['trimester'])
    }
health_knowledge['pregnancy'] = pregnancy_dict

# Add women's health knowledge
womens_dict = {}
for _, row in df_womens.iterrows():
    womens_dict[row['symptom']] = {
        'phase': row['phase'],
        'advice': row['advice'],
        'severity': row['severity']
    }
health_knowledge['womens_health'] = womens_dict

with open('../models/health_knowledge.json', 'w') as f:
    json.dump(health_knowledge, f, indent=2)

print("✓ Health Knowledge Base created!")

# Save metadata
metadata = {
    'project': 'HealthNest AI Health Assistant',
    'version': '1.0.0',
    'date_trained': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
    'models': {
        'qa_model': {
            'type': 'TF-IDF + Cosine Similarity',
            'knowledge_base_size': len(knowledge_base),
            'vocabulary_size': len(vectorizer.vocabulary_)
        },
        'calorie_predictor': {
            'type': 'Random Forest Regressor',
            'training_samples': len(X_train),
            'r2_score': float(r2)
        },
        'exercise_recommender': {
            'type': 'Random Forest Classifier',
            'accuracy': float(accuracy)
        }
    },
    'datasets': {
        'nutrition': len(df_nutrition),
        'exercise': len(df_exercise),
        'medical_qa': len(df_qa),
        'pregnancy': len(df_pregnancy),
        'womens_health': len(df_womens)
    }
}

with open('../models/model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("\n" + "=" * 60)
print("✅ HealthNest AI Model Training Complete!")
print("=" * 60)

print("\n📦 Trained Models:")
print("  1. Q&A Model (TF-IDF + Cosine Similarity)")
print("  2. Calorie Prediction Model (Random Forest Regressor)")
print("  3. Exercise Recommendation Model (Random Forest Classifier)")
print("  4. Health Knowledge Base (Rule-based System)")

print("\n💾 Saved Files:")
print("  - ../models/qa_vectorizer.pkl")
print("  - ../models/qa_database.pkl")
print("  - ../models/calorie_predictor.pkl")
print("  - ../models/exercise_recommender.pkl")
print("  - ../models/exercise_encoder.pkl")
print("  - ../models/health_knowledge.json")
print("  - ../models/model_metadata.json")

print("\n📝 Next Step:")
print("  Run backend: cd ../backend && python app.py")
