"""
Module: Prompt Builder
Chức năng: Xây dựng biến prompt từ dữ liệu slides (bao gồm sample data)
"""
from collections import OrderedDict
import json


def _format_sample_records(records, max_records=3):
    """
    Format sample records thành string dễ đọc với đầy đủ field
    
    Args:
        records (list): Danh sách records
        max_records (int): Số records tối đa
        
    Returns:
        str: Formatted string
    """
    if not records:
        return "Không có dữ liệu mẫu"
    
    formatted = []
    for i, record in enumerate(records[:max_records], 1):
        # Convert datetime objects to string
        record_clean = {}
        for key, value in record.items():
            if hasattr(value, 'isoformat'):  # datetime object
                record_clean[key] = value.isoformat()
            else:
                record_clean[key] = value
        
        # Format JSON với indent để dễ đọc
        json_str = json.dumps(record_clean, ensure_ascii=False, indent=2, default=str)
        formatted.append(f"Mẫu {i}:\n{json_str}")
    
    return "\n\n".join(formatted)


def build_prompt_variables(slides_data):
    """
    Xây dựng dictionary biến prompt từ dữ liệu slides (bao gồm sample data)
    
    Args:
        slides_data (dict): Dictionary chứa dữ liệu từng slide
        
    Returns:
        OrderedDict: Dictionary biến prompt
    """
    s1 = slides_data["slide_1"]
    s2 = slides_data["slide_2"]
    s3 = slides_data["slide_3"]
    s4 = slides_data["slide_4"]
    s5 = slides_data["slide_5"]
    s6 = slides_data["slide_6"]
    s7 = slides_data["slide_7"]
    s8 = slides_data["slide_8"]
    s9 = slides_data["slide_9"]
    s10 = slides_data["slide_10"]
    s11 = slides_data["slide_11"]
    s12 = slides_data["slide_12"]
    
    prompt_vars = OrderedDict({
        "PRIMARY_BRAND": s2["primary_brand"],
        "STUDY_PERIOD": s1["study_period"],
        "DATA_SOURCE": s1["data_source"],
        "COMPETITOR_LIST": s2["competitor_list"],
        "TOTAL_MENTIONS": f"{s1['total_mentions']:,}",
        "TOTAL_CHANNELS": s1["total_channels"],
        "TOTAL_BRANDS": s1["total_brands"],
        "TOTAL_TOPICS": s1["total_topics"],
        "SAMPLE_OVERVIEW_RECORDS": _format_sample_records(s1.get("sample_records", [])),
        "SOV_TABLE": s2["sov_table"],
        "SAMPLE_PRIMARY_BRAND_RECORDS": _format_sample_records(s2.get("sample_primary_brand", [])),
        "DAILY_BUZZ_TABLE": s3["daily_buzz_table"],
        "SAMPLE_HIGH_BUZZ_RECORDS": _format_sample_records(s3.get("sample_high_buzz_records", [])),
        "NUM_HIGHLIGHTS": s4["num_highlights"],
        "HIGHLIGHTED_URL_LIST": s4["highlighted_url_list"],
        "HIGHLIGHT_CHANNELS": s4["highlight_channels"],
        "INTERACTION_METRIC_STATUS": s4["interaction_metric_status"],
        "SAMPLE_HIGHLIGHTS": _format_sample_records(s4.get("sample_highlights", [])),
        "SENTIMENT_OVERVIEW_TABLE": s5["sentiment_overview_table"],
        "SAMPLE_SENTIMENT_RECORDS": _format_sample_records(s5.get("sample_sentiment_records", [])),
        "CHANNEL_VOLUME_TABLE": s6["channel_volume_table"],
        "SAMPLE_CHANNEL_RECORDS": _format_sample_records(s6.get("sample_channel_records", [])),
        "SENTIMENT_BY_CHANNEL_TABLE": s7["sentiment_by_channel_table"],
        "SAMPLE_SENTIMENT_CHANNEL_RECORDS": _format_sample_records(s7.get("sample_sentiment_channel_records", [])),
        "TOPIC_RANKING_TABLE": s8["topic_ranking_table"],
        "FOCUS_TOPIC_LIST": s8["focus_topic_list"],
        "SAMPLE_TOPIC_RECORDS": _format_sample_records(s8.get("sample_topic_records", [])),
        "TOPIC_TREND_DAILY_TABLE": s9["topic_trend_daily_table"],
        "SAMPLE_TREND_RECORDS": _format_sample_records(s9.get("sample_trend_records", [])),
        "TOPIC_BY_CHANNEL_TABLE": s10["topic_by_channel_table"],
        "SAMPLE_TOPIC_CHANNEL_RECORDS": _format_sample_records(s10.get("sample_topic_channel_records", [])),
        "SENTIMENT_BY_BRAND_TABLE": s11["sentiment_by_brand_table"],
        "BRAND_VOLUME_TABLE": s11["brand_volume_table"],
        "SAMPLE_BRAND_SENTIMENT_RECORDS": _format_sample_records(s11.get("sample_brand_sentiment_records", [])),
        "TOPIC_BY_BRAND_TABLE": s12["topic_by_brand_table"],
        "SAMPLE_TOPIC_BRAND_RECORDS": _format_sample_records(s12.get("sample_topic_brand_records", [])),
    })
    
    return prompt_vars
