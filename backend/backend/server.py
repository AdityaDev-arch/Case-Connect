'''from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/submitreport', methods=['GET','POST'])
def crime_report():
    name = request.form.get("name")
    place = request.form.get("place")
    category = request.form.get("category")
    description = request.form.get("description")
    
    # Handle file uploads
    evidence_files = request.files.getlist("evidence")
    
    # Save to database (pseudo-code)
    # db.insert_case(name, place, category, description, evidence_files)

    return jsonify({"status": "success", "message": "Report filed successfully"})

if __name__ == '__main__':
    app.run(debug=True) '''


from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="case_connect",
        user="postgres",
        password="nihar@123",
        host="localhost",  # Change this if using a remote database
        port="5432"
    )

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

        # Insert into database
        conn = get_db_connection()
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

if __name__ == '__main__':
    app.run(debug=True)
