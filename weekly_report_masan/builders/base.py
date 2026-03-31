#!/usr/bin/env python3
"""
Base classes for Masan Weekly Report Slide Prompt Builders
Shared formatting and layout logic.
"""
from datetime import datetime
import pandas as pd
from typing import Any, Dict, Optional


class BasePromptBuilder:
    """Provides common formatting tools for Masan prompt generation."""

    def format_number(self, num: Any) -> str:
        if isinstance(num, (int, float)):
            return f"{int(num):,}"
        return str(num)

    def format_date(self, date_str: Any) -> str:
        if isinstance(date_str, str):
            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y"]:
                try:
                    return datetime.strptime(date_str, fmt).strftime("%d/%m/%Y")
                except ValueError:
                    continue
            try:
                return pd.to_datetime(date_str).strftime("%d/%m/%Y")
            except Exception:
                return str(date_str)
        if isinstance(date_str, (datetime, pd.Timestamp)):
            return date_str.strftime("%d/%m/%Y")
        return str(date_str)

    def _header(self, title: str) -> str:
        return (
            "----------------------------------------------------------------\n"
            f"{title}\n"
            "----------------------------------------------------------------\n\n"
        )

    def build(self, slide_data: Dict[str, Any], **kwargs) -> str:
        """Each slide builder implements this."""
        raise NotImplementedError("Subclasses must implement build()")
