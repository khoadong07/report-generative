#!/usr/bin/env python3
"""
Data Processor for Masan Weekly Report
Handles merging raw data with product mapping
"""
import pandas as pd
from pathlib import Path


def merge_nganh_hang(df: pd.DataFrame, df_flat: pd.DataFrame) -> pd.DataFrame:
    """
    Merge dữ liệu raw với bộ mapping theo 2 giai đoạn:
    
    Giai đoạn 1:
        df.Labels1 == df_flat.Sản phẩm
        -> lấy Ngành hàng, Cate, Brand
    
    Giai đoạn 2:
        nếu chưa có Ngành hàng thì dùng:
        df.Topic == df_flat.Sản phẩm
        -> điền Ngành hàng
    
    Parameters
    ----------
    df : pd.DataFrame
        File raw excel đầu vào
    df_flat : pd.DataFrame
        File mapping chứa các cột:
        ['Ngành hàng', 'Cate', 'Brand', 'Sản phẩm']
    
    Returns
    -------
    pd.DataFrame
        DataFrame sau khi merge hoàn chỉnh
    """
    # Copy để tránh sửa trực tiếp dữ liệu gốc
    df = df.copy()
    df_flat = df_flat.copy()
    
    # =========================
    # 0. Kiểm tra cột bắt buộc
    # =========================
    required_df_cols = ["Labels1", "Topic"]
    required_flat_cols = ["Sản phẩm", "Ngành hàng", "Cate", "Brand"]
    
    missing_df = [col for col in required_df_cols if col not in df.columns]
    missing_flat = [col for col in required_flat_cols if col not in df_flat.columns]
    
    if missing_df:
        raise KeyError(f"df thiếu cột: {missing_df}")
    if missing_flat:
        raise KeyError(f"df_flat thiếu cột: {missing_flat}")
    
    # =========================
    # 1. Chuẩn hóa key để join
    # =========================
    df["Labels1"] = df["Labels1"].astype(str).str.strip()
    df["Topic"] = df["Topic"].astype(str).str.strip()
    
    df_flat["Sản phẩm"] = df_flat["Sản phẩm"].astype(str).str.strip()
    df_flat["Ngành hàng"] = df_flat["Ngành hàng"].astype(str).str.strip()
    df_flat["Cate"] = df_flat["Cate"].astype(str).str.strip()
    df_flat["Brand"] = df_flat["Brand"].astype(str).str.strip()
    
    # Loại bỏ các dòng mapping không hợp lệ
    df_flat = df_flat[df_flat["Sản phẩm"].notna() & (df_flat["Sản phẩm"] != "")]
    df_flat = df_flat.drop_duplicates(subset=["Sản phẩm"])
    
    # =========================
    # 2. Giai đoạn 1: merge theo Labels1
    # =========================
    df_flat_renamed = df_flat.rename(columns={"Sản phẩm": "Labels1"})
    df_merged = df.merge(
        df_flat_renamed[["Labels1", "Ngành hàng", "Cate", "Brand"]],
        on="Labels1",
        how="left"
    )
    
    # Gán cột Sản phẩm từ Labels1
    df_merged["Sản phẩm"] = df_merged["Labels1"]
    
    # =========================
    # 3. Giai đoạn 2: map Ngành hàng theo Topic = Sản phẩm
    #    chỉ fill vào chỗ còn thiếu
    # =========================
    map_nganh_hang = (
        df_flat[["Sản phẩm", "Ngành hàng"]]
        .dropna(subset=["Sản phẩm"])
        .drop_duplicates(subset=["Sản phẩm"])
        .set_index("Sản phẩm")["Ngành hàng"]
    )
    
    df_merged["Ngành hàng"] = df_merged["Ngành hàng"].replace("nan", pd.NA)
    df_merged["Ngành hàng"] = df_merged["Ngành hàng"].fillna(
        df_merged["Topic"].map(map_nganh_hang)
    )
    
    return df_merged


def load_mapping_file(mapping_path: str = None) -> pd.DataFrame:
    """
    Load the mapping file (Masan - Label_flat.csv).
    
    Parameters
    ----------
    mapping_path : str, optional
        Path to mapping file. If None, uses default path in project.
    
    Returns
    -------
    pd.DataFrame
        Mapping dataframe with columns: Ngành hàng, Cate, Brand, Sản phẩm
    """
    if mapping_path is None:
        # Default path in project
        project_root = Path(__file__).parent
        mapping_path = project_root / "data" / "Masan - Label_flat.csv"
    
    if not Path(mapping_path).exists():
        raise FileNotFoundError(f"Mapping file not found: {mapping_path}")
    
    df_flat = pd.read_csv(mapping_path)
    
    # Validate required columns
    required_cols = ["Sản phẩm", "Ngành hàng", "Cate", "Brand"]
    missing = [col for col in required_cols if col not in df_flat.columns]
    if missing:
        raise KeyError(f"Mapping file thiếu cột: {missing}")
    
    return df_flat


def process_uploaded_file(df_raw: pd.DataFrame, mapping_path: str = None) -> pd.DataFrame:
    """
    Process uploaded raw file by merging with mapping.
    
    Parameters
    ----------
    df_raw : pd.DataFrame
        Raw uploaded dataframe
    mapping_path : str, optional
        Path to mapping file. If None, uses default.
    
    Returns
    -------
    pd.DataFrame
        Processed dataframe ready for report generation
    """
    # Load mapping file
    df_flat = load_mapping_file(mapping_path)
    
    # Merge
    df_merged = merge_nganh_hang(df_raw, df_flat)
    
    return df_merged
