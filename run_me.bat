@echo off
echo --- Starting Property System Setup ---
pip install -r requirements.txt
echo --- Step 1: Fetching Data ---
python scraping.py
echo --- Step 2: Launching Dashboard ---
streamlit run app.py
pause