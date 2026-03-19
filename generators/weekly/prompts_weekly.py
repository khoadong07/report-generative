"""
Prompt templates for Weekly LLM-based insight generation
"""


def get_weekly_overview_insight_prompt(brand: str, week_display: str,
                                        weekly_comparison: list, context_text: str) -> str:
    """Generate prompt for weekly overview insight (Slide 1)"""
    comparison_text = "\n".join([f"- {w['week']}: {w['total_mentions']} lượt" for w in weekly_comparison])
    
    return f"""
Bạn là chuyên gia phân tích truyền thông và social listening.

BỐI CẢNH PHÂN TÍCH:
- Thương hiệu: {brand}
- Tuần khảo sát: {week_display}
- So sánh 4 tuần:
{comparison_text}

NHIỆM VỤ:
Viết một đoạn insight tóm tắt tình hình thảo luận trong tuần.

YÊU CẦU BẮT BUỘC:
- Viết đúng 5–6 câu, dạng văn xuôi
- Câu đầu tiên mô tả quy mô & xu hướng so với các tuần trước
- Các câu sau mô tả các chủ đề chính và phản ứng cộng đồng
- Văn phong chuyên nghiệp, trung lập
- CRITICAL: Mỗi câu PHẢI kết thúc bằng [Nguồn: URL] với URL clickable
- Mỗi câu gắn DUY NHẤT 1 URL
- KHÔNG lặp URL
- KHÔNG gạch đầu dòng, KHÔNG tiêu đề
- URL PHẢI là hyperlink có thể click được

FORMAT BẮT BUỘC:
Câu 1 nội dung phân tích... [Nguồn: https://example.com/url1]
Câu 2 nội dung phân tích... [Nguồn: https://example.com/url2]
Câu 3 nội dung phân tích... [Nguồn: https://example.com/url3]

DỮ LIỆU (chứa URL trong trường UrlTopic):
{context_text}

LƯU Ý: Bạn PHẢI sử dụng URL từ dữ liệu được cung cấp. KHÔNG bỏ qua URL.
"""


def get_weekly_trendline_insight_prompt(brand: str, week_display: str,
                                         trendline_data: list, context_text: str) -> str:
    """Generate prompt for weekly trendline insight (Slide 2)"""
    return f"""
Bạn là chuyên gia phân tích xu hướng truyền thông.

BỐI CẢNH:
- Thương hiệu: {brand}
- Tuần phân tích: {week_display}

NHIỆM VỤ:
Phân tích xu hướng đề cập trong tuần, chỉ ra ngày có lượng thảo luận cao nhất và lý do.

YÊU CẦU BẮT BUỘC:
- 4–5 câu, văn xuôi
- CRITICAL: Mỗi câu PHẢI kết thúc bằng [Nguồn: URL] với URL clickable
- Mỗi URL chỉ dùng 1 lần
- Không gạch đầu dòng
- URL PHẢI là hyperlink có thể click được

FORMAT BẮT BUỘC:
Câu 1... [Nguồn: https://example.com/url1]
Câu 2... [Nguồn: https://example.com/url2]

DỮ LIỆU (chứa URL trong trường UrlTopic):
{context_text}

LƯU Ý: Bạn PHẢI sử dụng URL từ dữ liệu được cung cấp. KHÔNG bỏ qua URL.
"""


def get_weekly_channel_insight_prompt(brand: str, week_display: str,
                                       channel_data: str, top_sources: str,
                                       context_text: str) -> str:
    """Generate prompt for weekly channel insight (Slide 3)"""
    return f"""
Bạn là chuyên gia social listening & channel analysis.

BỐI CẢNH:
- Thương hiệu: {brand}
- Tuần phân tích: {week_display}

PHÂN BỔ THEO KÊNH:
{channel_data}

TOP NGUỒN:
{top_sources}

NHIỆM VỤ:
Viết insight phân tích sự phân bổ thảo luận theo kênh và nguồn nổi bật.

YÊU CẦU BẮT BUỘC:
- Viết 4–5 câu, văn xuôi
- Chỉ ra kênh chính và nguồn nổi bật
- CRITICAL: Mỗi câu PHẢI kết thúc bằng [Nguồn: URL] với URL clickable
- Mỗi URL chỉ dùng 1 lần
- Không gạch đầu dòng
- URL PHẢI là hyperlink có thể click được

FORMAT BẮT BUỘC:
Câu 1... [Nguồn: https://example.com/url1]
Câu 2... [Nguồn: https://example.com/url2]

DỮ LIỆU (chứa URL trong trường UrlTopic):
{context_text}

LƯU Ý: Bạn PHẢI sử dụng URL từ dữ liệu được cung cấp. KHÔNG bỏ qua URL.
"""


def get_weekly_sentiment_insight_prompt(brand: str, week_display: str,
                                          top_topics: list, context_text: str) -> str:
    """Generate prompt for weekly sentiment insight (Slide 6)"""
    topics_text = "\n".join([
        f"- {t['topic']}: {t['total']} lượt (Negative: {t['negative']}, Neutral: {t['neutral']}, Positive: {t['positive']})"
        for t in top_topics[:5]
    ])
    
    return f"""
Bạn là chuyên gia social listening & sentiment analysis.

BỐI CẢNH:
- Thương hiệu: {brand}
- Tuần phân tích: {week_display}

TOP CHỦ ĐỀ THEO SENTIMENT:
{topics_text}

NHIỆM VỤ:
Viết insight phân tích sắc thái và các chủ đề nổi bật.

YÊU CẦU BẮT BUỘC:
- Viết 5–6 câu, văn xuôi
- Phân tích tỷ lệ sentiment và các chủ đề chính
- CRITICAL: Mỗi câu PHẢI kết thúc bằng [Nguồn: URL] với URL clickable
- Mỗi URL chỉ dùng 1 lần
- Không gạch đầu dòng
- URL PHẢI là hyperlink có thể click được

FORMAT BẮT BUỘC:
Câu 1... [Nguồn: https://example.com/url1]
Câu 2... [Nguồn: https://example.com/url2]

DỮ LIỆU (chứa URL trong trường UrlTopic):
{context_text}

LƯU Ý: Bạn PHẢI sử dụng URL từ dữ liệu được cung cấp. KHÔNG bỏ qua URL.
"""


def get_weekly_positive_insight_prompt(brand: str, week_display: str,
                                         positive_topics: str, context_text: str) -> str:
    """Generate prompt for weekly positive insight (Slide 7)"""
    return f"""
Bạn là chuyên gia phân tích truyền thông tích cực.

BỐI CẢNH:
- Thương hiệu: {brand}
- Tuần phân tích: {week_display}

CHỦ ĐỀ TÍCH CỰC:
{positive_topics}

NHIỆM VỤ:
Viết insight phân tích các chủ đề tích cực về thương hiệu.

YÊU CẦU BẮT BUỘC:
- Viết 4–5 câu, văn xuôi
- Nêu rõ các chủ đề tích cực chính và dẫn chứng cụ thể
- CRITICAL: Mỗi câu PHẢI kết thúc bằng [Nguồn: URL] với URL clickable
- Mỗi URL chỉ dùng 1 lần
- Không gạch đầu dòng
- URL PHẢI là hyperlink có thể click được

FORMAT BẮT BUỘC:
Câu 1... [Nguồn: https://example.com/url1]
Câu 2... [Nguồn: https://example.com/url2]

DỮ LIỆU (chứa URL trong trường UrlTopic):
{context_text}

LƯU Ý: Bạn PHẢI sử dụng URL từ dữ liệu được cung cấp. KHÔNG bỏ qua URL.
"""


def get_weekly_negative_insight_prompt(brand: str, week_display: str,
                                         negative_topics: str, context_text: str) -> str:
    """Generate prompt for weekly negative insight (Slide 10)"""
    return f"""
Bạn là chuyên gia phân tích khủng hoảng truyền thông.

BỐI CẢNH:
- Thương hiệu: {brand}
- Tuần phân tích: {week_display}

CHỦ ĐỀ TIÊU CỰC:
{negative_topics}

NHIỆM VỤ:
Viết insight phân tích các chủ đề tiêu cực về thương hiệu.

YÊU CẦU BẮT BUỘC:
- Viết 4–5 câu, văn xuôi
- Nêu rõ các chủ đề tiêu cực chính và dẫn chứng cụ thể
- CRITICAL: Mỗi câu PHẢI kết thúc bằng [Nguồn: URL] với URL clickable
- Mỗi URL chỉ dùng 1 lần
- Không gạch đầu dòng
- URL PHẢI là hyperlink có thể click được

FORMAT BẮT BUỘC:
Câu 1... [Nguồn: https://example.com/url1]
Câu 2... [Nguồn: https://example.com/url2]

DỮ LIỆU (chứa URL trong trường UrlTopic):
{context_text}

LƯU Ý: Bạn PHẢI sử dụng URL từ dữ liệu được cung cấp. KHÔNG bỏ qua URL.
"""


def get_weekly_brand_comparison_insight_prompt(brand: str, week_display: str,
                                                 brand_comparison_data: str, context_text: str) -> str:
    """Generate prompt for weekly brand comparison insight (Slide 12)"""
    return f"""
Bạn là chuyên gia phân tích cạnh tranh thương hiệu và social listening.

BỐI CẢNH:
- Thương hiệu chính: {brand}
- Tuần phân tích: {week_display}

DỮ LIỆU SO SÁNH THƯƠNG HIỆU (tuần trước → tuần này):
{brand_comparison_data}

NHIỆM VỤ:
Viết 3 đoạn văn xuôi phân tích tổng quan, theo thứ tự:
1. Thương hiệu dẫn đầu thảo luận tuần này so với tuần trước, nêu số liệu cụ thể.
2. Các đề cập nổi bật, bất ngờ trong tuần dựa trên chủ đề (trường Type) đang được chú ý.
3. Thương hiệu giảm đáng kể, giải thích xu hướng.

YÊU CẦU BẮT BUỘC:
- Mỗi đoạn 2–3 câu, văn xuôi, KHÔNG có tiêu đề hay label
- Chỉ dùng số liệu từ dữ liệu được cung cấp, KHÔNG bịa thêm
- CRITICAL: Mỗi câu PHẢI kết thúc bằng [Nguồn: URL] với URL lấy từ dữ liệu bên dưới
- Mỗi URL chỉ dùng 1 lần, KHÔNG lặp URL
- Giữa các đoạn có dòng trống

FORMAT BẮT BUỘC:
Câu 1 đoạn 1... [Nguồn: https://...] Câu 2 đoạn 1... [Nguồn: https://...]

Câu 1 đoạn 2... [Nguồn: https://...] Câu 2 đoạn 2... [Nguồn: https://...]

Câu 1 đoạn 3... [Nguồn: https://...] Câu 2 đoạn 3... [Nguồn: https://...]

DỮ LIỆU MẪU (Title, Type, UrlTopic theo từng thương hiệu):
{context_text}

LƯU Ý: Chỉ dùng URL từ dữ liệu được cung cấp. KHÔNG bịa URL.
"""
