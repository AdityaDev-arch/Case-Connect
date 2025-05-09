from django import db
from flask import Flask, request, jsonify, render_template, redirect, session, url_for, flash
import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin import firestore
import os
import psycopg2
import jwt
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

ADMIN_SIGNUP_SECRET_KEY="4d652b45aa45cd0870f52c02ca0b913560e9c89bd416f59c7403ec631d019406",
ADMIN_SIGNIN_SECRET_KEY="9e3e0edd71a0118c4209e27b2624ffcdd27e93688e64214bf5550e3631191fbc",
FIREBASE_API_KEY = "AIzaSyBGTHQb_4PTadKiHBsfh5PL9GyJ9MUprKU"

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app with custom templates and static folder paths
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '../templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '../static')
)
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")  # Use environment variable for security
CORS(app)
bcrypt = Bcrypt(app)

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\adity\Downloads\caseconnect-87388-firebase-adminsdk-fbsvc-aeff129314.json")
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret_key")  # Use environment variable for security
JWT_ALGORITHM = "HS256"

# Database configuration
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "case_connect"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "aditya@123"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

# Folder to store uploaded files
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to connect to the database
def connect_db():
    conn = psycopg2.connect(
        dbname='case_connect',
        user='postgres',
        password='aditya@123',
        host='localhost',
        port='5432'
    )
    return conn

# JWT Token Validation Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            request.user = decoded_token  # Attach user info to the request
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated

# Route for the home page
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Route for the widget page (latest crime)
@app.route('/latestcrime', methods=['GET'])
def latestcrime():
    return render_template('widget.html')

# Route for the table page
@app.route('/table', methods=['GET'])
def table():
    return render_template('table.html')

# Route for the "Report Crime" page (gotohome)
@app.route('/gotohome', methods=['GET'])
def gotohome():
    return render_template('form.html')  # Assuming "Report Crime" redirects to the form page

# Route for the "Criminal Details" page (gototable)
@app.route('/gototable', methods=['GET'])
def gototable():
    return render_template('table.html')  # Assuming "Criminal Details" redirects to the table page

@app.route('/criminal-list')
def criminal_list():
    return render_template('criminal_list.html')

@app.route('/api/criminals')
def get_criminals():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM criminals_display')
    criminals = [{'id': row[0], 'name': row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(criminals)

@app.route('/api/criminals/<int:criminal_id>')
def get_criminal_details(criminal_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT name, age, criminal_id, crime, in_custody, photo_url FROM criminals_display WHERE id = %s', (criminal_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return jsonify({
            'name': row[0],
            'age': row[1],
            'criminal_id': row[2],
            'crime': row[3],
            'in_custody': row[4],
            'photo_url': row[5]
        })
    else:
        return jsonify({'error': 'Criminal not found'}), 404

@app.route('/manage_criminals')
def manage_criminals():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, place, description, category FROM crime_reports")
    suspects = cursor.fetchall()
    conn.close()
    return render_template('manage_criminals.html', suspects=suspects)

@app.route('/add_criminal', methods=['GET', 'POST'])
def add_criminal():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        criminal_id = request.form['criminal_id']
        crime = request.form['crime']
        in_custody = request.form['in_custody'].lower() == 'true'

        # Handle uploaded photo
        photo = request.files['photo']
        photo_filename = secure_filename(photo.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo.save(photo_path)

        photo_url = photo_path  # Store path for display

        # Insert into criminals_display table
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO criminals_display (name, age, criminal_id, crime, in_custody, photo_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (name, age, criminal_id, crime, in_custody, photo_url))
        conn.commit()
        conn.close()

        return redirect(url_for('manage_criminals'))  # Redirect after success

    name = request.args.get('name', '')
    crime = request.args.get('category', '')
    return render_template('add_criminal.html', name=name, crime=crime)

@app.route('/api/verify-token/', methods=['POST'])
def verify_token():
    token = request.json.get('token')
    try:
        decoded_token = auth.verify_id_token(token)
        role = decoded_token.get('role', 'user')  # Retrieve role from custom claims
        return jsonify({"message": "Token verified", "role": role}), 200
    except Exception as e:
        return jsonify({"message": f"Error verifying token: {str(e)}"}), 401


def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Ensure the user is authenticated
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"message": "Token is missing"}), 401

            try:
                # Decode the JWT token
                decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                user_role = decoded_token.get('role', 'user')  # Default to 'user' if no role is found

                # Check if the user's role matches the required role
                if user_role != required_role:
                    return jsonify({"message": "Access denied: Insufficient permissions"}), 403

                # Attach user info to the request
                request.user = decoded_token
            except jwt.ExpiredSignatureError:
                return jsonify({"message": "Token has expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"message": "Invalid token"}), 401

            return f(*args, **kwargs)
        return decorated_function
    return decorator
    
@app.route('/admin-dashboard', methods=['GET'])
@role_required('admin')  # Only allow users with the 'admin' role
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/user-dashboard', methods=['GET'])
@role_required('user')  # Only allow users with the 'user' role
def user_dashboard():
    return render_template('user_dashboard.html')

# Route for the sign-up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    # Handle POST request for sign-up
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']  # Role can be 'normal' or 'admin'

    try:
        # Create a new user in Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password,
            display_name=username
        )

        # Assign a role to the user using custom claims
        auth.set_custom_user_claims(user.uid, {"role": role})

        flash(f"User created successfully with role '{role}'. Please sign in.", "success")
        return redirect(url_for('signin'))
    except Exception as e:
        # Flash an error message and reload the signup page
        flash(f"Error creating account: {str(e)}", "danger")
        return redirect(url_for('signup'))

# Route for the sign-in page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        input_admin_secret_key = request.form.get('admin_secret_key')

        try:
            user = auth.get_user_by_email(email)
            uid = user.uid
            user_doc = db.collection('users').document(uid).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                role = user_data.get('role', 'user')  # Default to 'user'

                # Admin trying to login must provide correct admin_secret_key
                if role == 'admin':
                    if input_admin_secret_key != ADMIN_SIGNIN_SECRET_KEY:
                        return 'Invalid admin secret key for sign in', 403

                # Verify password using Firebase REST (not Admin SDK)
                payload = {
                    "email": email,
                    "password": password,
                    "returnSecureToken": True
                }
                import requests
                url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
                r = requests.post(url, json=payload)
                if r.status_code != 200:
                    return 'Invalid credentials', 403

                # Login successful
                session['user_id'] = uid
                session['role'] = role

                if role == 'admin':
                    return redirect('/admin_dashboard')
                else:
                    return redirect('/home')

            return 'User data not found', 404
        except Exception as e:
            return f'Error: {str(e)}'

    return render_template('signin.html')

    
#Route to protect routes with authentication
@app.route('/protected-route', methods=['GET'])
@token_required
def protected_route():
    user = request.user  # Access user info from the decoded token
    return jsonify({"message": f"Welcome, {user['email']}!"})

# Route for the profile page (protected)
@app.route('/profile', methods=['GET'])
@token_required
def profile():
    user = request.user
    return render_template('profile.html', user=user)

# Route for the form page
@app.route('/form', methods=['GET'])
def form():
    return render_template('form.html')

# Route for the settings page
@app.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html')  # Ensure settings.html exists in the templates folder

# Route for logging out
@app.route('/logout', methods=['GET'])
def logout():
    # Clear session or perform logout logic here
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('signin'))  # Redirect to the sign-in page

import feedparser

@app.route('/fetch-rss', methods=['GET'])
def fetch_rss():
    # Google News RSS feed for crime news
    rss_url = "https://news.google.com/rss/search?q=crime"
    feed = feedparser.parse(rss_url)
    articles = []

    # Parse the RSS feed and extract relevant details
    for entry in feed.entries[:10]:  # Limit to 10 articles
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published if "published" in entry else "No Date",
        })

    return jsonify(articles)


@app.route('/submit-report', methods=['POST'])
def submit_report():
    try:
        name = request.form.get('name')
        place = request.form.get('place')
        category = request.form.get('category')
        description = request.form.get('description')

        # File handling (optional)
        if 'evidence' in request.files:
            evidence_files = request.files.getlist('evidence')
            evidence_paths = [file.filename for file in evidence_files]
        else:
            evidence_paths = None

        # Use correct DB connection function
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO crime_reports (name, place, category, description, evidence) VALUES (%s, %s, %s, %s, %s)",
            (name, place, category, description, str(evidence_paths))
        )
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "Report submitted successfully!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# Run the Flask app
if __name__ == "__main__":  # Fixed the issue here
    # Ensure the uploads folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)
