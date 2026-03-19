# Weekly Report - Tóm tắt thay đổi

## Slide 8 — Top bài đăng tích cực (table)
- **Trước:** `slide8_gen` dùng `WeeklySlide9Generator` nhưng bị gán nhầm, trả về `topic/count` không khớp với UI
- **Sau:** `slide8_gen` → `WeeklySlide9Generator(TOPIC_TYPES, COMMENT_TYPES)`, trả về `table_rows` với đầy đủ `content`, `published_date`, `channel`, `site_name`, `positive_comments`, `url`

## Slide 9 — Chủ đề tiêu cực (chart + insight)
- **Trước:** `slide9_gen` dùng `WeeklySlide10Generator` (trả về `negative_topics` + `insight`), nhưng `generate_complete_prompt` lại đọc `table_rows` → `KeyError: 'table_rows'`
- **Sau:** Giữ `slide9_gen` → `WeeklySlide10Generator` (đúng với `app_weekly.py`), sửa `generate_complete_prompt` để đọc `negative_topics` + `insight` thay vì `table_rows`
- Slide 9 trong prompt được đổi từ "TOP BAI DANG TICH CUC" (duplicate slide 8) thành "CAC CHU DE DE CAP TIEU CUC" với layout bar chart đúng

## Slide 10 — Top bài đăng tiêu cực (table)
- Không thay đổi logic, `slide10_gen` → `WeeklyNegativePostsGenerator` trả về `table_rows` với `negative_comments`

## Slide 12 — So sánh brand
- **Trước:** Nhận `week1_df` / `week2_df` đã bị filter theo brand → chỉ thấy data của 1 brand, không so sánh được
- **Sau:** Lưu `df_all = df.copy()` trước bước filter brand, tạo `week1_all_df` / `week2_all_df` filter chỉ theo thời gian, truyền vào `generate_slide12` → slide 12 thấy toàn bộ các brand trong cùng khoảng thời gian
