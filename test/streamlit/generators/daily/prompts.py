"""
Prompt templates for LLM-based insight generation
"""


def get_overview_insight_prompt(brand: str, report_day: str, compare_day: str, 
                                  report_total_buzz: int, compare_total_buzz: int, 
                                  buzz_pct: float, context_text: str) -> str:
    """
    Generate prompt for overview insight (Slide 1)
    
    Args:
        brand: Brand name
        report_day: Report date
        compare_day: Comparison date
        report_total_buzz: Total buzz on report day
        compare_total_buzz: Total buzz on comparison day
        buzz_pct: Percentage change in buzz
        context_text: Context from top negative topics
        
    Returns:
        Formatted prompt string
    """
    return f"""
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
- Mỗi câu gắn DUY NHẤT 1 URL từ dữ liệu được cung cấp
- CHỈ sử dụng URL có trong dữ liệu, KHÔNG tạo URL giả
- KHÔNG lặp URL
- KHÔNG gạch đầu dòng, KHÔNG tiêu đề

FORMAT BẮT BUỘC:
Câu insight... [Nguồn: URL_THẬT_TỪ_DỮ_LIỆU]

DỮ LIỆU (chứa URL thật trong trường URL):
{context_text}

LƯU Ý QUAN TRỌNG:
- CHỈ sử dụng URL có trong dữ liệu trên
- KHÔNG tạo ra URL giả như example.com
- KHÔNG sử dụng placeholder như URL_X, URL_Y
- Sao chép chính xác URL từ trường "URL:" trong dữ liệu
"""


def get_trendline_insight_prompt(brand: str, peak_day: str, peak_buzz: int,
                                   report_day: str, current_buzz: int,
                                   peak_context_text: str) -> str:
    """
    Generate prompt for trendline insight (Slide 2)
    
    Args:
        brand: Brand name
        peak_day: Date with highest buzz
        peak_buzz: Buzz count on peak day
        report_day: Current report date
        current_buzz: Current buzz count
        peak_context_text: Context from peak day topics
        
    Returns:
        Formatted prompt string
    """
    return f"""
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
- Mỗi câu gắn **1 URL thật từ dữ liệu**
- CHỈ sử dụng URL có trong dữ liệu được cung cấp
- KHÔNG tạo URL giả như example.com
- Format kết câu: [Nguồn: URL_THẬT]
- Không gạch đầu dòng

DỮ LIỆU (chứa URL thật trong trường URL):
{peak_context_text}

LƯU Ý QUAN TRỌNG:
- Sao chép chính xác URL từ trường "URL:" trong dữ liệu
- KHÔNG sử dụng placeholder như URL_X, URL_Y
"""


def get_channel_insight_prompt(brand: str, report_day: str, compare_day: str,
                                 channel_data: str, evidence_context: str) -> str:
    """
    Generate prompt for channel breakdown insight (Slide 3)
    
    Args:
        brand: Brand name
        report_day: Report date
        compare_day: Comparison date
        channel_data: Channel distribution data
        evidence_context: Evidence from top posts
        
    Returns:
        Formatted prompt string
    """
    return f"""
Bạn là chuyên gia social listening & channel analysis.

BỐI CẢNH:
- Thương hiệu: {brand}
- Ngày phân tích: {report_day}
- So sánh với: {compare_day}

PHÂN BỔ THEO KÊNH:
{channel_data}

DẪN CHỨNG (chứa URL thật trong trường URL):
{evidence_context}

NHIỆM VỤ:
Viết insight phân tích sự phân bổ thảo luận theo kênh truyền thông.

YÊU CẦU BẮT BUỘC:
- Viết 4–5 câu, văn xuôi
- Chỉ ra kênh chính và xu hướng
- Giải thích nguyên nhân và tác động
- Mỗi câu kết thúc bằng [Nguồn: URL_THẬT]
- CHỈ sử dụng URL có trong dữ liệu được cung cấp
- KHÔNG tạo URL giả như example.com
- Mỗi URL chỉ dùng 1 lần
- Không gạch đầu dòng

LƯU Ý QUAN TRỌNG:
- Sao chép chính xác URL từ trường "URL:" trong dữ liệu
- KHÔNG sử dụng placeholder như URL_X, URL_Y
"""


def get_sentiment_insight_prompt(brand: str, report_day: str,
                                   sentiment_dist: str, channel_sentiment: str,
                                   evidence_context: str, url_whitelist: str) -> str:
    """
    Generate prompt for sentiment & channel breakdown insight (Slide 4)
    
    Args:
        brand: Brand name
        report_day: Report date/time
        sentiment_dist: Overall sentiment distribution
        channel_sentiment: Sentiment breakdown by channel
        evidence_context: Evidence from top posts
        url_whitelist: Whitelist of valid URLs
        
    Returns:
        Formatted prompt string
    """
    return f"""
Bạn là chuyên gia social listening & sentiment analysis.

BỐI CẢNH:
- Thương hiệu: {brand}
- Khung giờ phân tích: {report_day}

PHÂN BỔ SENTIMENT TỔNG QUAN:
{sentiment_dist}

SENTIMENT THEO KÊNH:
{channel_sentiment}

DẪN CHỨNG (Top posts theo sentiment - chứa URL thật):
{evidence_context}

URL HỢP LỆ TRONG DỮ LIỆU:
{url_whitelist}

NHIỆM VỤ:
Viết insight phân tích Sentiment tổng quan và phân bố theo từng kênh.

YÊU CẦU BẮT BUỘC:
- Viết 5–6 câu, văn xuôi
- Câu 1-2: Phân tích tỷ lệ Negative / Neutral / Positive tổng quan
- Câu 3-4: Phân tích sentiment trên từng kênh chính (Facebook, Tiktok, Youtube, etc.)
- Câu 5-6: Nêu rõ nội dung chính của các bài đăng negative (quan trọng nhất)
- Mỗi câu kết thúc bằng [Nguồn: URL_THẬT]
- CHỈ sử dụng URL có trong danh sách "URL HỢP LỆ" ở trên
- KHÔNG tạo URL giả như example.com
- Mỗi URL chỉ dùng 1 lần

FORMAT BẮT BUỘC:
Câu insight về sentiment tổng quan... [Nguồn: URL_THẬT_1]
Câu insight về sentiment theo kênh... [Nguồn: URL_THẬT_2]

LƯU Ý QUAN TRỌNG:
- Sao chép chính xác URL từ danh sách "URL HỢP LỆ"
- KHÔNG sử dụng placeholder như URL_X, URL_Y
"""



def get_channel_breakdown_prompt(brand: str, report_day: str, top_channel: str,
                                   channel_data: str, buzz_context: str,
                                   url_whitelist: str) -> str:
    """
    Generate prompt for channel breakdown insight (Slide 3)
    
    Args:
        brand: Brand name
        report_day: Report date
        top_channel: Top channel name
        channel_data: Channel distribution data
        buzz_context: Evidence from top posts
        url_whitelist: Whitelist of valid URLs
        
    Returns:
        Formatted prompt string
    """
    return f"""
Bạn là chuyên gia social listening & crisis analysis.

BỐI CẢNH:
- Thương hiệu: {brand}
- Ngày phân tích: {report_day}
- Channel chiếm thảo luận cao nhất: {top_channel}
- Phân bố thảo luận theo channel so với hôm qua:
{channel_data}

DỮ LIỆU BUZZ (chứa URL thật):
{buzz_context}

URL HỢP LỆ TRONG DỮ LIỆU:
{url_whitelist}

NHIỆM VỤ:
Viết insight cho slide Channel Breakdown.

YÊU CẦU BẮT BUỘC:
- Viết đúng 6–7 câu, văn xuôi
- Mỗi câu kết thúc bằng [Nguồn: URL_THẬT]
- CHỈ sử dụng URL có trong danh sách "URL HỢP LỆ" ở trên
- KHÔNG tạo URL giả như example.com
- Mỗi URL chỉ dùng 1 lần

FORMAT BẮT BUỘC:
Câu insight... [Nguồn: URL_THẬT_TỪ_DANH_SÁCH]

LƯU Ý QUAN TRỌNG:
- Sao chép chính xác URL từ danh sách "URL HỢP LỆ"
- KHÔNG sử dụng placeholder như URL_X, URL_Y
"""
