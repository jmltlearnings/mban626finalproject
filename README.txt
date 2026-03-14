================================================================
MBAN626 Dashboard Project — README & Deployment Guide
================================================================
Course  : AI and Data Analytics Strategy
Lecturer: Ramachandra C. Torres
Term    : 2T 2025-2026
================================================================

----------------------------------------------------------------
PROJECT FILES
----------------------------------------------------------------
  MBAN626_Dashboard_Project.ipynb  — Main Jupyter Notebook
  app.py                           — Streamlit web app
  healthcare_dataset.csv           — Dataset (from Kaggle)
  requirements.txt                 — Python dependencies
  README.txt                       — This file

----------------------------------------------------------------
STEP 0 — Install dependencies (do this first, once)
----------------------------------------------------------------
  pip install -r requirements.txt

----------------------------------------------------------------
OPTION A — HTML Export from Jupyter Notebook (Simplest)
----------------------------------------------------------------
1. Open a terminal in the project folder.
2. Run:

     jupyter nbconvert --to html --execute MBAN626_Dashboard_Project.ipynb

3. This creates:  MBAN626_Dashboard_Project.html
4. Open the HTML file in any browser — no server needed.
5. Submit this HTML file to Canvas.

NOTE: The --execute flag runs all cells automatically before
      exporting, so you get a fully rendered output.

----------------------------------------------------------------
OPTION B — Voila Dashboard (Notebook-based, no extra code)
----------------------------------------------------------------
1. Open a terminal in the project folder.
2. Run:

     voila MBAN626_Dashboard_Project.ipynb

3. Voila will open automatically in your browser at:
     http://localhost:8866

4. The notebook runs and displays as a clean dashboard
   (no code cells visible — output only).

5. To take screenshots for Canvas submission:
   - Use your browser's screenshot tool or press PrtScn.

TIP: If Voila is not recognized, install it with:
     pip install voila

----------------------------------------------------------------
OPTION C — Streamlit App (Most Interactive)
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

5. To deploy online FREE (Streamlit Cloud):
   a. Push your project folder to a GitHub repository.
   b. Go to https://streamlit.io/cloud and sign in with GitHub.
   c. Click "New app" → select your repo → set main file to app.py
   d. Click Deploy. You get a public shareable URL.
   e. Submit this URL to Canvas under "Web App Link".

----------------------------------------------------------------
DATASET
----------------------------------------------------------------
Source  : Kaggle — prasad22/healthcare-dataset
URL     : https://www.kaggle.com/datasets/prasad22/healthcare-dataset
File    : healthcare_dataset.csv
Records : ~10,000 synthetic patient records
Columns : Name, Age, Gender, Blood Type, Medical Condition,
          Date of Admission, Doctor, Hospital, Insurance Provider,
          Billing Amount, Room Number, Admission Type,
          Discharge Date, Medication, Test Results

IMPORTANT: Place healthcare_dataset.csv in the SAME folder
as both the .ipynb and app.py files before running.

----------------------------------------------------------------
API USED
----------------------------------------------------------------
Open Disease API  —  https://disease.sh
Endpoint          :  GET https://disease.sh/v3/covid-19/all
Auth              :  None (completely free, no API key needed)
Data returned     :  Global COVID-19 stats (cases, deaths,
                     recovered, active, critical)

----------------------------------------------------------------
SUBMISSION CHECKLIST (Canvas — zipped folder)
----------------------------------------------------------------
  [x] MBAN626_Dashboard_Project.ipynb
  [x] MBAN626_Dashboard_Project.html  (from Option A)
  [x] app.py  (Streamlit — for Option C)
  [x] healthcare_dataset.csv
  [x] requirements.txt
  [x] Short_Report.pdf
  [x] README.txt  (this file)

================================================================
