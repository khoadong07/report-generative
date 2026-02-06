# Troubleshooting: Chart Showing Top 6 Instead of Top 8

## Problem
Chart is showing 6 channels instead of 8, even though code says `.head(8)`.

## Possible Causes

### 1. Cache Issue (Most Likely)
Streamlit is using cached old code that had different limit.

**Solution**:
```bash
# Force clear all cache
bash force_clear_cache.sh

# Or manually:
pkill -f streamlit
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
rm -rf ~/.streamlit/cache 2>/dev/null

# Restart
streamlit run app.py
```

### 2. Dataset Only Has 6 Channels
Your data might only have 6 unique channels after normalization.

**Check Debug Output**:
```
[Slide 4] 💭 Analyzing sentiment distribution...
         → Normalized channels: ['Facebook Users', 'Facebook Pages', 'Tiktok', 'Youtube', 'News', 'Forum']
         → Total channels available: 6
         → All channels: ['Facebook Users', 'Facebook Pages', 'Tiktok', 'Youtube', 'News', 'Forum']
         → Filtered to top 8 channels: ['Facebook Users', 'Facebook Pages', 'Tiktok', 'Youtube', 'News', 'Forum']
         → Number of channels in output: 6
```

If "Total channels available" is 6, then your dataset only has 6 channels.

### 3. Old Code Still Running
Multiple Python processes might be running with old code.

**Solution**:
```bash
# Check running processes
ps aux | grep streamlit
ps aux | grep python

# Kill all
pkill -9 -f streamlit
pkill -9 -f python

# Restart fresh
streamlit run app.py
```

---

## Verification Steps

### Step 1: Check Code
```bash
# Verify code has .head(8)
grep -n "head(8)" test/streamlit/slide_generators.py

# Should show:
# 505:        top_8_channels = channel_sentiment_pivot.head(8).copy()
```

### Step 2: Check Debug Output
When generating report, look for:
```
→ Total channels available: X
→ Filtered to top 8 channels: [...]
→ Number of channels in output: Y
```

- If X < 8: Dataset only has X channels (normal)
- If X >= 8 but Y = 6: Cache issue (clear cache)

### Step 3: Check Generated JSON
```python
# In Python console or Jupyter
import json

with open('report_data.json', 'r') as f:
    data = json.load(f)

channels = data['slide_4']['channel_sentiment']
print(f"Number of channels: {len(channels)}")
print("Channels:", [c['Channel'] for c in channels])
```

Expected: 8 channels (or less if dataset has fewer)

---

## Expected Debug Output

### If Dataset Has 8+ Channels
```
[Slide 4] 💭 Analyzing sentiment distribution...
         → Normalized channels: ['Facebook Users', 'Facebook Pages', 'Facebook Groups', 'Tiktok', 'Youtube', 'News', 'Forum', 'Blog', 'Instagram', 'Twitter']
         → Total channels available: 10
         → All channels: ['Facebook Users', 'Facebook Pages', 'Facebook Groups', 'Tiktok', 'Youtube', 'News', 'Forum', 'Blog', 'Instagram', 'Twitter']
         → Filtered to top 8 channels: ['Facebook Users', 'Facebook Pages', 'Facebook Groups', 'Tiktok', 'Youtube', 'News', 'Forum', 'Blog']
         → Number of channels in output: 8
```

### If Dataset Has 6 Channels
```
[Slide 4] 💭 Analyzing sentiment distribution...
         → Normalized channels: ['Facebook Users', 'Facebook Pages', 'Tiktok', 'Youtube', 'News', 'Forum']
         → Total channels available: 6
         → All channels: ['Facebook Users', 'Facebook Pages', 'Tiktok', 'Youtube', 'News', 'Forum']
         → Filtered to top 8 channels: ['Facebook Users', 'Facebook Pages', 'Tiktok', 'Youtube', 'News', 'Forum']
         → Number of channels in output: 6
```

This is NORMAL - can't show 8 if only 6 exist!

---

## Quick Fix Commands

```bash
# 1. Force clear everything
cd test/streamlit
bash force_clear_cache.sh

# 2. Verify code
grep "head(8)" slide_generators.py

# 3. Restart Streamlit
streamlit run app.py

# 4. Generate report and check debug output
# Look for: "Number of channels in output: X"
```

---

## If Still Showing 6

### Check 1: Is Code Actually Updated?
```bash
# Show the exact line
sed -n '505p' test/streamlit/slide_generators.py

# Should show:
# top_8_channels = channel_sentiment_pivot.head(8).copy()
```

### Check 2: Is Streamlit Using Right File?
```python
# In Streamlit app, add this at top:
import slide_generators
import inspect
print(inspect.getfile(slide_generators.Slide4Generator))

# Should show: test/streamlit/slide_generators.py
```

### Check 3: Multiple Streamlit Instances?
```bash
# Check how many Streamlit processes
ps aux | grep streamlit | grep -v grep | wc -l

# Should be 1 (or 0 if not running)
# If more than 1, kill all and restart
```

---

## Summary

**Most likely cause**: Cache issue

**Solution**: 
1. Clear all cache
2. Kill all Python/Streamlit processes
3. Restart Streamlit
4. Check debug output

**If dataset only has 6 channels**: This is normal! Code will show up to 8, but if only 6 exist, it shows 6.
