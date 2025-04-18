@echo off
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing required packages...
pip install --no-cache-dir streamlit streamlit-option-menu streamlit-extras

echo Starting Streamlit application...
python -m streamlit run app.py

pause 