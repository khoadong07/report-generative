# Slide Prompt Generator

Web interface and API for generating slide prompts for Manuss, Gamma, and Beautiful.ai

**Supports 2 report types:**
- **Daily Report** (6 slides) - Daily report with 24-hour window
- **Weekly Report** (16 slides) - Weekly report with 7-day window

## 🚀 Quick Start with Docker

### 1. Configure API Credentials

Create a `.env` file in the project root:

```bash
API_KEY=your_api_key_here
BASE_URL=your_base_url_here
```

### 2. Run Daily Services (Streamlit + API)

```bash
# Create required directories
mkdir -p uploads logs

# Run both Streamlit and API
docker-compose -f deployment/docker-compose.yml up --build

# Or run in background
docker-compose -f deployment/docker-compose.yml up -d --build
```

**Services will be available at:**
- 📊 **Streamlit App**: http://localhost:8522
- 🚀 **FastAPI Server**: http://localhost:8524  
- 📚 **API Documentation**: http://localhost:8524/docs

### 3. Run Weekly Service

```bash
# Run weekly service
docker-compose -f deployment/docker-compose.weekly.yml up --build
```

### 4. Stop Services

```bash
# Stop all services
docker-compose -f deployment/docker-compose.yml down

# Stop and remove volumes
docker-compose down -v

# Stop and remove images
docker-compose down --rmi all
```

### 5. View Logs

```bash
# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f streamlit-app
docker-compose logs -f api-server
```

## 📁 Project Structure

```
├── README.md                           # Documentation
├── .env.example                        # Environment variables template
├── requirements.txt                    # Python dependencies
├── requirements_api.txt                # API dependencies
├── Makefile                           # Build commands
│
├── core/                              # Core modules
│   ├── config.py                      # Configuration constants
│   ├── data_loader.py                 # Excel data loader
│   └── llm_client.py                  # OpenAI client wrapper
│
├── generators/                        # Report generators
│   ├── daily/                         # Daily report (6 slides)
│   │   ├── generate_slide_prompt.py
│   │   ├── report_generator.py
│   │   ├── slide_generators.py
│   │   └── prompts.py
│   └── weekly/                        # Weekly report (16 slides)
│       ├── generate_slide_prompt_weekly.py
│       ├── report_generator_weekly.py
│       ├── slide_generators_weekly.py
│       └── prompts_weekly.py
│
├── weekly_report/                     # New weekly architecture
│   ├── orchestrator.py                # Parallel slide generation
│   ├── prompt_builder.py              # Prompt construction
│   ├── prompts.py                     # LLM prompts
│   ├── app.py                         # Streamlit interface
│   └── slides/                        # 16 slide generators
│       ├── base.py
│       ├── slide01_overview.py
│       ├── slide02_trendline.py
│       ├── ...
│       └── slide16_top_commented_posts.py
│
├── interfaces/                        # User interfaces
│   ├── app.py                         # Daily Streamlit app
│   ├── app_weekly.py                  # Weekly Streamlit app
│   └── api_server.py                  # FastAPI server
│
├── deployment/                        # Docker deployment
│   ├── docker/
│   │   ├── Dockerfile                 # Daily Streamlit
│   │   ├── Dockerfile.api             # API server
│   │   └── Dockerfile.weekly          # Weekly Streamlit
│   ├── docker-compose.yml             # Daily services
│   ├── docker-compose.weekly.yml      # Weekly service
│   ├── docker-compose.api.yml         # API only
│   ├── nginx.conf                     # Nginx for Streamlit
│   └── nginx.api.conf                 # Nginx for API
│
├── uploads/                           # File upload directory
└── logs/                              # Application logs
```

## 🐳 Docker Commands

### Daily Services (Streamlit + API)
```bash
# Start both services
docker-compose -f deployment/docker-compose.yml up --build

# Start in background
docker-compose -f deployment/docker-compose.yml up -d --build

# Stop services
docker-compose -f deployment/docker-compose.yml down

# View logs
docker-compose -f deployment/docker-compose.yml logs -f
```

### Weekly Service
```bash
# Start weekly service
docker-compose -f deployment/docker-compose.weekly.yml up --build

# Stop weekly service
docker-compose -f deployment/docker-compose.weekly.yml down
```

### API Only
```bash
# Start API only
docker-compose -f deployment/docker-compose.api.yml up --build

# Stop API only
docker-compose -f deployment/docker-compose.api.yml down
```

## 📖 Usage Guide

### Daily Report (6 slides)

#### Step 1: Upload Excel File
- Click "Browse files" in sidebar
- Select Excel file containing brand data
- Supported formats: `.xlsx`, `.xls`

#### Step 2: Enter Brand Name
- Enter brand name (e.g., Vinamilk, Vinfast, Nestle)

#### Step 3: Select Report Date & Time
- Choose report date from date picker
- Select data cutoff time (default: 15:00)
- System automatically calculates 24-hour window

#### Step 4: Generate
- Click "🚀 Generate prompt" button
- Wait ~1 minute (parallel processing)
- View results in 3 tabs

---

### Weekly Report (16 slides)

#### Step 1: Upload Excel File
- Click "Browse files" in sidebar
- Select Excel file containing brand data

#### Step 2: Enter Brand Name
- Enter brand name

#### Step 3: Select End Date & Time
- Choose end date for current week
- Select data cutoff time (default: 15:00)
- System automatically calculates 4 weeks (current + 3 past weeks)

#### Step 4: Generate
- Click "🚀 Generate weekly report" button
- Wait ~2 minutes (parallel processing)
- View results in 3 tabs

---

### Output Tabs
- **Preview**: Preview the generated prompt
- **Copy**: Copy prompt to paste into slide platforms
- **Download**: Download .txt and .json files

## 📊 Features

### ✅ Daily Report (6 slides)
1. **Slide 1**: Brand Overview - KPIs with 24h comparison
2. **Slide 2**: Trendline - 7-day trend analysis
3. **Slide 3**: Channel Breakdown - Distribution by channel
4. **Slide 4**: Sentiment & Attributes - Sentiment analysis
5. **Slide 5**: Top 5 Posts - High engagement posts
6. **Slide 6**: Top 5 Deleted Posts - Deleted posts tracking

### ✅ Weekly Report (16 slides)
1. **Slide 1**: Weekly Overview - KPIs + 4-week comparison
2. **Slide 2**: Trendline - 7-day trend within the week
3. **Slide 3**: Channel Distribution - Pie chart + Top 10 sources
4. **Slide 4**: Top Sources by Engagement - Table
5. **Slide 5**: Top Posts by Engagement - Table
6. **Slide 6**: Sentiment & Topics - 2 pie charts + bar chart
7. **Slide 7**: Positive Topics - Chart + insight
8. **Slide 8**: Top Positive Posts - Table
9. **Slide 9**: Negative Topics - Chart + insight
10. **Slide 10**: Top Negative Posts - Table
11. **Slide 11**: Brand Comparison - Multi-brand analysis
12. **Slide 12**: Brand Trendline - Multi-brand trends
13. **Slide 13**: Channel Distribution - Multi-brand channels
14. **Slide 14**: Top Sources - Multi-brand sources
15. **Slide 15**: Topic Sentiment - Multi-brand sentiment
16. **Slide 16**: Top Commented Posts - Most discussed posts

### ✅ Technical Features
- **Parallel Processing** - Slides generated simultaneously
- **24-hour Window** (Daily) - Precise to the hour
- **7-day Window** (Weekly) - Auto-calculates 4 weeks
- **Progress Tracking** - Real-time updates
- **Error Handling** - Detailed traceback
- **Auto-cleanup** - Temporary files removed
- **Modular Architecture** - OCP-compliant slide system

## 🎨 UI Features

- **Responsive Layout** - Wide mode with sidebar
- **Custom Styling** - Professional color scheme
- **Progress Tracking** - Visual feedback for users
- **Success/Error Boxes** - Clear status indicators
- **Tabs Navigation** - Organized output display
- **Download Buttons** - Easy file export
- **Sorted Bar Charts** - Ascending order visualization

## 🔧 Technical Details

### Architecture Highlights

#### Weekly Report System
- **Orchestrator Pattern**: `WeeklyReportOrchestrator` coordinates all slide generation
- **Parallel Execution**: LLM slides run concurrently, data-only slides run sequentially
- **Open/Closed Principle**: Add new slides by registering them, no core modification needed
- **Single Responsibility**: Each slide class owns its own logic
- **Incremental Generation**: Regenerate specific slides without rebuilding entire report

#### Data Processing
- **Datetime Precision**: Filters use `>=` for inclusive start boundaries
- **No Duplicate Removal**: Raw data preserved unless explicitly filtered
- **Engagement Calculation**: `Reactions + Shares + Comments`
- **NSR Formula**: `(Pos% - Neg%) / (Pos% + Neg%) × 100`

### Dependencies
- `streamlit` - Web framework
- `pandas` - Data processing
- `openpyxl` - Excel file handling
- `python-dotenv` - Environment variables
- `fastapi` - API server
- `uvicorn` - ASGI server

## 🐛 Troubleshooting

### Error: Cannot import modules
**Solution**: Ensure all files exist in correct directories and Python path is configured

### Error: API credentials not found
**Solution**: Create `.env` file with `API_KEY` and `BASE_URL`

### Error: Excel file not valid
**Solution**: Check Excel file format, ensure required columns exist

### App runs slowly
**Normal**: Prompt generation takes 1-2 minutes due to LLM calls

### Charts not sorted correctly
**Solution**: Data is sorted before `set_index()` in DataFrame, not after

### Missing 11 rows in data
**Fixed**: Changed filter from `>` to `>=` for inclusive date boundaries

## 📝 Example Usage

### Daily Report
```bash
# Terminal: Start app
streamlit run interfaces/app.py

# Browser: http://localhost:8501
# 1. Upload: brand_data.xlsx
# 2. Brand: Vinamilk
# 3. Date: 2026-03-16, Time: 15:00
# 4. Click Generate
# 5. Wait ~1 minute
# 6. Copy/Download prompt
```

### Weekly Report
```bash
# Terminal: Start app
streamlit run weekly_report/app.py

# Browser: http://localhost:8501
# 1. Upload: brand_data.xlsx
# 2. Brand: SHB
# 3. End Date: 2026-03-16, Time: 00:00
# 4. System auto-calculates 4 weeks
# 5. Click Generate
# 6. Wait ~2 minutes
# 7. Copy/Download prompt
```

## 🎯 Next Steps After Generation

### Manuss
1. Open https://manuss.com
2. Paste prompt
3. Click "Generate"
4. Wait 30-60 seconds

### Gamma
1. Open https://gamma.app
2. Paste prompt
3. Click "Generate"
4. Wait 30-60 seconds

### Beautiful.ai
1. Open https://beautiful.ai
2. Paste prompt
3. Click "Generate"
4. Manually add hyperlinks if needed

## 💡 Tips

- **Save JSON Data** - For reuse or debugging
- **Check Preview** - Before copying
- **Test with Small Data** - To verify setup
- **Keep .env Secure** - Don't commit API keys
- **Use Docker** - For consistent deployment
- **Monitor Logs** - For troubleshooting

## 🔐 Security

- API credentials loaded from `.env`
- Temporary files auto-cleanup
- No data persistence (session-based)
- Safe file upload handling
- Docker isolation

## 📞 Support

If you encounter issues:
1. Check console logs
2. View error details in expander
3. Verify API credentials
4. Check Excel file format
5. Review Docker logs

## 🔄 Recent Changes

See `WEEKLY_CHANGES.md` for detailed changelog of weekly report improvements.

## 📄 License

[Add your license here]

## 👥 Contributors

[Add contributors here]
