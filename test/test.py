import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)

# =====================
# CONFIG
# =====================
FILE_PATH = "/content/Nestle_Gerber_15h_labeled.xlsx"

REPORT_DATE = "2026-02-01"
COMPARE_DATE = "2026-01-31"

TOP_N = 6
brand = "Nestlé"

TOPIC_TYPES = [
    "fbPageTopic", "fbGroupTopic", "fbUserTopic", "forumTopic",
    "youtubeTopic", "tiktokTopic", "linkedinTopic",
    "ecommerceTopic", "threadsTopic", "snsTopic"
]

# Get API credentials from environment
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

if not API_KEY or not BASE_URL:
    raise ValueError("API_KEY and BASE_URL must be set in .env file")

# =====================
# INIT LLM CLIENT
# =====================
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# =====================
# LOAD DATA
# =====================
df = pd.read_excel(FILE_PATH)

# =====================
# CLEAN TEXT
# =====================
for col in ["Title", "Content", "Description"]:
    if col in df.columns:
        df[col] = df[col].fillna("").astype(str)

# =====================
# DATE NORMALIZATION
# =====================
df["PublishedDate"] = pd.to_datetime(df["PublishedDate"], errors="coerce")
df = df[df["PublishedDate"].notna()].copy()
df["PublishedDay"] = df["PublishedDate"].dt.date

report_day = pd.to_datetime(REPORT_DATE).date()
compare_day = pd.to_datetime(COMPARE_DATE).date()

report_df = df[df["PublishedDay"] == report_day].copy()
compare_df = df[df["PublishedDay"] == compare_day].copy()

# =====================
# ENSURE NUMERIC
# =====================
for col in ["Reactions", "Shares", "Comments", "Views"]:
    if col in df.columns:
        report_df[col] = pd.to_numeric(report_df[col], errors="coerce").fillna(0)
        compare_df[col] = pd.to_numeric(compare_df[col], errors="coerce").fillna(0)

# =====================
# METRIC FUNCTIONS
# =====================
def pct_change(today, yesterday):
    if yesterday == 0:
        return 0.0 if today == 0 else 100.0
    return round((today - yesterday) / yesterday * 100, 2)

# =====================
# METRICS CALCULATION
# =====================

# Tổng thảo luận = tổng buzz
report_total_buzz = report_df.shape[0]
compare_total_buzz = compare_df.shape[0]
buzz_pct = pct_change(report_total_buzz, compare_total_buzz)

# Tổng bài đăng = Type ∈ TOPIC_TYPES
report_posts = report_df[report_df["Type"].isin(TOPIC_TYPES)].shape[0]
compare_posts = compare_df[compare_df["Type"].isin(TOPIC_TYPES)].shape[0]
post_pct = pct_change(report_posts, compare_posts)

# Reactions
today_reactions = report_df["Reactions"].sum()
yesterday_reactions = compare_df["Reactions"].sum()
reactions_pct = pct_change(today_reactions, yesterday_reactions)

# Shares
today_shares = report_df["Shares"].sum()
yesterday_shares = compare_df["Shares"].sum()
shares_pct = pct_change(today_shares, yesterday_shares)

# Comments = buzz - post
today_comments = report_total_buzz - report_posts
yesterday_comments = compare_total_buzz - compare_posts
comments_pct = pct_change(today_comments, yesterday_comments)

# Total engagement = reactions + shares + comments
today_engagement = today_reactions + today_shares + today_comments
yesterday_engagement = yesterday_reactions + yesterday_shares + yesterday_comments
engagement_pct = pct_change(today_engagement, yesterday_engagement)

# Views
today_views = report_df["Views"].sum()
yesterday_views = compare_df["Views"].sum()
views_pct = pct_change(today_views, yesterday_views)

# =====================
# NEGATIVE TOPIC INSIGHT EXTRACTION
# =====================
df_neg = report_df[
    (report_df["Sentiment"].str.lower() == "negative") &
    (report_df["Type"].isin(TOPIC_TYPES))
].copy()

df_neg["engagement"] = (
    df_neg["Reactions"] +
    df_neg["Shares"] +
    df_neg["Comments"]
)

df_top = (
    df_neg.sort_values("engagement", ascending=False)
          .drop_duplicates(subset=["UrlTopic"])
          .head(TOP_N)
)

# =====================
# BUILD LLM CONTEXT
# =====================
records = []
for _, row in df_top.iterrows():
    records.append(
        f"""
Tiêu đề: {row.get('Title', '')}
Mô tả: {row.get('Description', '')}
Nội dung: {row.get('Content', '')}
Engagement: {row.get('engagement', 0)}
URL: {row.get('UrlTopic', '')}
""".strip()
    )

context_text = "\n\n---\n\n".join(records)

# =====================
# PROMPT
# =====================
prompt = f"""
Bạn là chuyên gia phân tích khủng hoảng truyền thông và social listening.

BỐI CẢNH PHÂN TÍCH:
- Thương hiệu: {brand}
- Thời gian khảo sát: {report_day}
- Tổng thảo luận (buzz): {report_total_buzz}
- So với ngày {compare_day}: {compare_total_buzz} lượt (thay đổi {buzz_pct}%)
- Dữ liệu sử dụng: các bài viết/bình luận NEGATIVE có mức tương tác cao nhất

NHIỆM VỤ:
Viết một đoạn insight tóm tắt tình hình thảo luận trong ngày.

YÊU CẦU BẮT BUỘC:
- Viết đúng 5–6 câu, dạng văn xuôi
- Câu đầu tiên mô tả quy mô & mức độ chú ý
- Các câu sau mô tả diễn biến sự vụ và phản ứng cộng đồng
- Văn phong chuyên nghiệp, trung lập
- Mỗi câu gắn DUY NHẤT 1 URL
- KHÔNG lặp URL
- KHÔNG gạch đầu dòng, KHÔNG tiêu đề

FORMAT:
... [Nguồn: URL]

DỮ LIỆU:
{context_text}
"""

# =====================
# CALL LLM
# =====================
response = client.chat.completions.create(
    model="google/gemma-3-27b-it",
    messages=[
        {"role": "system", "content": "Bạn là chuyên gia crisis & executive insight."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
)

summary = response.choices[0].message.content.strip()

# =====================
# BUILD SLIDE JSON OUTPUT
# =====================
slide_1 = {
    "title": f"Tổng quan về thương hiệu {brand}",
    "subtitle": f"Ngày {report_day} (so sánh với {compare_day})",
    "data": [
        {
            "type": "buzz",
            "label": "Tổng thảo luận",
            "today": report_total_buzz,
            "yesterday": compare_total_buzz,
            "change_pct": buzz_pct
        },
        {
            "type": "post",
            "label": "Tổng bài đăng",
            "today": report_posts,
            "yesterday": compare_posts,
            "change_pct": post_pct
        },
        {
            "type": "engagement",
            "label": "Tổng tương tác",
            "today": today_engagement,
            "yesterday": yesterday_engagement,
            "change_pct": engagement_pct
        },
        {
            "type": "reactions",
            "label": "Lượt reactions",
            "today": today_reactions,
            "yesterday": yesterday_reactions,
            "change_pct": reactions_pct
        },
        {
            "type": "shares",
            "label": "Lượt chia sẻ",
            "today": today_shares,
            "yesterday": yesterday_shares,
            "change_pct": shares_pct
        },
        {
            "type": "comments",
            "label": "Bình luận",
            "today": today_comments,
            "yesterday": yesterday_comments,
            "change_pct": comments_pct
        },
        {
            "type": "views",
            "label": "Lượt xem",
            "today": today_views,
            "yesterday": yesterday_views,
            "change_pct": views_pct
        }
    ],
    "insight": summary
}

# =====================
# OVERVIEW METRICS (FIXED LOGIC)
# =====================

def pct_change(today, yesterday):
    if yesterday == 0:
        return 0.0 if today == 0 else 100.0
    return round((today - yesterday) / yesterday * 100, 2)

# Ensure numeric
for col in ["Reactions", "Shares", "Comments", "Views"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# =====================
# TOTAL BUZZ
# =====================
report_total_buzz = report_df.shape[0]
compare_total_buzz = compare_df.shape[0]
buzz_pct = pct_change(report_total_buzz, compare_total_buzz)

# =====================
# TOTAL POSTS (Type ∈ TOPIC_TYPES)
# =====================
report_posts = report_df[report_df["Type"].isin(TOPIC_TYPES)].shape[0]
compare_posts = compare_df[compare_df["Type"].isin(TOPIC_TYPES)].shape[0]
post_pct = pct_change(report_posts, compare_posts)

# =====================
# REACTIONS / SHARES
# =====================
today_reactions = report_df["Reactions"].sum()
yesterday_reactions = compare_df["Reactions"].sum()
reactions_pct = pct_change(today_reactions, yesterday_reactions)

today_shares = report_df["Shares"].sum()
yesterday_shares = compare_df["Shares"].sum()
shares_pct = pct_change(today_shares, yesterday_shares)

# =====================
# COMMENTS = BUZZ - POSTS
# =====================
today_comments = report_total_buzz - report_posts
yesterday_comments = compare_total_buzz - compare_posts
comments_pct = pct_change(today_comments, yesterday_comments)

# =====================
# TOTAL ENGAGEMENT
# =====================
today_engagement = today_reactions + today_shares + today_comments
yesterday_engagement = yesterday_reactions + yesterday_shares + yesterday_comments
engagement_pct = pct_change(today_engagement, yesterday_engagement)

# =====================
# VIEWS
# =====================
today_views = report_df["Views"].sum()
yesterday_views = compare_df["Views"].sum()
views_pct = pct_change(today_views, yesterday_views)

slide_2 = {
    "title": f"Tổng quan về thương hiệu {brand}",
    "subtitle": f"Ngày {report_day} (so sánh với {compare_day})",
    "data": [
        {
            "type": "buzz",
            "label": "Tổng thảo luận",
            "today": report_total_buzz,
            "yesterday": compare_total_buzz,
            "change_pct": buzz_pct
        },
        {
            "type": "post",
            "label": "Tổng bài đăng",
            "today": report_posts,
            "yesterday": compare_posts,
            "change_pct": post_pct
        },
        {
            "type": "engagement",
            "label": "Tổng tương tác",
            "today": today_engagement,
            "yesterday": yesterday_engagement,
            "change_pct": engagement_pct
        },
        {
            "type": "reactions",
            "label": "Lượt reactions",
            "today": today_reactions,
            "yesterday": yesterday_reactions,
            "change_pct": reactions_pct
        },
        {
            "type": "shares",
            "label": "Lượt chia sẻ",
            "today": today_shares,
            "yesterday": yesterday_shares,
            "change_pct": shares_pct
        },
        {
            "type": "comments",
            "label": "Bình luận",
            "today": today_comments,
            "yesterday": yesterday_comments,
            "change_pct": comments_pct
        },
        {
            "type": "views",
            "label": "Lượt xem",
            "today": today_views,
            "yesterday": yesterday_views,
            "change_pct": views_pct
        }
    ],
    "insight": summary.strip()
}


import pandas as pd
from datetime import timedelta
from openai import OpenAI

# =====================
# CONFIG
# =====================
brand = "Nestlé"

# =====================
# 1. INPUT
# =====================
FILE_PATH = "/content/Nestle_Gerber_15h_labeled.xlsx"
SHEET_NAME = "Data"

REPORT_DATE = "2026-02-01"
COMPARE_DATE = "2026-01-31"

# =====================
# 2. LOAD DATA
# =====================
df = pd.read_excel(FILE_PATH)


TOPIC_TYPES = [
    "fbPageTopic", "fbGroupTopic", "fbUserTopic", "forumTopic",
    "youtubeTopic", "tiktokTopic", "linkedinTopic",
    "ecommerceTopic", "threadsTopic", "snsTopic"
]

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


for col in ["Title", "Content", "Description"]:
    df[col] = df[col].fillna("").astype(str)

df["PublishedDate"] = pd.to_datetime(df["PublishedDate"], errors="coerce")
df = df[df["PublishedDate"].notna()].copy()
df["PublishedDay"] = df["PublishedDate"].dt.date

report_day = pd.to_datetime(REPORT_DATE).date()
start_day = report_day - timedelta(days=LOOKBACK_DAYS - 1)

df_window = df[
    (df["PublishedDay"] >= start_day) &
    (df["PublishedDay"] <= report_day)
].copy()

# =====================
# TRENDLINE (BUZZ / DAY)
# =====================
trend_df = (
    df_window
    .groupby("PublishedDay")
    .size()
    .reset_index(name="buzz")
    .sort_values("PublishedDay")
)

trendline_data = [
    {
        "date": str(row["PublishedDay"]),
        "buzz": int(row["buzz"])
    }
    for _, row in trend_df.iterrows()
]

# =====================
# PEAK DAY DETECTION
# =====================
peak_row = trend_df.loc[trend_df["buzz"].idxmax()]
peak_day = peak_row["PublishedDay"]
peak_buzz = int(peak_row["buzz"])

current_buzz = int(
    trend_df.loc[trend_df["PublishedDay"] == report_day, "buzz"].iloc[0]
) if report_day in trend_df["PublishedDay"].values else 0

is_still_hot = current_buzz >= 0.5 * peak_buzz

# =====================
# PEAK DAY EVENT (NEGATIVE + TOPIC)
# =====================
df_peak = df_window[
    (df_window["PublishedDay"] == peak_day) &
    (df_window["Sentiment"].str.lower() == "negative") &
    (df_window["Type"].isin(TOPIC_TYPES))
].copy()

for col in ["Reactions", "Shares", "Comments"]:
    df_peak[col] = pd.to_numeric(df_peak[col], errors="coerce").fillna(0)

df_peak["engagement"] = (
    df_peak["Reactions"] +
    df_peak["Shares"] +
    df_peak["Comments"]
)

df_peak_top = (
    df_peak
    .sort_values("engagement", ascending=False)
    .drop_duplicates(subset=["UrlTopic"])
    .head(3)
)

# =====================
# PEAK LINKS
# =====================
peak_links = (
    df_peak_top["UrlTopic"]
    .dropna()
    .unique()
    .tolist()
)

# =====================
# BUILD LLM CONTEXT
# =====================
peak_context = []
for _, row in df_peak_top.iterrows():
    peak_context.append(
        f"""
Tiêu đề: {row['Title']}
Mô tả: {row['Description']}
Nội dung: {row['Content']}
Engagement: {row['engagement']}
URL: {row['UrlTopic']}
""".strip()
    )

peak_context_text = "\n\n---\n\n".join(peak_context)

# =====================
# LLM SUMMARY
# =====================
prompt = f"""
Bạn là chuyên gia phân tích khủng hoảng truyền thông.

BỐI CẢNH:
- Thương hiệu: {brand}
- Ngày thảo luận cao nhất: {peak_day}
- Số lượt thảo luận: {peak_buzz}
- Ngày hiện tại: {report_day} ({current_buzz} lượt)

NHIỆM VỤ:
1. Tóm tắt sự vụ chính xảy ra trong ngày cao nhất.
2. Đánh giá đến ngày {report_day}, sự vụ này còn được cộng đồng quan tâm hay không.

YÊU CẦU BẮT BUỘC:
- 3–4 câu, văn xuôi
- Mỗi đoạn insight chỉ gắn **1 URL**
- URL phải lấy từ dữ liệu cung cấp
- Format kết câu: [Nguồn: URL]
- Không gạch đầu dòng

DỮ LIỆU:
{peak_context_text}
"""

response = client.chat.completions.create(
    model="google/gemma-3-27b-it",
    messages=[
        {"role": "system", "content": "Bạn là chuyên gia crisis & executive insight."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2,
)

trend_summary = response.choices[0].message.content.strip()

# =====================
# FINAL OUTPUT
# =====================
slide_3 = {
    "window": {
        "start_date": str(start_day),
        "end_date": str(report_day)
    },
    "trendline": trendline_data,
    "peak_day": {
        "date": str(peak_day),
        "buzz": peak_buzz,
        "links": peak_links
    },
    "current_day": {
        "date": str(report_day),
        "buzz": current_buzz,
        "is_still_hot": is_still_hot
    },
    "summary": trend_summary
}

import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI
import re

# =====================
# CONFIG
# =====================
FILE_PATH = "/content/Nestle_Gerber_15h_labeled.xlsx"
SHEET_NAME = "Data"

REPORT_DATE = "2026-02-01"
COMPARE_DATE = "2026-01-31"

TOP_N_ATTR = 6
brand = "Nestlé"

# =====================
# INIT LLM CLIENT
# =====================
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# =====================
# LOAD & CLEAN DATA
# =====================
df = pd.read_excel(FILE_PATH)

for col in ["Title", "Content", "Description", "Labels", "Sentiment"]:
    df[col] = df[col].fillna("").astype(str)

df["PublishedDate"] = pd.to_datetime(df["PublishedDate"], errors="coerce")
df = df[df["PublishedDate"].notna()].copy()
df["PublishedDay"] = df["PublishedDate"].dt.date

report_day = pd.to_datetime(REPORT_DATE).date()
compare_day = pd.to_datetime(COMPARE_DATE).date()

report_df = df[df["PublishedDay"] == report_day].copy()

# =====================
# NORMALIZE SENTIMENT & LABELS
# =====================
report_df["Sentiment"] = report_df["Sentiment"].str.capitalize()

report_df["Label_List"] = report_df["Labels"].apply(
    lambda x: [i.strip() for i in x.split(",") if i.strip()]
)

df_exploded = report_df.explode("Label_List")

# =====================
# PIE CHART – SENTIMENT DISTRIBUTION
# =====================
sentiment_dist = (
    report_df["Sentiment"]
    .value_counts()
    .reset_index(name='Count') # Explicitly name the count column 'Count'
    .rename(columns={"index": "Sentiment"}) # Rename the index column to 'Sentiment'
)

# =====================
# BAR CHART – ATTRIBUTE x SENTIMENT
# =====================
attr_sentiment = (
    df_exploded.groupby(["Label_List", "Sentiment"])
    .size()
    .reset_index(name="Count")
)

top_attrs = (
    attr_sentiment.groupby("Label_List")["Count"]
    .sum()
    .sort_values(ascending=False)
    .head(TOP_N_ATTR)
    .index
)

attr_sentiment_top = attr_sentiment[
    attr_sentiment["Label_List"].isin(top_attrs)
]

pivot_df = attr_sentiment_top.pivot(
    index="Label_List",
    columns="Sentiment",
    values="Count"
).fillna(0)


# =====================
# BUILD EVIDENCE (URL WHITELIST)
# =====================
evidence_df = (
    df_exploded[
        df_exploded["Label_List"].isin(top_attrs)
    ]
    .copy()
)

evidence_df["engagement"] = (
    pd.to_numeric(evidence_df.get("Reactions", 0), errors="coerce").fillna(0)
    + pd.to_numeric(evidence_df.get("Shares", 0), errors="coerce").fillna(0)
    + pd.to_numeric(evidence_df.get("Comments", 0), errors="coerce").fillna(0)
)

evidence_top = (
    evidence_df
    .sort_values("engagement", ascending=False)
    .drop_duplicates(subset=["UrlTopic"])
    .head(5)
    .reset_index(drop=True)
)

url_map = {}
evidence_blocks = []

for idx, row in evidence_top.iterrows():
    key = f"URL_{idx+1}"
    url_map[key] = row["UrlTopic"]

    evidence_blocks.append(
        f"""
[{key}]
Sentiment: {row['Sentiment']}
Brand Attribute: {row['Label_List']}
Tiêu đề: {row['Title']}
Mô tả: {row['Description']}
Nội dung: {row['Content']}
""".strip()
    )

evidence_context = "\n\n---\n\n".join(evidence_blocks)
url_whitelist_text = "\n".join([f"{k}: {v}" for k, v in url_map.items()])

# =====================
# PROMPT – INSIGHT
# =====================
prompt = f"""
Bạn là chuyên gia social listening & brand health analysis.

BỐI CẢNH:
- Thương hiệu: {brand}
- Ngày phân tích: {report_day}

PHÂN BỔ SENTIMENT:
{sentiment_dist.to_string(index=False)}

BRAND ATTRIBUTE THEO SENTIMENT:
{pivot_df.reset_index().to_string(index=False)}

DẪN CHỨNG:
{evidence_context}

URL HỢP LỆ:
{url_whitelist_text}

NHIỆU VỤ:
Viết insight phân tích Sentiment kết hợp Brand Attribute.

YÊU CẦU BẮT BUỘC:
- Viết 4–5 câu, văn xuôi
- So sánh Negative / Neutral / Positive
- Nêu rõ brand attribute nổi bật theo từng sắc thái
- Mỗi câu kết thúc bằng [Nguồn: URL_X]
- Mỗi URL_X chỉ dùng 1 lần
- Không ghi URL thật

FORMAT:
Câu insight... [Nguồn: URL_X]
"""

# =====================
# CALL LLM
# =====================
response = client.chat.completions.create(
    model="google/gemma-3-27b-it",
    messages=[
        {"role": "system", "content": "Bạn là chuyên gia brand insight & sentiment analysis."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2,
)

raw_insight = response.choices[0].message.content.strip()

# =====================
# POST-PROCESS: KEY → REAL URL
# =====================
final_insight = raw_insight
for key, real_url in url_map.items():
    final_insight = re.sub(
        rf"\[Nguồn:\s*{key}\]",
        f"[Nguồn: {real_url}]",
        final_insight
    )

# =====================
# FINAL SLIDE JSON
# =====================
slide_4 = {
    "title": "Sentiment & Brand Attribute",
    "subtitle": f"Ngày {report_day}",
    "sentiment_distribution": sentiment_dist.to_dict(orient="records"),
    "attribute_sentiment": pivot_df.reset_index().to_dict(orient="records"),
    "insight": final_insight
}

slide_4



slide = {
    "slide_1": slide_1,
    "slide_2": slide_2,
    "slide_3": slide_3,
    "slide_4": slide_4
}