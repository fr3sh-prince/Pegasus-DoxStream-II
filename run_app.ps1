# Get the current directory
$currentDir = Get-Location

# Activate virtual environment
Write-Host "Activating virtual environment..."
& "$currentDir\.venv\Scripts\Activate.ps1"

# Install required packages
Write-Host "Installing required packages..."
pip install streamlit streamlit-option-menu streamlit-extras

# Run the Streamlit application
Write-Host "Starting Streamlit application..."
streamlit run "$currentDir\app.py" 