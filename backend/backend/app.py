from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import firebase_admin
from firebase_admin import auth, credentials
import os
import psycopg2
import jwt
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask_cors import CORS
from dotenv import load_dotenv

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

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret_key")  # Use environment variable for security
JWT_ALGORITHM = "HS256"

# Database configuration
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "case_connect"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "nihar@123"),
    "host": os.getenv("DB_HOST", "152.58.30.93"),
    "port": os.getenv("DB_PORT", "5432")
}

# Folder to store uploaded files
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to connect to the database
def connect_db():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

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
    if request.method == 'GET':
        return render_template('signin.html')

    # Handle POST request for sign-in
    email = request.form['email']
    password = request.form['password']

    try:
        # Verify the user's email and password using Firebase Authentication
        user = auth.get_user_by_email(email)

        # Firebase does not directly verify passwords; this is handled on the client side.

        # Retrieve custom claims (role) from the user's token
        custom_claims = user.custom_claims
        role = custom_claims.get('role', 'user') if custom_claims else 'user'

        # Generate a JWT for the user
        token = jwt.encode({
            "uid": user.uid,
            "email": user.email,
            "role": role,
            "exp": datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
        }, JWT_SECRET, algorithm=JWT_ALGORITHM)

                # Store the token in the session or redirect to the index page
        flash("Sign-in successful!", "success")
        return redirect(url_for('home'))  # Redirect to the home page (index.html)
    except firebase_admin.auth.UserNotFoundError:
        flash("Invalid email or password", "danger")
        return redirect(url_for('signin'))
    except Exception as e:
        flash(f"Error during sign-in: {str(e)}", "danger")
        return redirect(url_for('signin'))
    
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

# Run the Flask app
if __name__ == "__main__":
    # Ensure the uploads folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)