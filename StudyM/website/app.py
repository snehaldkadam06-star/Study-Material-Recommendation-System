"""
StudyM - AI-Powered Study Material Recommendation System
Flask Web Application
"""

import os
import sqlite3
import pickle
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)
app.secret_key = 'studym_secret_key_2024'

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
MODEL_PATH = os.path.join(PROJECT_DIR, 'ml', 'knn_model.pkl')
DATASET_PATH = os.path.join(PROJECT_DIR, 'dataset', 'study_material_dataset.csv')
DB_PATH = os.path.join(BASE_DIR, 'database.db')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn
# Global model data (loaded once)
model_data = None


def init_database():
    """Initialize SQLite database for user authentication"""
    conn = get_db_connection()
    c = conn.cursor()

    # Check if users table exists
    c.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in c.fetchall()]

    if "first_name" not in columns:
        # Drop old table and recreate with new structure
        
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                
                )
        ''')

    conn.commit()
    conn.close()

# 2️⃣ CALL IT IMMEDIATELY
init_database()

def train_model():
    """Train and save the KNN model if not exists"""
    global model_data
    
    if os.path.exists(MODEL_PATH):
        return load_model()
    
    try:
        # Load dataset
        df = pd.read_csv(DATASET_PATH)
        
        # Create encoders
        le_subject = LabelEncoder()
        le_user_level = LabelEncoder()
        le_difficulty = LabelEncoder()
        le_topic = LabelEncoder()
        
        # Encode features
        df['subject_enc'] = le_subject.fit_transform(df['subject'])
        df['user_level_enc'] = le_user_level.fit_transform(df['user_level'])
        df['difficulty_enc'] = le_difficulty.fit_transform(df['difficulty'])
        df['topic_enc'] = le_topic.fit_transform(df['topic'])
        
        # Prepare features
        X = df[['subject_enc', 'user_level_enc', 'difficulty_enc', 'topic_enc']]
        X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)
        
        # Train KNN
        knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
        knn.fit(X_train)
        knn.fit(X)
        
        # Save model
        model_data = {
            'knn_model': knn,
            'dataset': df,
            'subject_encoder': le_subject,
            'user_level_encoder': le_user_level,
            'difficulty_encoder': le_difficulty,
            'topic_encoder': le_topic
        }
        
        with open(MODEL_PATH, 'wb') as file:
            pickle.dump(model_data, file)
        
        print(f"Model trained and saved to {MODEL_PATH}")
        return True
    except Exception as e:
        print(f"Error training model: {e}")
        return False


def load_model():
    """Load the KNN model and encoders from pickle file"""
    global model_data
    try:
        with open(MODEL_PATH, 'rb') as file:
            model_data = pickle.load(file)
        return True
    except FileNotFoundError:
        print(f"Model not found at: {MODEL_PATH}")
        return False
    except Exception as e:
        print(f"Error loading model: {e}")
        return False


def get_dropdown_data():
    """Get unique values for dropdown menus from dataset"""
    try:
        df = pd.read_csv(DATASET_PATH)
        subjects = sorted(df['subject'].unique().tolist())
        user_levels = sorted(df['user_level'].unique().tolist())
        difficulties = sorted(df['difficulty'].unique().tolist())
        topics = sorted(df['topic'].unique().tolist())
        return {
            'subjects': subjects,
            'user_levels': user_levels,
            'difficulties': difficulties,
            'topics': topics
        }
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return {
            'subjects': [],
            'user_levels': [],
            'difficulties': [],
            'topics': []
        }


def get_recommendations(subject, user_level, difficulty, topic):
    """Get study material recommendations using KNN model"""
    try:
        if model_data is None:
            return None, "Model not loaded"
        
        # Get encoders
        subject_encoder = model_data['subject_encoder']
        user_level_encoder = model_data['user_level_encoder']
        difficulty_encoder = model_data['difficulty_encoder']
        topic_encoder = model_data['topic_encoder']
        knn_model = model_data['knn_model']
        df = model_data['dataset']
        
        # Encode user inputs
        try:
            subject_enc = subject_encoder.transform([subject])[0]
            user_level_enc = user_level_encoder.transform([user_level])[0]
            difficulty_enc = difficulty_encoder.transform([difficulty])[0]
            topic_enc = topic_encoder.transform([topic])[0]
        except ValueError as e:
            return None, f"Invalid input values: {e}"
        
        # Create input array
        sample_input = np.array([[subject_enc, user_level_enc, difficulty_enc, topic_enc]])
        
        # Get recommendations
        distances, indices = knn_model.kneighbors(sample_input)
        
        # Get recommended materials
        recommendations = df.iloc[indices[0]][[
            'subject', 'user_level', 'difficulty', 'topic',
            'youtube_link', 'tutorial_site_link'
        ]].to_dict('records')
        
        return recommendations, None
    except Exception as e:
        return None, f"Error getting recommendations: {str(e)}"


# Initialize on startup
init_database()
train_model()


@app.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"].strip()

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        c = conn.cursor()

        try:
            c.execute("""
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (?, ?, ?, ?)
            """, (first_name, last_name, email, hashed_password))

            conn.commit()
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("Email already exists!", "error")
            return redirect(url_for("signup"))

        finally:
            conn.close()

    return render_template("signup.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"].strip()

        conn = get_db_connection()
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["first_name"] + " " + user["last_name"]
            return redirect(url_for("dashboard"))

        flash("Invalid email or password", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route('/logout')
def logout():
    """User logout"""
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """Main dashboard with recommendation form"""
    if 'user_id' not in session:
        flash('Please login to access dashboard', 'error')
        return redirect(url_for('login'))
    
    dropdown_data = get_dropdown_data()
    
    if request.method == 'POST':
        subject = request.form.get('subject')
        user_level = request.form.get('user_level')
        difficulty = request.form.get('difficulty')
        topic = request.form.get('topic')
        
        if not all([subject, user_level, difficulty, topic]):
            flash('Please fill in all fields', 'error')
            return render_template('dashboard.html', **dropdown_data, username=session['username'])
        
        recommendations, error = get_recommendations(subject, user_level, difficulty, topic)
        
        if error:
            flash(error, 'error')
            return render_template('dashboard.html', **dropdown_data, username=session['username'])
        
        return render_template('result.html', 
                             recommendations=recommendations,
                             username=session['username'],
                             search_params={'subject': subject, 'user_level': user_level, 
                                           'difficulty': difficulty, 'topic': topic})
    
    return render_template('dashboard.html', 
                         **dropdown_data, 
                         username=session['username'])


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""
        SELECT first_name, last_name, email, created_at
        FROM users
        WHERE id = ?
    """, (session["user_id"],))

    user = c.fetchone()
    conn.close()

    if user is None:
        return "User not found"

    # ✅ DEFINE VARIABLES HERE
    first_name = user["first_name"]
    last_name = user["last_name"]
    email = user["email"]
    created_at = user["created_at"]

    # ✅ THEN PASS THEM
    return render_template(
        "profile.html",
        first_name=first_name,
        last_name=last_name,
        email=email,
        created_at=created_at
    )


@app.route('/result')
def result():
    """Display recommendations result"""
    if 'user_id' not in session:
        flash('Please login to access', 'error')
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))


@app.errorhandler(404)
def not_found(e):
    """404 error page"""
    return render_template('index.html', error="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    """500 error page"""
    return render_template('index.html', error="Server error occurred"), 500


if __name__ == "__main__":
    app.run(debug=True)