# Hướng dẫn Restart Streamlit để áp dụng code mới

## Vấn đề
Code đã được fix nhưng Streamlit vẫn chạy code cũ do caching.

## Giải pháp

### Cách 1: Restart Streamlit (Khuyến nghị)
```bash
# 1. Dừng Streamlit (Ctrl+C trong terminal)
# 2. Clear Python cache
cd test/streamlit
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
rm -rf __pycache__

# 3. Restart Streamlit
streamlit run app.py
```

### Cách 2: Clear Cache trong Browser
1. Trong Streamlit app, nhấn phím `C` để mở menu
2. Chọn "Clear cache"
3. Hoặc click nút "🔄 Clear Cache & Refresh" trong sidebar

### Cách 3: Force Reload Module
Thêm code này vào đầu `app.py`:
```python
import sys
import importlib

# Force reload modules
if 'slide_generators' in sys.modules:
    importlib.reload(sys.modules['slide_generators'])
```

### Cách 4: Restart Python Process
```bash
# Kill tất cả Python processes
pkill -f streamlit

# Hoặc tìm và kill process cụ thể
ps aux | grep streamlit
kill -9 <PID>

# Restart
cd test/streamlit
streamlit run app.py
```

## Xác nhận Fix đã được áp dụng

Sau khi restart, kiểm tra log khi generate report:

### Trước khi fix (Lỗi):
```
[Slide 2] 💭 Analyzing 7-day trendline...
❌ Error generating slide_2: attempt to get argmax of an empty sequence
```

### Sau khi fix (Đúng):
```
[Slide 2] 💭 Analyzing 7-day trendline...
⚠️  Warning: No data in 7-day window, returning empty trendline
[Slide 2] ✅ Completed
```

## Kiểm tra Code đã được load

Thêm print statement để verify:
```python
# Trong slide_generators.py, dòng đầu tiên của Slide2Generator.generate()
print("🔍 DEBUG: Slide2Generator version with empty check")
```

Nếu thấy message này trong log, code mới đã được load.

## Nếu vẫn lỗi

### Kiểm tra file đúng đang được sử dụng:
```bash
# Xem file nào đang được import
python -c "
import sys
sys.path.insert(0, 'test/streamlit')
from slide_generators import Slide2Generator
import inspect
print(inspect.getfile(Slide2Generator))
"
```

### Kiểm tra có nhiều version của file:
```bash
find . -name "slide_generators.py" -type f
```

Nếu có nhiều file, đảm bảo đang edit đúng file trong `test/streamlit/`.
