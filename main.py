"""
Main Module: Social Listening Report Generator
Chức năng: Hàm main duy nhất nhận file đầu vào và sinh ra prompt báo cáo + save file .md
"""
import sys
import os
from datetime import datetime
from data_loader import load_data_from_file
from slides import SlideDataExtractor
from prompt_builder import build_prompt_variables
from prompt_template import PROMPT_MD_TEMPLATE, render_prompt


def generate_report(file_path, progress_callback=None):
    """
    Sinh báo cáo từ file Excel
    
    Args:
        file_path (str): Đường dẫn file Excel hoặc URL
        progress_callback (callable): Callback function để update progress
        
    Returns:
        tuple: (prompt báo cáo hoàn chỉnh, primary_brand)
    """
    # Bước 1: Load dữ liệu
    if progress_callback:
        progress_callback(0.1, "Loading data...")
    df = load_data_from_file(file_path, progress_callback)
    
    # Bước 2: Trích xuất dữ liệu từng slide
    if progress_callback:
        progress_callback(0.2, "Extracting slide data...")
    extractor = SlideDataExtractor(df, progress_callback)
    slides_data = extractor.extract_all()
    
    # Bước 3: Xây dựng biến prompt
    if progress_callback:
        progress_callback(0.85, "Building prompt variables...")
    prompt_vars = build_prompt_variables(slides_data)
    
    # Bước 4: Render prompt
    if progress_callback:
        progress_callback(0.95, "Rendering template...")
    final_prompt = render_prompt(PROMPT_MD_TEMPLATE, prompt_vars)
    
    if progress_callback:
        progress_callback(1.0, "Report generated successfully")
    
    # Lấy primary brand từ prompt_vars
    primary_brand = prompt_vars.get("PRIMARY_BRAND", "Report")
    
    return final_prompt, primary_brand


def save_report(report_content, primary_brand=None, output_dir="reports"):
    """
    Lưu báo cáo vào file .md
    
    Args:
        report_content (str): Nội dung báo cáo
        primary_brand (str): Tên thương hiệu chính (dùng cho tên file)
        output_dir (str): Thư mục lưu file (default: "reports")
        
    Returns:
        str: Đường dẫn file đã lưu
    """
    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Tạo tên file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if primary_brand:
        filename = f"{primary_brand}_report_{timestamp}.md"
    else:
        filename = f"report_{timestamp}.md"
    
    file_path = os.path.join(output_dir, filename)
    
    # Lưu file
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        return file_path
    except Exception as e:
        raise


def main():
    """Hàm main - điểm vào chính"""
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path> [output_dir]")
        print("Example: python main.py data.xlsx")
        print("Example: python main.py data.xlsx ./my_reports")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "reports"
    
    try:
        # Sinh báo cáo
        report, primary_brand = generate_report(file_path)
        
        # Lưu file
        saved_file = save_report(report, primary_brand, output_dir)
        
        # In báo cáo ra console
        print("\n" + "="*60)
        print("FINAL REPORT")
        print("="*60 + "\n")
        print(report)
        
        # In thông tin lưu file
        print("\n" + "="*60)
        print("SAVE SUMMARY")
        print("="*60)
        print(f"Primary Brand: {primary_brand}")
        print(f"Output File: {saved_file}")
        print(f"File Size: {os.path.getsize(saved_file)} bytes")
        print("="*60)
        
    except Exception as e:
        print(f"[✗] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
