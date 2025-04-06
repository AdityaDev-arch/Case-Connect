from flask import Flask, redirect, request, jsonify, render_template, session, url_for, flash
from flask_login import login_required
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
CORS(app)

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
    session.clear()  # Clear the user's session
    return redirect(url_for('signin'))  # Redirect to the sign-in page

# Route for profile
@app.route('/profile')
@login_required
def profile():
    user = session.get('user')  # Fetch the logged-in user's details from the session
    return render_template('profile.html', user=user)

# Route for settings
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user = session.get('user')  # Fetch the logged-in user's details from the session
    if request.method == 'POST':
        # Update user details
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        update_user_details(user['id'], username, email, password)
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('settings'))
    return render_template('settings.html', user=user)

# Route for fetching news
@app.route('/fetch-rss', methods=['GET'])
def fetch_rss():
    # RSS feed URL
    rss_url = "https://news.google.com/rss/search?q=crime+India&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        # Fetch the RSS feed
        response = requests.get(rss_url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.content, response.status_code, {'Content-Type': 'application/xml'}
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Folder to store uploaded files
UPLOAD_FOLDER = os.path.join(parent_dir, 'uploads')  # Ensure uploads folder is in the correct location
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database configuration
DB_CONFIG = {
    "dbname": "case_connect",
    "user": "postgres",
    "password": "nihar@123",
    "host": "localhost",
    "port": "5432"
}

# Function to connect to the database
def connect_db():
    return psycopg2.connect(**DB_CONFIG)

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