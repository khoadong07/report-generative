#!/usr/bin/env python3
"""
Tạo prompt hoàn chỉnh cho nền tảng slide từ dữ liệu báo cáo tuần.
Đầu vào: report_data dict (có thể chứa một tập con các slide)
Đầu ra: Chuỗi prompt chỉ nhúng các slide đã được build
"""

import json
from datetime import datetime
import pandas as pd


def format_number(num):
    if isinstance(num, (int, float)):
        return f"{int(num):,}"
    return str(num)


def format_date(date_str):
    if isinstance(date_str, str):
        for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y"]:
            try:
                return datetime.strptime(date_str, fmt).strftime("%d/%m/%Y")
            except ValueError:
                continue
        try:
            return pd.to_datetime(date_str).strftime("%d/%m/%Y")
        except Exception:
            return str(date_str)
    return date_str.strftime("%d/%m/%Y")


def _header(title):
    return (
        "----------------------------------------------------------------\n"
        f"{title}\n"
        "----------------------------------------------------------------\n\n"
    )


def generate_complete_prompt(report_data):
    metadata    = report_data.get("report_metadata", {})
    brand       = metadata.get("brand", "")
    week1_period = metadata.get("week1_period", "")

    show_interactions = True
    for k in ("slide_1", "slide_4", "slide_5"):
        if k in report_data:
            show_interactions = report_data[k].get("show_interactions", True)
            break

    built      = [k for k in report_data if k.startswith("slide_")]
    built_nums = sorted(int(k.split("_")[1]) for k in built)

    prompt  = f"Tạo bản trình bày chuyên nghiệp {len(built_nums)} slide cho Báo cáo Sức khoẻ Thương hiệu Tuần:\n\n"
    prompt += "===============================================================\n"
    prompt += f"THƯƠNG HIỆU: {brand}\n"
    prompt += f"KỲ BÁO CÁO: {week1_period} (7 ngày)\n"
    prompt += "LOẠI BÁO CÁO: Phân tích Tuần\n"
    prompt += "===============================================================\n\n"

    # ── SLIDE 1 ───────────────────────────────────────────────────────────────
    if "slide_1" in report_data:
        s = report_data["slide_1"]
        prompt += _header("SLIDE 1 - TỔNG QUAN VỀ THƯƠNG HIỆU")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        if show_interactions:
            prompt += (
                "BỐ CỤC: 2 CỘT\n"
                "  TRÁI (50%): Biểu đồ cột so sánh 4 tuần\n"
                "  PHẢI (50%): Lưới 6 thẻ KPI (2 hàng x 3 cột)\n"
                "  DƯỚI: Khung nhận định\n\n"
            )
        else:
            prompt += (
                "BỐ CỤC: 2 CỘT\n"
                "  TRÁI (50%): Biểu đồ cột so sánh 4 tuần\n"
                "  PHẢI (50%): 3 thẻ KPI (Tổng bài đăng, Tổng bình luận, Tổng thảo luận)\n"
                "  DƯỚI: Khung nhận định\n\n"
            )
        prompt += "CHỈ SỐ TUẦN HIỆN TẠI:\n"
        for m in s["current_week_metrics"]:
            cp   = m.get("change_percent")
            sign = f" ({'+' if cp > 0 else ''}{cp}% so với tuần trước)" if cp is not None else ""
            prompt += f"- {m['label']}: {format_number(m['value'])}{sign}\n"
        prompt += "\nSO SÁNH 4 TUẦN:\n"
        for w in s["weekly_comparison"]:
            gr   = w["growth_rate"]
            sign = f" ({'+' if gr > 0 else ''}{gr}%)" if gr is not None else ""
            prompt += f"- {w['week']}: {format_number(w['total_mentions'])} lượt{sign}\n"
        prompt += f"\nNHẬN ĐỊNH:\n{s['insight']}\n\n"

    # ── SLIDE 2 ───────────────────────────────────────────────────────────────
    if "slide_2" in report_data:
        s = report_data["slide_2"]
        prompt += _header("SLIDE 2 - XU HƯỚNG ĐỀ CẬP (ĐƯỜNG TRENDLINE)")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += (
            "BỐ CỤC: 1 CỘT\n"
            "  TRÊN: Biểu đồ đường xu hướng 7 ngày\n"
            "  DƯỚI: Khung nhận định\n\n"
        )
        prompt += "DỮ LIỆU XU HƯỚNG (7 ngày):\n"
        for p in s["trendline"]:
            prompt += f"- {format_date(p['date'])}: {format_number(p['mentions'])} lượt\n"
        prompt += f"\nNHẬN ĐỊNH:\n{s['insight']}\n\n"

    # ── SLIDE 3 ───────────────────────────────────────────────────────────────
    if "slide_3" in report_data:
        s = report_data["slide_3"]
        prompt += _header("SLIDE 3 - PHÂN BỔ LƯỢT ĐỀ CẬP THEO KÊNH")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += (
            "BỐ CỤC: 2 CỘT\n"
            "  TRÁI (50%): Biểu đồ donut phân bổ kênh\n"
            "  PHẢI (50%): Biểu đồ thanh ngang top 10 nguồn\n"
            "  DƯỚI: Khung nhận định\n\n"
        )
        prompt += "PHÂN BỔ THEO KÊNH:\n"
        total_ch = sum(c["count"] for c in s["channel_distribution"])
        for c in s["channel_distribution"]:
            pct = (c["count"] / total_ch * 100) if total_ch > 0 else 0
            prompt += f"- {c['Channel']}: {format_number(c['count'])} lượt ({pct:.1f}%)\n"
        prompt += "\nTOP 10 NGUỒN:\n"
        for src in s["top_sources"]:
            prompt += f"- {src['SiteName']}: {format_number(src['count'])} lượt\n"
        prompt += f"\nNHẬN ĐỊNH:\n{s['insight']}\n\n"

    # ── SLIDE 4 ───────────────────────────────────────────────────────────────
    if "slide_4" in report_data:
        s = report_data["slide_4"]
        prompt += _header("SLIDE 4 - TOP NGUỒN CÓ LƯỢNG TƯƠNG TÁC CAO NHẤT")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += "BỐ CỤC: Bảng toàn trang, KHÔNG có nhận định\n\n"
        if s.get("show_interactions") and s["table_rows"] and "total_engagement" in s["table_rows"][0]:
            prompt += "CỘT: STT | Nguồn | Tổng tương tác | Reactions | Shares | Bình luận\n\nDỮ LIỆU BẢNG:\n"
            for r in s["table_rows"]:
                prompt += (
                    f"- [{r['stt']}] {r['source_name']} | "
                    f"{format_number(r['total_engagement'])} | "
                    f"{format_number(r['reactions'])} | "
                    f"{format_number(r['shares'])} | "
                    f"{format_number(r['comments'])}\n"
                )
        else:
            prompt += "CỘT: STT | Nguồn | Số lượng đề cập\n\nDỮ LIỆU BẢNG:\n"
            for r in s["table_rows"]:
                prompt += f"- [{r['stt']}] {r['source_name']} | {format_number(r['count'])}\n"
        prompt += "\n"

    # ── SLIDE 5 ───────────────────────────────────────────────────────────────
    if "slide_5" in report_data:
        s = report_data["slide_5"]
        prompt += _header("SLIDE 5 - TOP BÀI ĐĂNG CÓ TƯƠNG TÁC CAO NHẤT")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += "BỐ CỤC: Bảng toàn trang, KHÔNG có nhận định\n\n"
        if s.get("show_interactions") and s["table_rows"] and "comments" in s["table_rows"][0]:
            prompt += "CỘT: STT | Nội dung | Ngày đăng | Kênh | Nguồn | Reactions | Shares | Bình luận\n\nDỮ LIỆU BẢNG:\n"
            for r in s["table_rows"]:
                preview = r["content"][:100] + "..." if len(r["content"]) > 100 else r["content"]
                prompt += (
                    f"- [{r['stt']}] {preview} | "
                    f"{format_date(r['published_date'])} | "
                    f"{r['channel']} | {r['site_name']} | "
                    f"{format_number(r.get('reactions', 0))} | "
                    f"{format_number(r.get('shares', 0))} | "
                    f"{format_number(r['comments'])} | {r['url']}\n"
                )
        else:
            prompt += "CỘT: STT | Nội dung | Ngày đăng | Kênh | Nguồn | URL\n\nDỮ LIỆU BẢNG:\n"
            for r in s["table_rows"]:
                preview = r["content"][:100] + "..." if len(r["content"]) > 100 else r["content"]
                prompt += (
                    f"- [{r['stt']}] {preview} | "
                    f"{format_date(r['published_date'])} | "
                    f"{r['channel']} | {r['site_name']} | {r['url']}\n"
                )
        prompt += "\n"

    # ── SLIDE 6 ───────────────────────────────────────────────────────────────
    if "slide_6" in report_data:
        s = report_data["slide_6"]
        prompt += _header("SLIDE 6 - SẮC THÁI VÀ CỤM CHỦ ĐỀ ĐỀ CẬP NỔI BẬT")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += (
            "BỐ CỤC: 2 CỘT\n"
            "  TRÁI (50%): Hai biểu đồ donut nhỏ (Tuần trước | Tuần này) + Chỉ số NSR\n"
            "  PHẢI (50%): Biểu đồ thanh ngang xếp chồng top 10 chủ đề\n"
            "  DƯỚI: Khung nhận định\n\n"
        )
        nsr_sign = "+" if s["nsr_growth"] > 0 else ""
        prompt += (
            f"NSR Tuần trước: {s['previous_nsr']}%\n"
            f"NSR Tuần này: {s['current_nsr']}%\n"
            f"Tăng trưởng NSR: {nsr_sign}{s['nsr_growth']:.2f}%\n\n"
        )
        prompt += "SẮC THÁI Tuần trước:\n"
        total_prev = sum(x["count"] for x in s["previous_sentiment"])
        for x in s["previous_sentiment"]:
            pct = (x["count"] / total_prev * 100) if total_prev > 0 else 0
            prompt += f"- {x['sentiment']}: {format_number(x['count'])} lượt ({pct:.1f}%)\n"
        prompt += "\nSẮC THÁI Tuần này:\n"
        total_curr = sum(x["count"] for x in s["current_sentiment"])
        for x in s["current_sentiment"]:
            pct = (x["count"] / total_curr * 100) if total_curr > 0 else 0
            prompt += f"- {x['sentiment']}: {format_number(x['count'])} lượt ({pct:.1f}%)\n"
        prompt += "\nTOP CHỦ ĐỀ THEO SẮC THÁI:\n"
        for t in s["top_topics_with_sentiment"]:
            prompt += (
                f"- {t['topic']}: Tổng {format_number(t['total'])} "
                f"(Tiêu cực: {t['negative']}, Trung tính: {t['neutral']}, Tích cực: {t['positive']})\n"
            )
        prompt += f"\nNHẬN ĐỊNH:\n{s['insight']}\n\n"

    # ── SLIDE 7 ───────────────────────────────────────────────────────────────
    if "slide_7" in report_data:
        s = report_data["slide_7"]
        prompt += _header("SLIDE 7 - CÁC CHỦ ĐỀ ĐỀ CẬP TÍCH CỰC")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += (
            "BỐ CỤC: 1 CỘT\n"
            "  TRÊN: Biểu đồ thanh ngang top 10 chủ đề tích cực (màu: #00C055)\n"
            "  DƯỚI: Khung nhận định\n\n"
        )
        prompt += "CHỦ ĐỀ TÍCH CỰC:\n"
        for t in s["positive_topics"]:
            prompt += f"- {t['Labels1']}: {format_number(t['count'])} lượt\n"
        prompt += f"\nNHẬN ĐỊNH:\n{s['insight']}\n\n"

    # ── SLIDE 8 ───────────────────────────────────────────────────────────────
    if "slide_8" in report_data:
        s = report_data["slide_8"]
        prompt += _header("SLIDE 8 - TOP BÀI ĐĂNG TÍCH CỰC")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += (
            "BỐ CỤC: Bảng toàn trang, KHÔNG có nhận định\n"
            "CỘT: STT | Nội dung | Ngày đăng | Kênh | Nguồn | Bình luận tích cực\n\n"
            "DỮ LIỆU BẢNG:\n"
        )
        for r in s["table_rows"]:
            preview = r["content"][:100] + "..." if len(r["content"]) > 100 else r["content"]
            prompt += (
                f"- [{r['stt']}] {preview} | "
                f"{format_date(r['published_date'])} | "
                f"{r['channel']} | {r['site_name']} | "
                f"{format_number(r['positive_comments'])} | {r['url']}\n"
            )
        prompt += "\n"

    # ── SLIDE 9 ───────────────────────────────────────────────────────────────
    if "slide_9" in report_data:
        s = report_data["slide_9"]
        prompt += _header("SLIDE 9 - CÁC CHỦ ĐỀ ĐỀ CẬP TIÊU CỰC")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += (
            "BỐ CỤC: 1 CỘT\n"
            "  TRÊN: Biểu đồ thanh ngang top 10 chủ đề tiêu cực (màu: #EC003F)\n"
            "  DƯỚI: Khung nhận định\n\n"
        )
        prompt += "CHỦ ĐỀ TIÊU CỰC:\n"
        for t in s["negative_topics"]:
            prompt += f"- {t['Labels1']}: {format_number(t['count'])} lượt\n"
        prompt += f"\nNHẬN ĐỊNH:\n{s['insight']}\n\n"

    # ── SLIDE 10 ──────────────────────────────────────────────────────────────
    if "slide_10" in report_data:
        s = report_data["slide_10"]
        prompt += _header("SLIDE 10 - TOP BÀI ĐĂNG TIÊU CỰC")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += (
            "BỐ CỤC: Bảng toàn trang, KHÔNG có nhận định\n"
            "CỘT: STT | Nội dung | Ngày đăng | Kênh | Nguồn | Bình luận tiêu cực\n\n"
            "DỮ LIỆU BẢNG:\n"
        )
        for r in s["table_rows"]:
            preview = r["content"][:100] + "..." if len(r["content"]) > 100 else r["content"]
            prompt += (
                f"- [{r['stt']}] {preview} | "
                f"{format_date(r['published_date'])} | "
                f"{r['channel']} | {r['site_name']} | "
                f"{format_number(r['negative_comments'])} | {r['url']}\n"
            )
        prompt += "\n"

    # ── SLIDE 11 ──────────────────────────────────────────────────────────────
    if "slide_11" in report_data:
        s = report_data["slide_11"]
        prompt += _header("SLIDE 11 - TỔNG QUAN ĐỀ CẬP VỀ THƯƠNG HIỆU VỚI CÁC ĐỐI THỦ")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += (
            "BỐ CỤC: 2 HÀNG\n"
            "  HÀNG 1: Khung nhận định\n"
            "  HÀNG 2 TRÁI (50%): Hai biểu đồ donut (Tuần trước | Tuần hiện tại)\n"
            "  HÀNG 2 PHẢI (50%): Biểu đồ cột đôi đứng\n\n"
        )
        prompt += f"NHẬN ĐỊNH:\n{s['insight']}\n\n"

        prompt += "─── BIỂU ĐỒ DONUT ───────────────────────────────────────────\n"
        prompt += "QUY TẮC: Tổng ở giữa, tỷ lệ % trên vòng ngoài, chú giải bên dưới\n\n"
        prev_data  = [i for i in s["donut_charts"]["week_before"]["data"]  if i["mentions"] > 0]
        curr_data  = [i for i in s["donut_charts"]["current_week"]["data"] if i["mentions"] > 0]
        total_prev = sum(i["mentions"] for i in prev_data)
        total_curr = sum(i["mentions"] for i in curr_data)

        prompt += f"DONUT TUẦN TRƯỚC — tổng: {format_number(total_prev)} lượt\n"
        for item in sorted(prev_data, key=lambda x: x["mentions"], reverse=True):
            pct = (item["mentions"] / total_prev * 100) if total_prev > 0 else 0
            prompt += f"  {item['brand']}: {format_number(item['mentions'])} lượt ({pct:.1f}%) | màu {item['color']}\n"

        prompt += f"\nDONUT TUẦN HIỆN TẠI — tổng: {format_number(total_curr)} lượt\n"
        for item in sorted(curr_data, key=lambda x: x["mentions"], reverse=True):
            pct = (item["mentions"] / total_curr * 100) if total_curr > 0 else 0
            prompt += f"  {item['brand']}: {format_number(item['mentions'])} lượt ({pct:.1f}%) | màu {item['color']}\n"

        prompt += "\nCHÚ GIẢI:\n"
        for item in s["legend"]:
            prompt += f"  ■ {item['brand']}: {item['color']}\n"

        prompt += "\n─── BIỂU ĐỒ CỘT ĐÔI ĐỨNG ──────────────────────────────────\n"
        prompt += f"Tiêu đề: {s['bar_chart']['title']}\n"
        prompt += "QUY TẮC: Cột TRÁI = Tuần trước, Cột PHẢI = Tuần này, sắp xếp giảm dần theo tuần hiện tại\n\n"
        prompt += "DỮ LIỆU:\n"
        for item in sorted(s["bar_chart"]["data"], key=lambda x: x["current_week"], reverse=True):
            sign  = "+" if item["percentage_change"] >= 0 else ""
            arrow = "↑" if item["percentage_change"] > 0 else ("↓" if item["percentage_change"] < 0 else "→")
            mau   = "xanh lá" if item["change_color"] == "green" else ("đỏ" if item["change_color"] == "red" else "xám")
            prompt += (
                f"  {item['brand']}: Tuần trước={format_number(item['week_before'])} | "
                f"Tuần này={format_number(item['current_week'])} | "
                f"{arrow} {sign}{item['percentage_change']}% ({mau})\n"
            )
        prompt += "\n"

    # ── SLIDE 12 ──────────────────────────────────────────────────────────────
    if "slide_12" in report_data:
        s = report_data["slide_12"]
        prompt += _header("SLIDE 12 - ĐƯỜNG BIỂU DIỄN XU HƯỚNG ĐỀ CẬP NHIỀU THƯƠNG HIỆU")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += (
            "BỐ CỤC: 1 CỘT TOÀN TRANG\n"
            "  TRÊN: Biểu đồ đường theo ngày, mỗi thương hiệu một đường màu riêng\n"
            "  DƯỚI: Chú giải màu sắc\n\n"
        )
        prompt += "DỮ LIỆU ĐƯỜNG XU HƯỚNG:\n"
        for b in s["brands"]:
            tl    = s["trendlines"].get(b, [])
            total = sum(p["mentions"] for p in tl)
            dates_str = " | ".join(
                f"{format_date(p['date'])}: {p['mentions']}"
                for p in tl if p["mentions"] > 0
            )
            prompt += f"  [{b}] Tổng: {format_number(total)} lượt\n"
            if dates_str:
                prompt += f"    {dates_str}\n"
        prompt += "\nĐIỂM ĐỈNH (PEAK) THEO THƯƠNG HIỆU:\n"
        for b, ann in s["annotations"].items():
            prompt += (
                f"  [{b}] Ngày {format_date(ann['date'])} — {format_number(ann['mentions'])} lượt\n"
                f"    Trích dẫn: \"{ann['snippet']}\"\n"
                f"    Đường dẫn: {ann['url']}\n"
            )
        prompt += "\n"

    # ── SLIDE 13 ──────────────────────────────────────────────────────────────
    if "slide_13" in report_data:
        s = report_data["slide_13"]
        prompt += _header("SLIDE 13 - PHÂN BỐ ĐỀ CẬP TRÊN CÁC KÊNH TRUYỀN THÔNG")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += (
            "BỐ CỤC: 2 HÀNG\n"
            "  HÀNG 1: 3 khung nhận định theo kênh (Facebook | Báo chí | Fanpage)\n"
            "  HÀNG 2: Biểu đồ cột xếp chồng phân bổ kênh theo từng thương hiệu/chủ đề\n\n"
        )

        for sec in s.get("insight_sections", []):
            prompt += f"--- NHẬN ĐỊNH KÊNH: {sec['group']} ---\n"
            for topic in sec.get("topics", []):
                prompt += f"  Chủ đề nổi bật: {topic['label']} ({format_number(topic['count'])} lượt)\n"
            prompt += f"  Tóm tắt: {sec.get('summary', '')}\n\n"

        chart = s.get("stacked_bar_chart", {})
        prompt += f"BIỂU ĐỒ CỘT XẾP CHỒNG: {chart.get('title', '')}\n"
        prompt += (
            "QUY TẮC: Mỗi cột = 1 thương hiệu/chủ đề, phân tầng theo nhóm kênh,\n"
            "  đỉnh cột = tổng lượt đề cập, đáy cột = tên chủ đề,\n"
            "  hiển thị nhãn % trên cột nếu >= 20%, chú giải cố định bên phải\n\n"
        )
        prompt += "DỮ LIỆU:\n"
        for row in chart.get("data", []):
            prompt += f"  [{row['topic']}] Tổng: {format_number(row['total'])} lượt\n"
            for seg in row.get("segments", []):
                if seg["percent"] > 0:
                    hien_thi = " (hiển thị nhãn)" if seg["show_label"] else " (ẩn nhãn)"
                    prompt += f"    - {seg['group']}: {format_number(seg['count'])} lượt ({seg['percent']}%){hien_thi}\n"

        prompt += "\nCHÚ GIẢI KÊNH (cố định):\n"
        for leg in s.get("channel_legend", []):
            prompt += f"  ■ {leg['group']}: {leg['color']}\n"
        prompt += "\n"

    # ── SLIDE 15 ──────────────────────────────────────────────────────────────
    if "slide_15" in report_data:
        s = report_data["slide_15"]
        prompt += _header("SLIDE 15 - SẮC THÁI ĐỀ CẬP THEO CHỦ ĐỀ (TOPIC)")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += (
            "BỐ CỤC: 3 HÀNG\n"
            "  HÀNG 1: Khung nhận định\n"
            "  HÀNG 2: Biểu đồ cột xếp chồng tỷ trọng sentiment theo Topic\n"
            "  HÀNG 3: Bảng tổng hợp (N, NSR%, Top Positive/Negative labels)\n\n"
        )
        prompt += f"NHẬN ĐỊNH:\n{s['insight']}\n\n"

        chart = s.get("stacked_bar_chart", {})
        prompt += f"BIỂU ĐỒ CỘT XẾP CHỒNG: {chart.get('title', '')}\n"
        prompt += "DỮ LIỆU BIỂU ĐỒ:\n"
        for row in chart.get("data", []):
            prompt += f"  [{row['topic']}] Tổng: {format_number(row['total'])} lượt\n"
            for seg in row.get("segments", []):
                if seg["percent"] > 0:
                    prompt += f"    - {seg['sentiment']}: {seg['percent']}% ({format_number(seg['count'])} lượt)\n"

        prompt += "\nBẢNG TỔNG HỢP THEO TOPIC:\n"
        tbl = s.get("summary_table", {})
        for topic in tbl.get("topics", []):
            nsr = tbl["NSR"].get(topic, 0)
            n   = tbl["N"].get(topic, 0)
            pos = " | ".join(tbl["top_positive"].get(topic, []))
            neg = " | ".join(tbl["top_negative"].get(topic, []))
            prompt += (
                f"  - {topic}: N={format_number(n)} | NSR={nsr:+.1f}% | "
                f"Tích cực: {pos} | Tiêu cực: {neg}\n"
            )
        prompt += "\n"

    # ── SLIDE 16 ──────────────────────────────────────────────────────────────
    if "slide_16" in report_data:
        s = report_data["slide_16"]
        prompt += _header("SLIDE 16 - TOP BÀI ĐĂNG CÓ LƯỢT BÌNH LUẬN CAO NHẤT")
        prompt += f"Tiêu đề: \"{s['title']}\"\nPhụ đề: \"{s['subtitle']}\"\n\n"
        prompt += (
            "BỐ CỤC: Bảng toàn trang, KHÔNG có nhận định\n"
            "CỘT CỐ ĐỊNH: STT | Thương hiệu | Bài đăng | Kênh | Nguồn | Bình luận\n\n"
            "DỮ LIỆU BẢNG:\n"
        )
        for r in s.get("table", []):
            content = r["content"][:150] + "..." if len(r["content"]) > 150 else r["content"]
            prompt += (
                f"- [{r['stt']}] {r['topic']} | {content} | "
                f"{r['channel']} | {r['source_name']} | "
                f"{format_number(r['comment_count'])} lượt | {r['source_url']}\n"
            )
        prompt += "\n"

    # ── THIẾT KẾ TỔNG THỂ ────────────────────────────────────────────────────
    prompt += "===============================================================\n"
    prompt += "THIẾT KẾ TỔNG THỂ\n"
    prompt += "===============================================================\n\n"
    prompt += (
        "BẢNG MÀU: Xanh chính #0045C4 | Tích cực #00C055 | Tiêu cực #EC003F | "
        "Trung tính #6b7280 | Nền #FFFFFF\n"
        "KIỂU CHỮ: Tiêu đề 32px Đậm | Mục 24px Đậm | Nội dung 14px Thường | Font: Inter/Roboto\n"
        "ĐỊNH DẠNG SỐ: dấu phẩy hàng nghìn (ví dụ: 1,234)\n\n"
    )
    prompt += "===============================================================\n"
    prompt += "HƯỚNG DẪN BẮT BUỘC:\n"
    prompt += (
        "1. Tạo đúng các slide có dữ liệu ở trên, tuân thủ bố cục từng slide\n"
        "2. Đảm bảo biểu đồ được định dạng và gán nhãn đúng\n"
        "3. Sử dụng bảng màu nhất quán, giữ nguyên đường dẫn (hyperlink)\n"
        "4. Slide 11 donut: tổng ở giữa, tỷ lệ % trên vòng ngoài, chú giải bên dưới\n"
        "5. Slide 11 cột đôi: sắp xếp giảm dần, số lượng + mũi tên biến động trên mỗi cặp cột\n"
        "6. Slide 12: đánh dấu điểm đỉnh (peak) mỗi thương hiệu, trích dẫn là hyperlink dẫn đến URL\n"
        "7. Slide 13: cột xếp chồng — đỉnh cột ghi tổng lượt, ẩn nhãn % nếu < 20%, chú giải kênh cố định bên phải\n"
        "8. Slide 14: bảng 4 cột cố định, sắp xếp giảm dần theo tổng lượt thảo luận\n"
        "9. Slide 15: biểu đồ cột xếp chồng sentiment, bảng tổng hợp hiển thị NSR% và các chủ đề tiêu biểu\n"
        "10. Slide 16: bảng top bài đăng có lượt bình luận cao nhất, hiển thị nội dung và link nguồn\n"
    )
    prompt += "===============================================================\n"

    return prompt
