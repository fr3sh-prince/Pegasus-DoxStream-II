import streamlit as st
import sys
import os
import tempfile
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.file_analysis import FileAnalysis

st.set_page_config(
    page_title="File Analysis - DoxStream",
    page_icon="📄",
    layout="wide"
)

st.title("📄 File Metadata Analysis")
st.markdown("""
This tool analyzes metadata from uploaded files:
- Basic file information
- EXIF data extraction
- Document metadata
- Image information
- And more...
""")

# File upload form
with st.form("file_analysis_form"):
    uploaded_file = st.file_uploader(
        "Upload a file to analyze:",
        type=["jpg", "jpeg", "png", "doc", "docx", "xls", "xlsx"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        analyze_button = st.form_submit_button("🔍 Analyze")
    with col2:
        export_format = st.selectbox("Export format:", ["JSON", "TXT"])

if analyze_button and uploaded_file is not None:
    with st.spinner(f"Analyzing file {uploaded_file.name}..."):
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            # Initialize FileAnalysis with the temporary file path
            file_analysis = FileAnalysis(tmp_file_path)
            
            # Analyze file
            results = file_analysis.analyze()
            
            # Display results
            st.markdown("### Analysis Results")
            
            # Create tabs for different views
            results_tab, raw_tab = st.tabs(["Formatted Results", "Raw Data"])
            
            with results_tab:
                formatted_results = "\n".join(file_analysis.format_results())
                st.markdown(formatted_results)
                
            with raw_tab:
                st.json(results)
            
            # Export results
            st.markdown("### Export Results")
            
            if export_format == "JSON":
                st.download_button(
                    label="📥 Download JSON",
                    data=str(results),
                    file_name=f"file_analysis_{uploaded_file.name}_results.json",
                    mime="application/json"
                )
            else:
                formatted_text = "\n".join(file_analysis.format_results())
                st.download_button(
                    label="📥 Download TXT",
                    data=formatted_text,
                    file_name=f"file_analysis_{uploaded_file.name}_results.txt",
                    mime="text/plain"
                )
                
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)

# Footer
st.markdown("---")
st.markdown("Letda Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE © 2025")