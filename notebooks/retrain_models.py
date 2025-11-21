"""
Retrain models with expanded dataset
"""

import pandas as pd
import numpy as np
import pickle
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("🤖 HealthNest AI - Model Retraining with Expanded Data")
print("=" * 60)

# Load expanded Q&A data
print("\n📚 Loading expanded Q&A dataset...")
qa_df = pd.read_csv('../datasets/raw/expanded_medical_qa.csv')
print(f"✅ Loaded {len(qa_df)} Q&A pairs")

# Train Q&A Model with better parameters
print("\n🔄 Training Q&A Model...")
vectorizer = TfidfVectorizer(
    max_features=1000,  # Increased from 500
    ngram_range=(1, 3),  # Increased to trigrams
    min_df=1,  # Include all words
    max_df=0.9
)

questions = qa_df['question'].values
question_vectors = vectorizer.fit_transform(questions)

qa_database = {
    'questions': questions.tolist(),
    'answers': qa_df['answer'].values.tolist(),
    'categories': qa_df['category'].values.tolist()
}

print(f"✅ Q&A Model trained with {len(vectorizer.vocabulary_)} vocabulary terms")

# Save Q&A model
with open('../models/qa_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

with open('../models/qa_database.pkl', 'wb') as f:
    pickle.dump(qa_database, f)

print("✅ Q&A model saved!")

# Load and train calorie predictor
print("\n🍎 Training Calorie Predictor...")
nutrition_df = pd.read_csv('../datasets/processed/nutrition_processed.csv')

X_cal = nutrition_df[['protein', 'fat', 'carbs']].values
y_cal = nutrition_df['calories'].values

if len(X_cal) > 2:
    X_train, X_test, y_train, y_test = train_test_split(X_cal, y_cal, test_size=0.2, random_state=42)
    
    calorie_model = RandomForestRegressor(n_estimators=100, random_state=42)
    calorie_model.fit(X_train, y_train)
    
    score = r2_score(y_test, calorie_model.predict(X_test))
    print(f"✅ Calorie Predictor trained (R² = {score:.3f})")
    
    with open('../models/calorie_predictor.pkl', 'wb') as f:
        pickle.dump(calorie_model, f)

# Load and train exercise recommender
print("\n💪 Training Exercise Recommender...")
exercise_df = pd.read_csv('../datasets/processed/exercise_processed.csv')

# Use available columns - encode intensity
intensity_map = {'low': 1, 'moderate': 2, 'high': 3}
exercise_df['intensity_encoded'] = exercise_df['intensity'].map(intensity_map)

X_ex = exercise_df[['body_weight', 'calories_per_hour', 'intensity_encoded']].values
y_ex = exercise_df['exercise_name'].values

encoder = LabelEncoder()
y_ex_encoded = encoder.fit_transform(y_ex)

exercise_model = RandomForestClassifier(n_estimators=100, random_state=42)
exercise_model.fit(X_ex, y_ex_encoded)

print(f"✅ Exercise Recommender trained with {len(encoder.classes_)} exercises")

with open('../models/exercise_recommender.pkl', 'wb') as f:
    pickle.dump(exercise_model, f)

with open('../models/exercise_encoder.pkl', 'wb') as f:
    pickle.dump(encoder, f)

# Update metadata
print("\n💾 Updating model metadata...")
metadata = {
    'trained_at': pd.Timestamp.now().isoformat(),
    'qa_model': {
        'vocabulary_size': len(vectorizer.vocabulary_),
        'num_questions': len(questions),
        'categories': list(qa_df['category'].unique())
    },
    'calorie_predictor': {
        'num_samples': len(X_cal),
        'r2_score': float(score) if len(X_cal) > 2 else 0
    },
    'exercise_recommender': {
        'num_exercises': len(encoder.classes_),
        'num_samples': len(X_ex)
    }
}

with open('../models/model_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)

print("\n" + "=" * 60)
print("✅ ALL MODELS RETRAINED SUCCESSFULLY!")
print("=" * 60)
print("\n📊 Model Statistics:")
print(f"  Q&A Vocabulary: {len(vectorizer.vocabulary_)} terms")
print(f"  Q&A Questions: {len(questions)}")
print(f"  Exercise Types: {len(encoder.classes_)}")
print(f"  Categories: {', '.join(metadata['qa_model']['categories'])}")
print("\n🚀 Ready to use improved models!")
