🛡️ Pegasus-DoxStream - OSINT Investigation Tool
Pegasus-DoxStream is a powerful OSINT (Open Source Intelligence) investigation tool built with Streamlit. It combines various OSINT tools into a user-friendly interface for gathering information about individuals, domains, emails, and more.

🚀 Features
👤 Name Search (Sherlock + Social Analyzer)

📧 Email Search (Holehe + H8mail)

🔍 Username Search

🌐 IP Address Lookup

📁 File Metadata Analysis

🔍 Domain/Subdomain Search

🐦 Twitter Scraping

📍 GPS Location Tracking

🌍 Browser Session Tracking

🔄 Full OSINT Scan

📋 Requirements
Python 3.8+

pip (Python package manager)

Git

🛠️ Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/sobri3195/pegasus-doxstream.git
cd pegasus-doxstream
Create a virtual environment:

bash
Copy
Edit
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
🚀 Usage
Start the Streamlit app:

bash
Copy
Edit
streamlit run app.py
Open your browser and navigate to http://localhost:8501

Select a tool from the sidebar menu

Follow the instructions for each tool

🔧 Tools Integration
Name Search
Uses Sherlock for username search across platforms

Integrates Social Analyzer for comprehensive social media analysis

Generates possible email patterns

Web crawling with Photon

Email Search (Coming Soon)
Email registration check with Holehe

Data breach search with H8mail

Domain discovery with Email2Domain

Username Search (Coming Soon)
Cross-platform username search

Social media profile discovery

Activity analysis

IP Search (Coming Soon)
Geolocation with IPinfo.io/GeoIP2

Network analysis

WHOIS information

📁 Project Structure
bash
Copy
Edit
pegasus-doxstream/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Documentation
├── /tools/             # OSINT tools and modules
│   ├── __init__.py
│   ├── name_search.py
│   └── ...
├── /pages/             # Streamlit pages
│   ├── 1_Name_Search.py
│   └── ...
└── /results/           # Output directory
⚠️ Disclaimer
This tool is for educational purposes only. Use responsibly and respect privacy laws and regulations.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📧 Contact
Author: Letda Kes dr. Sobri, S.Kom.
GitHub: sobri3195
Email: muhammadsobrimaulana31@gmail.com

☕ Support / Donate
If you find this project useful, consider supporting me: Donate Here

