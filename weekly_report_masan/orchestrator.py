#!/usr/bin/env python3
"""
Masan Weekly Report Orchestrator
Supports 4 slides + category detail slides
"""
from typing import Any, Dict
from weekly_report_masan.prompt_builder import generate_masan_prompt

# Masan slides
MASAN_SLIDES = ["slide_1_market", "slide_2_discussion", "slide_3_health", "slide_4_products", "slide_5_category"]

class MasanWeeklyReportOrchestrator:
    """
    Orchestrates report generation for Masan brands.
    Supports:
    - Slide 1: Consumer & Markets Overview
    - Slide 2: Discussion Overview (Market share, Comparison, Trends)
    - Slide 3: Health Index & Channels (Sentiment+NSR, Channels, Top sources, Health table)
    - Slide 4: Masan Consumer Products (Category analysis, Trends, Sentiment)
    - Slide 5+: Category Detail (One slide per category: Brand SOV, Cate distribution, Top products)
    """

    def __init__(self, slide_data: Dict[str, Any]):
        """
        Initialize with pre-generated slide data.
        
        Args:
            slide_data: Dictionary containing slide data
        """
        self.slide_data = slide_data

    def generate_masan_report_prompt(self) -> str:
        """
        Build the final prompt using Masan builders.
        
        Returns:
            Formatted prompt string for slide generation
        """
        return generate_masan_prompt(self.slide_data)
