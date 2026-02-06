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
Create a 5-slide presentation

BRAND: Vinamilk
REPORT DATE: 30/01/2026
COMPARE DATE: 29/01/2026

SLIDE 1 - BRAND OVERVIEW
- Total Buzz: 1,234 (+15%)
- Positive Sentiment: 567 (+20%)

SLIDE 2 - TRENDLINE
- 7-day trend analysis

SLIDE 3 - CHANNEL BREAKDOWN
- Top channels by buzz

SLIDE 4 - SENTIMENT & ATTRIBUTES
- Sentiment distribution
- Brand attributes

SLIDE 5 - TOP 5 POSTS
- Top posts by engagement
- Full table with metrics
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
                st.info("🚀 **Parallel Processing!** Generating 5 slides (4 with LLM + 1 data table). This will take ~1 minute.")

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

        # =====================
        # SLIDE PREVIEW TABS
        # =====================
        st.subheader("📊 Slide Preview")
        
        slide_tabs = st.tabs([
            "Slide 1: Overview",
            "Slide 2: Trendline", 
            "Slide 3: Channels",
            "Slide 4: Sentiment",
            "Slide 5: Top Posts"
        ])
        
        # Slide 1 Preview
        with slide_tabs[0]:
            if st.session_state.json_data and 'slide_1' in st.session_state.json_data:
                slide1 = st.session_state.json_data['slide_1']
                st.markdown(f"### {slide1['title']}")
                st.caption(slide1['subtitle'])
                
                cols = st.columns(3)
                for idx, item in enumerate(slide1['data'][:6]):
                    with cols[idx % 3]:
                        delta_color = "normal" if item['change_pct'] >= 0 else "inverse"
                        st.metric(
                            item['label'],
                            f"{item['today']:,}",
                            f"{item['change_pct']:.1f}%",
                            delta_color=delta_color
                        )
        
        # Slide 2 Preview
        with slide_tabs[1]:
            if st.session_state.json_data and 'slide_2' in st.session_state.json_data:
                slide2 = st.session_state.json_data['slide_2']
                st.markdown(f"### {slide2['title']}")
                st.caption(slide2['subtitle'])
                
                import pandas as pd
                df_trend = pd.DataFrame(slide2['trendline'])
                st.line_chart(df_trend.set_index('date')['buzz'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"🔥 **Peak Day**\n\n{slide2['peak_day']['date']}: {slide2['peak_day']['buzz']:,} lượt")
                with col2:
                    status = "🔥 Vẫn HOT" if slide2['current_day']['is_still_hot'] else "❄️ Đã hạ nhiệt"
                    st.info(f"**Current Status**\n\n{status}")
        
        # Slide 3 Preview
        with slide_tabs[2]:
            if st.session_state.json_data and 'slide_3' in st.session_state.json_data:
                slide3 = st.session_state.json_data['slide_3']
                st.markdown(f"### {slide3['title']}")
                st.caption(slide3['subtitle'])
                
                import pandas as pd
                df_channels = pd.DataFrame(slide3['channel_distribution'])
                st.bar_chart(df_channels.set_index('Channel')['today_buzz'])
                
                st.success(f"🏆 **Top Channel:** {slide3['top_channel']}")
        
        # Slide 4 Preview
        with slide_tabs[3]:
            if st.session_state.json_data and 'slide_4' in st.session_state.json_data:
                slide4 = st.session_state.json_data['slide_4']
                st.markdown(f"### {slide4['title']}")
                st.caption(slide4['subtitle'])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Sentiment Distribution**")
                    import pandas as pd
                    df_sent = pd.DataFrame(slide4['sentiment_distribution'])
                    st.dataframe(df_sent, hide_index=True)
                
                with col2:
                    st.markdown("**Top Attributes**")
                    df_attr = pd.DataFrame(slide4['attribute_sentiment'])
                    st.dataframe(df_attr.head(6), hide_index=True)
        
        # Slide 5 Preview - TOP POSTS TABLE
        with slide_tabs[4]:
            if st.session_state.json_data and 'slide_5' in st.session_state.json_data:
                slide5 = st.session_state.json_data['slide_5']
                st.markdown(f"### {slide5['title']}")
                st.caption(slide5['subtitle'])
                
                # Build table data
                import pandas as pd
                table_data = []
                for post in slide5['top_posts']:
                    # Format date
                    date_obj = datetime.strptime(post['ngay_dang'], "%Y-%m-%d %H:%M:%S")
                    date_formatted = date_obj.strftime("%d/%m/%Y")
                    
                    table_data.append({
                        'STT': post['stt'],
                        'Nội dung': post['noi_dung_bai_dang'][:100] + '...' if len(post['noi_dung_bai_dang']) > 100 else post['noi_dung_bai_dang'],
                        'Ngày đăng': date_formatted,
                        'Kênh': post['kenh'],
                        'Người đăng': post['nguoi_dang'],
                        'Like': f"{post['luong_tuong_tac']['like']:,}",
                        'Share': f"{post['luong_tuong_tac']['share']:,}",
                        'Comments': f"{post['luong_tuong_tac']['comments']:,}",
                        'Views': f"{post['luong_tuong_tac']['views']:,}",
                        'Link': post.get('url_topic', '')
                    })
                
                df_posts = pd.DataFrame(table_data)
                
                # Display table with styling
                st.dataframe(
                    df_posts,
                    hide_index=True,
                    use_container_width=True,
                    column_config={
                        'STT': st.column_config.NumberColumn('STT', width='small'),
                        'Nội dung': st.column_config.TextColumn('Nội dung bài đăng', width='large'),
                        'Ngày đăng': st.column_config.TextColumn('Ngày đăng', width='small'),
                        'Kênh': st.column_config.TextColumn('Kênh', width='small'),
                        'Người đăng': st.column_config.TextColumn('Người đăng', width='medium'),
                        'Like': st.column_config.TextColumn('Like', width='small'),
                        'Share': st.column_config.TextColumn('Share', width='small'),
                        'Comments': st.column_config.TextColumn('Comments', width='small'),
                        'Views': st.column_config.TextColumn('Views', width='small'),
                        'Link': st.column_config.LinkColumn('Link', width='small')
                    }
                )
                
                # Show full content in expanders
                st.markdown("---")
                st.markdown("**📝 Full Content**")
                for post in slide5['top_posts']:
                    with st.expander(f"#{post['stt']} - {post['nguoi_dang']} ({post['kenh']})"):
                        st.markdown(f"**Nội dung:**")
                        st.write(post['noi_dung_bai_dang'])
                        st.markdown(f"**Link:** [{post.get('url_topic', 'N/A')}]({post.get('url_topic', '#')})")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Like", f"{post['luong_tuong_tac']['like']:,}")
                        with col2:
                            st.metric("Share", f"{post['luong_tuong_tac']['share']:,}")
                        with col3:
                            st.metric("Comments", f"{post['luong_tuong_tac']['comments']:,}")
                        with col4:
                            st.metric("Views", f"{post['luong_tuong_tac']['views']:,}")
        
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

---

**📊 Presentation includes 5 slides:**
1. Brand Overview (KPIs)
2. Trendline (7-day trend)
3. Channel Breakdown
4. Sentiment & Attributes
5. **Top 5 Posts** (with engagement metrics)
"""
        )

# =====================
# FOOTER
# =====================
st.divider()
st.caption("Built with Streamlit · Slide Prompt Generator")
