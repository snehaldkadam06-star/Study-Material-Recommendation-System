# StudyM - AI Study Material Recommendation System

A professional AI-powered study material recommendation system built with Python, Flask, and scikit-learn (KNN algorithm).

![StudyM Banner](https://img.shields.io/badge/StudyM-AI%20Powered-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-2.0+-orange?style=for-the-badge)
![scikit-learn](https://img.shields.io/badge/scikit--learn-KNN-red?style=for-the-badge)

## 📚 Overview

StudyM is an intelligent study material recommendation system that uses machine learning (K-Nearest Neighbors algorithm) to suggest the best study resources based on user preferences including subject, skill level, difficulty, and topic.

## 🏗️ Project Structure

```
StudyM/
├── dataset/
│   └── study_material_dataset.csv    # Training dataset
├── ml/
│   ├── train_knn_model.ipynb         # Jupyter notebook for model training
│   └── knn_model.pkl                 # Trained model with encoders
├── website/
│   ├── app.py                        # Flask application
│   ├── database.db                   # SQLite user database
│   ├── templates/                    # HTML templates
│   │   ├── index.html               # Home page
│   │   ├── login.html               # Login page
│   │   ├── signup.html              # Signup page
│   │   ├── dashboard.html           # Main recommendation form
│   │   ├── profile.html             # User profile
│   │   └── result.html              # Results display
│   └── static/
│       └── style.css                 # Professional styling
└── README.md                         # This file
```

## ✨ Features

- 🤖 **AI-Powered Recommendations**: Uses KNN algorithm for intelligent matching
- 👤 **User Authentication**: Secure signup/login system with session management
- 📊 **Dynamic Dropdowns**: Subject, level, difficulty, and topic selection
- 🎯 **Personalized Results**: 5 best-matching study materials per search
- 📺 **YouTube & Tutorial Links**: Direct access to recommended resources
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎨 **Modern UI**: Professional gradient design with smooth animations

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **ML Library**: scikit-learn (KNN)
- **Serialization**: Pickle
- **Frontend**: HTML5, CSS3, JavaScript
- **Fonts**: Poppins (Google Fonts)

## 📋 Prerequisites

Before running the project, ensure you have:

1. **Python 3.8+** installed
2. **pip** package manager

## 🚀 Installation

### 1. Install Required Packages

```bash
pip install flask pandas numpy scikit-learn
```

Or install from requirements.txt:

```bash
# Create requirements.txt
echo "flask>=2.0.0
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0" > requirements.txt

pip install -r requirements.txt
```

### 2. Train the Model (Optional - Model already included)

The pre-trained model (`knn_model.pkl`) is already included. If you want to retrain:

```bash
cd StudyM/ml
jupyter notebook train_knn_model.ipynb
```

Or run as Python script:

```python
# Run the notebook cells manually or use nbconvert
jupyter nbconvert --to notebook --execute train_knn_model.ipynb
```

### 3. Start the Flask Application

```bash
cd StudyM/website
python app.py
```

The application will start at: **http://127.0.0.1:5000**

## 💻 Usage Guide

### Step 1: Create Account
- Visit the home page
- Click "Get Started" or "Sign Up"
- Enter username, email, and password
- Click "Create Account"

### Step 2: Login
- Use your credentials to login
- You'll be redirected to the dashboard

### Step 3: Get Recommendations
- Select subject (e.g., Python, Machine Learning)
- Select your level (Beginner, Intermediate, Advanced)
- Select difficulty (Easy, Medium, Hard)
- Select topic (e.g., Python Fundamentals)
- Click "Get Recommendations"

### Step 4: View Results
- Browse 5 recommended study materials
- Click "YouTube" to watch video tutorials
- Click "Tutorial" to read documentation

## 🔧 How It Works

### Data Processing
1. Load CSV dataset with study materials
2. Encode categorical variables using LabelEncoder
3. Create feature matrix with encoded values

### Model Training
1. Split data into training/test sets
2. Train KNN model with k=5 neighbors
3. Use Euclidean distance metric
4. Save model with encoders using pickle

### Prediction
1. Get user input (subject, level, difficulty, topic)
2. Encode inputs using saved encoders
3. Find k-nearest neighbors
4. Return top 5 recommendations

## 📊 Dataset

The dataset contains study materials with:
- **subject**: Programming/technical subject
- **user_level**: Beginner, Intermediate, Advanced
- **difficulty**: Easy, Medium, Hard
- **topic**: Specific topic within subject
- **youtube_link**: Curated YouTube channel
- **tutorial_site_link**: Official documentation site

## 🎨 Design Features

### Professional UI Elements
- Gradient hero section with floating cards
- Animated feature cards with hover effects
- Smooth transitions and animations
- Clean typography with Poppins font
- Responsive grid layouts
- Custom form styling
- Alert/notification system

### Color Scheme
- Primary: Indigo (#6366f1)
- Secondary: Emerald (#10b981)
- Dark Background: Slate (#0f172a)
- Light Background: White (#ffffff)

## 🔍 Error Handling

The application handles:
- Invalid credentials
- Missing model files
- Empty form submissions
- Database errors
- 404/500 errors

## 📝 Configuration

### Model Path
Model is loaded from: `../ml/knn_model.pkl`

### Dataset Path
Dataset is loaded from: `../dataset/study_material_dataset.csv`

### Database
SQLite database created automatically on first run: `database.db`

## 🤝 Contributing

Feel free to:
- Report issues
- Suggest new features
- Submit pull requests

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

StudyM - AI Study Material Recommendation System
Built with ❤️ for education

## 🆘 Troubleshooting

### Model Not Found Error
```
FileNotFoundError: [Errno 2] No such file or directory: '../ml/knn_model.pkl'
```
**Solution**: Run the Jupyter notebook to generate the model file.

### Import Errors
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**: Install required packages: `pip install flask pandas numpy scikit-learn`

### Port Already in Use
```
OSError: [Errno 98] Address already in use
```
**Solution**: Change port in app.py or kill existing process

## 📈 Future Enhancements

- [ ] Add more ML algorithms
- [ ] User history tracking
- [ ] Rating system for materials
- [ ] Export recommendations to PDF
- [ ] Email notifications
- [ ] Social sharing

---

**Note**: This is a final year project demonstration. The model uses KNN (Nearest Neighbors) as specified and does not include deep learning or additional preprocessing.
