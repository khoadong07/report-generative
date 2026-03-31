#!/usr/bin/env python3
"""
Masan Prompt Builder Registry
"""
from typing import Dict, Any, Type
from weekly_report_masan.builders.base import BasePromptBuilder
from weekly_report_masan.builders.slide01_market import Slide01MarketPromptBuilder
from weekly_report_masan.builders.slide02_discussion import Slide02DiscussionPromptBuilder
from weekly_report_masan.builders.slide03_health import Slide03HealthPromptBuilder
from weekly_report_masan.builders.slide04_products import Slide04ProductsPromptBuilder
from weekly_report_masan.builders.slide05_category import Slide05CategoryPromptBuilder
from weekly_report_masan.builders.slide06_channels import Slide06ChannelsPromptBuilder
from weekly_report_masan.builders.slide07_sentiment import Slide07SentimentPromptBuilder
from weekly_report_masan.builders.slide08_trends import Slide08TrendsPromptBuilder

# Registry mapping for Masan
MASAN_PROMPT_REGISTRY: Dict[str, Type[BasePromptBuilder]] = {
    "slide_1_market": Slide01MarketPromptBuilder,
    "slide_2_discussion": Slide02DiscussionPromptBuilder,
    "slide_3_health": Slide03HealthPromptBuilder,
    "slide_4_products": Slide04ProductsPromptBuilder,
    "slide_5_category": Slide05CategoryPromptBuilder,
    "slide_6_channels": Slide06ChannelsPromptBuilder,
    "slide_7_sentiment": Slide07SentimentPromptBuilder,
    "slide_8_trends": Slide08TrendsPromptBuilder,
}

def build_masan_slide_prompt(key: str, slide_data: Dict[str, Any], **kwargs) -> str:
    """Helper to build a Masan slide prompt."""
    builder_cls = MASAN_PROMPT_REGISTRY.get(key)
    if builder_cls:
        builder = builder_cls()
        return builder.build(slide_data, **kwargs)
    return f"Warning: No Masan prompt builder for '{key}'\n\n"
