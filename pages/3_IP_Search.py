import streamlit as st
import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.ip_search import IPSearch
import streamlit.components.v1 as components

st.set_page_config(
    page_title="IP Search - DoxStream",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 IP Address Search")
st.markdown("""
This tool performs comprehensive IP address analysis:
- Geolocation with map visualization
- Network/WHOIS information
- Threat intelligence data
""")

# Initialize the IP search tool
ip_search = IPSearch()

# IP validation function
def is_valid_ip(ip: str) -> bool:
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    octets = ip.split('.')
    return all(0 <= int(octet) <= 255 for octet in octets)

# Create the search form
with st.form("ip_search_form"):
    ip_address = st.text_input("Enter IP address:", placeholder="e.g. 8.8.8.8")
    col1, col2 = st.columns(2)
    
    with col1:
        search_button = st.form_submit_button("🔍 Search")
    with col2:
        export_format = st.selectbox("Export format:", ["JSON", "TXT"])

if search_button:
    if not ip_address:
        st.error("Please enter an IP address")
    elif not is_valid_ip(ip_address):
        st.error("Please enter a valid IP address")
    else:
        with st.spinner(f"Analyzing IP address {ip_address}..."):
            # Get IP information
            results = ip_search.get_ip_info(ip_address)
            
            # Display results in columns
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Create tabs for different views
                results_tab, raw_tab = st.tabs(["Formatted Results", "Raw Data"])
                
                with results_tab:
                    st.markdown(ip_search.format_results(results))
                    
                with raw_tab:
                    st.json(results)
                    
            with col2:
                # Display map if coordinates are available
                if not results["geolocation"].get("error"):
                    st.markdown("### 🗺️ Location Map")
                    map_path = ip_search.generate_map(
                        results["geolocation"]["latitude"],
                        results["geolocation"]["longitude"]
                    )
                    if map_path:
                        with open(map_path, 'r') as f:
                            components.html(f.read(), height=400)
                        os.remove(map_path)  # Clean up temporary file
            
            # Export results
            st.markdown("### Export Results")
            
            if export_format == "JSON":
                filename = ip_search.save_results(ip_address, results)
                with open(filename, 'r') as f:
                    st.download_button(
                        label="📥 Download JSON",
                        data=f.read(),
                        file_name=f"ip_search_{ip_address}_results.json",
                        mime="application/json"
                    )
            else:
                formatted_text = ip_search.format_results(results)
                st.download_button(
                    label="📥 Download TXT",
                    data=formatted_text,
                    file_name=f"ip_search_{ip_address}_results.txt",
                    mime="text/plain"
                )

# Footer
st.markdown("---")
st.markdown("Letda Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE © 2025") 