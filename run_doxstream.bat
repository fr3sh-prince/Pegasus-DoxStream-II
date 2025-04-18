@echo off
echo Installing/Updating DoxStream dependencies...
python -m pip install -e .

echo.
echo Starting DoxStream...
echo.
set PYTHONPATH=%~dp0
streamlit run app.py

pause 