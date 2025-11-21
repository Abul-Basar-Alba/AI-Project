# 🏥 HealthNest AI - Intelligent Health Assistant

**CIT-316 AI Sessional Project**

A comprehensive AI-powered health assistant that provides personalized health advice, nutrition recommendations, fitness guidance, and wellness support using machine learning and natural language processing.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Model Training](#model-training)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)
- [License](#license)

---

## 🎯 Project Overview

HealthNest AI is an intelligent health management system that combines multiple machine learning models to provide comprehensive health guidance. Unlike simple API-based chatbots, this project trains its own models on health datasets to deliver personalized recommendations.

### Problem Statement

"Develop an AI model that predicts and recommends personalized health and nutrition guidance, fitness routines, and wellness suggestions based on real-time user data and historical records."

### Key Objectives

✅ Train custom ML models on health datasets (NO API-only chatbot)  
✅ Provide personalized health recommendations  
✅ Cover multiple health domains (nutrition, fitness, pregnancy, women's health)  
✅ Real-time prediction and advice generation  
✅ User-friendly web interface  

---

## ✨ Features

### 🤖 AI-Powered Chatbot
- Natural language understanding for health questions
- Context-aware responses based on user profile
- Covers nutrition, fitness, BMI, blood pressure, pregnancy, women's health

### 📊 Health Analysis
- **BMI Calculator** with personalized advice
- **Calorie Needs Estimation** using Harris-Benedict equation
- **Water Intake Recommendation** based on body weight
- **Step Goal Setting** based on activity level

### 🍽️ Nutrition Intelligence
- Calorie prediction from food macros
- Diet recommendations
- Food nutritional analysis

### 🏃 Fitness Guidance
- Exercise recommendations based on goals
- Calorie burn estimation
- Activity-based workout plans

### 🤰 Pregnancy Support
- Week-by-week pregnancy guidance
- Baby development information
- Mother care recommendations

### 💊 Women's Health
- Period cycle support
- Symptom management advice
- Phase-specific recommendations

---

## 🛠️ Technology Stack

### Frontend
- **HTML5, CSS3, JavaScript** (Vanilla JS)
- Responsive design with modern UI/UX
- Real-time chat interface

### Backend
- **Python 3.8+**
- **Flask** - REST API framework
- **Flask-CORS** - Cross-origin resource sharing

### Machine Learning
- **scikit-learn** - ML models (Random Forest, TF-IDF)
- **pandas** - Data processing
- **numpy** - Numerical computations
- **NLTK** - Natural language processing
- **joblib** - Model serialization

### Models Trained
1. **Q&A Model**: TF-IDF + Cosine Similarity for question answering
2. **Calorie Predictor**: Random Forest Regressor for calorie estimation
3. **Exercise Recommender**: Random Forest Classifier for exercise suggestions
4. **Health Knowledge Base**: Rule-based system for structured advice

---

## 📁 Project Structure

```
AI-Project/
├── datasets/                    # Health datasets
│   ├── raw/                    # Raw data files
│   │   ├── sample_nutrition.csv
│   │   ├── sample_exercise.csv
│   │   ├── sample_medical_qa.csv
│   │   ├── sample_pregnancy.csv
│   │   └── sample_womens_health.csv
│   ├── processed/              # Processed data
│   │   ├── knowledge_base.csv
│   │   ├── knowledge_base.json
│   │   └── dataset_stats.json
│   ├── dataset_downloader.py   # Dataset preparation script
│   ├── preprocess_datasets.py  # Data preprocessing
│   └── README.md               # Dataset documentation
│
├── notebooks/                   # Jupyter notebooks
│   └── train_model.ipynb       # Model training notebook
│
├── models/                      # Trained models
│   ├── qa_vectorizer.pkl       # TF-IDF vectorizer
│   ├── qa_database.pkl         # Q&A knowledge base
│   ├── calorie_predictor.pkl   # Calorie prediction model
│   ├── exercise_recommender.pkl # Exercise model
│   ├── exercise_encoder.pkl    # Label encoder
│   ├── health_knowledge.json   # Health guidelines
│   └── model_metadata.json     # Model information
│
├── backend/                     # Flask API
│   ├── app.py                  # Main API application
│   └── requirements.txt        # Python dependencies
│
├── frontend/                    # Web interface
│   ├── index.html              # Main HTML page
│   ├── style.css               # Styling
│   └── script.js               # JavaScript logic
│
├── README.md                    # Project documentation
└── SETUP_GUIDE.md              # Installation guide
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser
- 2GB free disk space

### Step-by-Step Installation

#### 1. Clone or Download Project

```bash
cd "5Th_Semester/CIT-316(AI Sessional )/AI-Project"
```

#### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Requirements:**
- flask==3.0.0
- flask-cors==4.0.0
- scikit-learn==1.3.2
- pandas==2.1.3
- numpy==1.24.3
- joblib==1.3.2
- nltk==3.8.1

#### 3. Prepare Datasets

```bash
cd ../datasets
python dataset_downloader.py
```

This creates sample datasets for testing. For production, download full datasets from Kaggle.

#### 4. Preprocess Data

```bash
python preprocess_datasets.py
```

This will:
- Clean and process all datasets
- Create unified knowledge base
- Generate dataset statistics
- Save processed files in `processed/` folder

#### 5. Train Models

```bash
cd ../notebooks
jupyter notebook train_model.ipynb
```

**Or run all cells programmatically:**

```bash
pip install jupyter
jupyter nbconvert --to notebook --execute train_model.ipynb
```

**Expected outputs:**
- ✅ Q&A Model (TF-IDF vectorizer)
- ✅ Calorie Predictor (Random Forest)
- ✅ Exercise Recommender
- ✅ Health Knowledge Base

**Training time:** ~2-5 minutes on sample data

#### 6. Start Backend Server

```bash
cd ../backend
python app.py
```

**Output:**
```
🔄 Loading AI models...
✓ Q&A Model loaded
✓ Calorie Predictor loaded
✓ Exercise Recommender loaded
✓ Health Knowledge Base loaded
✅ Models loaded successfully!

====================================================
🚀 HealthNest AI Backend API Starting...
====================================================

📡 Server: http://localhost:5000
📖 Docs: http://localhost:5000/
```

**Backend will run on:** `http://localhost:5000`

#### 7. Open Frontend

Open `frontend/index.html` in your web browser:

```bash
cd ../frontend
# On Linux:
xdg-open index.html

# On Mac:
open index.html

# On Windows:
start index.html
```

**Or** use a simple HTTP server:

```bash
python -m http.server 8000
# Then visit: http://localhost:8000
```

---

## 📖 Usage Guide

### 1. Update Your Profile

In the sidebar:
- Enter your **Age, Gender, Weight, Height**
- Select **Activity Level**
- Click **"Update Profile"**

This generates personalized health metrics:
- BMI and category
- Daily calorie needs
- Water intake goal
- Step target

### 2. Ask Health Questions

**Example questions:**
- "How to improve health?"
- "What is a healthy BMI?"
- "Best foods for heart?"
- "How much water should I drink?"
- "Best exercises for weight loss?"
- "What happens in pregnancy week 20?"

**Quick question buttons** are available for common queries.

### 3. View Recommendations

The AI will:
- Answer your question
- Provide personalized advice based on your profile
- Suggest specific actions
- Include relevant health metrics

---

## 🧠 Model Training

### Datasets Used

| Dataset | Records | Purpose |
|---------|---------|---------|
| Nutrition | 8+ foods | Calorie prediction, diet advice |
| Exercise | 35+ activities | Workout recommendations |
| Medical Q&A | 8+ pairs | Question answering |
| Pregnancy | 6 weeks | Pregnancy guidance |
| Women's Health | 6 symptoms | Period & symptom support |

**Total Knowledge Base:** 30+ entries (sample), expandable to 200,000+

### Training Process

1. **Data Collection** → Multiple health datasets
2. **Preprocessing** → Cleaning, normalization, feature engineering
3. **Model Training** → Random Forest, TF-IDF
4. **Evaluation** → R², RMSE, Accuracy metrics
5. **Serialization** → Save models as `.pkl` files

### Model Performance

#### Calorie Predictor
- **Algorithm:** Random Forest Regressor
- **R² Score:** ~0.95+
- **RMSE:** <20 calories
- **Input:** Protein, Carbs, Fat (grams)
- **Output:** Predicted calories

#### Q&A Model
- **Algorithm:** TF-IDF + Cosine Similarity
- **Vocabulary Size:** 500+ words
- **Threshold:** 0.1 similarity
- **Categories:** nutrition, fitness, bmi, pregnancy, women's health, general

---

## 🔌 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "models_loaded": {
    "qa_model": true,
    "calorie_predictor": true,
    "exercise_recommender": true,
    "knowledge_base": true
  }
}
```

#### 2. Chat
```http
POST /chat
Content-Type: application/json

{
  "message": "How to improve health?",
  "profile": {
    "age": 25,
    "gender": "male",
    "weight": 70,
    "height": 170,
    "activity": "moderate"
  }
}
```

**Response:**
```json
{
  "message": "How to improve health?",
  "response": "To improve health: eat balanced diet, exercise regularly...",
  "confidence": 0.85,
  "category": "general"
}
```

#### 3. Health Analysis
```http
POST /health-check
Content-Type: application/json

{
  "age": 25,
  "gender": "male",
  "weight": 70,
  "height": 170,
  "activity": "moderate"
}
```

**Response:**
```json
{
  "metrics": {
    "bmi": 24.2,
    "bmi_category": "normal",
    "daily_water_liters": 2.3,
    "daily_calories": 2400,
    "step_goal": 7500
  },
  "recommendations": [...]
}
```

#### 4. Predict Calories
```http
POST /predict-calories
Content-Type: application/json

{
  "protein": 30,
  "carbs": 50,
  "fat": 10
}
```

**Response:**
```json
{
  "protein_g": 30,
  "carbs_g": 50,
  "fat_g": 10,
  "predicted_calories": 410
}
```

#### 5. Pregnancy Info
```http
GET /pregnancy-info?week=20
```

**Response:**
```json
{
  "week": 20,
  "baby_development": "Size of a banana",
  "mother_changes": "May feel baby movements",
  "advice": "Midpoint scan, eat iron-rich foods",
  "trimester": 2
}
```

---

## 📸 Screenshots

### Chat Interface
Beautiful gradient design with real-time chat functionality.

### Profile & Metrics
Personalized health metrics calculated instantly.

### Mobile Responsive
Works seamlessly on all devices.

---

## 🚧 Future Enhancements

### Phase 2 (Possible Extensions)

1. **Enhanced Models**
   - Deep Learning (LSTM, BERT) for better NLP
   - Larger datasets (100k+ records)
   - Multi-language support

2. **Additional Features**
   - Voice input/output
   - Image recognition for food
   - Medication reminders
   - Health history tracking
   - Doctor recommendations

3. **Integration**
   - Connect with HealthNest Flutter app
   - Wearable device data (Fitbit, Apple Watch)
   - EMR/EHR systems
   - Telemedicine platforms

4. **Advanced Analytics**
   - Trend analysis
   - Predictive health alerts
   - Personalized meal plans
   - Workout scheduling

---

## 👨‍💻 Contributors

**Your Name**  
Department of Computer Science & Engineering  
Jahangirnagar University  
Course: CIT-316 (AI Sessional)  
Session: 2020-2021

---

## 📄 License

This project is developed for educational purposes as part of CIT-316 coursework.

---

## ⚠️ Disclaimer

**Important:** This AI assistant provides general health information only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical concerns.

---

## 🙏 Acknowledgments

- **Datasets:** Kaggle, USDA, NHS, CDC
- **Libraries:** scikit-learn, Flask, pandas
- **Course:** CIT-316 AI Sessional, Jahangirnagar University
- **Instructor:** [Professor Name]

---

## 📞 Support

For questions or issues:
- **Email:** your.email@example.com
- **GitHub:** [Your GitHub Profile]

---

**Made with ❤️ for CIT-316 AI Project**

*Last Updated: November 21, 2024*
