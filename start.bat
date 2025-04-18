@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing required packages...
python -m pip install --upgrade pip
pip install streamlit streamlit-option-menu streamlit-extras

echo Starting Streamlit application...
streamlit run app.py --server.port=8501 --server.address=localhost

pause 