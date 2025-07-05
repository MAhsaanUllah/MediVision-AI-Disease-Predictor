import streamlit as st
import pandas as pd
import joblib
import numpy as np
from fpdf import FPDF
import tempfile
import base64
from datetime import datetime
import os
import sys

# ------------------ Streamlit Page Config ------------------
st.set_page_config(page_title="MediVision AI", layout="wide")

# ------------------ Import for Local Modules ------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.patient_data import store_patient_history, recommend_doctor

# ------------------ Load Models and Data ------------------
model = joblib.load('models/disease_model.pkl')
encoder = joblib.load('models/symptom_encoder.pkl')
precautions_df = pd.read_csv('data/symptom_precaution.csv')
disease_data = pd.read_csv('data/dataset.csv')
all_symptoms = encoder.classes_

# ------------------ Custom CSS Styling ------------------
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .stButton>button {
        background-color: #0047AB;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        border: none;
        padding: 0.6em 1.2em;
    }
    .stButton>button:hover {
        background-color: #6495ED;
    }
    .stDownloadButton>button {
        background-color: #009688;
        color: white;
        border-radius: 5px;
        font-weight: bold;
    }
    .stDownloadButton>button:hover {
        background-color: #00796B;
    }
    .download-button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 15px;
        font-weight: bold;
        color: white;
        background-color: #0047AB;
        border-radius: 8px;
        text-decoration: none;
    }
    .download-button:hover {
        background-color: #6495ED;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ PDF Generator ------------------
def generate_pdf(name, age, gender, city, disease, confidence, symptoms, precautions, doctor):
    pdf = FPDF()
    pdf.add_page()

    logo_path = "app/logo.png"
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=80, y=10, w=50)
    pdf.ln(50)

    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, txt="MediVision AI - Health Report", ln=True, align='C')

    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, txt=f"Date: {datetime.today().strftime('%d %B, %Y')}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, txt=f"Patient Name: {name}", ln=True)
    pdf.cell(0, 10, txt=f"Age: {age}", ln=True)
    pdf.cell(0, 10, txt=f"Gender: {gender}", ln=True)
    pdf.cell(0, 10, txt=f"City: {city}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, txt=f"Predicted Disease: {disease}", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 10, txt=f"Confidence: {confidence:.2f}%", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Symptoms:", ln=True)
    pdf.set_font("Arial", '', 11)
    for s in symptoms:
        pdf.cell(0, 8, txt=f"- {s}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Precautions:", ln=True)
    pdf.set_font("Arial", '', 11)
    for p in precautions:
        pdf.cell(0, 8, txt=f"- {p}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Recommended Doctor:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 8, doctor)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        pdf.output(tmpfile.name)
        with open(tmpfile.name, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        return f"""
        <a href="data:application/octet-stream;base64,{base64_pdf}" 
           download="MediVision_Report.pdf" 
           class="download-button">
           📥 Download Health Report
        </a>
        """

# ------------------ App Layout ------------------
st.markdown("<h1 style='color:#0047AB'>🤖 MediVision AI - Disease Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#555;'>Select symptoms to get an AI-powered disease prediction, treatment advice, and doctor recommendation.</p>", unsafe_allow_html=True)

# Sidebar: Top 10 Common Diseases
with st.sidebar:
    st.markdown("### 📊 Top 10 Common Diseases")
    top_diseases = disease_data['Disease'].value_counts().head(10)
    st.bar_chart(top_diseases)

# --- Patient Details ---
st.markdown("### 🧾 Patient Details")
col1, col2 = st.columns(2)
with col1:
    patient_name = st.text_input("👤 Name")
    age = st.number_input("🎂 Age", min_value=1, max_value=120, value=25)
with col2:
    gender = st.radio("⚧️ Gender", ['Male', 'Female', 'Other'])
    city = st.selectbox("📍 City", ['Lahore', 'Gujranwala', 'Islamabad', 'Rawalpindi', 'Karachi', 'Other'])

# --- Symptom Selection ---
st.markdown("### 🤒 Select Symptoms")
selected_symptoms = st.multiselect("Click to select symptoms", sorted(all_symptoms))

# --- Predict Button ---
if st.button("🔍 Predict Disease"):
    if not patient_name or not selected_symptoms:
        st.warning("Please enter your name and select symptoms.")
    else:
        input_vector = encoder.transform([selected_symptoms])
        prediction = model.predict(input_vector)
        predicted_disease = prediction[0]
        confidence_score = model.predict_proba(input_vector).max() * 100

        st.success(f"✅ **{predicted_disease}** detected with **{confidence_score:.2f}%** confidence.")

        # Precautions
        def get_precautions(disease_name):
            row = precautions_df[precautions_df['Disease'].str.lower() == disease_name.lower()]
            return [row[f'Precaution_{i}'].values[0] for i in range(1, 5)] if not row.empty else []

        precautions = get_precautions(predicted_disease)

        st.markdown("### 🛡️ Recommended Precautions:")
        for i, p in enumerate(precautions, 1):
            st.write(f"{i}. {p}")

        # Doctor Recommendation
        doctor = recommend_doctor(predicted_disease, city)
        st.markdown("### 👨‍⚕️ Recommended Doctor:")
        st.info(doctor)

        # Store Patient History
        store_patient_history(patient_name, gender, selected_symptoms, predicted_disease, precautions, doctor, city)

        # PDF Download
        st.markdown("---")
        st.markdown("### 📄 Download Full Report:")
        pdf_button = generate_pdf(patient_name, age, gender, city, predicted_disease, confidence_score, selected_symptoms, precautions, doctor)
        st.markdown(pdf_button, unsafe_allow_html=True)

