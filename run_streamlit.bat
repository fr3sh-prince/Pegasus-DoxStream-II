@echo off
set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python39\python.exe
set STREAMLIT_PATH=%LOCALAPPDATA%\Programs\Python\Python39\Scripts\streamlit.exe

echo Installing Streamlit...
"%PYTHON_PATH%" -m pip install streamlit

echo Running Streamlit application...
"%STREAMLIT_PATH%" run app.py

pause 