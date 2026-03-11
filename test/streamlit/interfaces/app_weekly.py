#!/usr/bin/env python3
"""
Streamlit App – Weekly Report Generator
Tạo báo cáo tuần với 12 slides
"""

import streamlit as st
import os
import json
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to Python path for imports
import sys
sys.path.insert(0, '/app')

# Force reload modules
import importlib

modules_to_reload = [
    'generators.weekly.slide_generators_weekly',
    'generators.weekly.report_generator_weekly', 
    'generators.weekly.generate_slide_prompt_weekly',
    'core.data_loader',
    'generators.weekly.prompts_weekly'
]

for module_name in modules_to_reload:
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])

# Load ENV
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

# Import local modules
from generators.weekly.generate_slide_prompt_weekly import generate_complete_prompt
from generators.weekly.report_generator_weekly import WeeklyReportGenerator

# Page config
st.set_page_config(
    page_title="Weekly Report Generator",
    page_icon="📊"
)

st.title("📊 Weekly Report Generator")
st.caption("Generate weekly brand health reports with 10 slides")

# Sidebar
with st.sidebar:
    st.header("Configuration")

    uploaded_file = st.file_uploader(
        "Upload Excel file",
        type=["xlsx", "xls"]
    )

    brand_name = st.text_input(
        "Brand name (from 'Topic' column)",
        placeholder="Enter brand name...",
        help="Enter the exact brand name as it appears in the 'Topic' column of your Excel file"
    )

    st.subheader("Report Time Window (Weekly)")
    
    col1, col2 = st.columns(2)
    with col1:
        report_date = st.date_input(
            "End date (tuần hiện tại)",
            value=datetime.now()
        )
    with col2:
        from datetime import time
        report_time = st.time_input(
            "Giờ cắt data",
            value=time(15, 0),
            help="Giờ kết thúc của tuần"
        )
    
    # Combine date and time
    report_datetime = datetime.combine(report_date, report_time)
    report_datetime_str = report_datetime.strftime("%Y-%m-%d %H:%M:%S")
    
    # Auto-calculate 4 weeks (current + 3 past weeks)
    week1_end = report_datetime
    week1_start = week1_end - timedelta(days=7)
    
    week2_end = week1_start
    week2_start = week2_end - timedelta(days=7)
    
    week3_end = week2_start
    week3_start = week3_end - timedelta(days=7)
    
    week4_end = week3_start
    week4_start = week4_end - timedelta(days=7)
    
    st.info(f"""
    **Tuần hiện tại (Week 1):**  
    📅 {week1_start.strftime('%d/%m/%Y %H:%M')} → {week1_end.strftime('%d/%m/%Y %H:%M')}
    
    **Tuần trước (Week 2):**  
    📅 {week2_start.strftime('%d/%m/%Y %H:%M')} → {week2_end.strftime('%d/%m/%Y %H:%M')}
    
    **2 tuần trước (Week 3):**  
    📅 {week3_start.strftime('%d/%m/%Y %H:%M')} → {week3_end.strftime('%d/%m/%Y %H:%M')}
    
    **3 tuần trước (Week 4):**  
    📅 {week4_start.strftime('%d/%m/%Y %H:%M')} → {week4_end.strftime('%d/%m/%Y %H:%M')}
    """)

    st.divider()
    
    st.subheader("Display Options")
    
    show_interactions = st.checkbox(
        "Hiển thị Interactions",
        value=True,
        help="Bật/tắt hiển thị các metrics tương tác (Views, Reactions, Shares, Comments) trong Slide 1. Nếu tắt, chỉ hiển thị Tổng đề cập và chart so sánh 4 tuần."
    )

    st.divider()

    if API_KEY and BASE_URL:
        st.success("API credentials loaded")
    else:
        st.error("Missing API credentials (.env)")
        st.stop()

    st.divider()

    generate_button = st.button(
        "Generate weekly report",
        disabled=not (uploaded_file and brand_name),
        type="primary",
        use_container_width=True
    )
    
    if st.button("🔄 Clear Cache & Refresh", use_container_width=True):
        st.cache_data.clear()
        st.session_state.clear()
        st.rerun()

# Main
if not uploaded_file or not brand_name:
    st.info(
        "Upload an Excel file and enter brand name to generate weekly report."
    )
else:
    if "weekly_prompt_generated" not in st.session_state:
        st.session_state.weekly_prompt_generated = False
        st.session_state.weekly_prompt_text = ""
        st.session_state.weekly_json_data = None

    if generate_button:
        # Clear previous state
        if 'weekly_prompt_generated' in st.session_state:
            st.session_state.weekly_prompt_generated = False
            st.session_state.weekly_prompt_text = ""
            st.session_state.weekly_json_data = None
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            progress = st.progress(0)
            status = st.empty()

            status.text("Validating inputs...")
            progress.progress(20)

            generator = WeeklyReportGenerator(
                api_key=API_KEY,
                base_url=BASE_URL,
                file_path=tmp_path,
                brand_name=brand_name,
                week1_end=week1_end.strftime("%Y-%m-%d %H:%M:%S"),
                week2_end=week2_end.strftime("%Y-%m-%d %H:%M:%S"),
                week3_end=week3_end.strftime("%Y-%m-%d %H:%M:%S"),
                week4_end=week4_end.strftime("%Y-%m-%d %H:%M:%S"),
                show_interactions=show_interactions
            )

            status.text("Generating weekly report data (parallel processing ~2 minutes)...")
            progress.progress(50)
            
            info_placeholder = st.empty()
            with info_placeholder.container():
                st.info(f"""
                🚀 **Parallel Processing!** Generating 10 slides for weekly report.  
                🏷️ **Brand Filter**: {brand_name}  
                📅 **Report Window**: {week1_start.strftime('%d/%m/%Y')} → {week1_end.strftime('%d/%m/%Y')} (7 days)  
                ⏱️ This will take ~2 minutes.
                """)

            report_data = generator.generate_report()
            
            info_placeholder.empty()

            status.text("Generating slide prompt...")
            progress.progress(80)

            st.session_state.weekly_json_data = report_data
            st.session_state.weekly_prompt_text = generate_complete_prompt(report_data)
            st.session_state.weekly_prompt_generated = True

            progress.progress(100)
            status.text("Done")

            st.success("Weekly report generated successfully")

        except Exception as e:
            st.error(str(e))
            import traceback
            st.code(traceback.format_exc())

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    if st.session_state.weekly_prompt_generated:
        st.divider()
        st.header("📊 Generated Weekly Report")

        # Create tabs for each slide
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
            "📈 Slide 1: Overview",
            "📉 Slide 2: Trendline", 
            "📡 Slide 3: Channels",
            "🏆 Slide 4: Top Sources",
            "💬 Slide 5: Top Posts",
            "💭 Slide 6: Sentiment",
            "😊 Slide 7: Positive Topics",
            "✨ Slide 8: Positive Posts",
            "😞 Slide 9: Negative Topics",
            "⚠️ Slide 10: Negative Posts"
        ])
        
        data = st.session_state.weekly_json_data
        import pandas as pd
        
        # SLIDE 1: Overview
        with tab1:
            slide1 = data['slide_1']
            st.subheader(slide1['title'])
            st.caption(slide1['subtitle'])
            
            st.markdown("### 📊 Current Week Metrics")
            cols = st.columns(3)
            for idx, metric in enumerate(slide1['current_week_metrics']):
                with cols[idx % 3]:
                    if 'change_percent' in metric:
                        st.metric(
                            metric['label'], 
                            f"{metric['value']:,}",
                            f"{metric['change_percent']:+.2f}%"
                        )
                    else:
                        st.metric(metric['label'], f"{metric['value']:,}")
            
            st.markdown("### 📊 4-Week Comparison")
            df_compare = pd.DataFrame(slide1['weekly_comparison'])
            
            # Display chart
            st.bar_chart(df_compare.set_index('week')['total_mentions'])
            
            # Display growth rates in table
            st.dataframe(
                df_compare[['week', 'total_mentions', 'growth_rate']].rename(columns={
                    'week': 'Week',
                    'total_mentions': 'Total Mentions',
                    'growth_rate': 'Growth Rate (%)'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("### 💡 Insight")
            st.info(slide1['insight'])
        
        # SLIDE 2: Trendline
        with tab2:
            slide2 = data['slide_2']
            st.subheader(slide2['title'])
            st.caption(slide2['subtitle'])
            
            st.markdown("### 📈 7-Day Trend")
            df_trend = pd.DataFrame(slide2['trendline'])
            df_trend['date'] = pd.to_datetime(df_trend['date'])
            
            st.line_chart(df_trend.set_index('date')['mentions'])
            
            # Show data table
            st.dataframe(
                df_trend.rename(columns={'date': 'Date', 'mentions': 'Mentions'}),
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("### 💡 Insight")
            st.info(slide2['insight'])
        
        # SLIDE 3: Channels
        with tab3:
            slide3 = data['slide_3']
            st.subheader(slide3['title'])
            st.caption(slide3['subtitle'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Channel Distribution")
                df_channel = pd.DataFrame(slide3['channel_distribution'])
                
                # Calculate percentages
                total = df_channel['count'].sum()
                df_channel['percentage'] = (df_channel['count'] / total * 100).round(1)
                
                # Display as bar chart
                st.bar_chart(df_channel.set_index('Channel')['count'])
                
                # Show table with percentages
                st.dataframe(
                    df_channel[['Channel', 'count', 'percentage']].rename(columns={
                        'count': 'Count',
                        'percentage': 'Percentage (%)'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            
            with col2:
                st.markdown("### 🏆 Top 10 Sources")
                df_sources = pd.DataFrame(slide3['top_sources'])
                
                st.bar_chart(df_sources.set_index('SiteName')['count'])
                
                st.dataframe(
                    df_sources.rename(columns={'SiteName': 'Source', 'count': 'Count'}),
                    use_container_width=True,
                    hide_index=True
                )
            
            st.markdown("### 💡 Insight")
            st.info(slide3['insight'])
        
        # SLIDE 4: Top Sources by Engagement
        with tab4:
            slide4 = data['slide_4']
            st.subheader(slide4['title'])
            st.caption(slide4['subtitle'])
            
            # Check if interactions are shown
            show_interactions_slide4 = slide4.get('show_interactions', True)
            
            if show_interactions_slide4:
                st.markdown("### 📊 Top Sources by Total Engagement")
                df_table = pd.DataFrame(slide4['table_rows'])
                df_table = df_table.rename(columns={
                    'stt': 'Rank',
                    'source_name': 'Source',
                    'total_engagement': 'Total Engagement',
                    'reactions': 'Reactions',
                    'shares': 'Shares',
                    'comments': 'Comments'
                })
                
                # Show bar chart
                st.bar_chart(df_table.set_index('Source')['Total Engagement'])
                
                # Show detailed table
                st.dataframe(df_table, use_container_width=True, hide_index=True)
            else:
                st.markdown("### 📊 Top Sources by Mention Count")
                df_table = pd.DataFrame(slide4['table_rows'])
                df_table = df_table.rename(columns={
                    'stt': 'Rank',
                    'source_name': 'Source',
                    'count': 'Mention Count'
                })
                
                # Show bar chart
                st.bar_chart(df_table.set_index('Source')['Mention Count'])
                
                # Show detailed table
                st.dataframe(df_table, use_container_width=True, hide_index=True)
        
        # SLIDE 5: Top Posts
        with tab5:
            slide5 = data['slide_5']
            st.subheader(slide5['title'])
            st.caption(slide5['subtitle'])
            
            # Check if interactions are shown
            show_interactions_slide5 = slide5.get('show_interactions', True)
            
            if show_interactions_slide5:
                st.markdown("### 💬 Top Posts by Engagement")
                for row in slide5['table_rows']:
                    with st.expander(f"#{row['stt']} - {row['site_name']} ({row['channel']})"):
                        st.markdown(f"**Content:** {row['content'][:200]}...")
                        st.markdown(f"**Published:** {row['published_date']}")
                        st.markdown(f"**Link:** [{row['url']}]({row['url']})")
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Reactions", f"{row['reactions']:,}")
                        col2.metric("Shares", f"{row['shares']:,}")
                        col3.metric("Comments", f"{row['comments']:,}")
            else:
                st.markdown("### 💬 Top Posts")
                for row in slide5['table_rows']:
                    with st.expander(f"#{row['stt']} - {row['site_name']} ({row['channel']})"):
                        st.markdown(f"**Content:** {row['content'][:200]}...")
                        st.markdown(f"**Published:** {row['published_date']}")
                        st.markdown(f"**Link:** [{row['url']}]({row['url']})")
        
        # SLIDE 6: Sentiment
        with tab6:
            slide6 = data['slide_6']
            st.subheader(slide6['title'])
            st.caption(slide6['subtitle'])
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.markdown("### 📊 Previous Week")
                df_prev = pd.DataFrame(slide6['previous_sentiment'])
                
                # Calculate percentages
                total_prev = df_prev['count'].sum()
                df_prev['percentage'] = (df_prev['count'] / total_prev * 100).round(1)
                
                st.bar_chart(df_prev.set_index('sentiment')['count'])
                
                st.metric("NSR (Previous)", f"{slide6['previous_nsr']:.1f}%")
                
                st.dataframe(
                    df_prev[['sentiment', 'count', 'percentage']].rename(columns={
                        'sentiment': 'Sentiment',
                        'count': 'Count',
                        'percentage': '%'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            
            with col2:
                st.markdown("### 📈 NSR Growth")
                st.metric(
                    "NSR Change",
                    f"{slide6['current_nsr']:.1f}%",
                    f"{slide6['nsr_growth']:+.2f}%"
                )
                
                st.markdown("---")
                st.markdown("**NSR Formula:**")
                st.code("NSR = [(Pos% - Neg%) / (Pos% + Neg%)] × 100")
            
            with col3:
                st.markdown("### 📊 Current Week")
                df_curr = pd.DataFrame(slide6['current_sentiment'])
                
                # Calculate percentages
                total_curr = df_curr['count'].sum()
                df_curr['percentage'] = (df_curr['count'] / total_curr * 100).round(1)
                
                st.bar_chart(df_curr.set_index('sentiment')['count'])
                
                st.metric("NSR (Current)", f"{slide6['current_nsr']:.1f}%")
                
                st.dataframe(
                    df_curr[['sentiment', 'count', 'percentage']].rename(columns={
                        'sentiment': 'Sentiment',
                        'count': 'Count',
                        'percentage': '%'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            
            st.markdown("### 📊 Top Topics with Sentiment Breakdown")
            df_topics = pd.DataFrame(slide6['top_topics_with_sentiment'])
            
            # Create stacked data
            st.bar_chart(df_topics.set_index('topic')[['negative', 'neutral', 'positive']])
            
            # Show detailed table
            st.dataframe(
                df_topics.rename(columns={
                    'topic': 'Topic',
                    'total': 'Total',
                    'negative': 'Negative',
                    'neutral': 'Neutral',
                    'positive': 'Positive'
                }),
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("### 💡 Insight")
            st.info(slide6['insight'])
        
        # SLIDE 7: Positive Topics
        with tab7:
            slide7 = data['slide_7']
            st.subheader(slide7['title'])
            st.caption(slide7['subtitle'])
            
            st.markdown("### 😊 Positive Topics")
            df_pos = pd.DataFrame(slide7['positive_topics'])
            
            if len(df_pos) > 0:
                st.bar_chart(df_pos.set_index('Labels1')['count'])
                
                st.dataframe(
                    df_pos.rename(columns={'Labels1': 'Topic', 'count': 'Count'}),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("No positive topics data available")
            
            st.markdown("### 💡 Insight")
            st.info(slide7['insight'])
        
        # SLIDE 8: Positive Posts
        with tab8:
            slide8 = data['slide_8']
            st.subheader(slide8['title'])
            st.caption(slide8['subtitle'])
            
            st.markdown("### ✨ Top Posts by Positive Comments")
            for row in slide8['table_rows']:
                with st.expander(f"#{row['stt']} - {row['site_name']} ({row['channel']})"):
                    st.markdown(f"**Content:** {row['content'][:200]}...")
                    st.markdown(f"**Published:** {row['published_date']}")
                    st.markdown(f"**Link:** [{row['url']}]({row['url']})")
                    st.metric("Positive Comments", f"{row['positive_comments']:,}", help="Number of positive sentiment comments")
        
        # SLIDE 9: Negative Topics
        with tab9:
            slide9 = data['slide_9']
            st.subheader(slide9['title'])
            st.caption(slide9['subtitle'])
            
            st.markdown("### 😞 Negative Topics")
            df_neg = pd.DataFrame(slide9['negative_topics'])
            
            if len(df_neg) > 0:
                st.bar_chart(df_neg.set_index('Labels1')['count'])
                
                st.dataframe(
                    df_neg.rename(columns={'Labels1': 'Topic', 'count': 'Count'}),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("No negative topics data available")
            
            st.markdown("### 💡 Insight")
            st.info(slide9['insight'])
        
        # SLIDE 10: Negative Posts
        with tab10:
            slide10 = data['slide_10']
            st.subheader(slide10['title'])
            st.caption(slide10['subtitle'])
            
            st.markdown("### ⚠️ Top Posts by Negative Comments")
            for row in slide10['table_rows']:
                with st.expander(f"#{row['stt']} - {row['site_name']} ({row['channel']})"):
                    st.markdown(f"**Content:** {row['content'][:200]}...")
                    st.markdown(f"**Published:** {row['published_date']}")
                    st.markdown(f"**Link:** [{row['url']}]({row['url']})")
                    st.metric("Negative Comments", f"{row['negative_comments']:,}", help="Number of negative sentiment comments")
        
        st.divider()
        st.header("📄 Generated Prompt")

        tab_preview, tab_copy, tab_download = st.tabs(
            ["Preview", "Copy", "Download"]
        )

        with tab_preview:
            st.text_area(
                "Prompt preview",
                st.session_state.weekly_prompt_text,
                height=400
            )

        with tab_copy:
            st.text_area(
                "Copy this prompt",
                st.session_state.weekly_prompt_text,
                height=400
            )

        with tab_download:
            st.download_button(
                "Download prompt (.txt)",
                st.session_state.weekly_prompt_text,
                file_name=f"{brand_name}_weekly_prompt_{report_date:%Y%m%d}.txt"
            )

            if st.session_state.weekly_json_data:
                st.download_button(
                    "Download JSON data",
                    json.dumps(
                        st.session_state.weekly_json_data,
                        ensure_ascii=False,
                        indent=2
                    ),
                    file_name=f"{brand_name}_weekly_data_{report_date:%Y%m%d}.json",
                    mime="application/json"
                )

st.divider()
st.caption("Built with Streamlit · Weekly Report Generator")
