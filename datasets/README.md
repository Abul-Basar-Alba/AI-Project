# Health Datasets for HealthNest AI Assistant

## Dataset Sources

### 1. Nutrition & Food Database
- **Source:** USDA FoodData Central + Kaggle Food Nutrition
- **Size:** 100,000+ food items
- **Features:** food_name, calories, protein, carbs, fat, vitamins
- **Download:** https://www.kaggle.com/datasets/trolukovich/nutritional-values-for-common-foods-and-products

### 2. Exercise & Fitness Dataset
- **Source:** MET (Metabolic Equivalent) Dataset + Kaggle Fitness
- **Size:** 500+ exercises
- **Features:** exercise_name, calories_burned_per_hour, intensity, muscle_group
- **Download:** https://www.kaggle.com/datasets/aadhavvignesh/calories-burned-during-exercise-and-activities

### 3. Health Metrics Dataset
- **Source:** Kaggle Health Datasets
- **Size:** 20,000+ records
- **Features:** age, gender, bmi, bp, glucose, cholesterol
- **Download:** https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database

### 4. Medical Q&A Dataset
- **Source:** HealthTap + Medical Questions Dataset
- **Size:** 50,000+ Q&A pairs
- **Features:** question, answer, category
- **Download:** https://www.kaggle.com/datasets/pradeeppandey2000/medical-question-answer-datasets

### 5. Pregnancy Week-by-Week Data
- **Source:** NHS Pregnancy Guide + Manual Compilation
- **Size:** 40 weeks comprehensive data
- **Features:** week_number, baby_development, mother_changes, advice

### 6. Women's Health Dataset
- **Source:** Period Tracker + Cycle Data
- **Size:** 10,000+ cycle records
- **Features:** cycle_length, symptoms, mood, medication

## Dataset Preparation Steps

1. Download all datasets using `dataset_downloader.py`
2. Run preprocessing: `python preprocess_datasets.py`
3. Combined dataset will be saved in `processed/` folder
4. Ready for model training!

## Total Combined Dataset Size
**~200,000 records** covering all health aspects of HealthNest app
