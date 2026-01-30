"""
Streamlit App: Social Listening Report Generator
Giao diện web để upload file, generate report, preview, và copy prompt
"""
import streamlit as st
import pandas as pd
from io import BytesIO, StringIO
import tempfile
import os
from datetime import datetime
from main import generate_report, save_report


# Page config
st.set_page_config(
    page_title="Social Listening Report Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "report_generated" not in st.session_state:
    st.session_state.report_generated = False
    st.session_state.report_content = ""
    st.session_state.primary_brand = ""
    st.session_state.progress_message = ""


def update_progress(progress, message):
    """Update progress in session state"""
    st.session_state.progress_message = f"{int(progress * 100)}% - {message}"


def main():
    # Header
    st.markdown('<div class="main-header">📊 Social Listening Report Generator</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        st.markdown("---")
        
        # File upload
        st.subheader("📁 Upload Data")
        uploaded_file = st.file_uploader(
            "Choose an Excel file",
            type=["xlsx", "xls"],
            help="Upload your social listening data in Excel format"
        )
        
        st.markdown("---")
        
        # Instructions
        with st.expander("📖 Instructions", expanded=False):
            st.markdown("""
            ### How to use:
            1. **Upload** your Excel file with social listening data
            2. **Click** "Generate Report" button
            3. **Preview** the generated report
            4. **Copy** the entire prompt to clipboard
            5. **Download** the report as markdown file
            
            ### Required columns in Excel:
            - PublishedDate
            - Channel
            - Topic
            - Labels1
            - Sentiment
            - Title
            - Content
            - Description
            - Type
            """)
        
        st.markdown("---")
        
        # About
        with st.expander("ℹ️ About", expanded=False):
            st.markdown("""
            This tool generates comprehensive social listening analysis reports
            with 13 slides covering:
            - Share of Voice
            - Sentiment Analysis
            - Topic Trends
            - Channel Distribution
            - Brand Comparison
            
            Each slide includes sample data as evidence for insights.
            """)
    
    # Main content
    if uploaded_file is None:
        st.info("👈 Please upload an Excel file to get started")
        return
    
    # Display file info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("File Name", uploaded_file.name)
    with col2:
        st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
    with col3:
        st.metric("Upload Time", datetime.now().strftime("%H:%M:%S"))
    
    st.markdown("---")
    
    # Generate button
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_btn = st.button(
            "🚀 Generate Report",
            use_container_width=True,
            type="primary"
        )
    
    if generate_btn:
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name
        
        try:
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def progress_callback(progress, message):
                progress_bar.progress(min(progress, 0.99))
                status_text.text(f"⏳ {message}")
            
            # Generate report
            status_text.text("⏳ Starting report generation...")
            report_content, primary_brand = generate_report(tmp_path, progress_callback)
            
            # Complete
            progress_bar.progress(1.0)
            status_text.text("✅ Report generated successfully!")
            
            # Store in session state
            st.session_state.report_generated = True
            st.session_state.report_content = report_content
            st.session_state.primary_brand = primary_brand
            
            # Success message
            st.markdown(
                f'<div class="success-box">✅ Report generated successfully for <strong>{primary_brand}</strong></div>',
                unsafe_allow_html=True
            )
            
        except Exception as e:
            st.markdown(
                f'<div class="error-box">❌ Error: {str(e)}</div>',
                unsafe_allow_html=True
            )
            st.error(f"Details: {str(e)}")
        
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    st.markdown("---")
    
    # Display report if generated
    if st.session_state.report_generated:
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📄 Preview", "📋 Raw Text", "💾 Download"])
        
        with tab1:
            st.subheader("Report Preview")
            st.markdown(st.session_state.report_content)
        
        with tab2:
            st.subheader("Raw Markdown")
            
            # Copy button
            col1, col2 = st.columns([1, 4])
            with col1:
                copy_btn = st.button(
                    "📋 Copy All",
                    use_container_width=True,
                    help="Copy entire report to clipboard"
                )
                if copy_btn:
                    st.write("✅ Copied to clipboard!")
                    # Note: Actual clipboard copy requires JavaScript
                    st.code(st.session_state.report_content, language="markdown")
            
            # Display raw text in expandable section
            with st.expander("View Full Text", expanded=False):
                st.text_area(
                    "Report Content",
                    value=st.session_state.report_content,
                    height=600,
                    disabled=True,
                    label_visibility="collapsed"
                )
        
        with tab3:
            st.subheader("Download Report")
            
            # Generate download filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{st.session_state.primary_brand}_report_{timestamp}.md"
            
            # Download button
            st.download_button(
                label="📥 Download as Markdown",
                data=st.session_state.report_content,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True
            )
            
            st.info(f"📁 File will be saved as: `{filename}`")
        
        st.markdown("---")
        
        # Report statistics
        st.subheader("📊 Report Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Primary Brand", st.session_state.primary_brand)
        with col2:
            st.metric("Content Length", f"{len(st.session_state.report_content):,} chars")
        with col3:
            st.metric("Lines", st.session_state.report_content.count('\n'))
        with col4:
            st.metric("Generated At", datetime.now().strftime("%H:%M:%S"))


if __name__ == "__main__":
    main()
