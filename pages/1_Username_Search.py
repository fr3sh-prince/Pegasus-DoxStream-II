import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.username_search import UsernameSearch

st.set_page_config(
    page_title="Username Search - DoxStream",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Username Search")
st.markdown("""
This tool searches for a username across multiple social media platforms using Sherlock.
Enter a username below to start the search.
""")

# Initialize the username search tool
username_search = UsernameSearch()

# Create the search form
with st.form("username_search_form"):
    username = st.text_input("Enter username to search:", placeholder="e.g. john_doe")
    col1, col2 = st.columns(2)
    
    with col1:
        search_button = st.form_submit_button("🔍 Search")
    with col2:
        export_format = st.selectbox("Export format:", ["JSON", "TXT"])

if search_button and username:
    with st.spinner(f"Searching for username '{username}' across platforms..."):
        # Perform the search
        results = username_search.search_username(username)
        
        # Display results
        st.markdown("### Search Results")
        
        # Create tabs for different views
        results_tab, raw_tab = st.tabs(["Formatted Results", "Raw Data"])
        
        with results_tab:
            st.markdown(username_search.format_results(results))
            
        with raw_tab:
            st.json(results)
        
        # Export results
        if results["found"] or results["not_found"]:
            st.markdown("### Export Results")
            
            if export_format == "JSON":
                filename = username_search.save_results(results, username)
                with open(filename, 'r') as f:
                    st.download_button(
                        label="📥 Download JSON",
                        data=f.read(),
                        file_name=f"sherlock_{username}_results.json",
                        mime="application/json"
                    )
            else:
                formatted_text = username_search.format_results(results)
                st.download_button(
                    label="📥 Download TXT",
                    data=formatted_text,
                    file_name=f"sherlock_{username}_results.txt",
                    mime="text/plain"
                )

# Footer
st.markdown("---")
st.markdown("Letda Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE © 2025") 