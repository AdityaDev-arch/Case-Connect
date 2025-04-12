from flask import Flask, redirect, request, jsonify, render_template, session, url_for, flash
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
import os
import psycopg2
from flask_cors import CORS
import requests

# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Initialize Flask app
app = Flask(
    __name__,
    template_folder=os.path.join(parent_dir, "templates"),
    static_folder=os.path.join(parent_dir, "static")  # Explicitly set the static folder
)
app.secret_key = "your_secret_key"  # Replace with a secure secret key
CORS(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"  # Redirect to this route if login is required
login_manager.login_message = "Please log in to access this page."

# Database configuration
DB_CONFIG = {
    "dbname": "case_connect",
    "user": "postgres",
    "password": "nihar@123",
    "host": "localhost",
    "port": "5432"
}

# Folder to store uploaded files
UPLOAD_FOLDER = os.path.join(parent_dir, 'uploads')  # Ensure uploads folder is in the correct location
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to connect to the database
def connect_db():
    return psycopg2.connect(**DB_CONFIG)

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()

    if user_data:
        return User(id=user_data[0], username=user_data[1], email=user_data[2])
    return None

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for the latest crime page
@app.route('/widget')
def latestcrime():
    return render_template("widget.html")

# Route for another page (example)
@app.route('/form')
def gotohome():
    return render_template("form.html")

# Route for the table page
@app.route('/table')
def gototable():
    return render_template("table.html")

# Route to login page when clicked on logout option
@app.route('/logout')
def logout():
    logout_user()  # Logs out the current user
    session.clear()  # Clear the user's session
    flash('You have been logged out.', 'success')
    return redirect(url_for('signin'))  # Redirect to the sign-in page

# Route for profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# Route for settings
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Update user details
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        update_user_details(current_user.id, username, email, password)
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('settings'))
    return render_template('settings.html', user=current_user)

# Route for fetching news
@app.route('/fetch-rss', methods=['GET'])
def fetch_rss():
    # RSS feed URL
    rss_url = "https://news.google.com/rss/search?q=crime+India&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        # Fetch the RSS feed
        response = requests.get(rss_url, headers={"Cache-Control": "no-cache"})
        response.raise_for_status()  # Raise an error for bad responses
        return response.content, response.status_code, {'Content-Type': 'application/xml'}
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch RSS feed: {str(e)}"}), 500

# Route for sign-in
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate user credentials
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM users WHERE username = %s AND password = %s", (username, password))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data:
            user = User(id=user_data[0], username=user_data[1], email=user_data[2])
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('signin.html')

# Route for sign-up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle sign-up form submission
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  # Capture the role from the form

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Insert the new user into the database with the role
            cursor.execute("""
                INSERT INTO users (username, email, password, role)
                VALUES (%s, %s, %s, %s)
            """, (username, email, password, role))

            conn.commit()
            cursor.close()
            conn.close()

            flash('Account created successfully! Please sign in.', 'success')
            return redirect(url_for('signin'))
        except Exception as e:
            flash(f'Error creating account: {str(e)}', 'danger')

    return render_template('signup.html')

# Function to update user details in the database
def update_user_details(user_id, username, email, password):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Update user details in the database
        cursor.execute("""
            UPDATE users
            SET username = %s, email = %s, password = %s
            WHERE id = %s
        """, (username, email, password, user_id))

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error updating user details: {e}")
        raise

# Route to handle crime report submission
@app.route("/submit-report", methods=["POST"])
def submit_report():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Get form data
        name = request.form.get("name")
        place = request.form.get("place")
        category = request.form.get("category")
        description = request.form.get("description")

        # Handle file uploads
        files = request.files.getlist("evidence")  # Ensure input name matches frontend
        saved_files = []

        for file in files:
            if file.filename:
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(file_path)
                saved_files.append(file.filename)  # Store only the file name in DB

        # Convert list of file names to a comma-separated string
        evidence = ",".join(saved_files)

        # Insert data into database
        cursor.execute("""
            INSERT INTO crime_reports (name, place, category, description, evidence)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, place, category, description, evidence))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Crime report submitted successfully.",
            "uploaded_files": saved_files
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    # Ensure the uploads folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)