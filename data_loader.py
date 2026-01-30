"""
Module: Data Loader
Chức năng: Load và preprocess dữ liệu từ file Excel
"""
import requests
import pandas as pd
from io import BytesIO


def load_data_from_file(file_path, progress_callback=None):
    """
    Load và preprocess dữ liệu từ file Excel hoặc URL
    
    Args:
        file_path (str): Đường dẫn file hoặc URL
        progress_callback (callable): Callback function để update progress
        
    Returns:
        pd.DataFrame: DataFrame với các cột ngày tháng đã xử lý
    """
    if progress_callback:
        progress_callback(0.1, "Loading file...")
    
    if file_path.startswith('http'):
        response = requests.get(file_path)
        df = pd.read_excel(BytesIO(response.content))
    else:
        df = pd.read_excel(file_path)
    
    if progress_callback:
        progress_callback(0.3, "Processing dates...")
    
    df["PublishedDate"] = pd.to_datetime(df["PublishedDate"])
    df["Date"] = df["PublishedDate"].dt.date
    
    if progress_callback:
        progress_callback(0.5, "Data loaded successfully")
    
    return df
