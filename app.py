import streamlit as st
from streamlit_option_menu import option_menu
import os
import json
import sys
from datetime import datetime
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

# Initialize required directories
def init_directories():
    """Initialize required directories for the application"""
    directories = ['results', 'tools', 'pages']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    return True

# Initialize application state
def init_app_state():
    """Initialize application state and configurations"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
        st.session_state.theme = "dark"
        st.session_state.current_tool = None
    return True

# Set page configuration
def set_page_config():
    """Configure Streamlit page settings"""
    try:
        st.set_page_config(
            page_title="DoxStream - OSINT Tool",
            page_icon="🔍",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        return True
    except Exception as e:
        st.error(f"Error configuring page: {str(e)}")
        return False

# Apply custom styling
def apply_custom_css():
    """Apply custom CSS styling"""
    st.markdown("""
    <style>
        .main {
            background-color: #0E1117;
            color: white;
        }
        .stButton button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #262730;
            border: 1px solid #4B4B4B;
        }
        .sidebar .sidebar-content {
            background-color: #262730;
        }
        .stProgress > div > div {
            background-color: #4CAF50;
        }
        .stAlert {
            background-color: #262730;
            color: white;
            border: 1px solid #4B4B4B;
        }
    </style>
    """, unsafe_allow_html=True)

def save_results(data, format="json"):
    """Save results to file in specified format"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = "results"
        
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
            
        if format == "json":
            filename = f"{results_dir}/result_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        else:
            filename = f"{results_dir}/result_{timestamp}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(data))
                
        return filename
    except Exception as e:
        st.error(f"Error saving results: {str(e)}")
        return None

def main():
    """Main application function"""
    try:
        # Initialize application
        if not init_directories():
            st.error("Failed to initialize directories")
            return
        
        if not init_app_state():
            st.error("Failed to initialize application state")
            return
            
        if not set_page_config():
            return
            
        apply_custom_css()

        # Sidebar
        with st.sidebar:
            st.title("🔍 DoxStream")
            st.markdown("### OSINT & Information Gathering Tool")
            
            # Theme toggle
            theme = st.selectbox(
                "🎨 Theme",
                ["Light", "Dark"],
                key="theme_selector"
            )
            
            if theme == "Dark":
                st.markdown("""
                    <style>
                        .stApp {
                            background-color: #0E1117;
                            color: #FAFAFA;
                        }
                    </style>
                    """, unsafe_allow_html=True)
                
            # Navigation menu
            selected = option_menu(
                "Main Menu",
                ["Name Search", "Email Search", "Username Search", "IP Search",
                 "File Analysis", "Domain Search", "Twitter Scraper",
                 "GPS Tracker", "Browser Tracker", "Full OSINT"],
                icons=["search", "envelope", "person", "globe",
                      "file-earmark", "diagram-3", "twitter",
                      "geo-alt", "browser", "tools"],
                menu_icon="cast",
                default_index=0,
            )
            
            # Footer
            st.markdown("---")
            st.markdown("### 📚 Resources")
            st.markdown("""
            * [Documentation](https://github.com/sobri3195/doxstream)
            * [Report Issues](https://github.com/sobri3195/doxstream/issues)
            * [Privacy Policy](https://github.com/sobri3195/doxstream/privacy)
            """)
            
        # Main content
        if selected == "Name Search":
            st.title("🔍 Name Search")
            st.markdown("""
            Search for information about a person using their name. This tool will:
            * Search social media profiles using Sherlock
            * Generate possible email addresses
            * Search for web presence and mentions
            * Find social media activity
            
            Enter a name below to begin your search.
            """)
            
        elif selected == "Email Search":
            st.title("📧 Email Search")
            st.markdown("""
            Search for information related to an email address. This tool will:
            * Check email registration across platforms using Holehe
            * Search for data breaches using H8mail
            * Find associated domains and websites
            * Discover linked social media accounts
            
            Enter an email address to begin your search.
            """)
            
        elif selected == "Username Search":
            st.title("👤 Username Search")
            st.markdown("""
            Search for a username across multiple platforms. This tool will:
            * Find social media profiles
            * Check gaming platforms
            * Search developer communities
            * Identify forum participation
            
            Enter a username to begin your search.
            """)
            
        elif selected == "IP Search":
            st.title("🌐 IP Search")
            st.markdown("""
            Analyze an IP address for detailed information. This tool will:
            * Determine geolocation using IPinfo.io/GeoIP2
            * Check for open ports and services
            * Identify hosting provider and network info
            * Search for associated domains
            
            Enter an IP address to begin your analysis.
            """)
            
        elif selected == "File Analysis":
            st.title("📁 File Analysis")
            st.markdown("""
            Extract and analyze metadata from files. This tool will:
            * Extract EXIF data from images
            * Analyze document metadata
            * Check file signatures and types
            * Identify creation and modification dates
            
            Upload a file to begin analysis.
            """)
            
        elif selected == "Domain Search":
            st.title("🔍 Domain Search")
            st.markdown("""
            Gather information about a domain name. This tool will:
            * Enumerate subdomains using Sublist3r
            * Check WHOIS information
            * Analyze DNS records
            * Identify web technologies with WhatWeb
            * Search for associated email addresses
            
            Enter a domain name to begin your search.
            """)
            
        elif selected == "Twitter Scraper":
            st.title("🐦 Twitter Scraper")
            st.markdown("""
            Collect and analyze Twitter data. This tool will:
            * Search tweets by username or keyword
            * Analyze user profiles and connections
            * Track hashtag usage
            * Generate engagement statistics
            
            Enter a Twitter username or search term to begin.
            """)
            
        elif selected == "GPS Tracker":
            st.title("📍 GPS Tracker")
            st.markdown("""
            **Manual Setup Required**
            
            Create and track GPS location links. This tool requires:
            1. Install and configure Seeker:
               * Clone the Seeker repository
               * Install dependencies
               * Configure tracking parameters
            
            2. Set up ngrok for tunneling:
               * Create ngrok account
               * Configure authentication token
               * Set up secure tunnel
            
            3. Follow the setup guide:
               * Configure port forwarding
               * Set up templates
               * Test tracking functionality
            
            ⚠️ Note: This tool is for educational purposes only. Always obtain proper consent before tracking.
            """)
            
        elif selected == "Browser Tracker":
            st.title("🌐 Browser Session Tracker")
            st.markdown("""
            **Manual Setup Required**
            
            Track and analyze browser sessions. This tool requires:
            1. Install and configure Trape:
               * Clone the Trape repository
               * Install required dependencies
               * Set up tracking modules
            
            2. Set up your tracking parameters:
               * Configure tracking hooks
               * Set up data collection rules
               * Define tracking duration
            
            3. Follow the setup guide:
               * Set up secure endpoints
               * Configure data storage
               * Test tracking capabilities
            
            ⚠️ Note: This tool is for educational purposes only. Always obtain proper consent before tracking.
            """)
            
        elif selected == "Full OSINT Scan":
            st.title("🔍 Full OSINT Scan")
            st.markdown("""
            Perform a comprehensive OSINT investigation. This tool will:
            * Run all available OSINT modules
            * Generate detailed reports
            * Cross-reference findings
            * Identify connections between data points
            
            Features include:
            * Email discovery and verification
            * Social media presence analysis
            * Domain and subdomain enumeration
            * Data breach checks
            * Web technology analysis
            * Digital footprint mapping
            
            Enter a target identifier (name, email, domain, etc.) to begin the full scan.
            
            ⚠️ Note: Full scans may take several minutes to complete.
            """)
            
        # Display warning
        st.sidebar.markdown("---")
        st.sidebar.warning("""
        ⚠️ **Disclaimer**: This tool is for educational purposes only.
        Use responsibly and respect privacy laws.
        """)

    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.error("Please check the console for more details")
        raise e

if __name__ == "__main__":
    main() 