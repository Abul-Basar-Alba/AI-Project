# 🚀 Quick Setup Guide - HealthNest AI

## ⚡ Fast Track Installation (5 Minutes)

### Step 1: Install Dependencies (1 min)

```bash
cd backend
pip install flask flask-cors scikit-learn pandas numpy joblib nltk
cd ..
```

### Step 2: Prepare Data & Train Models (2 min)

```bash
cd datasets
python dataset_downloader.py
python preprocess_datasets.py
cd ..
```

### Step 3: Train Models (2 min)

Open and run all cells in:
```bash
jupyter notebook notebooks/train_model.ipynb
```

**Alternative:** Use Python to execute:
```bash
pip install jupyter nbconvert
cd notebooks
jupyter nbconvert --to notebook --execute train_model.ipynb --ExecutePreprocessor.timeout=600
cd ..
```

### Step 4: Start Backend (30 sec)

```bash
cd backend
python app.py
```

Keep this terminal running! ✅

### Step 5: Open Frontend (30 sec)

Open `frontend/index.html` in your browser:

```bash
cd ../frontend
python -m http.server 8000
```

Visit: **http://localhost:8000** 🎉

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] All pip packages installed
- [ ] Datasets created in `datasets/raw/`
- [ ] Processed data in `datasets/processed/`
- [ ] Models saved in `models/` folder
- [ ] Backend running on port 5000
- [ ] Frontend accessible in browser
- [ ] Chat interface loads successfully
- [ ] Can send messages and get responses

---

## 🐛 Common Issues & Fixes

### Issue 1: "Module not found" error

**Fix:**
```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### Issue 2: NLTK data not found

**Fix:**
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Issue 3: Backend not reachable from frontend

**Fix:**
- Ensure backend is running on port 5000
- Check `API_BASE_URL` in `frontend/script.js`
- Verify CORS is enabled in Flask

### Issue 4: Models not loading

**Fix:**
- Verify models exist in `models/` folder
- Re-run training notebook
- Check file paths in `backend/app.py`

### Issue 5: Frontend shows "Offline"

**Fix:**
1. Start backend first: `python backend/app.py`
2. Wait for "Models loaded successfully!" message
3. Refresh frontend page

---

## 📋 Project Structure Verification

After setup, your structure should look like:

```
AI-Project/
├── datasets/
│   ├── raw/
│   │   ├── sample_nutrition.csv ✅
│   │   ├── sample_exercise.csv ✅
│   │   ├── sample_medical_qa.csv ✅
│   │   ├── sample_pregnancy.csv ✅
│   │   └── sample_womens_health.csv ✅
│   └── processed/
│       ├── knowledge_base.csv ✅
│       └── knowledge_base.json ✅
├── models/
│   ├── qa_vectorizer.pkl ✅
│   ├── qa_database.pkl ✅
│   ├── calorie_predictor.pkl ✅
│   └── health_knowledge.json ✅
├── backend/
│   └── app.py ✅ (running)
└── frontend/
    └── index.html ✅ (open in browser)
```

---

## 🧪 Test Your Setup

### Test 1: Backend API

Open browser: http://localhost:5000

Should show:
```json
{
  "message": "HealthNest AI Backend API",
  "status": "running"
}
```

### Test 2: Health Check

```bash
curl http://localhost:5000/health
```

Should return:
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

### Test 3: Chat

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How to improve health?"}'
```

Should return health advice! ✅

---

## 💡 Tips for Best Experience

1. **Update your profile first** in the sidebar
2. **Use quick question buttons** for common queries
3. **Ask specific questions** for better answers
4. **Include context** (e.g., "I'm 25, how many calories?")
5. **Try different health topics**: nutrition, fitness, BMI, pregnancy

---

## 🎯 Demo Questions to Try

- "How to improve health?"
- "What is a healthy BMI range?"
- "Best foods for heart health?"
- "How much water should I drink daily?"
- "Best exercises for weight loss?"
- "How to reduce blood pressure?"
- "What is normal blood sugar level?"
- "What happens in pregnancy week 20?"

---

## 📊 Expected Performance

### On Sample Data (Default)
- Knowledge Base: ~30 entries
- Response Time: <1 second
- Model Accuracy: Good for demonstration

### On Full Kaggle Datasets (Optional)
- Knowledge Base: 200,000+ entries
- Response Time: 1-2 seconds
- Model Accuracy: Production-ready

---

## 🔄 Update/Reset Setup

### To retrain models:
```bash
cd notebooks
jupyter nbconvert --to notebook --execute train_model.ipynb
```

### To reset data:
```bash
cd datasets
rm -rf raw processed
python dataset_downloader.py
python preprocess_datasets.py
```

### To restart backend:
```bash
# Press Ctrl+C to stop
python backend/app.py
```

---

## 📞 Need Help?

If you encounter issues:

1. **Check logs** in terminal where backend is running
2. **Verify file paths** are correct
3. **Ensure Python 3.8+** is installed
4. **Check port 5000** is not in use
5. **Try restarting** backend and refreshing frontend

---

## 🎓 For CIT-316 Submission

### What to Submit:

1. **Code:** Entire `AI-Project` folder
2. **Report:** Include README.md content
3. **Demo:** Screenshots or video
4. **Models:** Include trained `.pkl` files
5. **Datasets:** Sample datasets (or links to Kaggle)

### Presentation Points:

- Problem statement ✅
- Dataset description ✅
- Model architecture ✅
- Training process ✅
- Results & evaluation ✅
- Live demo ✅
- Future enhancements ✅

---

**Ready to go! 🚀**

Run the backend, open the frontend, and start chatting with your AI health assistant!
