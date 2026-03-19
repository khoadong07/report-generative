#!/usr/bin/env python3
"""
Script to generate complete prompt for weekly slide platforms
Input: Excel file, brand name, week dates
Output: Complete prompt with JSON data embedded (11 slides)
"""

import json
from datetime import datetime
import pandas as pd


def format_number(num):
    """Format number with commas"""
    if isinstance(num, (int, float)):
        return f"{int(num):,}"
    return str(num)


def format_date(date_str):
    """Format date to DD/MM/YYYY"""
    if isinstance(date_str, str):
        formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y"]
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime("%d/%m/%Y")
            except ValueError:
                continue
        try:
            date_obj = pd.to_datetime(date_str)
            return date_obj.strftime("%d/%m/%Y")
        except:
            return str(date_str)
    else:
        return date_str.strftime("%d/%m/%Y")


def generate_complete_prompt(report_data):
    """Generate complete prompt with all 11 slides embedded"""

    metadata = report_data['report_metadata']
    brand = metadata['brand']
    week1_period = metadata['week1_period']

    show_interactions = report_data['slide_1'].get('show_interactions', True)

    prompt = "Tạo bản trình bày chuyên nghiệp 11 slide cho Báo cáo Sức khỏe Thương hiệu Tuần:\n\n"
    prompt += "===============================================================\n"
    prompt += f"THƯƠNG HIỆU: {brand}\n"
    prompt += f"KỲ BÁO CÁO: {week1_period} (7 ngày)\n"
    prompt += "LOẠI BÁO CÁO: Phân tích Tuần\n"
    prompt += "===============================================================\n\n"

    # ── SLIDE 1 ──────────────────────────────────────────────────────────────
    prompt += "----------------------------------------------------------------\n"
    prompt += "SLIDE 1 - TỔNG QUAN VỀ THƯƠNG HIỆU\n"
    prompt += "----------------------------------------------------------------\n\n"
    prompt += f"Tiêu đề: \"{report_data['slide_1']['title']}\"\n"
    prompt += f"Phụ đề: \"{report_data['slide_1']['subtitle']}\"\n\n"

    if show_interactions:
        prompt += "BỐ CỤC: 2 CỘT\n"
        prompt += "  TRÁI (50%): Biểu đồ cột so sánh 4 tuần (giá trị tuyệt đối + % tăng trưởng)\n"
        prompt += "  PHẢI (50%): Lưới 6 thẻ KPI (2 hàng x 3 cột)\n"
        prompt += "  DƯỚI: Khung insight\n\n"
    else:
        prompt += "BỐ CỤC: 2 CỘT\n"
        prompt += "  TRÁI (50%): Biểu đồ cột so sánh 4 tuần (giá trị tuyệt đối + % tăng trưởng)\n"
        prompt += "  PHẢI (50%): Thẻ KPI lớn cho Tổng đề cập\n"
        prompt += "  DƯỚI: Khung insight\n\n"

    prompt += "CHỈ SỐ TUẦN HIỆN TẠI:\n"
    for metric in report_data['slide_1']['current_week_metrics']:
        if 'change_percent' in metric:
            sign = "+" if metric['change_percent'] > 0 else ""
            prompt += f"- {metric['label']}: {format_number(metric['value'])} ({sign}{metric['change_percent']}% so với tuần trước)\n"
        else:
            prompt += f"- {metric['label']}: {format_number(metric['value'])}\n"

    prompt += "\nSO SÁNH 4 TUẦN:\n"
    for week in report_data['slide_1']['weekly_comparison']:
        if week['growth_rate'] is not None:
            sign = "+" if week['growth_rate'] > 0 else ""
            prompt += f"- {week['week']}: {format_number(week['total_mentions'])} lượt ({sign}{week['growth_rate']}%)\n"
        else:
            prompt += f"- {week['week']}: {format_number(week['total_mentions'])} lượt\n"

    prompt += f"\nINSIGHT:\n{report_data['slide_1']['insight']}\n\n"

    # ── SLIDE 2 ──────────────────────────────────────────────────────────────
    prompt += "----------------------------------------------------------------\n"
    prompt += "SLIDE 2 - XU HƯỚNG ĐỀ CẬP (TRENDLINE)\n"
    prompt += "----------------------------------------------------------------\n\n"
    prompt += f"Tiêu đề: \"{report_data['slide_2']['title']}\"\n"
    prompt += f"Phụ đề: \"{report_data['slide_2']['subtitle']}\"\n\n"
    prompt += "BỐ CỤC: 1 CỘT\n"
    prompt += "  TRÊN: Biểu đồ đường xu hướng 7 ngày\n"
    prompt += "  DƯỚI: Khung insight\n\n"
    prompt += "DỮ LIỆU XU HƯỚNG (7 ngày):\n"
    for point in report_data['slide_2']['trendline']:
        prompt += f"- {format_date(point['date'])}: {format_number(point['mentions'])} lượt\n"
    prompt += f"\nINSIGHT:\n{report_data['slide_2']['insight']}\n\n"

    # ── SLIDE 3 ──────────────────────────────────────────────────────────────
    prompt += "----------------------------------------------------------------\n"
    prompt += "SLIDE 3 - PHÂN BỔ LƯỢT ĐỀ CẬP THEO KÊNH\n"
    prompt += "----------------------------------------------------------------\n\n"
    prompt += f"Tiêu đề: \"{report_data['slide_3']['title']}\"\n"
    prompt += f"Phụ đề: \"{report_data['slide_3']['subtitle']}\"\n\n"
    prompt += "BỐ CỤC: 2 CỘT\n"
    prompt += "  TRÁI (50%): Biểu đồ donut (phân bổ kênh) - KHÔNG nhãn trên biểu đồ, chú thích bên dưới\n"
    prompt += "  PHẢI (50%): Biểu đồ thanh ngang top 10 nguồn\n"
    prompt += "  DƯỚI: Khung insight\n\n"
    prompt += "PHÂN BỔ THEO KÊNH:\n"
    total_channel = sum(ch['count'] for ch in report_data['slide_3']['channel_distribution'])
    for ch in report_data['slide_3']['channel_distribution']:
        pct = (ch['count'] / total_channel * 100) if total_channel > 0 else 0
        prompt += f"- {ch['Channel']}: {format_number(ch['count'])} lượt ({pct:.1f}%)\n"
    prompt += "\nTOP 10 NGUỒN:\n"
    for src in report_data['slide_3']['top_sources']:
        prompt += f"- {src['SiteName']}: {format_number(src['count'])} lượt\n"
    prompt += f"\nINSIGHT:\n{report_data['slide_3']['insight']}\n\n"

    # ── SLIDE 4 ──────────────────────────────────────────────────────────────
    prompt += "----------------------------------------------------------------\n"
    prompt += "SLIDE 4 - TOP NGUỒN CÓ LƯỢNG TƯƠNG TÁC CAO NHẤT\n"
    prompt += "----------------------------------------------------------------\n\n"
    prompt += f"Tiêu đề: \"{report_data['slide_4']['title']}\"\n"
    prompt += f"Phụ đề: \"{report_data['slide_4']['subtitle']}\"\n\n"
    prompt += "BỐ CỤC: Bảng toàn trang, KHÔNG có insight\n\n"
    show_int4 = report_data['slide_4'].get('show_interactions', True)
    if show_int4:
        prompt += "CỘT: STT | Nguồn | Tổng tương tác | Reactions | Shares | Comments\n\n"
        prompt += "DỮ LIỆU BẢNG:\n"
        for row in report_data['slide_4']['table_rows']:
            prompt += f"- [{row['stt']}] {row['source_name']} | {format_number(row['total_engagement'])} | {format_number(row['reactions'])} | {format_number(row['shares'])} | {format_number(row['comments'])}\n"
    else:
        prompt += "CỘT: STT | Nguồn | Số lượng đề cập\n\n"
        prompt += "DỮ LIỆU BẢNG:\n"
        for row in report_data['slide_4']['table_rows']:
            prompt += f"- [{row['stt']}] {row['source_name']} | {format_number(row['count'])}\n"
    prompt += "\n"

    # ── SLIDE 5 ──────────────────────────────────────────────────────────────
    prompt += "----------------------------------------------------------------\n"
    prompt += "SLIDE 5 - TOP BÀI ĐĂNG CÓ TƯƠNG TÁC CAO NHẤT\n"
    prompt += "----------------------------------------------------------------\n\n"
    prompt += f"Tiêu đề: \"{report_data['slide_5']['title']}\"\n"
    prompt += f"Phụ đề: \"{report_data['slide_5']['subtitle']}\"\n\n"
    prompt += "BỐ CỤC: Bảng toàn trang, KHÔNG có insight\n\n"
    show_int5 = report_data['slide_5'].get('show_interactions', True)
    if show_int5:
        prompt += "CỘT: STT | Nội dung | Ngày đăng | Kênh | Nguồn | Reactions | Shares | Comments\n\n"
        prompt += "DỮ LIỆU BẢNG:\n"
        for row in report_data['slide_5']['table_rows']:
            preview = row['content'][:100] + '...' if len(row['content']) > 100 else row['content']
            prompt += f"- [{row['stt']}] {preview} | {format_date(row['published_date'])} | {row['channel']} | {row['site_name']} | {format_number(row['reactions'])} | {format_number(row['shares'])} | {format_number(row['comments'])} | {row['url']}\n"
    else:
        prompt += "CỘT: STT | Nội dung | Ngày đăng | Kênh | Nguồn | URL\n\n"
        prompt += "DỮ LIỆU BẢNG:\n"
        for row in report_data['slide_5']['table_rows']:
            preview = row['content'][:100] + '...' if len(row['content']) > 100 else row['content']
            prompt += f"- [{row['stt']}] {preview} | {format_date(row['published_date'])} | {row['channel']} | {row['site_name']} | {row['url']}\n"
    prompt += "\n"

    # ── SLIDE 6 ──────────────────────────────────────────────────────────────
    prompt += "----------------------------------------------------------------\n"
    prompt += "SLIDE 6 - SẮC THÁI VÀ CỤM CHỦ ĐỀ ĐỀ CẬP NỔI BẬT\n"
    prompt += "----------------------------------------------------------------\n\n"
    prompt += f"Tiêu đề: \"{report_data['slide_6']['title']}\"\n"
    prompt += f"Phụ đề: \"{report_data['slide_6']['subtitle']}\"\n\n"
    prompt += "BỐ CỤC: 2 CỘT\n"
    prompt += "  TRÁI (50%): Hai biểu đồ donut nhỏ cạnh nhau (Tuần trước | Tuần này) + ghi chú NSR\n"
    prompt += "  PHẢI (50%): Biểu đồ thanh ngang xếp chồng top 10 chủ đề theo sắc thái\n"
    prompt += "  DƯỚI: Khung insight\n\n"
    prompt += f"NSR Tuần trước: {report_data['slide_6']['previous_nsr']}%\n"
    prompt += f"NSR Tuần này: {report_data['slide_6']['current_nsr']}%\n"
    nsr_sign = "+" if report_data['slide_6']['nsr_growth'] > 0 else ""
    prompt += f"Tăng trưởng NSR: {nsr_sign}{report_data['slide_6']['nsr_growth']:.2f}%\n\n"
    prompt += "SẮC THÁI Tuần trước:\n"
    total_prev = sum(s['count'] for s in report_data['slide_6']['previous_sentiment'])
    for s in report_data['slide_6']['previous_sentiment']:
        pct = (s['count'] / total_prev * 100) if total_prev > 0 else 0
        prompt += f"- {s['sentiment']}: {format_number(s['count'])} lượt ({pct:.1f}%)\n"
    prompt += "\nSẮC THÁI Tuần này:\n"
    total_curr = sum(s['count'] for s in report_data['slide_6']['current_sentiment'])
    for s in report_data['slide_6']['current_sentiment']:
        pct = (s['count'] / total_curr * 100) if total_curr > 0 else 0
        prompt += f"- {s['sentiment']}: {format_number(s['count'])} lượt ({pct:.1f}%)\n"
    prompt += "\nTOP CHỦ ĐỀ THEO SẮC THÁI:\n"
    for t in report_data['slide_6']['top_topics_with_sentiment']:
        prompt += f"- {t['topic']}: Tổng {format_number(t['total'])} (Tiêu cực: {t['negative']}, Trung tính: {t['neutral']}, Tích cực: {t['positive']})\n"
    prompt += f"\nINSIGHT:\n{report_data['slide_6']['insight']}\n\n"

    # ── SLIDE 7 ──────────────────────────────────────────────────────────────
    prompt += "----------------------------------------------------------------\n"
    prompt += "SLIDE 7 - CÁC CHỦ ĐỀ ĐỀ CẬP TÍCH CỰC\n"
    prompt += "----------------------------------------------------------------\n\n"
    prompt += f"Tiêu đề: \"{report_data['slide_7']['title']}\"\n"
    prompt += f"Phụ đề: \"{report_data['slide_7']['subtitle']}\"\n\n"
    prompt += "BỐ CỤC: 1 CỘT\n"
    prompt += "  TRÊN: Biểu đồ thanh ngang top 10 chủ đề tích cực (màu: #00C055)\n"
    prompt += "  DƯỚI: Khung insight\n\n"
    prompt += "CHỦ ĐỀ TÍCH CỰC:\n"
    for t in report_data['slide_7']['positive_topics']:
        prompt += f"- {t['Labels1']}: {format_number(t['count'])} lượt\n"
    prompt += f"\nINSIGHT:\n{report_data['slide_7']['insight']}\n\n"

    # ── SLIDE 8 ──────────────────────────────────────────────────────────────
    prompt += "----------------------------------------------------------------\n"
    prompt += "SLIDE 8 - TOP BÀI ĐĂNG TÍCH CỰC\n"
    prompt += "----------------------------------------------------------------\n\n"
    prompt += f"Tiêu đề: \"{report_data['slide_8']['title']}\"\n"
    prompt += f"Phụ đề: \"{report_data['slide_8']['subtitle']}\"\n\n"
    prompt += "BỐ CỤC: Bảng toàn trang, KHÔNG có insight\n"
    prompt += "CỘT: STT | Nội dung | Ngày đăng | Kênh | Nguồn | Bình luận tích cực\n\n"
    prompt += "DỮ LIỆU BẢNG:\n"
    for row in report_data['slide_8']['table_rows']:
        preview = row['content'][:100] + '...' if len(row['content']) > 100 else row['content']
        prompt += f"- [{row['stt']}] {preview} | {format_date(row['published_date'])} | {row['channel']} | {row['site_name']} | {format_number(row['positive_comments'])} | {row['url']}\n"
    prompt += "\n"

    # ── SLIDE 9 ──────────────────────────────────────────────────────────────
    prompt += "----------------------------------------------------------------\n"
    prompt += "SLIDE 9 - CÁC CHỦ ĐỀ ĐỀ CẬP TIÊU CỰC\n"
    prompt += "----------------------------------------------------------------\n\n"
    prompt += f"Tiêu đề: \"{report_data['slide_9']['title']}\"\n"
    prompt += f"Phụ đề: \"{report_data['slide_9']['subtitle']}\"\n\n"
    prompt += "BỐ CỤC: 1 CỘT\n"
    prompt += "  TRÊN: Biểu đồ thanh ngang top 10 chủ đề tiêu cực (màu: #EC003F)\n"
    prompt += "  DƯỚI: Khung insight\n\n"
    prompt += "CHỦ ĐỀ TIÊU CỰC:\n"
    for t in report_data['slide_9']['negative_topics']:
        prompt += f"- {t['Labels1']}: {format_number(t['count'])} lượt\n"
    prompt += f"\nINSIGHT:\n{report_data['slide_9']['insight']}\n\n"

    # ── SLIDE 10 ─────────────────────────────────────────────────────────────
    prompt += "----------------------------------------------------------------\n"
    prompt += "SLIDE 10 - TOP BÀI ĐĂNG TIÊU CỰC\n"
    prompt += "----------------------------------------------------------------\n\n"
    prompt += f"Tiêu đề: \"{report_data['slide_10']['title']}\"\n"
    prompt += f"Phụ đề: \"{report_data['slide_10']['subtitle']}\"\n\n"
    prompt += "BỐ CỤC: Bảng toàn trang, KHÔNG có insight\n"
    prompt += "CỘT: STT | Nội dung | Ngày đăng | Kênh | Nguồn | Bình luận tiêu cực\n\n"
    prompt += "DỮ LIỆU BẢNG:\n"
    for row in report_data['slide_10']['table_rows']:
        preview = row['content'][:100] + '...' if len(row['content']) > 100 else row['content']
        prompt += f"- [{row['stt']}] {preview} | {format_date(row['published_date'])} | {row['channel']} | {row['site_name']} | {format_number(row['negative_comments'])} | {row['url']}\n"
    prompt += "\n"

    # ── SLIDE 11 ─────────────────────────────────────────────────────────────
    if 'slide_11' in report_data:
        s11 = report_data['slide_11']
        prompt += "----------------------------------------------------------------\n"
        prompt += "SLIDE 11 - TỔNG QUAN ĐỀ CẬP VỀ THƯƠNG HIỆU VỚI CÁC ĐỐI THỦ\n"
        prompt += "----------------------------------------------------------------\n\n"
        prompt += f"Tiêu đề: \"{s11['title']}\"\n"
        prompt += f"Phụ đề: \"{s11['subtitle']}\"\n\n"
        prompt += "BỐ CỤC: 2 HÀNG\n"
        prompt += "  HÀNG 1 (toàn trang): Khung insight tổng quan\n"
        prompt += "  HÀNG 2 TRÁI (50%): Hai biểu đồ donut cạnh nhau (Tuần trước | Tuần hiện tại)\n"
        prompt += "  HÀNG 2 PHẢI (50%): Biểu đồ cột đôi đứng so sánh thương hiệu\n\n"
        prompt += f"INSIGHT:\n{s11['insight']}\n\n"

        # Donut spec
        prompt += "─── BIỂU ĐỒ DONUT ───────────────────────────────────────────\n"
        prompt += "QUY TẮC THIẾT KẾ DONUT:\n"
        prompt += "  • Ở GIỮA vòng donut: số TỔNG lượng thảo luận (font lớn, bold)\n"
        prompt += "  • VÒNG NGOÀI mỗi cung: hiển thị % tỷ trọng của topic đó (vd: 45.2%)\n"
        prompt += "  • BÊN DƯỚI biểu đồ: chú thích màu sắc theo từng thương hiệu\n\n"

        prev_data = [i for i in s11['donut_charts']['week_before']['data'] if i['mentions'] > 0]
        curr_data = [i for i in s11['donut_charts']['current_week']['data'] if i['mentions'] > 0]
        total_prev = sum(i['mentions'] for i in prev_data)
        total_curr = sum(i['mentions'] for i in curr_data)

        prompt += f"DONUT TUẦN TRƯỚC — tổng ở giữa: {format_number(total_prev)} lượt\n"
        for item in sorted(prev_data, key=lambda x: x['mentions'], reverse=True):
            pct = (item['mentions'] / total_prev * 100) if total_prev > 0 else 0
            prompt += f"  {item['brand']}: {format_number(item['mentions'])} lượt ({pct:.1f}%) | màu {item['color']}\n"

        prompt += f"\nDONUT TUẦN HIỆN TẠI — tổng ở giữa: {format_number(total_curr)} lượt\n"
        for item in sorted(curr_data, key=lambda x: x['mentions'], reverse=True):
            pct = (item['mentions'] / total_curr * 100) if total_curr > 0 else 0
            prompt += f"  {item['brand']}: {format_number(item['mentions'])} lượt ({pct:.1f}%) | màu {item['color']}\n"

        prompt += "\nCHÚ THÍCH CHUNG (hiển thị bên dưới cả 2 donut):\n"
        for item in s11['legend']:
            prompt += f"  ■ {item['brand']}: {item['color']}\n"

        # Grouped bar chart spec
        prompt += "\n─── BIỂU ĐỒ CỘT ĐÔI ĐỨNG ──────────────────────────────────\n"
        prompt += f"Tiêu đề: {s11['bar_chart']['title']}\n"
        prompt += "QUY TẮC THIẾT KẾ CỘT ĐÔI:\n"
        prompt += "  • Mỗi thương hiệu = 1 cặp cột đứng cạnh nhau\n"
        prompt += "  • Cột TRÁI (màu nhạt) = Tuần trước | Cột PHẢI (màu đậm) = Tuần này\n"
        prompt += "  • Sắp xếp các cặp cột từ TRÁI sang PHẢI theo thứ tự GIẢM DẦN lượt tuần hiện tại\n"
        prompt += "  • TRÊN mỗi cột: hiển thị số lượng tương ứng\n"
        prompt += "  • TRÊN mỗi CẶP cột: hiển thị mũi tên biến động + % (↑ màu xanh lá / ↓ màu đỏ / → màu xám)\n"
        prompt += "  • Chú thích: ■ Tuần trước  ■ Tuần này\n\n"

        bar_sorted = sorted(s11['bar_chart']['data'], key=lambda x: x['current_week'], reverse=True)
        prompt += "DỮ LIỆU (thứ tự giảm dần theo tuần hiện tại):\n"
        for item in bar_sorted:
            sign = "+" if item['percentage_change'] >= 0 else ""
            arrow = "↑" if item['percentage_change'] > 0 else ("↓" if item['percentage_change'] < 0 else "→")
            color_label = "xanh lá" if item['change_color'] == "green" else ("đỏ" if item['change_color'] == "red" else "xám")
            prompt += (
                f"  {item['brand']}: "
                f"Tuần trước = {format_number(item['week_before'])} | "
                f"Tuần này = {format_number(item['current_week'])} | "
                f"{arrow} {sign}{item['percentage_change']}% ({color_label})\n"
            )
        prompt += "\n"

    # ── SLIDE 12 ─────────────────────────────────────────────────────────────
    if 'slide_12' in report_data:
        s12 = report_data['slide_12']
        prompt += "----------------------------------------------------------------\n"
        prompt += "SLIDE 12 - ĐƯỜNG BIỂU DIỄN XU HƯỚNG ĐỀ CẬP NHIỀU THƯƠNG HIỆU\n"
        prompt += "----------------------------------------------------------------\n\n"
        prompt += f"Tiêu đề: \"{s12['title']}\"\n"
        prompt += f"Phụ đề: \"{s12['subtitle']}\"\n\n"
        prompt += "BỐ CỤC: 1 CỘT TOÀN TRANG\n"
        prompt += "  TRÊN: Biểu đồ đường theo ngày, mỗi thương hiệu 1 đường màu riêng\n"
        prompt += "  DƯỚI: Chú thích màu sắc theo thương hiệu\n\n"
        prompt += "QUY TẮC ANNOTATION TRÊN PEAK:\n"
        prompt += "  - Mỗi thương hiệu: tìm ngày có lượt đề cập cao nhất\n"
        prompt += "  - Tại điểm peak đó: hiển thị hộp chú thích nổi gồm:\n"
        prompt += "      • Ngày (DD/MM/YYYY)\n"
        prompt += "      • Snippet ~5 từ đầu + (...) làm hyperlink dẫn đến URL bài viết\n"
        prompt += "  - Hộp chú thích dùng màu tương ứng với đường của thương hiệu đó\n\n"

        # Trendline data
        prompt += "DỮ LIỆU ĐƯỜNG XU HƯỚNG (theo ngày):\n"
        for b in s12['brands']:
            tl = s12['trendlines'].get(b, [])
            total = sum(p['mentions'] for p in tl)
            dates_str = " | ".join(
                f"{format_date(p['date'])}: {p['mentions']}" for p in tl if p['mentions'] > 0
            )
            prompt += f"  [{b}] Tổng: {format_number(total)} lượt\n"
            if dates_str:
                prompt += f"    Ngày có đề cập: {dates_str}\n"

        # Peak annotations
        prompt += "\nANNOTATION TẠI ĐIỂM PEAK:\n"
        for b, ann in s12['annotations'].items():
            prompt += (
                f"  [{b}] Ngày {format_date(ann['date'])} — {format_number(ann['mentions'])} lượt\n"
                f"    Snippet: \"{ann['snippet']}\"\n"
                f"    URL: {ann['url']}\n"
            )
        prompt += "\n"

    # ── DESIGN THEME ─────────────────────────────────────────────────────────
    prompt += "===============================================================\n"
    prompt += "THIẾT KẾ TỔNG THỂ\n"
    prompt += "===============================================================\n\n"
    prompt += "BẢNG MÀU:\n"
    prompt += "- Xanh chính: #0045C4\n"
    prompt += "- Xanh lá (tích cực): #00C055\n"
    prompt += "- Đỏ (tiêu cực): #EC003F\n"
    prompt += "- Xám trung tính: #6b7280\n"
    prompt += "- Nền: #FFFFFF\n\n"
    prompt += "TYPOGRAPHY:\n"
    prompt += "- Tiêu đề slide: 32px Bold\n"
    prompt += "- Tiêu đề mục: 24px Bold\n"
    prompt += "- Nội dung: 14px Regular\n"
    prompt += "- Font: Inter hoặc Roboto\n\n"
    prompt += "ĐỊNH DẠNG SỐ: dấu phẩy phân cách hàng nghìn, dấu chấm thập phân (vd: 1,234.5)\n\n"
    prompt += "MẪU BỐ CỤC:\n"
    prompt += "- Mẫu A (2 cột + Insight): Slide 1, 3, 6\n"
    prompt += "- Mẫu B (1 cột + Insight): Slide 2, 7, 9\n"
    prompt += "- Mẫu C (Bảng): Slide 4, 5, 8, 10\n"
    prompt += "- Mẫu D (2 hàng): Slide 11\n"
    prompt += "- Mẫu E (Đường nhiều brand + annotation): Slide 12\n\n"
    prompt += "===============================================================\n"
    prompt += "HƯỚNG DẪN BẮT BUỘC:\n"
    prompt += "1. Tạo tất cả slide với đúng dữ liệu được cung cấp ở trên\n"
    prompt += "2. Tuân thủ chính xác bố cục cho từng slide\n"
    prompt += "3. Đảm bảo tất cả biểu đồ được định dạng và gán nhãn đúng\n"
    prompt += "4. Sử dụng bảng màu đã chỉ định nhất quán\n"
    prompt += "5. Giữ nguyên tất cả đường dẫn nguồn dưới dạng hyperlink có thể click\n"
    prompt += "6. Áp dụng quy tắc định dạng số nhất quán\n"
    prompt += "7. Slide 11 donut: tổng ở giữa, % tỷ trọng trên vòng ngoài, chú thích bên dưới\n"
    prompt += "8. Slide 11 cột đôi: cột đứng, sắp xếp giảm dần, số lượng + mũi tên biến động trên mỗi cặp\n"
    prompt += "9. Slide 12: annotation tại peak mỗi brand, snippet là hyperlink dẫn URL bài viết\n"
    prompt += "===============================================================\n"

    return prompt
