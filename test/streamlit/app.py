#!/usr/bin/env python3
"""
Streamlit App – Slide Prompt Generator
Single-file version (no custom CSS)
"""

import streamlit as st
import os
import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# =====================
# LOAD ENV
# =====================
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

# =====================
# IMPORT LOCAL MODULES
# =====================
from generate_slide_prompt import generate_complete_prompt
from report_generator import ReportGenerator

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Slide Prompt Generator",
    page_icon="📊"
)

st.title("📊 Slide Prompt Generator")
st.caption("Generate slide prompts for Manus & Genspark")

# =====================
# SIDEBAR
# =====================
with st.sidebar:
    st.header("Configuration")

    uploaded_file = st.file_uploader(
        "Upload Excel file",
        type=["xlsx", "xls"]
    )

    brand_name = st.text_input(
        "Brand name",
        placeholder="Vinamilk, Nestlé, VinFast..."
    )

    report_date = st.date_input(
        "Report date",
        value=datetime.now()
    )

    compare_date = report_date - timedelta(days=1)
    st.caption(f"Compare date: {compare_date.strftime('%Y-%m-%d')}")

    st.divider()

    if API_KEY and BASE_URL:
        st.success("API credentials loaded")
    else:
        st.error("Missing API credentials (.env)")
        st.stop()

    st.divider()

    generate_button = st.button(
        "Generate prompt",
        disabled=not (uploaded_file and brand_name)
    )

# =====================
# MAIN
# =====================
if not uploaded_file or not brand_name:
    st.info(
        "Upload an Excel file and enter brand name to generate slide prompt."
    )

    with st.expander("Example output"):
        st.code(
            """
Create a 4-slide presentation

BRAND: Vinamilk
REPORT DATE: 30/01/2026
COMPARE DATE: 29/01/2026

SLIDE 1 - BRAND OVERVIEW
- Total Buzz: 1,234 (+15%)
- Positive Sentiment: 567 (+20%)
...
            """,
            language="text"
        )

else:
    if "prompt_generated" not in st.session_state:
        st.session_state.prompt_generated = False
        st.session_state.prompt_text = ""
        st.session_state.json_data = None

    if generate_button:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            progress = st.progress(0)
            status = st.empty()

            status.text("Validating inputs...")
            progress.progress(20)

            generator = ReportGenerator(
                api_key=API_KEY,
                base_url=BASE_URL,
                file_path=tmp_path,
                brand_name=brand_name,
                report_date=report_date.strftime("%Y-%m-%d"),
                compare_date=compare_date.strftime("%Y-%m-%d")
            )

            status.text("Generating report data (parallel processing ~1 minute)...")
            progress.progress(50)
            
            # Show info about parallel processing
            info_placeholder = st.empty()
            with info_placeholder.container():
                st.info("🚀 **Parallel Processing!** Generating 4 slides simultaneously. This will take ~1 minute instead of 3-4 minutes.")

            report_data = generator.generate_report()
            
            # Clear info message
            info_placeholder.empty()

            status.text("Generating slide prompt...")
            progress.progress(80)

            st.session_state.json_data = report_data
            st.session_state.prompt_text = generate_complete_prompt(report_data)
            st.session_state.prompt_generated = True

            progress.progress(100)
            status.text("Done")

            st.success("Prompt generated successfully")

        except Exception as e:
            st.error(str(e))

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    if st.session_state.prompt_generated:
        st.divider()
        st.header("Generated Prompt")

        tab_preview, tab_copy, tab_download = st.tabs(
            ["Preview", "Copy", "Download"]
        )

        with tab_preview:
            st.text_area(
                "Prompt preview",
                st.session_state.prompt_text,
                height=400
            )

        with tab_copy:
            st.text_area(
                "Copy this prompt",
                st.session_state.prompt_text,
                height=400
            )

        with tab_download:
            st.download_button(
                "Download prompt (.txt)",
                st.session_state.prompt_text,
                file_name=f"{brand_name}_prompt_{report_date:%Y%m%d}.txt"
            )

            if st.session_state.json_data:
                st.download_button(
                    "Download JSON data",
                    json.dumps(
                        st.session_state.json_data,
                        ensure_ascii=False,
                        indent=2
                    ),
                    file_name=f"{brand_name}_data_{report_date:%Y%m%d}.json",
                    mime="application/json"
                )

        # =====================
        # NEXT STEPS (2 ONLY)
        # =====================
        st.divider()
        st.subheader("Next steps")
        st.markdown(
            """
### 1️⃣ Manus
- Paste prompt
- Click **Generate**
- Wait 30–60 seconds  
👉 https://manus.im/

### 2️⃣ Genspark
- Paste prompt
- Click **Generate**
- Review & refine slides  
👉 https://www.genspark.ai/
"""
        )

# =====================
# FOOTER
# =====================
st.divider()
st.caption("Built with Streamlit · Slide Prompt Generator")
