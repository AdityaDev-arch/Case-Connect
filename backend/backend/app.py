from flask import Flask, request, jsonify, render_template, url_for
import os
import psycopg2
from flask_cors import CORS

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

#route for latest crime page
@app.route('/widget')
def latestcrime():
    return render_template("widget.html")



# Route for another page (example)
@app.route('/form')
def gotohome():
    return render_template("form.html")

#route for table page
@app.route('/table')
def gototable():
    return render_template("table.html")


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