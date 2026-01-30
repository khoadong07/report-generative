# Social Listening Report Generator

A Python-based tool that generates comprehensive social listening analysis reports from Excel data. The script processes social media mentions, analyzes sentiment, topics, channels, and brands to produce structured markdown reports with insights and strategic recommendations.

## Overview

This tool automates the creation of 13-slide social listening reports by:
- Loading and preprocessing social media data from Excel files
- Extracting key metrics and statistics for each slide
- Generating sample data records as evidence for insights
- Rendering a complete markdown report with analysis framework

## Features

- **Data Loading**: Supports local Excel files and remote URLs
- **Multi-dimensional Analysis**: Analyzes data across brands, channels, topics, and sentiment
- **Sample Data Integration**: Includes actual data samples as evidence for each analysis section
- **Structured Output**: Generates markdown reports following the INSIGHT FRAMEWORK (WHAT, WHY, SO WHAT)
- **Automated File Management**: Saves reports with timestamps and brand names

## Installation

### Prerequisites
- Python 3.7+
- Required packages: `pandas`, `requests`

### Setup

1. Clone or download the project
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install pandas requests openpyxl
   ```

## Usage

### Basic Usage

Run the script with an Excel file:

```bash
python main.py data.xlsx
```

This will:
1. Load data from `data.xlsx`
2. Generate a complete report
3. Save the report to `reports/` directory with timestamp
4. Display the report in console

### Advanced Usage

Specify a custom output directory:

```bash
python main.py data.xlsx ./my_reports
```

### Using Remote Data

You can also load data from a URL:

```bash
python main.py "https://example.com/data.xlsx"
```

## Input Data Format

The Excel file should contain the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `PublishedDate` | datetime | Date when the mention was published |
| `Channel` | string | Social media channel (e.g., Facebook, Twitter, Instagram) |
| `Topic` | string | Brand or main topic being discussed |
| `Labels1` | string | Specific topic/category label |
| `Sentiment` | string | Sentiment classification (Positive, Negative, Neutral) |
| `Title` | string | Title or headline of the mention |
| `Content` | string | Main content/text of the mention |
| `Description` | string | Additional description |
| `Type` | string | Type of content (e.g., Post, Comment, Review) |

## Output

The script generates a markdown report with 13 slides:

1. **Report Overview** - Study period, data source, total metrics
2. **Share of Voice (SOV)** - Brand comparison and market share
3. **Buzz Evolution** - Daily mention trends
4. **Highlight Buzz** - Notable mentions and content
5. **Sentiment Overview** - Positive/Negative/Neutral breakdown
6. **Channel Mix** - Distribution across social channels
7. **Sentiment by Channel** - Sentiment analysis per channel
8. **Top Topics** - Most discussed topics/themes
9. **Topic Trends** - Topic evolution over time
10. **Topics by Channel** - Topic distribution across channels
11. **Sentiment by Brand** - Comparative sentiment analysis
12. **Topics by Brand** - Topic distribution across brands
13. **Conclusions & Strategic Implications** - Key insights and recommendations

### Report Structure

Each slide includes:
- **Data Tables**: Quantitative metrics and statistics
- **Sample Records**: Actual data examples as evidence
- **Insight Framework**: WHAT (findings), WHY (reasons), SO WHAT (implications)

### Output Location

Reports are saved to: `reports/{PRIMARY_BRAND}_report_{TIMESTAMP}.md`

Example: `reports/Vinfast_report_20260130_214437.md`

## Module Documentation

### `main.py`
Main entry point that orchestrates the report generation pipeline.

**Key Functions:**
- `generate_report(file_path)` - Loads data and generates complete report
- `save_report(report_content, primary_brand, output_dir)` - Saves report to file
- `main()` - CLI entry point

### `data_loader.py`
Handles data loading and preprocessing.

**Key Functions:**
- `load_data_from_file(file_path)` - Loads Excel data from file or URL, processes dates

### `slides.py`
Extracts and structures data for each slide.

**Key Class:**
- `SlideDataExtractor` - Extracts metrics and sample data for all 12 slides
  - `slide_1_overview()` - General statistics
  - `slide_2_sov()` - Share of voice analysis
  - `slide_3_daily_buzz()` - Daily trends
  - `slide_4_highlight_buzz()` - Notable mentions
  - `slide_5_sentiment_overview()` - Sentiment distribution
  - `slide_6_channel_mix()` - Channel analysis
  - `slide_7_sentiment_by_channel()` - Sentiment per channel
  - `slide_8_top_topics()` - Topic ranking
  - `slide_9_topic_trend()` - Topic trends
  - `slide_10_topic_by_channel()` - Topics per channel
  - `slide_11_sentiment_by_brand()` - Brand sentiment comparison
  - `slide_12_topic_by_brand()` - Topics per brand

### `prompt_builder.py`
Builds variables for report template rendering.

**Key Functions:**
- `build_prompt_variables(slides_data)` - Creates dictionary of all report variables
- `_format_sample_records(records, max_records)` - Formats sample data for display

### `prompt_template.py`
Defines the markdown template and rendering logic.

**Key Components:**
- `PROMPT_MD_TEMPLATE` - Complete markdown template with placeholders
- `render_prompt(template, variables)` - Replaces placeholders with actual values

## Example Workflow

```bash
# 1. Prepare your Excel file with social listening data
# File: weekly_data.xlsx

# 2. Run the script
python main.py weekly_data.xlsx

# 3. Check the output
# Report saved to: reports/Vinfast_report_20260130_214437.md

# 4. Open and review the report
cat reports/Vinfast_report_20260130_214437.md
```

## Error Handling

The script includes error handling for:
- Missing input files
- Invalid Excel format
- Network errors when loading remote data
- File write permissions

Error messages are displayed in the console with detailed traceback information.

## Performance Notes

- Processing time depends on data size (typically 1-5 seconds for 1000+ records)
- Sample data is randomly selected from the first 50 records of each category
- Large datasets (10,000+ records) may take longer to process

## Troubleshooting

### "File not found" error
- Ensure the Excel file path is correct
- Use absolute paths if relative paths don't work

### "No module named 'pandas'" error
- Install required packages: `pip install pandas requests openpyxl`

### Report not saving
- Check that the `reports/` directory exists or has write permissions
- Verify disk space is available

### Empty sample data in report
- Ensure the Excel file has data in the expected columns
- Check that column names match exactly (case-sensitive)

## License

This project is provided as-is for internal use.

## Support

For issues or questions, please review the code comments and module documentation above.
