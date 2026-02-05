# 🎨 Landing Page Template

## ✨ Tính năng mới

### 1. **Landing Page Layout**
- ✅ Dạng trang cuộn (scrollable) thay vì slides
- ✅ Responsive design (mobile-friendly)
- ✅ Smooth scroll navigation
- ✅ Scroll animations (fade-in effects)

### 2. **Design Improvements**
- ✅ Gradient background đẹp mắt
- ✅ Sticky header với navigation
- ✅ Hero section với metadata
- ✅ Card-based layout cho từng section
- ✅ Modern color scheme (purple gradient)
- ✅ Hover effects và transitions

### 3. **Layout Structure**

```
┌─────────────────────────────────────┐
│         Sticky Header               │
│  Logo | Nav Links (Overview, etc.)  │
├─────────────────────────────────────┤
│         Hero Section                │
│  Title + Subtitle + Meta Info       │
├─────────────────────────────────────┤
│                                     │
│  Section 1: Overview                │
│  ├─ KPI Grid (3 columns)           │
│  └─ Insight Box                     │
│                                     │
├─────────────────────────────────────┤
│                                     │
│  Section 2: Trendline               │
│  ├─ Line Chart                      │
│  └─ Insight Box                     │
│                                     │
├─────────────────────────────────────┤
│                                     │
│  Section 3: Channel Breakdown       │
│  ├─ Bar Chart (left)                │
│  └─ Insight Box (right)             │
│                                     │
├─────────────────────────────────────┤
│                                     │
│  Section 4: Sentiment Analysis      │
│  ├─ Pie Chart + Bar Chart (left)    │
│  └─ Insight Box (right)             │
│                                     │
├─────────────────────────────────────┤
│         Footer                      │
└─────────────────────────────────────┘
```

### 4. **Color Scheme**

- **Primary Gradient**: Purple (#667eea → #764ba2)
- **Background**: White sections on gradient background
- **Text**: Dark gray (#1a202c, #2d3748)
- **Accent**: Purple for highlights
- **Positive**: Green (#48bb78)
- **Negative**: Red (#f56565)
- **Neutral**: Gray (#9ca3af)

### 5. **Components**

#### Header
- Sticky navigation
- Logo on left
- Nav links on right
- Smooth scroll to sections

#### Hero Section
- Large title
- Subtitle
- Meta information (date, number of analyses)
- Gradient background

#### KPI Cards
- Grid layout (auto-fit, min 280px)
- Hover effects (lift + shadow)
- Color-coded changes (green/red)
- Left border accent

#### Insight Boxes
- Gradient background (purple)
- White text
- Icon + title
- Linked content with gold links

#### Charts
- Light gray background
- Rounded corners
- Proper spacing
- Responsive height

### 6. **Responsive Design**

**Desktop (> 768px)**:
- Full navigation
- Multi-column layouts
- Large charts

**Mobile (< 768px)**:
- Single column layout
- Hidden navigation
- Stacked sections
- Smaller text sizes

### 7. **Animations**

- **Scroll Animations**: Fade-in on scroll
- **Hover Effects**: Cards lift and show shadow
- **Smooth Scroll**: Navigation links
- **Transitions**: All interactive elements

## 🚀 Usage

### Generate and Render

```bash
cd test

# 1. Generate report
python generate_report.py

# 2. Render HTML (uses template_landing.html)
python render_html.py

# 3. Open in browser
open final_report.html
```

### Template Files

- **`template_landing.html`** - New landing page template ⭐
- **`template_parameterized.html`** - Old slides template
- **`template.html`** - Original template

## 🎨 Customization

### Change Colors

Edit CSS variables in `<style>` section:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to blue gradient */
background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);

/* Change to orange gradient */
background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
```

### Change Layout

Modify grid columns:

```css
/* KPI Grid - 3 columns */
.kpi-grid {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

/* Change to 4 columns */
.kpi-grid {
    grid-template-columns: repeat(4, 1fr);
}
```

### Add/Remove Sections

Simply add/remove section blocks:

```html
<div class="section fade-in" id="new-section">
    <div class="section-title">
        <div class="section-icon"><i class="fas fa-icon"></i></div>
        Section Title
    </div>
    <!-- Content here -->
</div>
```

## 📊 Features

### Navigation
- Click nav links to scroll to sections
- Smooth scroll animation
- Active section highlighting (can be added)

### Charts
- Interactive tooltips
- Responsive sizing
- Modern styling
- Gradient colors

### Performance
- Lazy loading animations
- Optimized CSS
- CDN resources
- Minimal JavaScript

## 🎯 Advantages

### vs Slides Template

| Feature | Slides | Landing Page |
|---------|--------|--------------|
| Layout | Fixed slides | Scrollable |
| Navigation | Buttons | Smooth scroll |
| Mobile | Limited | Fully responsive |
| Animations | Basic | Advanced |
| Readability | Good | Excellent |
| Print-friendly | No | Yes |
| SEO-friendly | No | Yes |

### Benefits

1. **Better UX**: Natural scrolling behavior
2. **More Content**: Can show all data at once
3. **Responsive**: Works on all devices
4. **Modern**: Contemporary design trends
5. **Accessible**: Better for screen readers
6. **Shareable**: Single URL, no navigation needed

## 🔧 Technical Details

### Dependencies
- Tailwind CSS (CDN)
- Font Awesome (CDN)
- Chart.js (CDN)
- Google Fonts - Inter (CDN)

### Browser Support
- Chrome/Edge: ✅
- Firefox: ✅
- Safari: ✅
- Mobile browsers: ✅

### File Size
- HTML: ~15KB
- With data: ~20-30KB
- Fast loading

## 💡 Tips

1. **Print**: Use browser print (Ctrl+P) for PDF export
2. **Share**: Single HTML file, easy to share
3. **Embed**: Can be embedded in iframe
4. **Customize**: Easy to modify colors and layout
5. **Extend**: Add more sections as needed

---

**Template file**: `test/template_landing.html`
**Render script**: `test/render_html.py`
