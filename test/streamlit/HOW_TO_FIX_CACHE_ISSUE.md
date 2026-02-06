# How to Fix: Streamlit Cache Issue

## Problem
You're still seeing the error:
```
time data '03/02/2026 15:00' does not match format '%Y-%m-%d'
```

Even though the code has been fixed, **Streamlit is using cached old code**.

---

## Solution: Force Clear All Cache

### Step 1: Stop Streamlit
In the terminal running Streamlit, press:
```
Ctrl + C
```

### Step 2: Clear Python Cache
```bash
cd test/streamlit

# Clear all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Clear all .pyc files
find . -type f -name "*.pyc" -delete 2>/dev/null

# Clear Streamlit cache
rm -rf ~/.streamlit/cache 2>/dev/null
```

Or use the script:
```bash
bash clear_cache.sh
```

### Step 3: Verify Files Are Updated
Check that the fixes are in place:

```bash
# Check parse_date_flexible exists
grep -n "parse_date_flexible" slide_generators.py

# Should show the function definition around line 25-60
```

### Step 4: Restart Streamlit
```bash
streamlit run app.py
```

### Step 5: Verify New Code Is Loaded
When you generate a report, you should see these debug messages:

```
[Slide 2] 📈 Calculating trendline data...
🔍 DEBUG: Slide2Generator with empty dataframe fix loaded
🔍 DEBUG: parse_date_flexible() called with: '2026-02-03 15:00:00'
✅ Parsed with format: %Y-%m-%d %H:%M:%S
[Slide 2] 🤖 Calling LLM for insights...
```

If you see these messages, the new code is loaded! ✅

---

## Alternative: Force Module Reload

If cache clearing doesn't work, the app now has auto-reload built in.

Check the top of `app.py`:
```python
# Force reload modules to pick up latest changes
import sys
import importlib

modules_to_reload = [
    'slide_generators',
    'report_generator', 
    'generate_slide_prompt',
    'data_loader',
    'prompts'
]

for module_name in modules_to_reload:
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
```

This will reload modules every time the app runs.

---

## Verification Checklist

- [ ] Stopped Streamlit (Ctrl+C)
- [ ] Cleared __pycache__ directories
- [ ] Cleared .pyc files
- [ ] Cleared Streamlit cache
- [ ] Restarted Streamlit
- [ ] Saw debug messages in console
- [ ] No more date format errors

---

## If Still Not Working

### Check 1: Are you editing the right file?
```bash
# Find all slide_generators.py files
find . -name "slide_generators.py" -type f

# Should only show:
# ./test/streamlit/slide_generators.py
```

If you see multiple files, make sure you're editing the one in `test/streamlit/`.

### Check 2: Is Python using the right file?
```bash
python -c "
import sys
sys.path.insert(0, 'test/streamlit')
from slide_generators import parse_date_flexible
import inspect
print(inspect.getfile(parse_date_flexible))
"
```

Should show: `test/streamlit/slide_generators.py`

### Check 3: Test the function directly
```bash
cd test/streamlit
python -c "
from slide_generators import parse_date_flexible
result = parse_date_flexible('03/02/2026 15:00')
print(f'✅ Success: {result}')
"
```

Should print: `✅ Success: 2026-02-03 15:00:00`

---

## Nuclear Option: Restart Everything

If nothing works:

```bash
# 1. Kill all Python processes
pkill -f python
pkill -f streamlit

# 2. Clear all cache
cd test/streamlit
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
rm -rf ~/.streamlit/cache 2>/dev/null

# 3. Restart terminal (close and open new terminal)

# 4. Navigate back
cd test/streamlit

# 5. Start fresh
streamlit run app.py
```

---

## Expected Behavior After Fix

### Before Fix (Error):
```
[Slide 2] 📈 Calculating trendline data...
❌ Error generating slide_2: time data '03/02/2026 15:00' does not match format '%Y-%m-%d'
```

### After Fix (Success):
```
[Slide 2] 📈 Calculating trendline data...
🔍 DEBUG: Slide2Generator with empty dataframe fix loaded
🔍 DEBUG: parse_date_flexible() called with: '2026-02-03 15:00:00'
✅ Parsed with format: %Y-%m-%d %H:%M:%S
[Slide 2] 🤖 Calling LLM for insights...
[Slide 2] ✅ Completed
```

---

## Summary

The code has been fixed with:
1. ✅ `parse_date_flexible()` function added
2. ✅ `format_date()` updated
3. ✅ Module auto-reload added to app.py
4. ✅ Debug messages added

**The issue is cache, not code!**

Follow the steps above to clear cache and restart Streamlit.
