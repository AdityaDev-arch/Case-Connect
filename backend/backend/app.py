"""
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Database Configuration
DB_CONFIG = {
    "dbname": "case_connect",
    "user": "postgres",
    "password": "nihar@123",
    "host": "localhost",
    "port": "5432",  # Default PostgreSQL port
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

# Home Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to Case-Connect API!"})

# User Signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# User Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({"message": "Login successful!", "username": user["username"]}), 200
        else:
            return jsonify({"error": "Invalid credentials!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
"""
'''
---------------------------------------------------
from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows frontend to communicate with backend

# Step 3: Connect Flask to PostgreSQL
DB_CONFIG = {
    "dbname": "case_connect",
    "user": "postgres",   # Replace with your PostgreSQL username
    "password": "nihar@123",  # Replace with your PostgreSQL password
    "host": "localhost",
    "port": "5432"
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/submit-report", methods=["POST"])
def submit_report():
    try:
        conn = connect_db()  # Establish database connection
        cursor = conn.cursor()

        # Get form data from request
        data = request.json
        name = data.get("name")
        place = data.get("place")
        category = data.get("category")
        description = data.get("description")

        # Insert data into database
        cursor.execute("""
            INSERT INTO crime_reports (name, place, category, description) 
            VALUES (%s, %s, %s, %s)
        """, (name, place, category, description))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"status": "success", "message": "Crime report submitted successfully."})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
    --------------------------------------------------
'''
from flask import Flask, request, jsonify, render_template
import os
import psycopg2
from flask_cors import CORS


# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(__name__, template_folder=os.path.join(parent_dir, "templates"))
CORS(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home')
def gotohome():
    return render_template("home.html")


UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DB_CONFIG = {
    "dbname": "case_connect",
    "user": "postgres",
    "password": "nihar@123",
    "host": "localhost",
    "port": "5432"
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG) 




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

if __name__ == "__main__":
    app.run(debug=True)

