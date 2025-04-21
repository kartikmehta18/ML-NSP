from flask import Flask, request, render_template
import numpy as np
import pickle
import sqlite3
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Function to load models using pickle
def load_pickle_model(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

# Load models using pickle
model = load_pickle_model('models/Heart_model.pkl')
modeldia = load_pickle_model('models/Diabetic_model.pkl')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/heart')
def heart():
    return render_template('heart.html')

@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')

@app.route('/output')
def output():
    return render_template('output.html')

def get_db_connection():
    conn = sqlite3.connect('Database/HeartCare.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO submit_form (name, email, message) VALUES (?, ?, ?)', (name, email, message))
        conn.commit()
        conn.close()
        logging.info("Contact form submitted successfully.")
    except Exception as e:
        logging.error(f"Error submitting contact form: {e}")
    
    return render_template('home.html')

@app.route('/heart_predict', methods=['POST'])
def heart_predict():
    try:
        age = int(request.form['age'])
        sex = int(request.form['sex'])
        cp = int(request.form['cp'])
        trestbps = int(request.form['trestbps'])
        chol = int(request.form['chol'])
        fbs = int(request.form['fbs'])
        restecg = int(request.form['restecg'])
        thalach = int(request.form['thalach'])
        exang = int(request.form['exang'])
        oldpeak = float(request.form['oldpeak'])
        slope = int(request.form['slope'])
        ca = int(request.form['ca'])
        thal = int(request.form['thal'])
        
        features = [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]
        
        prediction = model.predict(features)[0]
        logging.info(f"Heart model prediction: {prediction}")

        out = 1 if prediction == 1 else 0

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO heart_disease_data (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, prediction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, out))
        conn.commit()
        conn.close()
        
        result = 'Unhealthy' if prediction == 1 else 'Healthy'
        logging.info(f"Heart prediction result: {result}")
        
        return render_template('output.html', output=result)
    except Exception as e:
        logging.error(f"Error during heart prediction: {e}")
        return render_template('output.html', output='Error occurred during prediction.')

@app.route('/diabetes_predict', methods=['POST'])
def diabetes_predict():
    try:
        pregnancies = int(request.form['pregnancies'])
        glucose = float(request.form['glucose'])
        blood_pressure = int(request.form['blood_pressure'])
        skin_thickness = float(request.form['skin_thickness'])
        insulin = float(request.form['insulin'])
        bmi = float(request.form['bmi'])
        pedigree_function = float(request.form['pedigree_function'])
        age = int(request.form['age'])

        featuresdia = [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, pedigree_function, age]]
        
        prediction = modeldia.predict(featuresdia)[0]

        out = 1 if prediction == 1 else 0

        logging.info(f"Diabetes model prediction: {prediction}")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO diabetes_data (Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Prediction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, pedigree_function, age, out))
        conn.commit()
        conn.close()
        
        result = 'Unhealthy' if prediction == 1 else 'Healthy'
        logging.info(f"Diabetes prediction result: {result}")
        
        return render_template('output.html', output=result)
    except Exception as e:
        logging.error(f"Error during diabetes prediction: {e}")
        return render_template('output.html', output='Error occurred during prediction.')

@app.route('/records')
def records():
    try:
        conn = get_db_connection()
        
        contact_records = conn.execute('SELECT * FROM submit_form').fetchall()
        heart_records = conn.execute('SELECT * FROM heart_disease_data').fetchall()
        diabetes_records = conn.execute('SELECT * FROM diabetes_data').fetchall()
        
        conn.close()
        
        return render_template('records.html', contact_records=contact_records, heart_records=heart_records, diabetes_records=diabetes_records)
    except Exception as e:
        logging.error(f"Error retrieving records: {e}")
        return render_template('records.html', contact_records=[], heart_records=[], diabetes_records=[])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

