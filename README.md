# MediVision AI - Disease Predictor 🤖🩺

MediVision AI is a machine learning-powered disease prediction web app built with **Streamlit**. It uses user-reported symptoms to predict possible diseases, recommend precautions, and suggest doctors based on the user's city.

---

## 🔍 Features

- ✅ Symptom-based disease prediction
- ✅ Confidence score of prediction
- ✅ Suggested precautions for the disease
- ✅ Doctor recommendation by specialty & city
- ✅ Patient history stored in SQLite
- ✅ Downloadable health report (PDF)

---

## 🏗️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, SQLite
- **ML Models**: Trained with scikit-learn
- **PDF Generator**: FPDF
- **Libraries**: Pandas, NumPy, Joblib, scikit-learn

---

## 📁 Folder Structure

MediVision-AI-Disease-Predictor/
├── app/ → Streamlit UI
├── backend/ → Database and doctor logic
├── data/ → CSV data files (symptoms, precautions)
├── models/ → Trained ML models (.pkl)
├── notebook/ → Jupyter notebooks for model training
├── visualizations/ → Graphs, charts
├── main.py → Streamlit main app
├── README.md → Project overview
└── requirements.txt → Required Python libraries


---

## 📦 Installation Guide

```bash
# 1. Clone the repo
git clone https://github.com/MAhsaanUllah/MediVision-AI-Disease-Predictor.git
cd MediVision-AI-Disease-Predictor

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Run the app
streamlit run main.py


🧠 Model Training
The model was trained on a symptoms-diseases dataset with multi-label classification using scikit-learn.

📄 License
This project is for educational purposes and not intended for medical diagnosis.