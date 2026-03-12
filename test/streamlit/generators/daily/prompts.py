"""
Prompt templates for LLM-based insight generation
"""


def get_overview_insight_prompt_basic(brand: str, report_day: str, compare_day: str, 
                                       report_total_buzz: int, compare_total_buzz: int, 
                                       buzz_pct: float, context_text: str) -> str:
    """
    Generate prompt for overview insight (Slide 1) - Basic metrics version (no interactions)
    
    Args:
        brand: Brand name
        report_day: Report date
        compare_day: Comparison date
        report_total_buzz: Total buzz on report day
        compare_total_buzz: Total buzz on comparison day
        buzz_pct: Percentage change in buzz
        context_text: Context from top negative topics
        
    Returns:
        Formatted prompt string for basic metrics mode
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
Viết một đoạn insight ngắn gọn phân tích tình hình thảo luận và sự kiện chính.

YÊU CẦU BẮT BUỘC:
- Viết đúng 4–5 câu, dạng văn xuôi (NGẮN GỌN cho slide)
- Câu 1: Nêu tổng số thảo luận và % thay đổi so với ngày trước
- Câu 2: Mô tả SỰ KIỆN CHÍNH gây ra thảo luận (nguyên nhân cốt lõi)
- Câu 3: Phân tích cách thông tin lan truyền trên các kênh chính
- Câu 4: Mô tả PHẢN ỨNG CỦA CỘNG ĐỒNG
- Câu 5 (tùy chọn): Đánh giá tác động hiện tại
- Văn phong chuyên nghiệp, trung lập, súc tích
- CRITICAL: Mỗi câu PHẢI kết thúc bằng hyperlink dạng [Nguồn](URL)
- Mỗi câu gắn DUY NHẤT 1 URL từ dữ liệu được cung cấp
- CHỈ sử dụng URL có trong dữ liệu, KHÔNG tạo URL giả
- KHÔNG lặp URL
- KHÔNG gạch đầu dòng, KHÔNG tiêu đề

CẤU TRÚC INSIGHT MONG MUỐN (NGẮN GỌN):
1. Số liệu tổng quan + % thay đổi
2. Sự kiện chính (nguyên nhân)
3. Cách thông tin lan truyền
4. Phản ứng cộng đồng
5. Tác động hiện tại (nếu cần)

FORMAT BẮT BUỘC (Markdown hyperlink):
Tổng cộng có {report_total_buzz} thảo luận về {brand} trong vòng 24 giờ qua, [tăng/giảm] {abs(buzz_pct):.1f}% so với ngày trước đó [Nguồn](URL_1). Sự [tăng/giảm] này diễn ra trong bối cảnh [mô tả sự kiện chính ngắn gọn] [Nguồn](URL_2). Thông tin nhanh chóng lan rộng trên [kênh chính], thu hút sự quan tâm của [đối tượng] [Nguồn](URL_3). Phản ứng từ cộng đồng chủ yếu thể hiện [mô tả cảm xúc ngắn gọn] [Nguồn](URL_4). [Đánh giá tình hình hiện tại ngắn gọn] [Nguồn](URL_5).

VÍ DỤ THAM KHẢO (4 câu):
Tổng cộng có 2,229 thảo luận về Petrolimex trong vòng 24 giờ qua, giảm 46.35% so với ngày trước đó [Nguồn](URL_1). Sự sụt giảm này diễn ra trong bối cảnh sự việc nhân viên cây xăng từ chối bán 500ml xăng cho người đàn ông lớn tuổi [Nguồn](URL_2). Thông tin lan truyền nhanh trên Facebook, gây phản ứng bức xúc từ cộng đồng [Nguồn](URL_3). Hiện tại sự việc vẫn ảnh hưởng tiêu cực đến hình ảnh thương hiệu [Nguồn](URL_4).

DỮ LIỆU (chứa URL thật trong trường URL):
{context_text}

LƯU Ý QUAN TRỌNG:
- CHỈ sử dụng URL có trong dữ liệu trên
- KHÔNG tạo ra URL giả như example.com
- KHÔNG sử dụng placeholder như URL_X, URL_Y
- Sao chép chính xác URL từ trường "URL:" trong dữ liệu
- Format hyperlink: [Nguồn](URL) để tạo link có thể click được
- PHẢI phân tích SỰ KIỆN CHÍNH, không chỉ so sánh số liệu
- Insight phải NGẮN GỌN và SÚCÍCH cho slide presentation
- Tối đa 4-5 câu, mỗi câu không quá 25 từ
"""


def get_overview_insight_prompt(brand: str, report_day: str, compare_day: str, 
                                  report_total_buzz: int, compare_total_buzz: int, 
                                  buzz_pct: float, context_text: str) -> str:
    """
    Generate prompt for overview insight (Slide 1) - Full interactions version
    
    Args:
        brand: Brand name
        report_day: Report date
        compare_day: Comparison date
        report_total_buzz: Total buzz on report day
        compare_total_buzz: Total buzz on comparison day
        buzz_pct: Percentage change in buzz
        context_text: Context from top negative topics
        
    Returns:
        Formatted prompt string for full interactions mode
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
Viết một đoạn insight chi tiết phân tích tình hình thảo luận và sự kiện chính xảy ra với thương hiệu.

YÊU CẦU BẮT BUỘC:
- Viết đúng 6–7 câu, dạng văn xuôi
- Câu 1: Nêu tổng số thảo luận và % thay đổi so với ngày trước
- Câu 2-3: Mô tả chi tiết SỰ KIỆN CHÍNH gây ra thảo luận (nguyên nhân cốt lõi)
- Câu 4: Phân tích cách thông tin lan truyền trên các kênh truyền thông
- Câu 5-6: Mô tả PHẢN ỨNG CỦA CỘNG ĐỒNG và tâm lý người tiêu dùng
- Câu 7: Đánh giá tác động và xu hướng hiện tại
- Văn phong chuyên nghiệp, trung lập, có chiều sâu phân tích
- CRITICAL: Mỗi câu PHẢI kết thúc bằng hyperlink dạng [Nguồn](URL)
- Mỗi câu gắn DUY NHẤT 1 URL từ dữ liệu được cung cấp
- CHỈ sử dụng URL có trong dữ liệu, KHÔNG tạo URL giả
- KHÔNG lặp URL
- KHÔNG gạch đầu dòng, KHÔNG tiêu đề

CẤU TRÚC INSIGHT MONG MUỐN:
1. Số liệu tổng quan + % thay đổi
2. Mô tả sự kiện chính (nguyên nhân)
3. Chi tiết về sự kiện (bối cảnh, tác động)
4. Cách thông tin lan truyền
5. Phản ứng của cộng đồng
6. Tâm lý người tiêu dùng
7. Đánh giá tình hình hiện tại

FORMAT BẮT BUỘC (Markdown hyperlink):
Tổng cộng có {report_total_buzz} thảo luận về {brand} trong vòng 24 giờ qua, [tăng/giảm] {abs(buzz_pct):.1f}% so với ngày trước đó [Nguồn](URL_1). Sự [tăng/giảm] này diễn ra trong bối cảnh [mô tả sự kiện chính] [Nguồn](URL_2). [Chi tiết về sự kiện và tác động] [Nguồn](URL_3). Thông tin này nhanh chóng lan rộng trên các nền tảng mạng xã hội, đặc biệt là [kênh chính], thu hút sự quan tâm của [đối tượng] [Nguồn](URL_4). Phản ứng từ cộng đồng chủ yếu thể hiện [mô tả cảm xúc và thái độ] [Nguồn](URL_5). [Mô tả tâm lý và hành vi người tiêu dùng] [Nguồn](URL_6). [Đánh giá tình hình hiện tại và xu hướng] [Nguồn](URL_7).

VÍ DỤ THAM KHẢO:
Tổng cộng có 506 thảo luận về Nestle trong vòng 24 giờ qua, giảm đáng kể 70.7% so với ngày trước đó [Nguồn](URL_1). Sự sụt giảm này diễn ra trong bối cảnh thông tin về việc Cục Quản lý Thực phẩm và Dược phẩm Hoa Kỳ (FDA) thu hồi 21 lô bánh ăn dặm Gerber do lo ngại về nguy cơ lẫn tạp chất nhựa và giấy [Nguồn](URL_2). Thông tin này nhanh chóng lan rộng trên các nền tảng mạng xã hội, đặc biệt là Facebook và TikTok, thu hút sự quan tâm của người tiêu dùng [Nguồn](URL_3). Phản ứng từ cộng đồng chủ yếu thể hiện sự lo lắng và hoài nghi về chất lượng sản phẩm của Nestle [Nguồn](URL_4). Một số phụ huynh bày tỏ sự thất vọng và băn khoăn trong việc lựa chọn sản phẩm an toàn cho con em mình [Nguồn](URL_5). Hiện tại, Việt Nam chưa có khuyến cáo chính thức về vấn đề này, tuy nhiên thông tin về đợt thu hồi vẫn đang được chia sẻ rộng rãi [Nguồn](URL_6). Một số ý kiến cho rằng đây là một dấu hiệu cho thấy Nestle đang gặp vấn đề về kiểm soát chất lượng [Nguồn](URL_7).

DỮ LIỆU (chứa URL thật trong trường URL):
{context_text}

LƯU Ý QUAN TRỌNG:
- CHỈ sử dụng URL có trong dữ liệu trên
- KHÔNG tạo ra URL giả như example.com
- KHÔNG sử dụng placeholder như URL_X, URL_Y
- Sao chép chính xác URL từ trường "URL:" trong dữ liệu
- Format hyperlink: [Nguồn](URL) để tạo link có thể click được
- PHẢI phân tích SỰ KIỆN CHÍNH, không chỉ so sánh số liệu
- Insight phải có CHIỀU SÂU và NỘI DUNG PHÂN TÍCH, không chỉ mô tả bề mặt
"""
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
Viết một đoạn insight chi tiết phân tích tình hình thảo luận và sự kiện chính xảy ra với thương hiệu.

YÊU CẦU BẮT BUỘC:
- Viết đúng 6–7 câu, dạng văn xuôi
- Câu 1: Nêu tổng số thảo luận và % thay đổi so với ngày trước
- Câu 2-3: Mô tả chi tiết SỰ KIỆN CHÍNH gây ra thảo luận (nguyên nhân cốt lõi)
- Câu 4: Phân tích cách thông tin lan truyền trên các kênh truyền thông
- Câu 5-6: Mô tả PHẢN ỨNG CỦA CỘNG ĐỒNG và tâm lý người tiêu dùng
- Câu 7: Đánh giá tác động và xu hướng hiện tại
- Văn phong chuyên nghiệp, trung lập, có chiều sâu phân tích
- CRITICAL: Mỗi câu PHẢI kết thúc bằng hyperlink dạng [Nguồn](URL)
- Mỗi câu gắn DUY NHẤT 1 URL từ dữ liệu được cung cấp
- CHỈ sử dụng URL có trong dữ liệu, KHÔNG tạo URL giả
- KHÔNG lặp URL
- KHÔNG gạch đầu dòng, KHÔNG tiêu đề

CẤU TRÚC INSIGHT MONG MUỐN:
1. Số liệu tổng quan + % thay đổi
2. Mô tả sự kiện chính (nguyên nhân)
3. Chi tiết về sự kiện (bối cảnh, tác động)
4. Cách thông tin lan truyền
5. Phản ứng của cộng đồng
6. Tâm lý người tiêu dùng
7. Đánh giá tình hình hiện tại

FORMAT BẮT BUỘC (Markdown hyperlink):
Tổng cộng có {report_total_buzz} thảo luận về {brand} trong vòng 24 giờ qua, [tăng/giảm] {abs(buzz_pct):.1f}% so với ngày trước đó [Nguồn](URL_1). Sự [tăng/giảm] này diễn ra trong bối cảnh [mô tả sự kiện chính] [Nguồn](URL_2). [Chi tiết về sự kiện và tác động] [Nguồn](URL_3). Thông tin này nhanh chóng lan rộng trên các nền tảng mạng xã hội, đặc biệt là [kênh chính], thu hút sự quan tâm của [đối tượng] [Nguồn](URL_4). Phản ứng từ cộng đồng chủ yếu thể hiện [mô tả cảm xúc và thái độ] [Nguồn](URL_5). [Mô tả tâm lý và hành vi người tiêu dùng] [Nguồn](URL_6). [Đánh giá tình hình hiện tại và xu hướng] [Nguồn](URL_7).

VÍ DỤ THAM KHẢO:
Tổng cộng có 506 thảo luận về Nestle trong vòng 24 giờ qua, giảm đáng kể 70.7% so với ngày trước đó [Nguồn](URL_1). Sự sụt giảm này diễn ra trong bối cảnh thông tin về việc Cục Quản lý Thực phẩm và Dược phẩm Hoa Kỳ (FDA) thu hồi 21 lô bánh ăn dặm Gerber do lo ngại về nguy cơ lẫn tạp chất nhựa và giấy [Nguồn](URL_2). Thông tin này nhanh chóng lan rộng trên các nền tảng mạng xã hội, đặc biệt là Facebook và TikTok, thu hút sự quan tâm của người tiêu dùng [Nguồn](URL_3). Phản ứng từ cộng đồng chủ yếu thể hiện sự lo lắng và hoài nghi về chất lượng sản phẩm của Nestle [Nguồn](URL_4). Một số phụ huynh bày tỏ sự thất vọng và băn khoăn trong việc lựa chọn sản phẩm an toàn cho con em mình [Nguồn](URL_5). Hiện tại, Việt Nam chưa có khuyến cáo chính thức về vấn đề này, tuy nhiên thông tin về đợt thu hồi vẫn đang được chia sẻ rộng rãi [Nguồn](URL_6). Một số ý kiến cho rằng đây là một dấu hiệu cho thấy Nestle đang gặp vấn đề về kiểm soát chất lượng [Nguồn](URL_7).

DỮ LIỆU (chứa URL thật trong trường URL):
{context_text}

LƯU Ý QUAN TRỌNG:
- CHỈ sử dụng URL có trong dữ liệu trên
- KHÔNG tạo ra URL giả như example.com
- KHÔNG sử dụng placeholder như URL_X, URL_Y
- Sao chép chính xác URL từ trường "URL:" trong dữ liệu
- Format hyperlink: [Nguồn](URL) để tạo link có thể click được
- PHẢI phân tích SỰ KIỆN CHÍNH, không chỉ so sánh số liệu
- Insight phải có CHIỀU SÂU và NỘI DUNG PHÂN TÍCH, không chỉ mô tả bề mặt
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
- CRITICAL: Mỗi câu PHẢI kết thúc bằng hyperlink dạng [Nguồn](URL)
- Mỗi câu gắn **1 URL thật từ dữ liệu**
- CHỈ sử dụng URL có trong dữ liệu được cung cấp
- KHÔNG tạo URL giả như example.com
- KHÔNG sử dụng placeholder như URL_X, URL_Y
- Không gạch đầu dòng

FORMAT BẮT BUỘC (Markdown hyperlink):
Câu insight... [Nguồn](URL_THẬT_TỪ_DỮ_LIỆU)

VÍ DỤ FORMAT:
Sự vụ ABC đạt đỉnh thảo luận vào ngày 15/3 với 2,500 lượt. [Nguồn](https://facebook.com/posts/123456)

DỮ LIỆU (chứa URL thật trong trường URL):
{peak_context_text}

LƯU Ý QUAN TRỌNG:
- Sao chép chính xác URL từ trường "URL:" trong dữ liệu
- Format hyperlink: [Nguồn](URL) để tạo link có thể click được
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
- CRITICAL: Mỗi câu PHẢI kết thúc bằng hyperlink dạng [Nguồn](URL)
- CHỈ sử dụng URL có trong dữ liệu được cung cấp
- KHÔNG tạo URL giả như example.com
- Mỗi URL chỉ dùng 1 lần
- Không gạch đầu dòng

FORMAT BẮT BUỘC (Markdown hyperlink):
Câu insight... [Nguồn](URL_THẬT_TỪ_DỮ_LIỆU)

VÍ DỤ FORMAT:
Facebook chiếm 65% tổng thảo luận về thương hiệu trong ngày. [Nguồn](https://facebook.com/posts/123456)

DỮ LIỆU (chứa URL thật trong trường URL):
{evidence_context}

LƯU Ý QUAN TRỌNG:
- Sao chép chính xác URL từ trường "URL:" trong dữ liệu
- KHÔNG sử dụng placeholder như URL_X, URL_Y
- Format hyperlink: [Nguồn](URL) để tạo link có thể click được
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
- CRITICAL: Mỗi câu PHẢI kết thúc bằng hyperlink dạng [Nguồn](URL)
- CHỈ sử dụng URL có trong danh sách "URL HỢP LỆ" ở trên
- KHÔNG tạo URL giả như example.com
- Mỗi URL chỉ dùng 1 lần

FORMAT BẮT BUỘC (Markdown hyperlink):
Câu insight về sentiment tổng quan... [Nguồn](URL_THẬT_1)
Câu insight về sentiment theo kênh... [Nguồn](URL_THẬT_2)

VÍ DỤ FORMAT:
Sentiment tiêu cực chiếm 45% tổng thảo luận trong ngày. [Nguồn](https://facebook.com/posts/123456)

LƯU Ý QUAN TRỌNG:
- Sao chép chính xác URL từ danh sách "URL HỢP LỆ"
- KHÔNG sử dụng placeholder như URL_X, URL_Y
- Format hyperlink: [Nguồn](URL) để tạo link có thể click được
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
- CRITICAL: Mỗi câu PHẢI kết thúc bằng hyperlink dạng [Nguồn](URL)
- CHỈ sử dụng URL có trong danh sách "URL HỢP LỆ" ở trên
- KHÔNG tạo URL giả như example.com
- Mỗi URL chỉ dùng 1 lần

FORMAT BẮT BUỘC (Markdown hyperlink):
Câu insight... [Nguồn](URL_THẬT_TỪ_DANH_SÁCH)

VÍ DỤ FORMAT:
Facebook dẫn đầu với 1,200 lượt thảo luận, tăng 25% so với hôm qua. [Nguồn](https://facebook.com/posts/123456)

LƯU Ý QUAN TRỌNG:
- Sao chép chính xác URL từ danh sách "URL HỢP LỆ"
- KHÔNG sử dụng placeholder như URL_X, URL_Y
- Format hyperlink: [Nguồn](URL) để tạo link có thể click được
"""
