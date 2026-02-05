#!/usr/bin/env python3
"""
Simple script to run report generation
Usage: python test/run_simple.py
"""

import os
import sys
import json
from pathlib import Path

# Load .env file
try:
    from dotenv import load_dotenv
    # Try to load .env from test directory
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded .env from: {env_path}")
    else:
        load_dotenv()
        print("✅ Loaded .env from current directory")
except ImportError:
    print("⚠️  python-dotenv not installed")
    print("   Install with: pip install python-dotenv")
    print("   Or set environment variables manually")

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_dependencies():
    """Check if required packages are installed"""
    required = ['pandas', 'openpyxl', 'openai']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\nInstall with: pip install " + " ".join(missing))
        return False
    
    print("✅ All dependencies installed")
    return True


def check_api_credentials():
    """Check if API credentials are set"""
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    
    if not api_key or not base_url:
        print("❌ API credentials not set")
        print("\nPlease set environment variables:")
        print("  export API_KEY='your_api_key'")
        print("  export BASE_URL='your_base_url'")
        return False, None, None
    
    print("✅ API credentials found")
    return True, api_key, base_url


def check_data_file():
    """Check if data file exists"""
    try:
        import config
        FILE_PATH = config.FILE_PATH
    except ImportError:
        try:
            from test import config
            FILE_PATH = config.FILE_PATH
        except:
            FILE_PATH = "Nestle_Gerber_15h_labeled.xlsx"
    
    if not os.path.exists(FILE_PATH):
        print(f"❌ Data file not found: {FILE_PATH}")
        print("\nPlease update FILE_PATH in config.py")
        return False
    
    print(f"✅ Data file found: {FILE_PATH}")
    return True


def run_report_generation(api_key, base_url):
    """Run the report generation"""
    try:
        # Try importing without test prefix (when running from test directory)
        import report_generator
        ReportGenerator = report_generator.ReportGenerator
    except ImportError:
        # Try with test prefix (when running from parent directory)
        from test import report_generator
        ReportGenerator = report_generator.ReportGenerator
    
    print("\n" + "="*60)
    print("STARTING REPORT GENERATION")
    print("="*60)
    
    try:
        generator = ReportGenerator(api_key, base_url)
        report = generator.generate_and_save("report_output.json")
        
        print("\n✅ Report generated successfully!")
        print(f"   Output: report_output.json")
        
        return True, report
        
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def render_html_report():
    """Render HTML from JSON"""
    try:
        import template_renderer
        TemplateRenderer = template_renderer.TemplateRenderer
    except ImportError:
        from test import template_renderer
        TemplateRenderer = template_renderer.TemplateRenderer
    
    print("\n" + "="*60)
    print("RENDERING HTML REPORT")
    print("="*60)
    
    try:
        # Load report data
        with open('report_output.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Render
        renderer = TemplateRenderer('template_parameterized.html')
        renderer.render_to_file(data, 'final_report.html')
        
        print("\n✅ HTML rendered successfully!")
        print(f"   Output: final_report.html")
        print("\n   Open in browser to view the report")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error rendering HTML: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function"""
    print("\n" + "="*60)
    print("REPORT GENERATION SYSTEM")
    print("="*60 + "\n")
    
    # Step 1: Check dependencies
    print("Step 1: Checking dependencies...")
    if not check_dependencies():
        return
    
    # Step 2: Check API credentials
    print("\nStep 2: Checking API credentials...")
    has_creds, api_key, base_url = check_api_credentials()
    if not has_creds:
        return
    
    # Step 3: Check data file
    print("\nStep 3: Checking data file...")
    if not check_data_file():
        return
    
    # Step 4: Generate report
    print("\nStep 4: Generating report...")
    success, report = run_report_generation(api_key, base_url)
    if not success:
        return
    
    # Step 5: Render HTML
    print("\nStep 5: Rendering HTML...")
    if not render_html_report():
        return
    
    # Success!
    print("\n" + "="*60)
    print("✅ ALL STEPS COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nGenerated files:")
    print("  - test/report_output.json (JSON data)")
    print("  - test/final_report.html (HTML report)")
    print("\nNext steps:")
    print("  1. Open test/final_report.html in your browser")
    print("  2. Review the generated insights")
    print("  3. Customize config.py for different dates/brands")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
