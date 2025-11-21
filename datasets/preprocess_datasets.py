"""
HealthNest AI - Data Preprocessing Pipeline
Cleans and combines all health datasets for model training
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import json

print("=" * 60)
print("HealthNest AI - Data Preprocessing")
print("=" * 60)

# Create processed directory
os.makedirs("processed", exist_ok=True)

# Load all datasets
print("\n📂 Loading datasets...")

try:
    df_nutrition = pd.read_csv('raw/sample_nutrition.csv')
    print(f"✓ Nutrition: {len(df_nutrition)} records")
except:
    print("✗ Nutrition dataset not found")
    df_nutrition = pd.DataFrame()

try:
    df_exercise = pd.read_csv('raw/sample_exercise.csv')
    print(f"✓ Exercise: {len(df_exercise)} records")
except:
    print("✗ Exercise dataset not found")
    df_exercise = pd.DataFrame()

try:
    df_qa = pd.read_csv('raw/sample_medical_qa.csv')
    print(f"✓ Medical Q&A: {len(df_qa)} records")
except:
    print("✗ Medical Q&A dataset not found")
    df_qa = pd.DataFrame()

try:
    df_pregnancy = pd.read_csv('raw/sample_pregnancy.csv')
    print(f"✓ Pregnancy: {len(df_pregnancy)} records")
except:
    print("✗ Pregnancy dataset not found")
    df_pregnancy = pd.DataFrame()

try:
    df_womens = pd.read_csv('raw/sample_womens_health.csv')
    print(f"✓ Women's Health: {len(df_womens)} records")
except:
    print("✗ Women's Health dataset not found")
    df_womens = pd.DataFrame()

# Process Nutrition Data
print("\n🔄 Processing nutrition data...")
if not df_nutrition.empty:
    # Add derived features
    df_nutrition['calories_per_100g'] = df_nutrition['calories']
    df_nutrition['protein_ratio'] = df_nutrition['protein'] / (df_nutrition['calories'] + 1)
    df_nutrition['carb_ratio'] = df_nutrition['carbs'] / (df_nutrition['calories'] + 1)
    df_nutrition['fat_ratio'] = df_nutrition['fat'] / (df_nutrition['calories'] + 1)
    
    # Categorize by calorie density
    df_nutrition['calorie_density'] = pd.cut(df_nutrition['calories'], 
                                               bins=[0, 50, 150, 300, 1000],
                                               labels=['very_low', 'low', 'medium', 'high'])
    
    df_nutrition.to_csv('processed/nutrition_processed.csv', index=False)
    print(f"✓ Processed {len(df_nutrition)} nutrition records")

# Process Exercise Data
print("\n🔄 Processing exercise data...")
if not df_exercise.empty:
    # Normalize calories per different body weights
    weights = [50, 60, 70, 80, 90]  # kg
    exercise_expanded = []
    
    for _, row in df_exercise.iterrows():
        for weight in weights:
            # Adjust calories based on weight (rough estimation)
            calories_adjusted = row['calories_per_hour'] * (weight / 70)
            exercise_expanded.append({
                'exercise_name': row['exercise_name'],
                'body_weight': weight,
                'calories_per_hour': calories_adjusted,
                'intensity': row['intensity'],
                'type': row['type']
            })
    
    df_exercise_exp = pd.DataFrame(exercise_expanded)
    df_exercise_exp.to_csv('processed/exercise_processed.csv', index=False)
    print(f"✓ Processed {len(df_exercise_exp)} exercise records")

# Process Medical Q&A
print("\n🔄 Processing medical Q&A data...")
if not df_qa.empty:
    # Clean text
    df_qa['question'] = df_qa['question'].str.strip()
    df_qa['answer'] = df_qa['answer'].str.strip()
    
    # Add metadata
    df_qa['question_length'] = df_qa['question'].str.len()
    df_qa['answer_length'] = df_qa['answer'].str.len()
    
    df_qa.to_csv('processed/medical_qa_processed.csv', index=False)
    print(f"✓ Processed {len(df_qa)} Q&A records")

# Process Pregnancy Data
print("\n🔄 Processing pregnancy data...")
if not df_pregnancy.empty:
    df_pregnancy.to_csv('processed/pregnancy_processed.csv', index=False)
    print(f"✓ Processed {len(df_pregnancy)} pregnancy records")

# Process Women's Health Data
print("\n🔄 Processing women's health data...")
if not df_womens.empty:
    # Encode severity
    severity_map = {'mild': 1, 'moderate': 2, 'severe': 3}
    df_womens['severity_score'] = df_womens['severity'].map(severity_map)
    
    df_womens.to_csv('processed/womens_health_processed.csv', index=False)
    print(f"✓ Processed {len(df_womens)} women's health records")

# Create unified knowledge base for chatbot
print("\n🔄 Creating unified knowledge base...")

knowledge_base = []

# Add nutrition knowledge
if not df_nutrition.empty:
    for _, row in df_nutrition.iterrows():
        knowledge_base.append({
            'category': 'nutrition',
            'topic': row['food_name'],
            'question': f"What is the nutritional value of {row['food_name']}?",
            'answer': f"{row['food_name']} contains {row['calories']} calories, {row['protein']}g protein, {row['carbs']}g carbs, and {row['fat']}g fat per serving.",
            'data': row.to_dict()
        })

# Add exercise knowledge
if not df_exercise.empty:
    for _, row in df_exercise.iterrows():
        knowledge_base.append({
            'category': 'fitness',
            'topic': row['exercise_name'],
            'question': f"How many calories does {row['exercise_name']} burn?",
            'answer': f"{row['exercise_name']} burns approximately {row['calories_per_hour']} calories per hour. It's a {row['intensity']} intensity {row['type']} exercise.",
            'data': row.to_dict()
        })

# Add medical Q&A knowledge
if not df_qa.empty:
    for _, row in df_qa.iterrows():
        knowledge_base.append({
            'category': row['category'],
            'topic': row['category'],
            'question': row['question'],
            'answer': row['answer'],
            'data': {}
        })

# Add pregnancy knowledge
if not df_pregnancy.empty:
    for _, row in df_pregnancy.iterrows():
        knowledge_base.append({
            'category': 'pregnancy',
            'topic': f"Week {row['week']}",
            'question': f"What happens during pregnancy week {row['week']}?",
            'answer': f"Week {row['week']}: Baby - {row['baby_development']}. Mother - {row['mother_changes']}. Advice: {row['advice']}",
            'data': row.to_dict()
        })

# Add women's health knowledge
if not df_womens.empty:
    for _, row in df_womens.iterrows():
        knowledge_base.append({
            'category': 'womens_health',
            'topic': row['symptom'],
            'question': f"What to do for {row['symptom']}?",
            'answer': f"For {row['symptom']} during {row['phase']} phase: {row['advice']}",
            'data': row.to_dict()
        })

# Save knowledge base
kb_df = pd.DataFrame(knowledge_base)
kb_df.to_csv('processed/knowledge_base.csv', index=False)
kb_df.to_json('processed/knowledge_base.json', orient='records', indent=2)

print(f"✓ Created unified knowledge base: {len(knowledge_base)} entries")

# Create dataset statistics
stats = {
    'total_records': len(knowledge_base),
    'categories': {
        'nutrition': len([k for k in knowledge_base if k['category'] == 'nutrition']),
        'fitness': len([k for k in knowledge_base if k['category'] == 'fitness']),
        'medical': len([k for k in knowledge_base if k['category'] in ['general', 'hydration', 'bmi', 'blood_pressure', 'diabetes', 'sleep']]),
        'pregnancy': len([k for k in knowledge_base if k['category'] == 'pregnancy']),
        'womens_health': len([k for k in knowledge_base if k['category'] == 'womens_health'])
    },
    'nutrition_foods': len(df_nutrition) if not df_nutrition.empty else 0,
    'exercises': len(df_exercise) if not df_exercise.empty else 0,
    'qa_pairs': len(df_qa) if not df_qa.empty else 0,
    'pregnancy_weeks': len(df_pregnancy) if not df_pregnancy.empty else 0,
    'womens_health_records': len(df_womens) if not df_womens.empty else 0
}

with open('processed/dataset_stats.json', 'w') as f:
    json.dump(stats, f, indent=2)

print("\n" + "=" * 60)
print("✅ Data Preprocessing Complete!")
print("=" * 60)
print(f"\n📊 Dataset Statistics:")
print(f"  Total Knowledge Base Entries: {stats['total_records']}")
print(f"  - Nutrition: {stats['categories']['nutrition']}")
print(f"  - Fitness: {stats['categories']['fitness']}")
print(f"  - Medical Q&A: {stats['categories']['medical']}")
print(f"  - Pregnancy: {stats['categories']['pregnancy']}")
print(f"  - Women's Health: {stats['categories']['womens_health']}")

print(f"\n💾 Output Files:")
print("  - processed/nutrition_processed.csv")
print("  - processed/exercise_processed.csv")
print("  - processed/medical_qa_processed.csv")
print("  - processed/pregnancy_processed.csv")
print("  - processed/womens_health_processed.csv")
print("  - processed/knowledge_base.csv")
print("  - processed/knowledge_base.json")
print("  - processed/dataset_stats.json")

print("\n📝 Next Step:")
print("  Run model training: jupyter notebook ../notebooks/train_model.ipynb")
