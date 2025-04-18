import streamlit as st
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.domain_search import DomainSearch

st.set_page_config(
    page_title="Domain Search - DoxStream",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Domain Search & Analysis")
st.markdown("""
This tool performs comprehensive domain analysis:
- WHOIS information
- DNS records
- Subdomain enumeration
- Technology stack detection
""")

# Initialize the domain search tool
domain_search = DomainSearch()

# Domain validation function
def is_valid_domain(domain: str) -> bool:
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))

# Create the search form
with st.form("domain_search_form"):
    domain = st.text_input("Enter domain to analyze:", placeholder="e.g. example.com")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        check_whois = st.checkbox("WHOIS Lookup", value=True)
    with col2:
        check_subdomains = st.checkbox("Find Subdomains", value=True)
    with col3:
        check_tech = st.checkbox("Detect Technologies", value=True)
        
    col4, col5 = st.columns(2)
    with col4:
        search_button = st.form_submit_button("🔍 Analyze")
    with col5:
        export_format = st.selectbox("Export format:", ["JSON", "TXT"])

if search_button:
    if not domain:
        st.error("Please enter a domain")
    elif not is_valid_domain(domain):
        st.error("Please enter a valid domain name")
    else:
        with st.spinner(f"Analyzing domain {domain}..."):
            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Analyze domain
            results = domain_search.analyze_domain(domain)
            
            # Update progress
            progress_bar.progress(100)
            status_text.empty()
            
            # Display results in columns
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Create tabs for different views
                results_tab, raw_tab = st.tabs(["Formatted Results", "Raw Data"])
                
                with results_tab:
                    st.markdown(domain_search.format_results(results))
                    
                with raw_tab:
                    st.json(results)
                    
            with col2:
                # Display summary statistics
                st.markdown("### 📊 Analysis Summary")
                
                metrics = {
                    "DNS Records": len(results["dns"].get("records", {})),
                    "Subdomains": len(results["subdomains"].get("subdomains", [])),
                    "Technologies": len(results["technologies"].get("technologies", []))
                }
                
                for label, value in metrics.items():
                    st.metric(label, value)
            
            # Export results
            st.markdown("### Export Results")
            
            if export_format == "JSON":
                filename = domain_search.save_results(domain, results)
                with open(filename, 'r') as f:
                    st.download_button(
                        label="📥 Download JSON",
                        data=f.read(),
                        file_name=f"domain_search_{domain}_results.json",
                        mime="application/json"
                    )
            else:
                formatted_text = domain_search.format_results(results)
                st.download_button(
                    label="📥 Download TXT",
                    data=formatted_text,
                    file_name=f"domain_search_{domain}_results.txt",
                    mime="text/plain"
                )

# Footer
st.markdown("---")
st.markdown("Letda Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE © 2025") 