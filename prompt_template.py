"""
Module: Prompt Template
Chức năng: Định nghĩa template markdown cho báo cáo
"""

PROMPT_MD_TEMPLATE = """
BÁO CÁO SOCIAL LISTENING INSIGHT — {{PRIMARY_BRAND}}

Thời gian nghiên cứu: {{STUDY_PERIOD}}

============================================================
QUY CHUẨN PHÂN TÍCH & ĐẦU RA
============================================================

1. Báo cáo phải được trình bày dưới dạng SLIDE.
2. Mỗi slide phải tuân thủ INSIGHT FRAMEWORK:
   - WHAT: Điều gì đang xảy ra? (xu hướng, chênh lệch, bất thường)
   - WHY: Vì sao điều này xảy ra / có ý nghĩa?
   - SO WHAT: Hàm ý chiến lược cho thương hiệu / truyền thông
3. Không liệt kê số liệu thuần túy. Mọi bảng dữ liệu phải được diễn giải.
4. Ưu tiên so sánh {{PRIMARY_BRAND}} với đối thủ.
5. Ngôn ngữ: tiếng Việt, chuẩn báo cáo nội bộ ngành Social Listening.
6. Sử dụng dữ liệu mẫu (sample data) dưới đây làm bằng chứng cụ thể khi viết insight.

============================================================
SLIDE 1. TỔNG QUAN BÁO CÁO
============================================================

Thông tin dữ liệu:
- Thương hiệu chính: {{PRIMARY_BRAND}}
- Đối thủ: {{COMPETITOR_LIST}}
- Tổng thảo luận: {{TOTAL_MENTIONS}}
- Kênh: {{TOTAL_CHANNELS}} | Thương hiệu: {{TOTAL_BRANDS}} | Chủ đề: {{TOTAL_TOPICS}}

Dữ liệu mẫu (Sample Records):
{{SAMPLE_OVERVIEW_RECORDS}}

============================================================
SLIDE 2. SHARE OF VOICE
============================================================

{{SOV_TABLE}}

Dữ liệu mẫu (Sample Records - {{PRIMARY_BRAND}}):
{{SAMPLE_PRIMARY_BRAND_RECORDS}}

============================================================
SLIDE 3. DIỄN BIẾN BUZZ THEO THỜI GIAN
============================================================

{{DAILY_BUZZ_TABLE}}

Dữ liệu mẫu (Sample Records - Ngày có buzz cao):
{{SAMPLE_HIGH_BUZZ_RECORDS}}

============================================================
SLIDE 4. HIGHLIGHT BUZZ
============================================================

Số lượng nội dung nổi bật: {{NUM_HIGHLIGHTS}}  
Kênh xuất hiện: {{HIGHLIGHT_CHANNELS}}  
Tình trạng dữ liệu tương tác: {{INTERACTION_METRIC_STATUS}}

Danh sách nội dung:
{{HIGHLIGHTED_URL_LIST}}

Dữ liệu mẫu (Sample Highlights):
{{SAMPLE_HIGHLIGHTS}}

============================================================
SLIDE 5. TỔNG QUAN CẢM XÚC
============================================================

{{SENTIMENT_OVERVIEW_TABLE}}

Dữ liệu mẫu (Sample Records - Theo Sentiment):
{{SAMPLE_SENTIMENT_RECORDS}}

============================================================
SLIDE 6. CƠ CẤU KÊNH THẢO LUẬN
============================================================

{{CHANNEL_VOLUME_TABLE}}

Dữ liệu mẫu (Sample Records - Top Channels):
{{SAMPLE_CHANNEL_RECORDS}}

============================================================
SLIDE 7. CẢM XÚC THEO KÊNH
============================================================

{{SENTIMENT_BY_CHANNEL_TABLE}}

Dữ liệu mẫu (Sample Records - Sentiment by Channel):
{{SAMPLE_SENTIMENT_CHANNEL_RECORDS}}

============================================================
SLIDE 8. CHỦ ĐỀ THẢO LUẬN NỔI BẬT
============================================================

{{TOPIC_RANKING_TABLE}}

Dữ liệu mẫu (Sample Records - Top Topics):
{{SAMPLE_TOPIC_RECORDS}}

============================================================
SLIDE 9. XU HƯỚNG CHỦ ĐỀ THEO THỜI GIAN
============================================================

Chủ đề trọng tâm: {{FOCUS_TOPIC_LIST}}

{{TOPIC_TREND_DAILY_TABLE}}

Dữ liệu mẫu (Sample Records - Topic Trend):
{{SAMPLE_TREND_RECORDS}}

============================================================
SLIDE 10. CHỦ ĐỀ THEO KÊNH
============================================================

{{TOPIC_BY_CHANNEL_TABLE}}

Dữ liệu mẫu (Sample Records - Topic by Channel):
{{SAMPLE_TOPIC_CHANNEL_RECORDS}}

============================================================
SLIDE 11. CẢM XÚC THEO THƯƠNG HIỆU
============================================================

{{SENTIMENT_BY_BRAND_TABLE}}

Khối lượng thảo luận:
{{BRAND_VOLUME_TABLE}}

Dữ liệu mẫu (Sample Records - Sentiment by Brand):
{{SAMPLE_BRAND_SENTIMENT_RECORDS}}

============================================================
SLIDE 12. CHỦ ĐỀ THEO THƯƠNG HIỆU
============================================================

{{TOPIC_BY_BRAND_TABLE}}

Dữ liệu mẫu (Sample Records - Topic by Brand):
{{SAMPLE_TOPIC_BRAND_RECORDS}}

============================================================
SLIDE 13. KẾT LUẬN & HÀM Ý CHIẾN LƯỢC
============================================================

Insight then chốt:
YÊU CẦU KHAI THÁC INSIGHT THEN CHỐT
- Trình bày từ 3–5 insight quan trọng nhất.
- Mỗi insight phải tuân thủ cấu trúc:
  - Insight: (mô tả ngắn gọn, 1–2 câu)
  - Bằng chứng dữ liệu: (dẫn chiếu slide/chỉ số/chủ đề/kênh liên quan + sử dụng sample data làm ví dụ cụ thể)
- Không lặp lại số liệu chi tiết, chỉ nêu bằng chứng đủ để chứng minh insight.

Hành động đề xuất:
YÊU CẦU ĐỀ XUẤT HÀNH ĐỘNG
- Mỗi hành động phải:
  - Xuất phát trực tiếp từ một hoặc nhiều insight ở trên.
  - Chỉ rõ mục tiêu truyền thông mà {{PRIMARY_BRAND}} cần giải quyết.
- Ưu tiên các hành động:
  - Giảm thiểu sentiment tiêu cực.
  - Kiểm soát rủi ro từ các topic nhạy cảm.
  - Tối ưu hiệu quả trên các kênh đóng góp buzz lớn.
- Trình bày theo cấu trúc:
  - Hành động đề xuất
  - Insight liên quan
  - Mục tiêu truyền thông

KPI theo dõi:
YÊU CẦU XÁC ĐỊNH KPI THEO DÕI
- KPI phải:
  - Đo lường được bằng dữ liệu social listening.
  - Gắn trực tiếp với hành động đề xuất ở trên.
- Mỗi KPI cần nêu rõ:
  - Chỉ số theo dõi (ví dụ: tỷ trọng Negative sentiment, volume topic, SOV theo kênh).
  - Mục đích theo dõi.
  - Kỳ vọng xu hướng (tăng/giảm/ổn định).

"""


def render_prompt(template, variables):
    """
    Render prompt template với biến
    
    Args:
        template (str): Template markdown
        variables (dict): Dictionary chứa các biến
        
    Returns:
        str: Prompt đã render
    """
    result = template
    for key, value in variables.items():
        result = result.replace(f"{{{{{key}}}}}", str(value))
    return result
