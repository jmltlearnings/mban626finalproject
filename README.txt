================================================================
MBAN626 Dashboard Project — README & Deployment Guide
================================================================
Submitted by: TOMOL, Jairus Mark L. (MAN-2025190256)

================================================================

----------------------------------------------------------------
PROJECT FILES
----------------------------------------------------------------
  MBAN626_TOMOL_Dashboard.ipynb  — Main Jupyter Notebook
  app.py                           — Streamlit web app
  healthcare_dataset.csv           — Dataset (from Kaggle)
  requirements.txt                 — Python dependencies
  README.txt                       — This file

----------------------------------------------------------------
STEP 1 — Install dependencies (do this first, once)
----------------------------------------------------------------
  pip install -r requirements.txt


----------------------------------------------------------------
STEP 2 — Streamlit App
----------------------------------------------------------------
1. Open a terminal in the project folder.
2. Run:

     streamlit run app.py

3. The dashboard opens automatically at:
     http://localhost:8501

4. Features:
   - Sidebar filters (condition, admission type, insurance, year)
   - 6 interactive Plotly charts
   - Live KPI metric cards
   - Live API data from disease.sh
   - Condition summary table


----------------------------------------------------------------
DATASET
----------------------------------------------------------------
Source  : Kaggle — prasad22/healthcare-dataset
URL     : https://www.kaggle.com/datasets/prasad22/healthcare-dataset
File    : healthcare_dataset.csv
Records : ~55,000 synthetic patient records
Columns : Name, Age, Gender, Blood Type, Medical Condition,
          Date of Admission, Doctor, Hospital, Insurance Provider,
          Billing Amount, Room Number, Admission Type,
          Discharge Date, Medication, Test Results

----------------------------------------------------------------
API USED
----------------------------------------------------------------
Open Disease API  —  https://disease.sh
Endpoint          :  GET https://disease.sh/v3/covid-19/all
Auth              :  None (completely free, no API key needed)
Data returned     :  Global COVID-19 stats (cases, deaths,
                     recovered, active, critical)


----------------------------------------------------------------
DEPLOYMENT
----------------------------------------------------------------

Live Dashboard: https://mban626finalproject-tomol.streamlit.app/#hospital-analytics-dashboard

GitHub Repository: https://github.com/jmltlearnings/mban626finalproject