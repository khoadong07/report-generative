#!/usr/bin/env python3
"""Streamlit App – Masan Weekly Report Generator"""
import os, json, tempfile, sys
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from dotenv import load_dotenv
from pathlib import Path

# Ensure project root is on sys.path
_ROOT = str(Path(__file__).resolve().parent.parent)
for _p in (_ROOT, '/app'):
    if _p not in sys.path:
        sys.path.insert(0, _p)

load_dotenv(Path(_ROOT) / '.env')
API_KEY  = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL    = os.getenv("MODEL", "meta-llama/Meta-Llama-3.1-70B-Instruct")  # Default model

from core.llm_client import LLMClient
from core.data_loader import DataLoader
from core.config import TEXT_COLUMNS, METRIC_COLUMNS
from weekly_report_masan.data_processor import process_uploaded_file
from weekly_report_masan.slides.slide01_masan_market import Slide01MasanMarket
from weekly_report_masan.slides.slide02_discussion_overview import Slide02DiscussionOverview
from weekly_report_masan.slides.slide03_health_channels import Slide03HealthChannels
from weekly_report_masan.slides.slide04_products import Slide04Products
from weekly_report_masan.slides.slide05_category_detail import Slide05CategoryDetail
from weekly_report_masan.slides.slide06_category_channels import Slide06CategoryChannels
from weekly_report_masan.slides.slide07_category_sentiment import Slide07CategorySentiment
from weekly_report_masan.slides.slide08_category_trends import Slide08CategoryTrends
from weekly_report_masan.prompt_builder import generate_masan_prompt

# Page config
st.set_page_config(
    page_title="Masan Weekly Report", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""<style>
.block-container{padding-top:1.5rem;padding-bottom:1rem}
.stTabs [data-baseweb="tab"]{font-size:.8rem;padding:6px 10px}
div[data-testid="stMetric"]{background:#f8f9fa;border-radius:8px;padding:10px}
</style>""", unsafe_allow_html=True)

# Session state initialization
for k, v in {
    "report_generated": False,
    "report_data": None,
    "prompt_text": "",
    "llm_client": None,
    "selected_competitors": []
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

@st.cache_data(show_spinner="Đang đọc và xử lý file...")
def load_excel(file_bytes: bytes) -> pd.DataFrame:
    """Load and process Excel file with mapping."""
    import io
    
    # Read raw file
    df_raw = pd.read_excel(io.BytesIO(file_bytes))
    
    # Process with mapping
    try:
        df_processed = process_uploaded_file(df_raw)
        return df_processed
    except Exception as e:
        st.error(f"Lỗi khi merge dữ liệu: {e}")
        # Return raw data if merge fails
        return df_raw

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Masan Weekly Report")
    
    # Check API credentials
    if not (API_KEY and BASE_URL):
        st.error("Thiếu API credentials trong .env")
        st.info("Cần có: API_KEY, BASE_URL, MODEL (optional)")
        st.stop()
    st.success("API credentials OK")
    st.caption(f"Model: {MODEL}")
    st.divider()

    # 1. Upload data
    st.subheader("1. Upload dữ liệu")
    uploaded_file = st.file_uploader(
        "File Excel (.xlsx / .xls)", 
        type=["xlsx", "xls"],
        help="Upload file dữ liệu với các cột: Topic, Type, Sentiment, PublishedDate, etc."
    )
    
    df_full, available_topics = None, []
    if uploaded_file:
        try:
            df_full = load_excel(uploaded_file.getvalue())
            
            # Preprocess datetime
            if "PublishedDate" in df_full.columns:
                df_full["PublishedDate"] = pd.to_datetime(df_full["PublishedDate"], errors="coerce")
            
            # Extract unique topics from Topic column
            if "Topic" not in df_full.columns:
                st.error("File không có cột 'Topic'. Vui lòng kiểm tra lại file dữ liệu.")
                st.stop()
            
            available_topics = sorted(df_full["Topic"].dropna().unique().tolist())
            
            if not available_topics:
                st.error("Không tìm thấy topics trong file. Cột 'Topic' có thể trống.")
                st.stop()
            
            # Show merge status
            if "Ngành hàng" in df_full.columns:
                nganh_hang_count = df_full["Ngành hàng"].notna().sum()
                nganh_hang_pct = round(nganh_hang_count / len(df_full) * 100, 1)
                st.success(f"Đã merge: {nganh_hang_count:,}/{len(df_full):,} dòng có Ngành hàng ({nganh_hang_pct}%)")
            else:
                st.warning("Không có cột 'Ngành hàng' sau khi merge")
            
            # Show available topics
            with st.expander("Xem danh sách Topics"):
                st.write(", ".join(available_topics))
            
            # Show data preview
            with st.expander("Xem mẫu dữ liệu"):
                preview_cols = ["Topic", "Type", "Sentiment", "PublishedDate"]
                if "Ngành hàng" in df_full.columns:
                    preview_cols.append("Ngành hàng")
                if "Brand" in df_full.columns:
                    preview_cols.append("Brand")
                if "Sản phẩm" in df_full.columns:
                    preview_cols.append("Sản phẩm")
                
                available_preview_cols = [col for col in preview_cols if col in df_full.columns]
                st.dataframe(
                    df_full.head(10)[available_preview_cols],
                    use_container_width=True,
                    hide_index=True
                )
                
        except Exception as e:
            st.error(f"Lỗi đọc file: {e}")
            import traceback
            st.code(traceback.format_exc())
            st.stop()

    # 2. Brand selection
    st.subheader("2. Thương hiệu")
    
    if available_topics:
        # Quick filter for topics
        if len(available_topics) > 10:
            filter_keyword = st.text_input(
                "Lọc topics (tùy chọn)",
                placeholder="Nhập từ khóa để lọc...",
                help="Lọc danh sách topics theo từ khóa"
            )
            if filter_keyword:
                filtered_topics = [t for t in available_topics if filter_keyword.lower() in t.lower()]
                if filtered_topics:
                    st.caption(f"Tìm thấy {len(filtered_topics)} topics phù hợp")
                    available_topics_display = filtered_topics
                else:
                    st.warning(f"Không tìm thấy topic nào chứa '{filter_keyword}'")
                    available_topics_display = available_topics
            else:
                available_topics_display = available_topics
        else:
            available_topics_display = available_topics
        
        # Main brand selection with search
        main_brand = st.selectbox(
            "Main Brand (Masan)", 
            options=available_topics_display,
            help="Chọn thương hiệu chính để phân tích",
            index=0
        )
        
        # Show main brand stats
        if df_full is not None and main_brand:
            main_brand_count = len(df_full[df_full["Topic"] == main_brand])
            st.caption(f"{main_brand}: {main_brand_count:,} dòng dữ liệu")
        
        # Quick select buttons for competitors
        if len(available_topics) > 1:
            col_all, col_clear = st.columns(2)
            with col_all:
                if st.button("Chọn tất cả đối thủ", use_container_width=True, key="select_all_comp"):
                    st.session_state.selected_competitors = [t for t in available_topics if t != main_brand]
            with col_clear:
                if st.button("Bỏ chọn tất cả", use_container_width=True, key="clear_comp"):
                    st.session_state.selected_competitors = []
        
        # Competitors selection
        competitors = st.multiselect(
            "Đối thủ cạnh tranh",
            options=[t for t in available_topics if t != main_brand],
            help="Chọn các đối thủ để so sánh (có thể chọn nhiều)",
            default=st.session_state.selected_competitors if st.session_state.selected_competitors else [],
            key="competitors_multiselect"
        )
        
        # Update session state
        st.session_state.selected_competitors = competitors
        
        # Show competitors stats
        if competitors and df_full is not None:
            st.caption(f"Đã chọn {len(competitors)} đối thủ:")
            comp_cols = st.columns(min(len(competitors), 3))
            for idx, comp in enumerate(competitors):
                comp_count = len(df_full[df_full["Topic"] == comp])
                with comp_cols[idx % 3]:
                    st.caption(f"• {comp}: {comp_count:,} dòng")
    else:
        st.warning("Vui lòng upload file để chọn thương hiệu")
        main_brand = None
        competitors = []

    # 3. Report period
    st.subheader("3. Kỳ báo cáo")
    col_d, col_t = st.columns([3, 2])
    with col_d:
        report_date = st.date_input(
            "Ngày kết thúc", 
            value=datetime.now(),
            help="Ngày cuối cùng của tuần báo cáo"
        )
    with col_t:
        report_time = st.time_input(
            "Giờ cắt", 
            value=time(23, 59),
            help="Giờ cắt dữ liệu"
        )
    
    report_datetime = datetime.combine(report_date, report_time)
    
    # Calculate 4 weeks
    week1_end = report_datetime
    week1_start = week1_end - timedelta(days=6)
    week2_end = week1_start - timedelta(days=1)
    week2_start = week2_end - timedelta(days=6)
    week3_end = week2_start - timedelta(days=1)
    week3_start = week3_end - timedelta(days=6)
    week4_end = week3_start - timedelta(days=1)
    week4_start = week4_end - timedelta(days=6)
    
    def _fmt(dt): 
        return dt.strftime("%d/%m")
    
    st.caption(
        f"4 tuần phân tích:\n\n"
        f"W4: {_fmt(week4_start)} - {_fmt(week4_end)} (3 tuần trước)\n\n"
        f"W3: {_fmt(week3_start)} - {_fmt(week3_end)} (2 tuần trước)\n\n"
        f"W2: {_fmt(week2_start)} - {_fmt(week2_end)} (Tuần trước)\n\n"
        f"W1: {_fmt(week1_start)} - {_fmt(week1_end)} (Tuần hiện tại)"
    )

    # 4. Slide selection
    st.subheader("4. Chọn slides")
    
    slide_options = {
        "slide_1": "Slide 1: Consumer & Markets",
        "slide_2": "Slide 2: Tổng quan thảo luận",
        "slide_3": "Slide 3: Chỉ số sức khỏe và kênh",
        "slide_4": "Slide 4: Sản phẩm Masan Consumer"
    }
    
    selected_slides = []
    for key, label in slide_options.items():
        if st.checkbox(label, value=True, key=f"chk_{key}"):
            selected_slides.append(key)
    
    # Category detail slides (Slide 5+)
    st.markdown("Slide chi tiết theo ngành hàng:")
    
    # Get available categories from uploaded data
    available_categories = []
    if df_full is not None and "Ngành hàng" in df_full.columns:
        available_categories = sorted(df_full["Ngành hàng"].dropna().unique().tolist())
    
    selected_categories = []
    if available_categories:
        st.caption(f"Có {len(available_categories)} ngành hàng: {', '.join(available_categories)}")
        
        # Quick select buttons
        col_all_cat, col_clear_cat = st.columns(2)
        with col_all_cat:
            if st.button("Chọn tất cả ngành", use_container_width=True, key="select_all_cat"):
                st.session_state.selected_categories = available_categories.copy()
        with col_clear_cat:
            if st.button("Bỏ chọn ngành", use_container_width=True, key="clear_cat"):
                st.session_state.selected_categories = []
        
        # Initialize session state for categories
        if "selected_categories" not in st.session_state:
            st.session_state.selected_categories = []
        
        # Category multiselect
        selected_categories = st.multiselect(
            "Chọn ngành hàng để tạo slide chi tiết",
            options=available_categories,
            default=st.session_state.selected_categories,
            help="Mỗi ngành hàng sẽ tạo 1 slide riêng (Slide 5, 6, 7...)",
            key="categories_multiselect"
        )
        
        # Update session state
        st.session_state.selected_categories = selected_categories
        
        if selected_categories:
            st.success(f"Sẽ tạo {len(selected_categories)} slide chi tiết cho: {', '.join(selected_categories)}")
    
    if not selected_slides and not selected_categories:
        st.warning("Vui lòng chọn ít nhất 1 slide")

    st.divider()
    
    # Generate button
    can_generate = bool(uploaded_file and main_brand and competitors and (selected_slides or selected_categories))
    
    if not uploaded_file:
        st.info("Bước 1: Upload file dữ liệu")
    elif not main_brand:
        st.info("Bước 2: Chọn Main Brand")
    elif not competitors:
        st.info("Bước 3: Chọn ít nhất 1 đối thủ")
    elif not selected_slides and not selected_categories:
        st.info("Bước 4: Chọn ít nhất 1 slide")
    else:
        total_slides = len(selected_slides) + (len(selected_categories) * 4)  # Each category has 4 slides
        st.success(f"Sẵn sàng tạo {total_slides} slide(s)")
    
    generate_btn = st.button(
        f"Tạo {len(selected_slides) + (len(selected_categories) * 4)} slide(s)" if (selected_slides or selected_categories) else "Tạo báo cáo",
        disabled=not can_generate,
        type="primary",
        use_container_width=True,
        help="Tạo báo cáo Masan"
    )
    
    # Reset button
    if st.button("Reset", use_container_width=True):
        st.cache_data.clear()
        st.session_state.update(
            report_generated=False,
            report_data=None,
            prompt_text="",
            llm_client=None,
            selected_competitors=[],
            selected_categories=[]
        )
        st.rerun()

# ── MAIN CONTENT ─────────────────────────────────────────────────────────────
if not can_generate:
    st.info(
        "Hướng dẫn sử dụng:\n\n"
        "1. Upload file Excel chứa dữ liệu\n"
        "2. Chọn Main Brand và các đối thủ\n"
        "3. Chọn kỳ báo cáo\n"
        "4. Nhấn 'Tạo báo cáo'"
    )
    st.stop()

# ── GENERATE REPORT ──────────────────────────────────────────────────────────
if generate_btn:
    st.session_state.report_generated = False
    
    total_slides = len(selected_slides) + (len(selected_categories) * 4)  # Each category has 4 slides
    
    with st.status(f"Đang tạo {total_slides} slide(s)...", expanded=True) as status:
        try:
            # Initialize LLM client
            st.write("⚙️ Khởi tạo LLM client...")
            if not st.session_state.llm_client:
                st.session_state.llm_client = LLMClient(
                    api_key=API_KEY, 
                    base_url=BASE_URL,
                    model=MODEL
                )
            llm_client = st.session_state.llm_client
            
            # Prepare report data
            report_data = {
                "report_metadata": {
                    "report_date": report_datetime.strftime("%Y-%m-%d"),
                    "main_brand": main_brand,
                    "competitors": competitors,
                    "selected_categories": selected_categories,
                }
            }
            
            # Generate Slide 1
            if "slide_1" in selected_slides:
                st.write("Tạo Slide 1: Consumer & Markets...")
                slide1_generator = Slide01MasanMarket(llm_client)
                slide1_data = slide1_generator.generate(
                    df=df_full,
                    main_brand=main_brand,
                    competitors=competitors,
                    report_date=report_datetime.strftime("%Y-%m-%d")
                )
                report_data["slide_1_market"] = slide1_data
            
            # Generate Slide 2
            if "slide_2" in selected_slides:
                st.write("Tạo Slide 2: Tổng quan thảo luận...")
                slide2_generator = Slide02DiscussionOverview(llm_client)
                all_brands = [main_brand] + competitors
                slide2_data = slide2_generator.generate(
                    df=df_full,
                    brands=all_brands,
                    current_week_start=week1_start,
                    current_week_end=week1_end,
                    previous_week_start=week2_start,
                    previous_week_end=week2_end
                )
                report_data["slide_2_discussion"] = slide2_data
            
            # Generate Slide 3
            if "slide_3" in selected_slides:
                st.write("Tạo Slide 3: Chỉ số sức khỏe và kênh...")
                slide3_generator = Slide03HealthChannels(llm_client)
                slide3_data = slide3_generator.generate(
                    df=df_full,
                    main_brand=main_brand,
                    competitors=competitors,
                    week_start=week1_start,
                    week_end=week1_end
                )
                report_data["slide_3_health"] = slide3_data
            
            # Generate Slide 4
            if "slide_4" in selected_slides:
                st.write("Tạo Slide 4: Sản phẩm Masan Consumer...")
                slide4_generator = Slide04Products(llm_client)
                slide4_data = slide4_generator.generate(
                    df=df_full,
                    current_week_start=week1_start,
                    current_week_end=week1_end,
                    previous_week_start=week2_start,
                    previous_week_end=week2_end
                )
                report_data["slide_4_products"] = slide4_data
            
            # Generate Category Detail Slides (Slide 5+)
            if selected_categories:
                st.write(f"Tạo {len(selected_categories) * 4} slide chi tiết theo ngành hàng...")
                slide5_generator = Slide05CategoryDetail(llm_client)
                slide6_generator = Slide06CategoryChannels(llm_client)
                slide7_generator = Slide07CategorySentiment(llm_client)
                slide8_generator = Slide08CategoryTrends(llm_client)
                
                category_slides = {}
                for idx, category in enumerate(selected_categories):
                    slide_num = 5 + (idx * 4)
                    
                    # Slide 5.x: Category detail
                    st.write(f"  └─ Slide {slide_num}: {category} - Chi tiết...")
                    category_data = slide5_generator.generate(
                        df=df_full,
                        category_name=category,
                        week_start=week1_start,
                        week_end=week1_end
                    )
                    
                    # Slide 6.x: Category channels
                    st.write(f"  └─ Slide {slide_num + 1}: {category} - Kênh...")
                    channels_data = slide6_generator.generate(
                        df=df_full,
                        category_name=category,
                        week_start=week1_start,
                        week_end=week1_end
                    )
                    
                    # Slide 7.x: Category sentiment
                    st.write(f"  └─ Slide {slide_num + 2}: {category} - Sắc thái...")
                    sentiment_data = slide7_generator.generate(
                        df=df_full,
                        category_name=category,
                        week_start=week1_start,
                        week_end=week1_end
                    )
                    
                    # Slide 8.x: Category trends
                    st.write(f"  └─ Slide {slide_num + 3}: {category} - Xu hướng...")
                    trends_data = slide8_generator.generate(
                        df=df_full,
                        category_name=category,
                        week_start=week1_start,
                        week_end=week1_end
                    )
                    
                    category_slides[category] = {
                        "detail": category_data,
                        "channels": channels_data,
                        "sentiment": sentiment_data,
                        "trends": trends_data
                    }
                
                report_data["category_slides"] = category_slides
            
            # Build prompt
            st.write("📝 Tạo prompt...")
            prompt = generate_masan_prompt(report_data)
            
            # Save to session state
            st.session_state.report_data = report_data
            st.session_state.prompt_text = prompt
            st.session_state.report_generated = True
            
            status.update(label="Hoàn thành!", state="complete")
            
        except Exception as e:
            st.error(f"Lỗi khi tạo báo cáo: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            st.stop()

# ── DISPLAY RESULTS ──────────────────────────────────────────────────────────
if not st.session_state.report_generated:
    st.stop()

data = st.session_state.report_data

# Header
st.markdown(f"# Báo cáo Masan")
st.caption(f"Main Brand: {main_brand} | Đối thủ: {', '.join(competitors)}")

# Check which slides were generated
has_slide1 = "slide_1_market" in data
has_slide2 = "slide_2_discussion" in data
has_slide3 = "slide_3_health" in data
has_slide4 = "slide_4_products" in data
has_category_slides = "category_slides" in data

slide_count = sum([has_slide1, has_slide2, has_slide3, has_slide4])
if has_category_slides:
    slide_count += len(data["category_slides"]) * 4  # Each category has 4 slides

slide_names = []
if has_slide1:
    slide_names.append("Slide 1 (Consumer & Markets)")
if has_slide2:
    slide_names.append("Slide 2 (Tổng quan thảo luận)")
if has_slide3:
    slide_names.append("Slide 3 (Sức khỏe & Kênh)")
if has_slide4:
    slide_names.append("Slide 4 (Sản phẩm)")
if has_category_slides:
    categories = list(data["category_slides"].keys())
    slide_names.append(f"Slide 5-{4+(len(categories)*4)} ({len(categories)} ngành, {len(categories)*4} slides)")

if slide_count > 0:
    st.info(f"Đã tạo {slide_count} slide(s): {', '.join(slide_names)}")

st.divider()

# Create tabs dynamically
tab_labels = []
if has_slide1:
    tab_labels.append("Slide 1: Consumer & Markets")
if has_slide2:
    tab_labels.append("Slide 2: Tổng quan thảo luận")
if has_slide3:
    tab_labels.append("Slide 3: Sức khỏe & Kênh")
if has_slide4:
    tab_labels.append("Slide 4: Sản phẩm")

# Add category detail tabs
if has_category_slides:
    category_slides = data["category_slides"]
    slide_num = 5
    for category in category_slides.keys():
        tab_labels.append(f"Slide {slide_num}: {category} - Chi tiết")
        tab_labels.append(f"Slide {slide_num + 1}: {category} - Kênh")
        tab_labels.append(f"Slide {slide_num + 2}: {category} - Sắc thái")
        tab_labels.append(f"Slide {slide_num + 3}: {category} - Xu hướng")
        slide_num += 4

tab_labels.append("Prompt")

tabs = st.tabs(tab_labels)
tab_idx = 0

# ── TAB: SLIDE 1 ─────────────────────────────────────────────────────────────
if has_slide1:
    with tabs[tab_idx]:
        tab_idx += 1
        st.subheader("Slide 1: Consumer & Markets")
        
        slide1_data = data["slide_1_market"]
        part1 = slide1_data["part1_main_brand"]
        part2 = slide1_data["part2_competitors"]
        
        # ── SECTION 1: MAIN BRAND OVERVIEW ───────────────────────────────────────
        st.markdown("### Phần 1: Main Brand Overview")
        
        col1, col2, col3 = st.columns(3)
        
        # 1.1 Weekly Buzz Trend
        with col1:
            st.markdown("1. Xu hướng Buzz 4 tuần")
            df_buzz = pd.DataFrame(part1["weekly_buzz_trend"])
            st.bar_chart(df_buzz.set_index("week")["buzz_count"], height=250)
            st.caption("Biểu đồ cột đứng")
        
        # 1.2 Sentiment Distribution
        with col2:
            st.markdown("2. Sentiment tuần hiện tại")
            sentiment = part1["sentiment_distribution"]
            df_sent = pd.DataFrame([
                {"Sentiment": "Positive", "Count": sentiment['positive']['count']},
                {"Sentiment": "Neutral", "Count": sentiment['neutral']['count']},
                {"Sentiment": "Negative", "Count": sentiment['negative']['count']},
            ])
            st.bar_chart(df_sent.set_index("Sentiment")["Count"], height=250)
            st.metric("Tổng Buzz", f"{sentiment['total_buzz']:,}")
            st.caption("Biểu đồ donut (tổng ở giữa)")
        
        # 1.3 Channel Distribution
        with col3:
            st.markdown("3. Phân bố Kênh")
            df_channel = pd.DataFrame(part1["channel_distribution"])
            if not df_channel.empty:
                st.bar_chart(df_channel.set_index("channel")["count"], height=250)
                st.caption("Biểu đồ donut")
            else:
                st.warning("Không có dữ liệu")
        
        # Channel Insight
        st.info(f"Insight Kênh: {part1['channel_insight']}")
        
        st.divider()
        
        # ── SECTION 2: COMPETITOR COMPARISON ──────────────────────────────────────
        st.markdown("### Phần 2: So sánh với Đối thủ")
        
        col1, col2 = st.columns(2)
        
        # 2.1 Channel by Brand
        with col1:
            st.markdown("4. Kênh theo Brand")
            st.caption("Stacked column chart")
            
            channel_data = part2["channel_distribution"]
            if channel_data:
                all_channels = set()
                for brand_data in channel_data:
                    for ch in brand_data["channels"]:
                        all_channels.add(ch["channel"])
                all_channels = sorted(list(all_channels))
                
                chart_dict = {}
                for brand_data in channel_data:
                    brand = brand_data["brand"]
                    ch_map = {ch["channel"]: ch["percent"] for ch in brand_data["channels"]}
                    chart_dict[brand] = [ch_map.get(ch, 0) for ch in all_channels]
                
                df_channel_chart = pd.DataFrame.from_dict(
                    chart_dict, orient="index", columns=all_channels
                )
                st.bar_chart(df_channel_chart, height=300)
        
        # 2.2 Sentiment by Brand
        with col2:
            st.markdown("5. Sắc thái theo Brand")
            st.caption("Stacked column chart")
            
            sentiment_data = part2["sentiment_distribution"]
            if sentiment_data:
                sentiments = ["Positive", "Neutral", "Negative"]
                
                chart_dict = {}
                for brand_data in sentiment_data:
                    brand = brand_data["brand"]
                    sent_map = {s["sentiment"]: s["percent"] for s in brand_data["sentiments"]}
                    chart_dict[brand] = [sent_map.get(s, 0) for s in sentiments]
                
                df_sentiment_chart = pd.DataFrame.from_dict(
                    chart_dict, orient="index", columns=sentiments
                )
                st.bar_chart(df_sentiment_chart, height=300)
        
        st.divider()
        
        # ── SECTION 3: CONCLUSION ─────────────────────────────────────────────────
        st.markdown("### Phần 3: Đúc kết và Khuyến nghị")
        st.success(slide1_data["conclusion"])
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            current_buzz = part1["weekly_buzz_trend"][-1]["buzz_count"]
            prev_buzz = part1["weekly_buzz_trend"][-2]["buzz_count"] if len(part1["weekly_buzz_trend"]) > 1 else 0
            change = ((current_buzz - prev_buzz) / prev_buzz * 100) if prev_buzz > 0 else 0
            st.metric("Buzz tuần hiện tại", f"{current_buzz:,}", f"{change:+.1f}%" if prev_buzz > 0 else None)
        
        with col2:
            sentiment = part1["sentiment_distribution"]
            pos_pct = sentiment["positive"]["percent"]
            neg_pct = sentiment["negative"]["percent"]
            nsr = ((pos_pct - neg_pct) / (pos_pct + neg_pct) * 100) if (pos_pct + neg_pct) > 0 else 0
            st.metric("NSR", f"{nsr:.1f}%")
        
        with col3:
            top_channel = part1["channel_distribution"][0]["channel"] if part1["channel_distribution"] else "N/A"
            st.metric("Kênh chính", top_channel)

# ── TAB: SLIDE 2 ─────────────────────────────────────────────────────────────
if has_slide2:
    with tabs[tab_idx]:
        tab_idx += 1
        st.subheader("Slide 2: Tổng quan thảo luận")
        
        slide2_data = data["slide_2_discussion"]
        
        # Market Share
        st.markdown("### 1. Thị phần thảo luận")
        market_share = slide2_data["market_share"]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Tổng thảo luận", f"{market_share['total_discussions']:,}")
        with col2:
            df_share = pd.DataFrame(market_share["shares"])
            if not df_share.empty:
                st.bar_chart(df_share.set_index("brand")["percent"], height=200)
        
        st.divider()
        
        # Weekly Comparison
        st.markdown("### 2. So sánh tuần trước vs tuần này")
        weekly_comp = slide2_data["weekly_comparison"]
        df_comp = pd.DataFrame(weekly_comp)
        
        if not df_comp.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(
                    df_comp.rename(columns={
                        "brand": "Brand",
                        "previous_week": "Tuần trước",
                        "current_week": "Tuần này",
                        "change_percent": "Thay đổi (%)"
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            with col2:
                # Show comparison chart
                import plotly.graph_objects as go
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name='Tuần trước',
                    x=df_comp['brand'],
                    y=df_comp['previous_week'],
                    marker_color='lightblue'
                ))
                fig.add_trace(go.Bar(
                    name='Tuần này',
                    x=df_comp['brand'],
                    y=df_comp['current_week'],
                    marker_color='darkblue'
                ))
                fig.update_layout(barmode='group', height=300)
                st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        # Trend Lines
        st.markdown("### 3. Xu hướng thảo luận 2 tuần")
        trend_data = slide2_data["trend_lines"]
        trends = trend_data.get("trends", {})
        peaks = trend_data.get("peak_annotations", {})
        
        if trends:
            # Prepare data for line chart
            all_dates = set()
            for brand_trends in trends.values():
                for point in brand_trends:
                    all_dates.add(point["date"])
            all_dates = sorted(list(all_dates))
            
            # Create dataframe for chart
            chart_data = {}
            for brand, brand_trends in trends.items():
                date_map = {point["date"]: point["count"] for point in brand_trends}
                chart_data[brand] = [date_map.get(date, 0) for date in all_dates]
            
            df_trends = pd.DataFrame(chart_data, index=all_dates)
            st.line_chart(df_trends, height=350)
            
            # Show peak annotations
            if peaks:
                st.markdown("Peak Days với dẫn chứng:")
                for brand, peak in peaks.items():
                    with st.expander(f"{brand} - Peak: {peak['date']} ({peak['count']} buzz)"):
                        st.caption(f"Type: {peak['type']}")
                        st.write(peak['content'])
                        if peak['url']:
                            st.markdown(f"[🔗 Xem bài viết]({peak['url']})")
        
        st.divider()
        
        # Insight
        st.markdown("### Insight nổi bật")
        st.info(slide2_data.get("insight", "Không có insight"))

# ── TAB: SLIDE 3 ─────────────────────────────────────────────────────────────
if has_slide3:
    with tabs[tab_idx]:
        tab_idx += 1
        st.subheader("Slide 3: Chỉ số sức khỏe và kênh thảo luận")
        
        slide3_data = data["slide_3_health"]
        
        # Sentiment + NSR
        st.markdown("### 1. Sắc thái thảo luận và NSR")
        sentiment_nsr = slide3_data["sentiment_nsr"]
        df_sent_nsr = pd.DataFrame(sentiment_nsr)
        
        if not df_sent_nsr.empty:
            col1, col2 = st.columns([2, 1])
            with col1:
                # Stacked bar for sentiment
                df_sent_chart = df_sent_nsr[["brand", "positive_pct", "neutral_pct", "negative_pct"]].set_index("brand")
                st.bar_chart(df_sent_chart, height=300)
            with col2:
                # NSR table
                st.dataframe(
                    df_sent_nsr[["brand", "nsr"]].rename(columns={"brand": "Brand", "nsr": "NSR"}),
                    use_container_width=True,
                    hide_index=True
                )
        
        st.divider()
        
        # Channel Distribution
        st.markdown("### 2. Tỉ trọng kênh thảo luận")
        channel_dist = slide3_data["channel_distribution"]
        
        if channel_dist:
            all_channels = set()
            for item in channel_dist:
                for ch in item.get("channels", []):
                    all_channels.add(ch["channel"])
            all_channels = sorted(list(all_channels))
            
            chart_dict = {}
            for item in channel_dist:
                brand = item["brand"]
                ch_map = {ch["channel"]: ch["percent"] for ch in item.get("channels", [])}
                chart_dict[brand] = [ch_map.get(ch, 0) for ch in all_channels]
            
            df_channel_chart = pd.DataFrame.from_dict(
                chart_dict, orient="index", columns=all_channels
            )
            st.bar_chart(df_channel_chart, height=300)
        
        st.divider()
        
        # Top Sources
        st.markdown("### 3. Top nguồn thảo luận (Đối thủ)")
        top_sources = slide3_data["top_sources"]
        
        if top_sources:
            df_sources = pd.DataFrame(top_sources)
            st.bar_chart(
                df_sources.set_index("site_name")["buzz_count"],
                height=250,
                horizontal=True
            )
            st.dataframe(
                df_sources.rename(columns={
                    "rank": "#",
                    "site_name": "Nguồn",
                    "buzz_count": "Buzz"
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("Không có dữ liệu nguồn")
        
        st.divider()
        
        # Health Table
        st.markdown("### 4. Bảng chỉ số sức khỏe theo chủ đề")
        health_table = slide3_data["health_table"]
        labels = health_table.get("labels", [])
        health_data = health_table.get("data", {})
        
        if labels and health_data:
            # Create dataframe for table
            table_data = []
            for label in labels:
                row = {"Chủ đề (Labels1)": label}
                for brand in slide3_data["brands"]:
                    nsr = health_data.get(brand, {}).get(label)
                    row[brand] = f"{nsr:+.1f}" if nsr is not None else "-"
                table_data.append(row)
            
            df_health = pd.DataFrame(table_data)
            st.dataframe(df_health, use_container_width=True, hide_index=True)
        else:
            st.warning("Không có dữ liệu Labels1")
        
        st.divider()
        
        # Insight
        st.markdown("### Insight")
        insight_text = slide3_data.get("insight", "Không có insight")
        # Split into 2 paragraphs if possible
        paragraphs = insight_text.split("\n\n")
        for para in paragraphs:
            if para.strip():
                st.info(para.strip())


# ── TAB: SLIDE 4 ─────────────────────────────────────────────────────────────
if has_slide4:
    with tabs[tab_idx]:
        tab_idx += 1
        st.subheader("Slide 4: Sản phẩm Masan Consumer")
        
        slide4_data = data["slide_4_products"]
        categories = slide4_data.get("categories", [])
        
        if not categories:
            st.warning("Không có dữ liệu cột 'Ngành hàng' trong file")
        else:
            st.info(f"📦 Phân tích {len(categories)} ngành hàng: {', '.join(categories)}")
            
            # Weekly Comparison
            st.markdown("### 1. Tổng thảo luận - So sánh tuần")
            weekly_comp = slide4_data.get("weekly_comparison", [])
            
            if weekly_comp:
                df_comp = pd.DataFrame(weekly_comp)
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.dataframe(
                        df_comp.rename(columns={
                            "category": "Ngành hàng",
                            "previous_week": "Tuần trước",
                            "current_week": "Tuần này",
                            "change_percent": "Thay đổi (%)"
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
                
                with col2:
                    # Comparison chart
                    import plotly.graph_objects as go
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        name='Tuần trước',
                        x=df_comp['category'],
                        y=df_comp['previous_week'],
                        marker_color='lightcoral'
                    ))
                    fig.add_trace(go.Bar(
                        name='Tuần này',
                        x=df_comp['category'],
                        y=df_comp['current_week'],
                        marker_color='darkred'
                    ))
                    fig.update_layout(barmode='group', height=300)
                    st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # Market Share
            st.markdown("### 2. Thị phần thảo luận theo ngành hàng")
            market_share = slide4_data.get("market_share", [])
            
            if market_share:
                df_share = pd.DataFrame(market_share)
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.dataframe(
                        df_share.rename(columns={
                            "category": "Ngành hàng",
                            "buzz_count": "Buzz",
                            "percent": "%"
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
                
                with col2:
                    # Pie chart
                    import plotly.express as px
                    fig = px.pie(
                        df_share,
                        values='buzz_count',
                        names='category',
                        title='Thị phần theo ngành hàng'
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # Trend Lines
            st.markdown("### 3. Xu hướng thảo luận (2 tuần)")
            trend_data = slide4_data.get("trend_lines", {})
            trends = trend_data.get("trends", {})
            peaks = trend_data.get("peak_annotations", {})
            
            if trends:
                # Prepare data for line chart
                all_dates = set()
                for cat_trends in trends.values():
                    for point in cat_trends:
                        all_dates.add(point["date"])
                all_dates = sorted(list(all_dates))
                
                # Create dataframe for chart
                chart_data = {}
                for category, cat_trends in trends.items():
                    date_map = {point["date"]: point["count"] for point in cat_trends}
                    chart_data[category] = [date_map.get(date, 0) for date in all_dates]
                
                df_trends = pd.DataFrame(chart_data, index=all_dates)
                st.line_chart(df_trends, height=350)
                
                # Show peak annotations
                if peaks:
                    st.markdown("Peak Days với dẫn chứng:")
                    for category, peak in peaks.items():
                        with st.expander(f"{category} - Peak: {peak['date']} ({peak['count']} buzz)"):
                            st.write(peak['content'])
                            if peak['url']:
                                st.markdown(f"[🔗 Xem bài viết]({peak['url']})")
            
            st.divider()
            
            # Overall Sentiment
            st.markdown("### 4. Sắc thái thảo luận tổng thể")
            sentiment = slide4_data.get("overall_sentiment", {})
            
            if sentiment:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Tổng buzz", f"{sentiment.get('total', 0):,}")
                with col2:
                    st.metric("Positive", f"{sentiment.get('positive_pct', 0)}%")
                with col3:
                    st.metric("Negative", f"{sentiment.get('negative_pct', 0)}%")
                with col4:
                    nsr = sentiment.get('nsr')
                    if nsr is not None:
                        st.metric("NSR", f"{nsr:+.1f}%")
                    else:
                        st.metric("NSR", "N/A")
                
                # Sentiment chart
                df_sent = pd.DataFrame([
                    {"Sentiment": "Positive", "Percent": sentiment.get('positive_pct', 0)},
                    {"Sentiment": "Neutral", "Percent": sentiment.get('neutral_pct', 0)},
                    {"Sentiment": "Negative", "Percent": sentiment.get('negative_pct', 0)},
                ])
                st.bar_chart(df_sent.set_index("Sentiment")["Percent"], height=250)
            
            st.divider()
            
            # Insight
            st.markdown("### Insight & Phân tích")
            insight = slide4_data.get("insight", {})
            
            # Positive
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("Điểm tích cực")
                st.success(insight.get("positive", "Không có insight"))
                
                pos_evidence = insight.get("positive_evidence", [])
                if pos_evidence:
                    with st.expander(f"📝 Dẫn chứng ({len(pos_evidence)} bình luận)"):
                        for idx, ev in enumerate(pos_evidence, 1):
                            st.caption(f"{idx}. {ev}")
            
            # Negative
            with col2:
                st.markdown("Điểm cần cải thiện")
                st.warning(insight.get("negative", "Không có insight"))
                
                neg_evidence = insight.get("negative_evidence", [])
                if neg_evidence:
                    with st.expander(f"📝 Dẫn chứng ({len(neg_evidence)} bình luận)"):
                        for idx, ev in enumerate(neg_evidence, 1):
                            st.caption(f"{idx}. {ev}")


# ── TAB: CATEGORY DETAIL SLIDES ──────────────────────────────────────────────
if has_category_slides:
    category_slides = data["category_slides"]
    
    for category_name, category_data_dict in category_slides.items():
        # Slide X: Category Detail
        category_data = category_data_dict["detail"]
        
        with tabs[tab_idx]:
            tab_idx += 1
            st.subheader(f"{category_data['title']}")
            st.caption(category_data['subtitle'])
            
            total_buzz = category_data.get("total_buzz", 0)
            
            if total_buzz == 0:
                st.warning(f"Không có dữ liệu cho ngành {category_name}")
                continue
            
            st.info(f"Tổng thảo luận: {total_buzz:,}")
            
            # Brand SOV
            st.markdown("### 1. Thị phần thảo luận của các thương hiệu")
            st.caption("Biểu đồ Donut - Tổng thảo luận ở giữa")
            
            brand_sov = category_data.get("brand_sov", {})
            brands = brand_sov.get("brands", [])
            
            if brands:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.metric("Tổng thảo luận", f"{brand_sov.get('total', 0):,}")
                    st.dataframe(
                        pd.DataFrame(brands).rename(columns={
                            "brand": "Thương hiệu",
                            "buzz_count": "Buzz",
                            "percent": "%"
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
                
                with col2:
                    # Donut/Pie chart
                    import plotly.graph_objects as go
                    fig = go.Figure(data=[go.Pie(
                        labels=[b["brand"] for b in brands],
                        values=[b["buzz_count"] for b in brands],
                        hole=.4,
                        textinfo='label+percent',
                        textposition='outside'
                    )])
                    fig.update_layout(
                        title="Share of Voice (SOV)",
                        annotations=[dict(text=f'{brand_sov.get("total", 0):,}', x=0.5, y=0.5, font_size=20, showarrow=False)],
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Không có dữ liệu thương hiệu")
            
            st.divider()
            
            # Cate Distribution
            st.markdown("### 2. Thị phần thảo luận theo nhóm sản phẩm")
            st.caption("Biểu đồ Pie")
            
            cate_dist = category_data.get("cate_distribution", [])
            
            if cate_dist:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.dataframe(
                        pd.DataFrame(cate_dist).rename(columns={
                            "cate": "Nhóm sản phẩm",
                            "buzz_count": "Buzz",
                            "percent": "%"
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
                
                with col2:
                    import plotly.express as px
                    fig = px.pie(
                        pd.DataFrame(cate_dist),
                        values='buzz_count',
                        names='cate',
                        title='Phân bố theo nhóm sản phẩm'
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Không có dữ liệu nhóm sản phẩm")
            
            st.divider()
            
            # Top Products
            st.markdown("### 3. Top sản phẩm theo lượng thảo luận")
            st.caption("Top 10 sản phẩm được thảo luận nhiều nhất")
            
            top_products = category_data.get("top_products", [])
            
            if top_products:
                df_products = pd.DataFrame(top_products)
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.dataframe(
                        df_products.rename(columns={
                            "rank": "#",
                            "product": "Sản phẩm",
                            "buzz_count": "Buzz"
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
                
                with col2:
                    # Horizontal bar chart
                    fig = go.Figure(go.Bar(
                        x=df_products['buzz_count'],
                        y=df_products['product'],
                        orientation='h',
                        text=df_products['buzz_count'],
                        textposition='outside'
                    ))
                    fig.update_layout(
                        title="Top 10 sản phẩm",
                        xaxis_title="Buzz",
                        yaxis_title="",
                        height=400,
                        yaxis={'categoryorder':'total ascending'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Không có dữ liệu sản phẩm")
            
            st.divider()
            
            # Insight
            st.markdown("### Insight & Phân tích")
            
            insight = category_data.get("insight", {})
            para1 = insight.get("paragraph1", "Không có insight")
            para2 = insight.get("paragraph2", "Không có insight")
            
            st.markdown("Vị thế thị trường:")
            st.info(para1)
            
            st.markdown("Hiệu suất sản phẩm & Khuyến nghị:")
            st.success(para2)
        
        # Slide X+1: Category Channels
        channels_data = category_data_dict["channels"]
        
        with tabs[tab_idx]:
            tab_idx += 1
            st.subheader(f"{channels_data['title']}")
            st.caption(channels_data['subtitle'])
            
            total_buzz_ch = channels_data.get("total_buzz", 0)
            
            if total_buzz_ch == 0:
                st.warning(f"Không có dữ liệu kênh cho ngành {category_name}")
                continue
            
            st.info(f"Tổng thảo luận: {total_buzz_ch:,}")
            st.caption("Layout: 2 charts trên cùng 1 hàng, insight ở dưới")
            
            col1, col2 = st.columns(2)
            
            # Chart 1: Top Sources
            with col1:
                st.markdown("### 1. Top nguồn theo thảo luận")
                
                top_sources = channels_data.get("top_sources", [])
                
                if top_sources:
                    df_sources = pd.DataFrame(top_sources)
                    
                    # Horizontal bar chart
                    fig = go.Figure(go.Bar(
                        x=df_sources['buzz_count'],
                        y=df_sources['source'],
                        orientation='h',
                        text=df_sources['buzz_count'],
                        textposition='outside'
                    ))
                    fig.update_layout(
                        title="Top 5 nguồn",
                        xaxis_title="Buzz",
                        yaxis_title="",
                        height=350,
                        yaxis={'categoryorder':'total ascending'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(
                        df_sources.rename(columns={
                            "rank": "#",
                            "source": "Nguồn",
                            "buzz_count": "Buzz"
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.warning("Không có dữ liệu nguồn")
            
            # Chart 2: Channel Distribution
            with col2:
                st.markdown("### 2. Tỉ trọng kênh theo brand")
                
                channel_dist = channels_data.get("channel_distribution", [])
                
                if channel_dist:
                    # Prepare data for stacked bar
                    channels_list = ["Facebook", "Fanpage", "Forum", "News", "Khác"]
                    brands_list = [item["brand"] for item in channel_dist]
                    
                    chart_data = {}
                    for channel in channels_list:
                        chart_data[channel] = []
                        for brand_data in channel_dist:
                            ch_pct = next((ch["percent"] for ch in brand_data["channels"] if ch["channel"] == channel), 0)
                            chart_data[channel].append(ch_pct)
                    
                    df_channel_chart = pd.DataFrame(chart_data, index=brands_list)
                    st.bar_chart(df_channel_chart, height=350)
                    
                    # Show details
                    with st.expander("Chi tiết phân bố kênh"):
                        for brand_data in channel_dist:
                            st.markdown(f"{brand_data['brand']} ({brand_data['total']:,} buzz)")
                            for ch in brand_data["channels"]:
                                if ch["count"] > 0:
                                    st.caption(f"  • {ch['channel']}: {ch['count']:,} ({ch['percent']}%)")
                else:
                    st.warning("Không có dữ liệu kênh")
            
            st.divider()
            
            # Insight
            st.markdown("### Insight & Phân tích")
            
            insight_ch = channels_data.get("insight", {})
            para1_ch = insight_ch.get("paragraph1", "Không có insight")
            para2_ch = insight_ch.get("paragraph2", "Không có insight")
            para3_ch = insight_ch.get("paragraph3", "Không có insight")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("Tổng quan kênh:")
                st.info(para1_ch)
            
            with col2:
                st.markdown("Nguồn nổi bật:")
                st.info(para2_ch)
            
            with col3:
                st.markdown("Chiến lược & Khuyến nghị:")
                st.success(para3_ch)
        
        # Slide X+2: Category Sentiment
        sentiment_data = category_data_dict["sentiment"]
        
        with tabs[tab_idx]:
            tab_idx += 1
            st.subheader(f"{sentiment_data['title']}")
            st.caption(sentiment_data['subtitle'])
            
            total_buzz_sent = sentiment_data.get("total_buzz", 0)
            
            if total_buzz_sent == 0:
                st.warning(f"Không có dữ liệu sắc thái cho ngành {category_name}")
                continue
            
            st.info(f"Tổng thảo luận: {total_buzz_sent:,}")
            st.caption("Layout: Biểu đồ full size hàng ngang, insight ở dưới")
            
            # Sentiment + NSR Chart
            st.markdown("### Sắc thái và NSR theo thương hiệu")
            
            sentiment_nsr = sentiment_data.get("sentiment_nsr", [])
            
            if sentiment_nsr:
                # Prepare data for chart
                brands_list = [item["brand"] for item in sentiment_nsr]
                pos_pcts = [item["positive_pct"] for item in sentiment_nsr]
                neu_pcts = [item["neutral_pct"] for item in sentiment_nsr]
                neg_pcts = [item["negative_pct"] for item in sentiment_nsr]
                nsrs = [item["nsr"] if item["nsr"] is not None else 0 for item in sentiment_nsr]
                
                # Create combined chart
                import plotly.graph_objects as go
                from plotly.subplots import make_subplots
                
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                # Add stacked bars
                fig.add_trace(
                    go.Bar(name='Positive', x=brands_list, y=pos_pcts, marker_color='#28a745'),
                    secondary_y=False
                )
                fig.add_trace(
                    go.Bar(name='Neutral', x=brands_list, y=neu_pcts, marker_color='#ffc107'),
                    secondary_y=False
                )
                fig.add_trace(
                    go.Bar(name='Negative', x=brands_list, y=neg_pcts, marker_color='#dc3545'),
                    secondary_y=False
                )
                
                # Add NSR line
                fig.add_trace(
                    go.Scatter(name='NSR', x=brands_list, y=nsrs, mode='lines+markers',
                              marker=dict(size=10, color='#0045C4'),
                              line=dict(width=3, color='#0045C4')),
                    secondary_y=True
                )
                
                # Update layout
                fig.update_layout(
                    barmode='stack',
                    title='Sắc thái (%) và NSR theo thương hiệu',
                    xaxis_title='Thương hiệu',
                    height=500,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                fig.update_yaxes(title_text="Sentiment (%)", secondary_y=False, range=[0, 100])
                fig.update_yaxes(title_text="NSR", secondary_y=True, range=[-100, 100])
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show data table
                with st.expander("Chi tiết dữ liệu"):
                    df_sentiment = pd.DataFrame(sentiment_nsr)
                    st.dataframe(
                        df_sentiment[[
                            "brand", "total", "positive_pct", "neutral_pct", 
                            "negative_pct", "nsr"
                        ]].rename(columns={
                            "brand": "Thương hiệu",
                            "total": "Buzz",
                            "positive_pct": "Positive %",
                            "neutral_pct": "Neutral %",
                            "negative_pct": "Negative %",
                            "nsr": "NSR"
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
            else:
                st.warning("Không có dữ liệu sentiment")
            
            st.divider()
            
            # Insight
            st.markdown("### Insight & Phân tích")
            insight_sent = sentiment_data.get("insight", "Không có insight")
            st.info(insight_sent)
        
        # Slide X+3: Category Trends
        trends_data = category_data_dict["trends"]
        
        with tabs[tab_idx]:
            tab_idx += 1
            st.subheader(f"{trends_data['title']}")
            st.caption(trends_data['subtitle'])
            
            total_buzz_trends = trends_data.get("total_buzz", 0)
            
            if total_buzz_trends == 0:
                st.warning(f"Không có dữ liệu xu hướng cho ngành {category_name}")
                continue
            
            st.info(f"Tổng thảo luận: {total_buzz_trends:,}")
            
            # Trend Lines
            st.markdown("### Xu hướng thảo luận theo ngày")
            
            trends = trends_data.get("trends", {})
            peaks = trends_data.get("peak_annotations", {})
            
            if trends:
                # Prepare data for line chart
                all_dates = set()
                for brand_trends in trends.values():
                    for point in brand_trends:
                        all_dates.add(point["date"])
                all_dates = sorted(list(all_dates))
                
                # Create dataframe for chart
                chart_data = {}
                for brand, brand_trends in trends.items():
                    date_map = {point["date"]: point["count"] for point in brand_trends}
                    chart_data[brand] = [date_map.get(date, 0) for date in all_dates]
                
                df_trends = pd.DataFrame(chart_data, index=all_dates)
                st.line_chart(df_trends, height=400)
                
                # Show peak annotations
                if peaks:
                    st.markdown("Peak Days với dẫn chứng:")
                    
                    for brand, peak in peaks.items():
                        with st.expander(f"{brand} - Peak: {peak['date']} ({peak['count']} buzz)"):
                            st.caption(f"Type: {peak['type']}")
                            st.write(peak['content'])
                            if peak['url']:
                                st.markdown(f"[🔗 Xem bài viết]({peak['url']})")
                
                # Show trend data table
                with st.expander("Chi tiết dữ liệu xu hướng"):
                    for brand, brand_trends in trends.items():
                        st.markdown(f"{brand}")
                        df_brand_trend = pd.DataFrame(brand_trends)
                        st.dataframe(
                            df_brand_trend.rename(columns={
                                "date": "Ngày",
                                "count": "Buzz"
                            }),
                            use_container_width=True,
                            hide_index=True
                        )
            else:
                st.warning("Không có dữ liệu xu hướng")
            
            st.divider()
            
            # Insight
            st.markdown("### Insight & Phân tích")
            insight_trends = trends_data.get("insight", "Không có insight")
            st.info(insight_trends)




# ── TAB: PROMPT ──────────────────────────────────────────────────────────────
with tabs[tab_idx if has_slide1 or has_slide2 or has_slide3 or has_slide4 or has_category_slides else 0]:
    st.subheader("Prompt cho Slide Platform")
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Tải Prompt (.txt)",
            st.session_state.prompt_text,
            file_name=f"masan_weekly_{report_date:%Y%m%d}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col2:
        st.download_button(
            "Tải JSON Data",
            json.dumps(data, ensure_ascii=False, indent=2),
            file_name=f"masan_weekly_{report_date:%Y%m%d}.json",
            mime="application/json",
            use_container_width=True
        )
    
    st.code(st.session_state.prompt_text, language=None, wrap_lines=True)
