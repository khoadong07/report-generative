#!/usr/bin/env python3
"""
Streamlit App – Weekly Report Generator
"""

import streamlit as st
import os
import json
import tempfile
import pandas as pd
from datetime import datetime, timedelta, time
from pathlib import Path
from dotenv import load_dotenv
import sys

sys.path.insert(0, '/app')

# ── Reload modules in dev ────────────────────────────────────────────────────
import importlib
for _mod in [
    'generators.weekly.slide_generators_weekly',
    'generators.weekly.report_generator_weekly',
    'generators.weekly.generate_slide_prompt_weekly',
    'core.data_loader',
    'generators.weekly.prompts_weekly',
]:
    if _mod in sys.modules:
        importlib.reload(sys.modules[_mod])

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

from weekly_report.orchestrator import WeeklyReportOrchestrator, ALL_SLIDES
from weekly_report.prompt_builder import generate_complete_prompt
from core.data_loader import DataLoader
from core.config import TEXT_COLUMNS, METRIC_COLUMNS

SLIDE_LABELS = {
    "slide_1":  "1 · Tổng quan KPIs",
    "slide_2":  "2 · Trendline 7 ngày",
    "slide_3":  "3 · Phân bổ kênh",
    "slide_4":  "4 · Top nguồn",
    "slide_5":  "5 · Top bài đăng",
    "slide_6":  "6 · Sentiment",
    "slide_7":  "7 · Chủ đề tích cực",
    "slide_8":  "8 · Bài đăng tích cực",
    "slide_9":  "9 · Chủ đề tiêu cực",
    "slide_10": "10 · Bài đăng tiêu cực",
    "slide_11": "11 · So sánh thương hiệu",
    "slide_12": "12 · Trendline nhiều brand",
    "slide_13": "13 · Phân bổ kênh truyền thông",
    "slide_14": "14 · Top nguồn thảo luận",
    "slide_15": "15 · Sắc thái theo Topic",
    "slide_16": "16 · Top bài bình luận cao",
}
LLM_SLIDES = {
    "slide_1", "slide_2", "slide_3", "slide_6",
    "slide_7", "slide_9", "slide_11", "slide_13", "slide_15",
}

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Weekly Report Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    .stTabs [data-baseweb="tab"] { font-size: 0.8rem; padding: 6px 10px; }
    .metric-card { background: #f8f9fa; border-radius: 8px; padding: 12px; text-align: center; }
    div[data-testid="stMetric"] { background: #f8f9fa; border-radius: 8px; padding: 10px; }
</style>
""", unsafe_allow_html=True)


# ── Cached data loader ───────────────────────────────────────────────────────
@st.cache_data(show_spinner="Đang đọc file...")
def load_excel(file_bytes: bytes) -> pd.DataFrame:
    """Load và preprocess Excel, cache theo nội dung file."""
    import io
    loader = DataLoader(io.BytesIO(file_bytes), TEXT_COLUMNS, METRIC_COLUMNS)
    return loader.preprocess()


# ── Session state defaults ───────────────────────────────────────────────────
for key, default in {
    "report_generated": False,
    "report_data": None,
    "prompt_text": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.title("📊 Weekly Report")

    if not (API_KEY and BASE_URL):
        st.error("Thiếu API credentials trong .env")
        st.stop()
    st.success("API credentials ✓", icon="✅")
    st.divider()

    # ── 1. Upload ────────────────────────────────────────────────────────────
    st.subheader("1. Upload dữ liệu")
    uploaded_file = st.file_uploader("File Excel (.xlsx / .xls)", type=["xlsx", "xls"])

    df_full = None
    available_topics = []

    if uploaded_file:
        file_bytes = uploaded_file.getvalue()
        try:
            df_full = load_excel(file_bytes)
            available_topics = sorted(df_full["Topic"].dropna().unique().tolist())
            st.caption(f"✅ {len(df_full):,} dòng · {len(available_topics)} topics")
        except Exception as e:
            st.error(f"Lỗi đọc file: {e}")
            st.stop()

    # ── 2. Brand & Competitors ───────────────────────────────────────────────
    st.subheader("2. Thương hiệu")

    if available_topics:
        brand_name = st.selectbox("Brand chính", options=available_topics)
        competitor_options = [t for t in available_topics if t != brand_name]
        competitor_brands = st.multiselect(
            "Đối thủ (Slide 11–15)",
            options=competitor_options,
            help="Để trống = so sánh tất cả topics trong file",
        )
    else:
        brand_name = st.text_input("Brand name (cột Topic)", placeholder="Nhập tên brand...")
        competitor_brands = []

    # ── 3. Thời gian ─────────────────────────────────────────────────────────
    st.subheader("3. Kỳ báo cáo")

    col_d, col_t = st.columns([3, 2])
    with col_d:
        report_date = st.date_input("Ngày kết thúc", value=datetime.now())
    with col_t:
        report_time = st.time_input("Giờ cắt", value=time(15, 0))

    week1_end = datetime.combine(report_date, report_time)
    week2_end = week1_end - timedelta(days=7)
    week3_end = week2_end - timedelta(days=7)
    week4_end = week3_end - timedelta(days=7)

    def _fmt(dt): return dt.strftime("%d/%m %H:%M")
    st.caption(
        f"W1: {_fmt(week1_end - timedelta(days=7))} → {_fmt(week1_end)}  \n"
        f"W2: {_fmt(week2_end - timedelta(days=7))} → {_fmt(week2_end)}  \n"
        f"W3: {_fmt(week3_end - timedelta(days=7))} → {_fmt(week3_end)}  \n"
        f"W4: {_fmt(week4_end - timedelta(days=7))} → {_fmt(week4_end)}"
    )

    # ── 4. Tuỳ chọn ──────────────────────────────────────────────────────────
    st.subheader("4. Tuỳ chọn")
    show_interactions = st.toggle("Hiển thị Interactions", value=True,
                                   help="Bật: KPI đầy đủ (reactions/shares/comments). Tắt: chỉ tổng đề cập.")

    # ── 5. Chọn slides ────────────────────────────────────────────────────────
    st.subheader("5. Chọn slides cần build")
    col_all, col_none = st.columns(2)
    with col_all:
        if st.button("✅ Tất cả", use_container_width=True):
            for k in ALL_SLIDES: st.session_state[f"chk_{k}"] = True
    with col_none:
        if st.button("☐ Bỏ chọn", use_container_width=True):
            for k in ALL_SLIDES: st.session_state[f"chk_{k}"] = False
    for k in ALL_SLIDES:
        if f"chk_{k}" not in st.session_state:
            st.session_state[f"chk_{k}"] = True

    selected_slides = []
    for k in ALL_SLIDES:
        icon = "🤖" if k in LLM_SLIDES else "⚡"
        if st.checkbox(f"{icon} {SLIDE_LABELS[k]}", key=f"chk_{k}"):
            selected_slides.append(k)
    st.caption("🤖 = cần LLM  ·  ⚡ = data only")

    st.divider()

    can_generate = bool(uploaded_file and brand_name and selected_slides)
    generate_btn = st.button(
        f"🚀 Build {len(selected_slides)} slide(s)",
        disabled=not can_generate,
        type="primary",
        use_container_width=True,
    )
    rebuild_btn = False
    if st.session_state.report_generated:
        rebuild_btn = st.button(
            f"🔁 Rebuild {len(selected_slides)} slide đã chọn",
            disabled=not selected_slides, use_container_width=True,
            help="Chạy lại slides đã chọn, merge vào báo cáo hiện tại",
        )

    if st.button("🔄 Reset", use_container_width=True):
        st.cache_data.clear()
        for k in ["report_generated", "report_data", "prompt_text"]:
            st.session_state[k] = False if k == "report_generated" else (None if k == "report_data" else "")
        st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# MAIN AREA – trước khi generate
# ════════════════════════════════════════════════════════════════════════════
if not can_generate:
    st.info("👈 Upload file Excel và chọn brand name để bắt đầu.", icon="ℹ️")
    st.stop()


def _run_build(keys: list, existing_report=None):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name
    try:
        with st.status(f"Đang build {len(keys)} slide(s)...", expanded=True) as status:
            st.write("⚙️ Khởi tạo orchestrator...")
            orch = WeeklyReportOrchestrator(
                api_key=API_KEY, base_url=BASE_URL,
                file_path=tmp_path, brand_name=brand_name,
                week1_end=week1_end.strftime("%Y-%m-%d %H:%M:%S"),
                week2_end=week2_end.strftime("%Y-%m-%d %H:%M:%S"),
                week3_end=week3_end.strftime("%Y-%m-%d %H:%M:%S"),
                week4_end=week4_end.strftime("%Y-%m-%d %H:%M:%S"),
                show_interactions=show_interactions,
                competitor_brands=competitor_brands if competitor_brands else None,
            )
            llm_n  = sum(1 for k in keys if k in LLM_SLIDES)
            data_n = len(keys) - llm_n
            st.write(f"🤖 {llm_n} LLM slide(s) + ⚡ {data_n} data slide(s)...")
            report_data = orch.generate_slides(keys, existing_report=existing_report)
            st.write("📝 Tạo prompt...")
            st.session_state.report_data = report_data
            st.session_state.prompt_text = generate_complete_prompt(report_data)
            st.session_state.report_generated = True
            status.update(label="✅ Hoàn thành!", state="complete")
    except Exception as e:
        st.error(str(e))
        import traceback
        st.code(traceback.format_exc())
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


# ── Generate ─────────────────────────────────────────────────────────────────
if generate_btn:
    st.session_state.report_generated = False
    _run_build(selected_slides)

if rebuild_btn:
    _run_build(selected_slides, existing_report=st.session_state.report_data)


# ════════════════════════════════════════════════════════════════════════════
# RESULTS
# ════════════════════════════════════════════════════════════════════════════
if not st.session_state.report_generated:
    st.stop()

data = st.session_state.report_data
built_keys = [k for k in ALL_SLIDES if k in data]
week1_start = week1_end - timedelta(days=7)

st.markdown(f"### 📊 Báo cáo tuần — **{brand_name}**")
st.caption(f"Kỳ: {week1_start.strftime('%d/%m/%Y')} → {week1_end.strftime('%d/%m/%Y')}  ·  Đã build: {len(built_keys)}/16 slides")
st.divider()

tab_labels = [SLIDE_LABELS[k] for k in built_keys] + ["📄 Prompt"]
tabs = st.tabs(tab_labels)

def _tab(key):
    if key not in built_keys: return None
    return tabs[built_keys.index(key)]

# Slide 1
if (t := _tab("slide_1")):
    with t:
        s = data["slide_1"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        cols = st.columns(len(s["current_week_metrics"]))
        for i, m in enumerate(s["current_week_metrics"]):
            with cols[i]:
                delta = f"{m['change_percent']:+.1f}%" if "change_percent" in m else None
                st.metric(m["label"], f"{m['value']:,}", delta)
        st.markdown("**So sánh 4 tuần**")
        df_cmp = pd.DataFrame(s["weekly_comparison"])
        st.bar_chart(df_cmp.set_index("week")["total_mentions"].sort_values(), height=220)
        st.dataframe(df_cmp.rename(columns={"week":"Tuần","total_mentions":"Đề cập","growth_rate":"Tăng trưởng (%)"}),
                     use_container_width=True, hide_index=True)
        st.info(s["insight"])

# Slide 2
if (t := _tab("slide_2")):
    with t:
        s = data["slide_2"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        df_trend = pd.DataFrame(s["trendline"])
        df_trend["date"] = pd.to_datetime(df_trend["date"])
        st.line_chart(df_trend.set_index("date")["mentions"], height=250)
        st.dataframe(df_trend.rename(columns={"date":"Ngày","mentions":"Đề cập"}),
                     use_container_width=True, hide_index=True)
        st.info(s["insight"])

# Slide 3
if (t := _tab("slide_3")):
    with t:
        s = data["slide_3"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Phân bổ kênh**")
            df_ch = pd.DataFrame(s["channel_distribution"])
            st.bar_chart(df_ch.set_index("Channel")["count"].sort_values(), height=220)
            st.dataframe(df_ch, use_container_width=True, hide_index=True)
        with c2:
            st.markdown("**Top 10 nguồn**")
            df_src = pd.DataFrame(s["top_sources"])
            st.bar_chart(df_src.set_index("SiteName")["count"].sort_values(), height=220)
            st.dataframe(df_src.rename(columns={"SiteName":"Nguồn","count":"Đề cập"}),
                         use_container_width=True, hide_index=True)
        st.info(s["insight"])

# Slide 4
if (t := _tab("slide_4")):
    with t:
        s = data["slide_4"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        df_t = pd.DataFrame(s["table_rows"])
        if s.get("show_interactions", True) and "total_engagement" in df_t.columns:
            df_t = df_t.rename(columns={"stt":"#","source_name":"Nguồn","total_engagement":"Tổng tương tác",
                                         "reactions":"Reactions","shares":"Shares","comments":"Comments"})
            st.bar_chart(df_t.set_index("Nguồn")["Tổng tương tác"].sort_values(), height=220)
        else:
            df_t = df_t.rename(columns={"stt":"#","source_name":"Nguồn","count":"Đề cập"})
            st.bar_chart(df_t.set_index("Nguồn")["Đề cập"].sort_values(), height=220)
        st.dataframe(df_t, use_container_width=True, hide_index=True)

# Slide 5
if (t := _tab("slide_5")):
    with t:
        s = data["slide_5"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        for row in s["table_rows"]:
            with st.expander(f"#{row['stt']} · {row['site_name']} ({row['channel']}) · {row['published_date'][:10]}"):
                st.write(row["content"][:300])
                st.markdown(f"[🔗 Xem bài]({row['url']})")
                if s.get("show_interactions", True) and "reactions" in row:
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Reactions", f"{row.get('reactions',0):,}")
                    c2.metric("Shares",    f"{row.get('shares',0):,}")
                    c3.metric("Comments",  f"{row.get('comments',0):,}")

# Slide 6
if (t := _tab("slide_6")):
    with t:
        s = data["slide_6"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        c1, c2, c3 = st.columns([2,1,2])
        with c1:
            st.markdown("**Tuần trước**")
            st.bar_chart(pd.DataFrame(s["previous_sentiment"]).set_index("sentiment")["count"].sort_values(), height=180)
            st.metric("NSR", f"{s['previous_nsr']:.1f}%")
        with c2:
            st.metric("NSR hiện tại", f"{s['current_nsr']:.1f}%", f"{s['nsr_growth']:+.2f}%")
            st.caption("NSR = (Pos%-Neg%) / (Pos%+Neg%) x 100")
        with c3:
            st.markdown("**Tuần này**")
            st.bar_chart(pd.DataFrame(s["current_sentiment"]).set_index("sentiment")["count"].sort_values(), height=180)
            st.metric("NSR", f"{s['current_nsr']:.1f}%")
        st.markdown("**Top chủ đề theo sắc thái**")
        df_top = pd.DataFrame(s["top_topics_with_sentiment"])
        st.bar_chart(df_top.set_index("topic")[["negative","neutral","positive"]], height=250)
        st.dataframe(df_top.rename(columns={"topic":"Chủ đề","total":"Tổng",
                                             "negative":"Tiêu cực","neutral":"Trung tính","positive":"Tích cực"}),
                     use_container_width=True, hide_index=True)
        st.info(s["insight"])

# Slide 7
if (t := _tab("slide_7")):
    with t:
        s = data["slide_7"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        df_pos = pd.DataFrame(s["positive_topics"])
        if not df_pos.empty and df_pos["count"].sum() > 0:
            st.bar_chart(df_pos.set_index("Labels1")["count"].sort_values(), height=250)
            st.dataframe(df_pos.rename(columns={"Labels1":"Chủ đề","count":"Đề cập"}),
                         use_container_width=True, hide_index=True)
        else:
            st.warning("Không có dữ liệu tích cực.")
        st.info(s["insight"])

# Slide 8
if (t := _tab("slide_8")):
    with t:
        s = data["slide_8"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        for row in s["table_rows"]:
            with st.expander(f"#{row['stt']} · {row['site_name']} ({row['channel']}) · {row['published_date'][:10]}"):
                st.write(row["content"][:300])
                st.markdown(f"[🔗 Xem bài]({row['url']})")
                st.metric("Bình luận tích cực", f"{row['positive_comments']:,}")

# Slide 9
if (t := _tab("slide_9")):
    with t:
        s = data["slide_9"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        df_neg = pd.DataFrame(s["negative_topics"])
        if not df_neg.empty and df_neg["count"].sum() > 0:
            st.bar_chart(df_neg.set_index("Labels1")["count"].sort_values(), height=250)
            st.dataframe(df_neg.rename(columns={"Labels1":"Chủ đề","count":"Đề cập"}),
                         use_container_width=True, hide_index=True)
        else:
            st.warning("Không có dữ liệu tiêu cực.")
        st.info(s["insight"])

# Slide 10
if (t := _tab("slide_10")):
    with t:
        s = data["slide_10"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        for row in s["table_rows"]:
            with st.expander(f"#{row['stt']} · {row['site_name']} ({row['channel']}) · {row['published_date'][:10]}"):
                st.write(row["content"][:300])
                st.markdown(f"[🔗 Xem bài]({row['url']})")
                st.metric("Bình luận tiêu cực", f"{row['negative_comments']:,}")

# Slide 11
if (t := _tab("slide_11")):
    with t:
        s = data["slide_11"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        st.info(s["insight"])
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Tuần trước**")
            df_prev = pd.DataFrame(s["donut_charts"]["week_before"]["data"])
            st.bar_chart(df_prev[df_prev["mentions"]>0].set_index("brand")["mentions"].sort_values(), height=220)
        with c2:
            st.markdown("**Tuần này**")
            df_curr = pd.DataFrame(s["donut_charts"]["current_week"]["data"])
            st.bar_chart(df_curr[df_curr["mentions"]>0].set_index("brand")["mentions"].sort_values(), height=220)
        st.markdown("**So sánh tăng trưởng**")
        df_bar = pd.DataFrame(s["bar_chart"]["data"]).rename(columns={
            "brand":"Thương hiệu","week_before":"Tuần trước",
            "current_week":"Tuần này","percentage_change":"% Thay đổi",
        })
        st.dataframe(df_bar[["Thương hiệu","Tuần trước","Tuần này","% Thay đổi"]],
                     use_container_width=True, hide_index=True)

# Slide 12
if (t := _tab("slide_12")):
    with t:
        s = data["slide_12"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        dfs = []
        for b in s["brands"]:
            tl = s["trendlines"].get(b, [])
            if not tl: continue
            df_b = pd.DataFrame(tl)
            df_b["date"] = pd.to_datetime(df_b["date"])
            dfs.append(df_b.set_index("date").rename(columns={"mentions": b}))
        if dfs:
            import functools
            df_chart = functools.reduce(lambda a, b: a.join(b, how="outer"), dfs).fillna(0)
            st.line_chart(df_chart, height=320)
        ann_rows = [
            {"Thương hiệu": b, "Ngày peak": v["date"],
             "Lượt": v["mentions"], "Snippet": v["snippet"], "URL": v["url"]}
            for b, v in s["annotations"].items()
        ]
        if ann_rows:
            st.dataframe(pd.DataFrame(ann_rows),
                         column_config={"URL": st.column_config.LinkColumn("URL"),
                                        "Lượt": st.column_config.NumberColumn(format="%d")},
                         use_container_width=True, hide_index=True)

# Slide 13
if (t := _tab("slide_13")):
    with t:
        s = data["slide_13"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        st.markdown("#### Insight theo kênh")
        n_sec = len(s["insight_sections"])
        insight_cols = st.columns(max(n_sec, 1))
        for i, sec in enumerate(s["insight_sections"]):
            with insight_cols[i]:
                color = sec.get("color", "#666666")
                st.markdown(
                    f'<div style="border-left:4px solid {color};padding-left:10px;margin-bottom:8px">'
                    f'<b style="color:{color}">{sec["group"]}</b></div>',
                    unsafe_allow_html=True,
                )
                for topic in sec.get("topics", []):
                    st.caption(f"{topic['label']} – {topic['count']} lượt")
                st.info(sec.get("summary", ""))
        st.divider()
        chart_data = s["stacked_bar_chart"]
        st.markdown(f"#### {chart_data['title']}")
        bar_rows = chart_data["data"]
        if bar_rows:
            all_groups = [leg["group"] for leg in s["channel_legend"]]
            chart_dict = {}
            for row in bar_rows:
                seg_map = {seg["group"]: seg["count"] for seg in row["segments"]}
                chart_dict[row["topic"]] = [seg_map.get(g, 0) for g in all_groups]
            df_bar13 = pd.DataFrame.from_dict(chart_dict, orient="index", columns=all_groups)
            st.bar_chart(df_bar13, height=350)
            table_rows = []
            for row in bar_rows:
                r = {"Topic": row["topic"], "Tổng buzz": row["total"]}
                for seg in row["segments"]:
                    r[seg["group"]] = f"{seg['count']} ({seg['percent']}%)"
                table_rows.append(r)
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
        st.markdown("**Chú giải kênh:**")
        leg_cols = st.columns(len(s["channel_legend"]))
        for i, leg in enumerate(s["channel_legend"]):
            with leg_cols[i]:
                st.markdown(
                    f'<span style="background:{leg["color"]};color:white;padding:3px 10px;'
                    f'border-radius:4px;font-size:0.8rem">{leg["group"]}</span>',
                    unsafe_allow_html=True,
                )

# Slide 14
if (t := _tab("slide_14")):
    with t:
        s = data["slide_14"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        rows = s.get("table", [])
        if rows:
            df14 = pd.DataFrame(rows).rename(columns={
                "stt": "STT", "source_name": "Nguồn",
                "channel": "Kênh truyền thông", "total": "Tổng",
            })
            st.dataframe(df14[["STT","Nguồn","Kênh truyền thông","Tổng"]],
                         use_container_width=True, hide_index=True)
        else:
            st.warning("Không có dữ liệu.")

# Slide 15
if (t := _tab("slide_15")):
    with t:
        s = data["slide_15"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        st.info(s["insight"])
        st.divider()
        chart_data = s["stacked_bar_chart"]
        st.markdown(f"#### {chart_data['title']}")
        bar_rows = chart_data["data"]
        if bar_rows:
            sent_order = [leg["sentiment"] for leg in s["sentiment_legend"]]
            chart_dict = {}
            for row in bar_rows:
                seg_map = {seg["sentiment"]: seg["percent"] for seg in row["segments"]}
                chart_dict[row["topic"]] = [seg_map.get(sent, 0.0) for sent in sent_order]
            df_bar15 = pd.DataFrame.from_dict(chart_dict, orient="index", columns=sent_order)
            st.bar_chart(df_bar15, height=320, color=["#2A9D5C", "#ADB5BD", "#E63946"])
        leg_cols = st.columns(len(s["sentiment_legend"]))
        for i, leg in enumerate(s["sentiment_legend"]):
            with leg_cols[i]:
                st.markdown(
                    f'<span style="background:{leg["color"]};color:white;padding:3px 14px;'
                    f'border-radius:4px;font-size:0.85rem">{leg["sentiment"]}</span>',
                    unsafe_allow_html=True,
                )
        st.divider()
        st.markdown("#### Bảng tổng hợp theo Topic")
        tbl = s["summary_table"]
        topics = tbl["topics"]
        max_nsr = tbl.get("max_nsr_topic")
        table_rows = []
        for topic in topics:
            nsr_val = tbl["NSR"].get(topic, 0.0)
            nsr_str = f"★ {nsr_val:+.1f}%" if topic == max_nsr else f"{nsr_val:+.1f}%"
            table_rows.append({
                "Topic":                    topic,
                "N (buzz)":                 tbl["N"].get(topic, 0),
                "NSR (%)":                  nsr_str,
                "Chủ đề tích cực nổi bật":  " | ".join(tbl["top_positive"].get(topic, [])) or "—",
                "Chủ đề tiêu cực nổi bật":  " | ".join(tbl["top_negative"].get(topic, [])) or "—",
            })
        st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True,
                     column_config={"N (buzz)": st.column_config.NumberColumn(format="%d")})
        st.markdown("#### Bài viết mẫu theo Topic")
        for topic in topics:
            samples = tbl["sample_posts"].get(topic, [])
            if not samples: continue
            with st.expander(f"📌 {topic} – {len(samples)} mẫu"):
                for post in samples:
                    sent_color = {"Positive": "#2A9D5C", "Negative": "#E63946"}.get(post["sentiment"], "#ADB5BD")
                    st.markdown(
                        f'<span style="background:{sent_color};color:white;padding:2px 8px;'
                        f'border-radius:3px;font-size:0.75rem">{post["sentiment"]}</span> '
                        f'<b>{post["label"]}</b>',
                        unsafe_allow_html=True,
                    )
                    st.caption(post["text"][:250])
                    if post.get("url") and post["url"].startswith("http"):
                        st.markdown(f"[🔗 Xem bài]({post['url']})")
                    st.markdown("---")

# Slide 16
if (t := _tab("slide_16")):
    with t:
        s = data["slide_16"]
        st.subheader(s["title"]); st.caption(s["subtitle"])
        rows = s.get("table", [])
        if rows:
            display_rows = []
            for row in rows:
                display_rows.append({
                    "STT":         row["stt"],
                    "Thương hiệu": row["topic"],
                    "Bài đăng":    row["content"][:200] if row["content"] else "—",
                    "Kênh":        row["channel"],
                    "Nguồn":       row.get("source_name", ""),
                    "Link":        row.get("source_url", ""),
                    "Bình luận":   row["comment_count"],
                })
            df_display = pd.DataFrame(display_rows)
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "STT":       st.column_config.NumberColumn(width="small"),
                    "Bài đăng":  st.column_config.TextColumn(width="large"),
                    "Link":      st.column_config.LinkColumn("🔗 Link"),
                    "Bình luận": st.column_config.NumberColumn(format="%d"),
                },
            )
        else:
            st.warning("Không có dữ liệu bình luận.")

# ── Prompt tab ────────────────────────────────────────────────────────────────
with tabs[-1]:
    st.subheader("📄 Prompt cho slide platform")
    col_txt, col_json = st.columns(2)
    with col_txt:
        st.download_button("⬇️ Tải prompt (.txt)", st.session_state.prompt_text,
                           file_name=f"{brand_name}_weekly_{report_date:%Y%m%d}.txt",
                           use_container_width=True)
    with col_json:
        st.download_button("⬇️ Tải JSON data",
                           json.dumps(data, ensure_ascii=False, indent=2),
                           file_name=f"{brand_name}_weekly_{report_date:%Y%m%d}.json",
                           mime="application/json", use_container_width=True)
    st.code(st.session_state.prompt_text, language=None, wrap_lines=True)

