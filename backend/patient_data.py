import sqlite3
import datetime
import pandas as pd

# --- Doctor Recommendation Data ---
doctors_by_city = {
    "Lahore": {
        "Cardiology": "Dr. Usman Tariq - Punjab Institute of Cardiology",
        "Dermatology": "Dr. Sarah Malik - Cosmo Clinic",
        "Neurology": "Dr. Ahsan Raza - Hameed Latif Hospital",
        "General": "Dr. Huma Khan - Lahore General Hospital"
    },
    "Gujranwala": {
        "Cardiology": "Dr. Shabbir Ahmed - City Hospital",
        "Dermatology": "Dr. Neelam Bashir - Skin Clinic Gujranwala",
        "Neurology": "Dr. Haris Javed - DHQ Gujranwala",
        "General": "Dr. Faiza Anwar - Civil Hospital Gujranwala"
    },
    "Islamabad": {
        "Cardiology": "Dr. Imran Nisar - PIMS",
        "Dermatology": "Dr. Nadia Anwar - SkinTech Islamabad",
        "Neurology": "Dr. Talha Malik - Shifa International Hospital",
        "General": "Dr. Saima Zubair - Polyclinic Islamabad"
    },
    "Rawalpindi": {
        "Cardiology": "Dr. Rizwan Aziz - Rawalpindi Institute of Cardiology",
        "Dermatology": "Dr. Mahnoor Khan - Skin Wellness Center",
        "Neurology": "Dr. Muneeb Khan - Benazir Bhutto Hospital",
        "General": "Dr. Maria Qureshi - Holy Family Hospital"
    },
    "Karachi": {
        "Cardiology": "Dr. Sameer Ansari - NICVD",
        "Dermatology": "Dr. Hina Khan - Agha Khan Dermatology",
        "Neurology": "Dr. Sohail Yousuf - Liaquat National Hospital",
        "General": "Dr. Farah Hussain - Jinnah Hospital"
    }
}

# --- Disease to Specialist Mapping ---
specialist_map = {
    "heart attack": "Cardiology",
    "hypertension": "Cardiology",
    "skin infection": "Dermatology",
    "acne": "Dermatology",
    "migraine": "Neurology",
    "epilepsy": "Neurology",
    "flu": "General",
    "fever": "General",
    "cold": "General"
}

# --- Create Table with City ---
def initialize_db():
    conn = sqlite3.connect('D:/ML Projects/diseases_predictor/data/patient_history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gender TEXT,
            city TEXT,
            symptoms TEXT,
            predicted_disease TEXT,
            precautions TEXT,
            doctor TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- Store Patient History ---
def store_patient_history(name, gender, symptoms, predicted_disease, precautions, doctor, city):
    conn = sqlite3.connect('D:/ML Projects/diseases_predictor/data/patient_history.db')
    c = conn.cursor()
    c.execute('''INSERT INTO history (name, gender, city, symptoms, predicted_disease, precautions, doctor, date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (name, gender, city, ', '.join(symptoms), predicted_disease, ', '.join(precautions), doctor,
               datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

# --- Recommend Doctor Based on Disease and City ---
def recommend_doctor(disease_name, city):
    city = city.strip().title()
    specialist_area = specialist_map.get(disease_name.lower(), "General")
    city_doctors = doctors_by_city.get(city)

    if city_doctors:
        return city_doctors.get(specialist_area, "No specialist available in your city.")
    else:
        return f"No doctor found for {specialist_area} in {city}. Try selecting a nearby city."

# --- Retrieve Patient History (For Phase 6) ---
def get_patient_history():
    conn = sqlite3.connect('D:/ML Projects/diseases_predictor/data/patient_history.db')
    df = pd.read_sql_query("SELECT * FROM history ORDER BY date DESC", conn)
    conn.close()
    return df

# --- Initialize DB on import ---
initialize_db()
