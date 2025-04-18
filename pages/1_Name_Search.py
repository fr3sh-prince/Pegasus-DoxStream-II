import streamlit as st
import asyncio
from tools.name_search import NameSearch
import json
import os

st.set_page_config(
    page_title="Name Search - DoxStream",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'name_search_results' not in st.session_state:
    st.session_state.name_search_results = None
if 'download_ready' not in st.session_state:
    st.session_state.download_ready = False

def main():
    st.title("🔍 Name Search")
    st.markdown("""
    Search for information about a person using their name. This tool will:
    * Search for social media profiles using Sherlock
    * Analyze social media presence using Social Analyzer
    * Generate possible email addresses
    * Search the web for relevant information using Photon
    """)
    
    # Input section
    with st.form("name_search_form"):
        name = st.text_input("Enter the name to search:", placeholder="John Doe")
        col1, col2 = st.columns(2)
        with col1:
            search_social = st.checkbox("Search Social Media", value=True)
        with col2:
            search_web = st.checkbox("Search Web", value=True)
            
        submitted = st.form_submit_button("Start Search")
        
    if submitted and name:
        with st.spinner("🔍 Searching... This may take a few minutes..."):
            try:
                name_search = NameSearch()
                
                # Create progress bars
                if search_social:
                    social_progress = st.progress(0)
                    st.markdown("### 📱 Searching Social Media...")
                if search_web:
                    web_progress = st.progress(0)
                    st.markdown("### 🌐 Searching Web...")
                
                # Perform searches
                social_results = {"profiles": [], "possible_emails": [], "social_media": [], "error": None}
                web_results = {"websites": [], "emails": [], "social_links": [], "error": None}
                
                if search_social:
                    social_results = asyncio.run(name_search.search_social_media(name))
                    social_progress.progress(100)
                    
                if search_web:
                    web_results = name_search.search_web(name)
                    web_progress.progress(100)
                
                # Save results
                result_file = name_search.save_results(name, social_results, web_results)
                
                # Store results in session state
                st.session_state.name_search_results = {
                    "social": social_results,
                    "web": web_results,
                    "file": result_file
                }
                st.session_state.download_ready = True
                
                # Display results
                st.markdown("## 📊 Search Results")
                
                if search_social:
                    st.markdown("### 📱 Social Media Profiles")
                    if social_results["profiles"]:
                        for profile in social_results["profiles"]:
                            st.markdown(f"- **{profile['platform']}**: [{profile['url']}]({profile['url']})")
                    else:
                        st.info("No social media profiles found.")
                        
                    st.markdown("### 🌐 Social Media Analysis")
                    if social_results["social_media"]:
                        for profile in social_results["social_media"]:
                            st.markdown(f"""
                            - **Platform**: {profile['platform']}
                              - URL: [{profile['url']}]({profile['url']})
                              - Username: {profile['username']}
                              - Name: {profile['name']}
                            """)
                    else:
                        st.info("No additional social media information found.")
                        
                    st.markdown("### 📧 Possible Email Addresses")
                    if social_results["possible_emails"]:
                        for email in social_results["possible_emails"]:
                            st.markdown(f"- `{email}`")
                    else:
                        st.info("No possible email addresses generated.")
                        
                if search_web:
                    st.markdown("### 🌍 Web Presence")
                    if web_results["websites"]:
                        st.markdown("#### Websites:")
                        for website in web_results["websites"][:10]:
                            st.markdown(f"- [{website}]({website})")
                    else:
                        st.info("No relevant websites found.")
                        
                    if web_results["social_links"]:
                        st.markdown("#### Social Links:")
                        for link in web_results["social_links"]:
                            st.markdown(f"- [{link}]({link})")
                            
                # Download section
                if st.session_state.download_ready and result_file:
                    st.markdown("## 💾 Download Results")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        with open(result_file, 'r', encoding='utf-8') as f:
                            st.download_button(
                                "Download as TXT",
                                f.read(),
                                file_name=f"name_search_{name.replace(' ', '_')}.txt",
                                mime="text/plain"
                            )
                    
                    with col2:
                        st.download_button(
                            "Download as JSON",
                            json.dumps({
                                "social_results": social_results,
                                "web_results": web_results
                            }, indent=2),
                            file_name=f"name_search_{name.replace(' ', '_')}.json",
                            mime="application/json"
                        )
                
            except Exception as e:
                st.error(f"An error occurred during the search: {str(e)}")
                
    # Display helpful tips
    with st.expander("💡 Search Tips"):
        st.markdown("""
        * Use the person's full name for better results
        * Try different variations of the name
        * Some searches might take a few minutes to complete
        * Not all social media platforms may be accessible
        * Results are saved automatically and can be downloaded
        """)
        
if __name__ == "__main__":
    main() 