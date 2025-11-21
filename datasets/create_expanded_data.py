"""
Create expanded health Q&A dataset with better coverage
"""

import pandas as pd
import json
import os

print("🔄 Creating expanded health dataset...")

# Expanded Q&A data with exercise, steps, period tips, general health
qa_data = {
    'question': [
        # Exercise questions - variations
        'Which exercise is better for me?',
        'What exercises should I do?',
        'Best workout for weight loss?',
        'How to start exercising?',
        'Exercise for beginners?',
        'Cardio or strength training?',
        'How long should I exercise?',
        'Best time to workout?',
        'What is best exercise?',
        'Which workout is good?',
        'Exercise recommendation please',
        'Suggest some exercises',
        'What should I do for fitness?',
        'Best fitness routine?',
        'How to get fit?',
        'Workout suggestions?',
        
        # Steps and walking - variations
        'How many steps per day?',
        'How much should I walk?',
        'Is 10000 steps necessary?',
        'Steps for good health?',
        'Walking benefits?',
        'How many steps to lose weight?',
        'Daily steps target?',
        'How much walking is enough?',
        'Step count for health?',
        'Walking everyday good?',
        'Should I walk daily?',
        'How many steps needed?',
        
        # Period and women's health - variations
        'Period tips?',
        'How to reduce period pain?',
        'Menstrual cramp relief?',
        'Period irregularity?',
        'What to eat during periods?',
        'Exercise during menstruation?',
        'PMS symptoms?',
        'Period cramps help?',
        'Painful periods relief?',
        'Menstrual pain medicine?',
        'Period care tips?',
        'Menstruation advice?',
        
        # General health - variations
        'How to improve health?',
        'Tips for healthy lifestyle?',
        'How to stay healthy?',
        'Daily health routine?',
        'Healthy habits?',
        'How to be fit?',
        'Health improvement tips?',
        'Stay healthy naturally?',
        'What is good for health?',
        'How to maintain health?',
        'Healthy living tips?',
        'Be healthier?',
        'Health advice please?',
        'How to live healthy?',
        
        # BMI and weight
        'What is a healthy BMI?',
        'What is normal BMI?',
        'BMI range?',
        'How to calculate BMI?',
        'Ideal body weight?',
        'Am I overweight?',
        
        # Blood pressure
        'How to lower blood pressure?',
        'Normal blood pressure?',
        'High BP treatment?',
        'BP control tips?',
        
        # Diabetes
        'What are symptoms of diabetes?',
        'Diabetes prevention?',
        'Blood sugar control?',
        
        # Hydration
        'How much water to drink daily?',
        'Water intake per day?',
        'Hydration tips?',
        
        # Heart health
        'What is normal heart rate?',
        'Heart healthy habits?',
        'Cardiovascular health?',
        
        # Immunity
        'How to improve immunity?',
        'Boost immune system?',
        'Immunity foods?',
        
        # Mental health
        'How to reduce stress?',
        'Stress management tips?',
        'Anxiety relief?',
        
        # Sleep
        'How much sleep needed?',
        'Better sleep tips?',
        'Insomnia cure?',
    ],
    'answer': [
        # Exercise answers
        '💪 **Exercise Recommendations:**\n\n**For Beginners:**\n• Walking: 30 mins daily\n• Bodyweight exercises: Squats, push-ups, planks\n• Light yoga or stretching\n\n**For Weight Loss:**\n• HIIT workouts: 20-30 mins, 3x/week\n• Running/jogging: 30-45 mins\n• Cycling or swimming\n\n**For Muscle Building:**\n• Strength training: 3-4x/week\n• Progressive overload with weights\n• Compound movements (squats, deadlifts)\n\n**For Overall Fitness:**\n• Mix cardio + strength training\n• 150 mins moderate exercise/week\n• Stay consistent and enjoy the process!',
        
        '💪 Best exercises include:\n• **Cardio:** Walking, running, cycling, swimming (150 mins/week)\n• **Strength:** Weight training, bodyweight exercises (2-3x/week)\n• **Flexibility:** Yoga, stretching (daily)\n• **Core:** Planks, crunches, leg raises\n\nChoose activities you enjoy to stay consistent!',
        
        '🔥 **Weight Loss Workouts:**\n1. **HIIT (High-Intensity Interval Training)**: Most effective, 20-30 mins\n2. **Running/Jogging**: 300-400 calories/30 mins\n3. **Cycling**: 250-350 calories/30 mins\n4. **Swimming**: Full body, 400+ calories/hour\n5. **Jump rope**: 300+ calories/30 mins\n\n**Combine with:** Strength training 2-3x/week + Calorie deficit diet!\n\nRemember: 70% diet, 30% exercise for weight loss!',
        
        '🚀 **Starting Exercise Plan:**\n\n**Week 1-2:** Walk 15-20 mins daily\n**Week 3-4:** Increase to 30 mins + light jogging\n**Week 5-6:** Add bodyweight exercises (squats, push-ups, planks)\n**Week 7+:** Join gym or structured program\n\n**Tips:**\n• Start slow, avoid injuries\n• Warm up before, stretch after\n• Rest days are important\n• Stay hydrated\n• Listen to your body!',
        
        '👶 **Beginner Exercises:**\n\n**Cardio (Start here!):**\n• Walking: 20-30 mins\n• Light jogging\n• Cycling\n• Swimming\n\n**Strength (Bodyweight):**\n• Squats: 3 sets × 10 reps\n• Push-ups: 3 × 8 (knee push-ups OK)\n• Planks: 3 × 20-30 seconds\n• Lunges: 3 × 10 each leg\n\n**Flexibility:**\n• Basic stretching: 5-10 mins\n• Beginner yoga\n\nStart 3x/week, gradually increase!',
        
        '🤔 **Cardio vs Strength:**\n\n**Cardio (Running, Cycling, Swimming):**\n✅ Burns calories during workout\n✅ Improves heart health\n✅ Better for immediate weight loss\n\n**Strength Training (Weights, Resistance):**\n✅ Builds muscle\n✅ Boosts metabolism (burns calories 24/7)\n✅ Tones body, improves posture\n\n**Best Approach:**\n🎯 **3x Cardio + 2x Strength per week** for balanced fitness!\n\nBoth are essential for optimal health!',
        
        '⏱️ **Exercise Duration:**\n\n**Minimum for Health:**\n• 150 mins moderate exercise/week\n• = 30 mins × 5 days\n\n**For Weight Loss:**\n• 300+ mins moderate exercise/week\n• = 45-60 mins × 5-6 days\n\n**For Fitness:**\n• 45-60 mins per session\n• Mix cardio + strength\n\n**Short on time?**\n• 10-minute walks count!\n• Break into shorter sessions\n• Consistency > Duration',
        
        '🕐 **Best Workout Time:**\n\n**Morning (6-8 AM):**\n✅ Boosts energy for the day\n✅ Improves mood\n✅ More consistent (fewer distractions)\n✅ Better for weight loss\n\n**Evening (5-7 PM):**\n✅ Better performance (body warmed up)\n✅ Stress relief after work\n✅ Muscle strength peaks\n\n**Truth:** Best time is when **YOU can be consistent!**\n\nChoose what fits your schedule. Regular exercise beats perfect timing!',
        
        '💪 Best exercises: Walking, running, swimming, cycling, strength training, yoga. Mix cardio + strength for balanced fitness. Start with what you enjoy and build consistency!',
        
        '🏋️ Good workouts: Cardio (walking, jogging, cycling) for heart health + Strength training (weights, bodyweight) for muscle + Flexibility (yoga, stretching) for mobility. Do 150 mins/week!',
        
        '💪 Exercise recommendations: For beginners - walking, bodyweight exercises. For weight loss - HIIT, running. For muscle - strength training. Mix different types for best results!',
        
        '🎯 Exercise suggestions: Start with 30 min walks daily, add squats and push-ups 3x/week, try yoga for flexibility. Gradually increase intensity. Stay consistent!',
        
        '🏃 For fitness: Do cardio 3-4x/week (walking, jogging, cycling), strength training 2-3x/week (bodyweight or weights), stretch daily. Aim for 150+ mins total exercise weekly!',
        
        '💪 Best fitness routine: Monday/Wednesday/Friday - Strength training, Tuesday/Thursday - Cardio, Weekend - Active recovery (walking, yoga). Rest one day. Stay hydrated!',
        
        '🎯 Get fit: Exercise regularly (150 mins/week), eat balanced diet, sleep 7-8 hours, stay hydrated, be consistent. Start small and build habits!',
        
        '🏋️ Workout suggestions: Beginners - walking + bodyweight exercises. Intermediate - running + gym. Advanced - HIIT + weight training. Choose based on your fitness level!',
        
        # Steps answers
        '👣 **Daily Steps Target:**\n\n**Minimum:** 5,000 steps (sedentary prevention)\n**Good:** 7,000-8,000 steps (health benefits)\n**Optimal:** 10,000 steps (fitness goal)\n**Active:** 12,000+ steps (very active lifestyle)\n\n**Benefits:**\n• Improved heart health\n• Weight management\n• Better mood\n• Stronger bones\n• Reduced disease risk\n\n**Tips to Increase Steps:**\n• Take stairs instead of elevator\n• Park farther from entrance\n• Walk during phone calls\n• Walk after meals\n• Use fitness tracker to monitor\n\nEvery step counts towards better health!',
        
        '🚶 **Walking Guidelines:**\n\n**Daily Minimum:** 30 minutes (3,000-4,000 steps)\n**For Health:** 45-60 mins (6,000-8,000 steps)\n**For Fitness:** 60+ mins (8,000-10,000 steps)\n**For Weight Loss:** 60-90 mins (10,000-12,000 steps)\n\n**Benefits:**\n• Burns 150-300 calories/hour\n• Improves cardiovascular health\n• Reduces stress\n• No equipment needed\n• Easy on joints\n\n**Best Practices:**\n• Walk briskly (3-4 mph)\n• Maintain good posture\n• Wear comfortable shoes\n• Walk after meals for digestion\n• Listen to music/podcasts',
        
        '🎯 **About 10,000 Steps:**\n\nWhile 10,000 steps is a popular goal, recent research shows:\n\n**7,000-8,000 steps** provides significant health benefits!\n\n**Step Scale:**\n• <5,000: Sedentary (health risks)\n• 5,000-7,000: Low active (basic health)\n• 7,000-10,000: Active (good health)\n• 10,000+: Very active (excellent fitness)\n\n**Key Points:**\n✅ 7,000 steps reduces mortality risk by 50-70%\n✅ More is better, but 10,000 not mandatory\n✅ Quality matters: Brisk walking > slow steps\n✅ Any increase is beneficial\n\n**Goal:** Be more active than yesterday! Progress > Perfection',
        
        '👣 **Steps for Good Health:**\n\n**Minimum:** 5,000 steps daily\n**Recommended:** 7,000-10,000 steps\n**Benefits at each level:**\n\n**5,000 steps:**\n• Basic activity level\n• Prevents sedentary risks\n\n**7,000 steps:**\n• Significant health improvements\n• Reduced disease risk\n• Better mood and energy\n\n**10,000 steps:**\n• Optimal fitness\n• Weight management\n• Enhanced cardiovascular health\n\n**Tracking Tips:**\n• Use smartphone or fitness watch\n• Track weekly average\n• Celebrate small increases\n• Make it a habit!',
        
        '🚶 **Walking Benefits:**\n\n**Physical Health:**\n• Improves heart health, lowers BP\n• Aids weight loss (150-300 cal/hour)\n• Strengthens bones and muscles\n• Reduces joint pain\n• Lowers blood sugar\n• Boosts immune system\n\n**Mental Health:**\n• Reduces stress and anxiety\n• Improves mood (releases endorphins)\n• Enhances creativity\n• Better sleep quality\n\n**Other Benefits:**\n• Free and accessible\n• Low injury risk\n• Social activity\n• Easy to start\n\n**Just 30 minutes daily makes a huge difference!**',
        
        '👣 **Steps for Weight Loss:**\n\n**Target:** 10,000-12,000 steps daily\n• Equals 5-6 kilometers\n• Burns 300-500 calories\n\n**Weight Loss Plan:**\n1. **Week 1-2:** Establish baseline, aim 7,000\n2. **Week 3-4:** Increase to 8,500\n3. **Week 5-6:** Target 10,000\n4. **Week 7+:** Maintain 10,000-12,000\n\n**Maximize Fat Burning:**\n• Walk briskly (break a sweat)\n• Walk after meals\n• Take stairs\n• Add incline walking\n• Morning walks (fasted cardio)\n\n**Combine With:**\n• Calorie deficit diet\n• Drink 8-10 glasses water\n• Adequate sleep\n\nConsistency is key!',
        
        '🎯 Daily steps target: Aim for 7,000-10,000 steps. Minimum 5,000 for sedentary people. Use stairs, walk during breaks, track with phone!',
        
        '🚶 Walk at least 30 mins daily (4,000 steps minimum). For fitness: 45-60 mins (8,000 steps). For weight loss: 10,000+ steps!',
        
        '👣 Step count: 7,000-8,000 steps shows great health benefits. 10,000 is optimal but not mandatory. Every step counts!',
        
        '🚶 Yes! Walking daily improves heart health, helps weight management, boosts mood, strengthens bones. Aim 30-60 mins per day!',
        
        '✅ Yes, walk daily! 30 minutes minimum. Benefits: heart health, weight control, stress relief, better sleep, improved energy!',
        
        '🎯 Need 7,000-10,000 steps daily for good health. Start with 5,000 and increase gradually. Track progress!',
        
        # Period/women's health answers
        '🩸 **Period Tips:**\n\n**Pain Relief:**\n• Heat therapy (heating pad on abdomen)\n• Gentle massage\n• Light exercise (walking, yoga)\n• Pain medication (ibuprofen)\n\n**Foods to Eat:**\n• Iron-rich: Spinach, red meat, lentils, dates\n• Anti-inflammatory: Ginger, turmeric\n• Fruits: Watermelon, banana\n• Dark chocolate (small amount)\n• Warm herbal teas\n\n**Avoid:**\n• Excess caffeine\n• High salt foods\n• Processed foods\n• Excess sugar\n\n**Self-Care:**\n• Stay hydrated (8-10 glasses water)\n• Adequate rest\n• Track your cycle\n• Use comfortable sanitary products\n\nIf pain is severe or irregular, consult gynecologist!',
        
        '💊 **Period Pain Relief:**\n\n**Immediate Relief:**\n1. **Heat therapy:** Heating pad or hot water bottle on lower abdomen (15-20 mins)\n2. **Pain medication:** Ibuprofen or naproxen\n3. **Position:** Fetal position, knees to chest\n\n**Natural Remedies:**\n• Ginger tea (anti-inflammatory)\n• Cinnamon tea\n• Fennel seeds\n• Chamomile tea (relaxing)\n\n**Exercise:**\n• Light walking\n• Gentle yoga (child pose, cat-cow)\n• Stretching\n\n**Massage:**\n• Circular motions on abdomen\n• Lower back massage\n\n**Lifestyle:**\n• Stay hydrated\n• Avoid caffeine\n• Adequate sleep\n• Reduce stress\n\n**See doctor if:** Pain is severe, interferes with daily life, or getting worse!',
        
        '😣 Menstrual cramp relief: Apply heat, take ibuprofen, gentle exercise, stay hydrated, eat anti-inflammatory foods (ginger, turmeric). Rest when needed!',
        
        '📅 Period irregularity causes: Stress, PCOS, thyroid, weight changes. Track cycle, maintain healthy lifestyle. See gynecologist if persistently irregular!',
        
        '🍎 Foods during periods: Iron-rich (spinach, lentils, dates), omega-3 (fish, walnuts), bananas, dark chocolate, ginger tea. Avoid excess caffeine and salt!',
        
        '🏃 Yes, light exercise during periods helps! Walking, gentle yoga, stretching reduce cramps. Avoid intense workouts if feeling weak. Listen to your body!',
        
        '😔 PMS symptoms: Mood swings, bloating, fatigue, cramps, cravings. Manage with exercise, balanced diet, adequate sleep, stress management, hydration!',
        
        '💊 Period cramps help: Heat pad, pain medicine, rest, light walking, ginger tea, stay hydrated. If severe pain, consult doctor!',
        
        '😣 Painful periods relief: Heat therapy, medication (ibuprofen), yoga poses, herbal tea, rest. Track severity and consult gynecologist if needed!',
        
        '💊 Menstrual pain medicine: Ibuprofen (Advil), naproxen (Aleve), or acetaminophen. Take with food. Follow dosage instructions!',
        
        '🩸 Period care: Use comfortable sanitary products, change regularly, maintain hygiene, eat nutritious foods, stay hydrated, rest adequately!',
        
        '📅 Menstruation advice: Track cycle, eat iron-rich foods, exercise regularly, manage stress, stay hygienic. Consult doctor for concerns!',
        
        # General health answers
        '🏥 To improve health: Eat balanced diet (fruits, vegetables, lean proteins), exercise 150 mins/week, sleep 7-8 hours, stay hydrated (8-10 glasses water), manage stress, avoid smoking/excess alcohol, regular checkups!',
        
        '💚 Healthy lifestyle tips: Nutritious meals 5-6x/day, exercise daily 30+ mins, sleep 7-8 hours, drink plenty water, manage stress (yoga, meditation), social connections, avoid smoking, limit alcohol, positive mindset!',
        
        '✅ Stay healthy: Eat whole foods (avoid processed), move your body daily, prioritize sleep, hydrate well, manage stress, maintain relationships, regular health screenings, practice gratitude!',
        
        '📅 Daily health routine: Wake early, drink water, exercise/yoga 30 mins, healthy breakfast, fruits mid-morning, balanced lunch, evening walk, nutritious dinner, relaxation, sleep by 10-11 PM!',
        
        '🎯 Healthy habits: Regular exercise, balanced nutrition, adequate sleep, stress management, hydration, no smoking, limited alcohol, mindfulness, social connections, continuous learning!',
        
        '💪 Be fit: Exercise 5-6x/week (mix cardio + strength), eat protein-rich foods, stay active throughout day, sleep well, manage stress, track progress, stay consistent!',
        
        '📈 Health improvement: Start small (add vegetables, walk 20 mins, drink more water), set realistic goals, track progress, stay consistent, get support, celebrate wins!',
        
        '🌿 Stay healthy naturally: Whole foods diet, regular movement, adequate sleep, stress reduction (meditation, nature), sunlight exposure, avoid chemicals, herbal remedies, social wellness!',
        
        '✅ Good for health: Nutritious food, regular exercise, quality sleep, stress management, hydration, positive relationships, purpose in life!',
        
        '🏥 Maintain health: Balanced diet, active lifestyle, regular checkups, stress control, adequate rest, avoid harmful habits, stay hydrated, positive mindset!',
        
        '💚 Healthy living: Eat colorful vegetables/fruits, exercise daily, sleep 7-8 hours, drink water, manage stress, laugh often, nurture relationships!',
        
        '📈 Be healthier: Small daily improvements - take stairs, eat more vegetables, walk 10 mins, drink water, sleep on time. Consistency beats perfection!',
        
        '🏥 Health advice: Exercise regularly, eat whole foods, prioritize sleep, manage stress, stay hydrated, avoid smoking, limit alcohol, regular checkups!',
        
        '💪 Live healthy: Balanced nutrition, active lifestyle, quality sleep, stress management, strong relationships, purpose, continuous learning, gratitude practice!',
        
        # BMI answers
        'A healthy BMI is between 18.5 and 24.9. Below 18.5 is underweight, 25-29.9 is overweight, 30+ is obese. Calculate: weight(kg) / height(m)²',
        
        '📊 Normal BMI: 18.5-24.9 is healthy. <18.5 underweight, 25-29.9 overweight, 30+ obese. Maintain healthy weight through diet and exercise!',
        
        '📏 BMI ranges: Underweight <18.5, Normal 18.5-24.9, Overweight 25-29.9, Obese 30+. BMI = weight(kg) / height(m)²',
        
        '🧮 Calculate BMI: Divide your weight in kg by your height in meters squared. Example: 70kg / (1.75m)² = 22.9 (normal)',
        
        '⚖️ Ideal body weight depends on height. For 170cm: 58-72kg (BMI 18.5-24.9). Use BMI calculator for your height!',
        
        '📊 Check BMI: Calculate weight(kg) / height(m)². If 25-29.9, you may be overweight. Consult doctor for personalized advice!',
        
        # Blood pressure answers
        'Lower blood pressure: Reduce salt intake, exercise regularly, maintain healthy weight, limit alcohol, manage stress, eat potassium-rich foods, take prescribed medications!',
        
        '💓 Normal blood pressure: 120/80 mmHg or lower. 120-129/<80 is elevated. 130-139/80-89 is stage 1 hypertension. Monitor regularly!',
        
        '🩺 High BP treatment: Reduce salt, exercise 150 mins/week, lose weight, limit alcohol, manage stress, eat DASH diet, medication if prescribed!',
        
        '💊 BP control: Low-sodium diet, regular exercise, maintain healthy weight, limit caffeine/alcohol, stress management, adequate sleep, monitor daily!',
        
        # Diabetes answers
        'Diabetes symptoms: Increased thirst, frequent urination, extreme hunger, unexplained weight loss, fatigue, blurred vision, slow-healing sores. Check blood sugar!',
        
        '🩸 Diabetes prevention: Maintain healthy weight, exercise regularly, eat whole grains/vegetables, limit sugar, avoid processed foods, regular checkups!',
        
        '📊 Blood sugar control: Monitor regularly, eat balanced meals, exercise daily, take medications as prescribed, manage stress, adequate sleep!',
        
        # Hydration answers
        'Drink 8-10 glasses (2-3 liters) of water daily. More if exercising or in hot weather. Stay hydrated for optimal health!',
        
        '💧 Water intake: 2.5-3 liters per day for adults. More during exercise. Divide weight(kg) by 30 for personalized amount in liters!',
        
        '💦 Hydration tips: Drink water upon waking, before meals, carry water bottle, eat water-rich fruits, monitor urine color (pale yellow is good)!',
        
        # Heart health answers
        'Normal resting heart rate: 60-100 bpm for adults. Athletes may have 40-60 bpm. Check pulse regularly!',
        
        '❤️ Heart healthy habits: Exercise regularly, eat heart-healthy diet (fish, nuts, vegetables), maintain healthy weight, don\'t smoke, limit alcohol, manage stress!',
        
        '💓 Cardiovascular health: Regular aerobic exercise, Mediterranean diet, maintain healthy cholesterol/BP, don\'t smoke, manage stress, regular checkups!',
        
        # Immunity answers
        'Boost immunity: Eat fruits/vegetables, exercise regularly, get adequate sleep (7-8 hours), manage stress, stay hydrated, avoid smoking, maintain hygiene!',
        
        '🛡️ Immune system boost: Vitamin C foods (citrus, bell peppers), zinc (nuts, seeds), probiotics (yogurt), adequate sleep, regular exercise, stress management!',
        
        '🥗 Immunity foods: Citrus fruits, garlic, ginger, turmeric, yogurt, spinach, almonds, green tea, mushrooms. Eat colorful variety!',
        
        # Mental health answers
        'Reduce stress: Regular exercise, meditation, deep breathing, adequate sleep, healthy diet, social connections, time management, hobbies, professional help if needed!',
        
        '😌 Stress management: Exercise, mindfulness meditation, deep breathing, adequate sleep, healthy boundaries, social support, time in nature, journaling!',
        
        '😰 Anxiety relief: Deep breathing exercises, progressive muscle relaxation, physical activity, limit caffeine, adequate sleep, talk therapy, mindfulness!',
        
        # Sleep answers
        '😴 Adults need 7-9 hours sleep nightly. Teenagers: 8-10 hours. Consistent sleep schedule, dark room, no screens before bed!',
        
        '💤 Better sleep tips: Consistent schedule, cool dark room, avoid screens 1 hour before bed, limit caffeine, exercise (not before bed), relaxation routine!',
        
        '😴 Insomnia cure: Regular sleep schedule, relaxing bedtime routine, avoid screens, limit caffeine/alcohol, exercise earlier in day. See doctor if persistent!',
    ],
    'category': [
        'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise',
        'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise',
        'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise', 'exercise',
        'exercise', 'exercise', 'exercise', 'exercise',
        'womens_health', 'womens_health', 'womens_health', 'womens_health', 'womens_health', 'womens_health', 'womens_health',
        'womens_health', 'womens_health', 'womens_health', 'womens_health', 'womens_health',
        'general', 'general', 'general', 'general', 'general', 'general', 'general', 'general',
        'general', 'general', 'general', 'general', 'general', 'general',
        'bmi', 'bmi', 'bmi', 'bmi', 'bmi', 'bmi',
        'blood_pressure', 'blood_pressure', 'blood_pressure', 'blood_pressure',
        'diabetes', 'diabetes', 'diabetes',
        'hydration', 'hydration', 'hydration',
        'heart', 'heart', 'heart',
        'immunity', 'immunity', 'immunity',
        'mental_health', 'mental_health', 'mental_health',
        'sleep', 'sleep', 'sleep'
    ]
}

# Save as CSV
df = pd.DataFrame(qa_data)
df.to_csv('raw/expanded_medical_qa.csv', index=False)
print(f"✅ Created expanded Q&A dataset with {len(df)} questions")

# Save detailed JSON
with open('raw/expanded_medical_qa.json', 'w', encoding='utf-8') as f:
    json.dump(qa_data, f, indent=2, ensure_ascii=False)
print("✅ Saved JSON version")

# Print statistics
print(f"\n📊 Dataset Statistics:")
print(f"Total questions: {len(df)}")
print(f"\nQuestions by category:")
print(df['category'].value_counts())

print("\n✅ Expanded dataset created successfully!")
