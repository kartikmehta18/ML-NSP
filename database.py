import sqlite3

database_name = 'HeartCare.db'
conn = sqlite3.connect(database_name)

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE submit_form (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    message TEXT NOT NULL)
''')

cursor.execute('''
CREATE TABLE heart_disease_data (
    age INTEGER,
    sex TEXT,
    cp INTEGER,
    trestbps INTEGER,
    chol INTEGER,
    fbs INTEGER,
    restecg INTEGER,
    thalach INTEGER,
    exang INTEGER,
    oldpeak REAL,
    slope INTEGER,
    ca INTEGER,
    thal TEXT,
    prediction INTEGER
);
''')

cursor.execute('''
CREATE TABLE diabetes_data (
    Pregnancies INTEGER,
    Glucose INTEGER,
    BloodPressure INTEGER,
    SkinThickness INTEGER,
    Insulin INTEGER,
    BMI REAL,
    DiabetesPedigreeFunction REAL,
    Age INTEGER,
    Prediction INTEGER
);
''')

conn.commit()
conn.close()