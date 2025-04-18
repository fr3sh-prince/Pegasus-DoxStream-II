import streamlit as st
import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.email_search import EmailSearch

st.set_page_config(
    page_title="Email Search - DoxStream",
    page_icon="📧",
    layout="wide"
)

st.title("📧 Email Search")
st.markdown("""
This tool performs comprehensive email analysis using multiple tools:
- Service Registration Check (Holehe)
- Data Breach Search (H8mail)
- Domain Email Search (Multiple Sources)
""")

# Initialize the email search tool
email_search = EmailSearch()

# Create the search form
with st.form("email_search_form"):
    email = st.text_input("Enter email to analyze:", placeholder="e.g. john.doe@example.com")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        check_services = st.checkbox("Check Services", value=True)
    with col2:
        check_breaches = st.checkbox("Check Breaches", value=True)
    with col3:
        check_domain = st.checkbox("Search Domain Emails", value=True)
        
    col4, col5 = st.columns(2)
    with col4:
        search_button = st.form_submit_button("🔍 Search")
    with col5:
        export_format = st.selectbox("Export format:", ["JSON", "TXT"])

if search_button and email:
    if '@' not in email:
        st.error("Please enter a valid email address")
    else:
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initialize results
        services_results = {"registered": [], "not_registered": [], "error": None}
        breaches_results = {"breaches": [], "error": None}
        domain_info_results = {"emails": [], "sources": [], "error": None}
        
        # Get domain from email
        domain = email.split('@')[1]
        
        # Check services
        if check_services:
            status_text.text("Checking service registrations...")
            services_results = asyncio.run(email_search.check_email_services(email))
            progress_bar.progress(33)
            
        # Check breaches
        if check_breaches:
            status_text.text("Searching for data breaches...")
            breaches_results = email_search.check_email_breaches(email)
            progress_bar.progress(66)
            
        # Search domain emails
        if check_domain:
            status_text.text("Searching for domain email addresses...")
            domain_info_results = email_search.search_domain_emails(domain)
            progress_bar.progress(100)
        
        # Clear status
        status_text.empty()
        progress_bar.empty()
        
        # Display results
        st.markdown("### Search Results")
        
        # Create tabs for different views
        results_tab, raw_tab = st.tabs(["Formatted Results", "Raw Data"])
        
        with results_tab:
            st.markdown(email_search.format_results(
                services_results,
                breaches_results,
                domain_info_results
            ))
            
        with raw_tab:
            st.json({
                "email": email,
                "services": services_results,
                "breaches": breaches_results,
                "domain_info": domain_info_results
            })
        
        # Export results
        if any([services_results["registered"], breaches_results["breaches"], domain_info_results["emails"]]):
            st.markdown("### Export Results")
            
            if export_format == "JSON":
                filename = email_search.save_results(
                    email,
                    services_results,
                    breaches_results,
                    domain_info_results
                )
                with open(filename, 'r') as f:
                    st.download_button(
                        label="📥 Download JSON",
                        data=f.read(),
                        file_name=f"email_search_{email}_results.json",
                        mime="application/json"
                    )
            else:
                formatted_text = email_search.format_results(
                    services_results,
                    breaches_results,
                    domain_info_results
                )
                st.download_button(
                    label="📥 Download TXT",
                    data=formatted_text,
                    file_name=f"email_search_{email}_results.txt",
                    mime="text/plain"
                )

# Footer
st.markdown("---")
st.markdown("Letda Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE © 2025") 