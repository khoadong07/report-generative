import json
import re
import os
import asyncio
from typing import List, Dict, Any, Tuple

import pandas as pd
from tqdm import tqdm
from openai import OpenAI

# ==================================================
# CONFIG
# ==================================================

RULE_PATH = "label_data/rules/label_classification.93cd0348.json"
INPUT_FILE = "label_data/VNM.xlsx"
OUTPUT_FILE = "VNM_fixed.xlsx"

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "EMPTY")
MODEL_NAME = "qwen3-1.7b-viettel-qa"

MAX_CONCURRENCY = 8   # Reduced concurrency to avoid overload

client = OpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY
)

# ==================================================
# Utils
# ==================================================

def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def merge_text(title: str, content: str, description: str) -> str:
    parts = [title, content, description]
    return "\n".join([p for p in parts if isinstance(p, str) and p.strip()])

# ==================================================
# Load rules
# ==================================================

def load_rules(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        rules = json.load(f)
    return [r for r in rules if r.get("is_active") is True]

def build_label_lookup(rules: List[Dict[str, Any]]) -> Dict[str, Dict[str, str]]:
    return {
        r["label_id"]: {
            "label_vie": r["label_vie"],
            "label_eng": r["label_eng"]
        }
        for r in rules
    }

# ==================================================
# Rule-based classify
# ==================================================

def rule_based_classify(content: str, rules: List[Dict[str, Any]]) -> List[str]:
    content_norm = normalize_text(content)
    matched = []

    for rule in rules:
        for kw in rule.get("keywords", []):
            if normalize_text(kw) in content_norm:
                matched.append(rule["label_id"])
                break

    return matched

# ==================================================
# Prompt builder (OPTIMIZED FOR CONTEXT SIZE)
# ==================================================

def build_compact_prompt(content: str, rules: List[Dict[str, Any]]) -> str:
    """Build a compact prompt to avoid context size limits"""
    # Truncate content if too long
    max_content_length = 150
    if len(content) > max_content_length:
        content = content[:max_content_length] + "..."
    
    # Create compact label blocks with only essential info
    label_blocks = []
    for r in rules:
        # Only include essential fields and truncate long definitions
        definition = r["definition"]
        if len(definition) > 80:
            definition = definition[:80] + "..."
            
        label_blocks.append(f"[{r['label_id']}] {r['label_vie']}: {definition}")

    labels_text = "\n".join(label_blocks)

    return f"""Classify Vietnamese text into ONE label_id.

Content: {content}

Labels:
{labels_text}

Output JSON only:
{{"label_id": "..."}}"""

def build_minimal_prompt(content: str, rules: List[Dict[str, Any]]) -> str:
    """Minimal prompt for very small context limits"""
    # Severely truncate content
    content = content[:80] + "..." if len(content) > 80 else content
    
    # Only show first 8 rules to stay within limits
    limited_rules = rules[:8]
    
    labels = "\n".join([f"{r['label_id']}: {r['label_vie']}" for r in limited_rules])
    
    return f"""Classify: {content}

Options:
{labels}

JSON: {{"label_id": "..."}}"""

def build_qwen_prompt(content: str, rules: List[Dict[str, Any]]) -> str:
    """Optimized prompt builder with fallback strategies"""
    # Calculate approximate prompt size
    estimated_size = len(content) + sum(len(str(r.get("definition", ""))) for r in rules)
    
    if estimated_size > 2000:  # If too large, use minimal version
        return build_minimal_prompt(content, rules)
    elif estimated_size > 1000:  # If moderately large, use compact version
        return build_compact_prompt(content, rules)
    else:
        # Use compact version as default (safer than original)
        return build_compact_prompt(content, rules)

# ==================================================
# Async LLM call (thread-safe with better error handling)
# ==================================================

async def llm_classify_async(prompt: str) -> str:
    loop = asyncio.get_running_loop()

    try:
        response = await loop.run_in_executor(
            None,
            lambda: client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a text classifier. Return only JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=32,  # Reduced max_tokens for faster response
                timeout=30  # Add timeout
            )
        )

        raw = response.choices[0].message.content
        
        # Extract JSON block safely
        match = re.search(r"\{[\s\S]*?\}", raw)
        if not match:
            # Try to find just the label_id value
            label_match = re.search(r'"label_id":\s*"([^"]+)"', raw)
            if label_match:
                return label_match.group(1)
            raise ValueError(f"No JSON object found in LLM output: {raw}")

        result = json.loads(match.group())
        return result["label_id"]
        
    except Exception as e:
        print(f"LLM API Error: {e}")
        raise

# ==================================================
# Async classify single text (with better error handling)
# ==================================================

async def classify_single_text_async(
    text: str,
    rules: List[Dict[str, Any]],
    label_lookup: Dict[str, Dict[str, str]],
    semaphore: asyncio.Semaphore
) -> Tuple[str, Dict[str, str]]:

    # Default result in case of error or unknown label
    unknown_label_result = {
        "label_vie": "Không xác định (Lỗi phân loại)", 
        "label_eng": "Unknown (Classification Error)"
    }

    # Rule-based classification first
    matched = rule_based_classify(text, rules)
    if matched:
        label_id = matched[0]
        if label_id in label_lookup:
            return text, {
                "label_vie": label_lookup[label_id]["label_vie"],
                "label_eng": label_lookup[label_id]["label_eng"]
            }
        else:
            print(f"Warning: Rule-based matched label_id '{label_id}' not found in lookup for text: '{text[:50]}...'")

    # LLM fallback with better error handling
    async with semaphore:
        try:
            prompt = build_qwen_prompt(text, rules)
            llm_classified_label_id = await llm_classify_async(prompt)
            
            if llm_classified_label_id in label_lookup:
                return text, {
                    "label_vie": label_lookup[llm_classified_label_id]["label_vie"],
                    "label_eng": label_lookup[llm_classified_label_id]["label_eng"]
                }
            else:
                print(f"Warning: LLM returned unknown label_id '{llm_classified_label_id}' for text: '{text[:50]}...'")
                return text, unknown_label_result
                
        except Exception as e:
            print(f"Error during LLM classification for text: '{text[:50]}...'. Error: {e}")
            return text, unknown_label_result

# ==================================================
# Async classify all texts
# ==================================================

async def async_classify_texts(
    texts: List[str],
    rules: List[Dict[str, Any]],
    label_lookup: Dict[str, Dict[str, str]],
    max_concurrency: int
) -> Dict[str, Dict[str, str]]:

    semaphore = asyncio.Semaphore(max_concurrency)

    tasks = [
        classify_single_text_async(text, rules, label_lookup, semaphore)
        for text in texts
    ]

    results: Dict[str, Dict[str, str]] = {}

    for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Classifying"):
        text, result = await coro
        results[text] = result

    return results

# ==================================================
# Main async pipeline
# ==================================================

async def process_excel_async():
    print("Loading Excel file...")
    df = pd.read_excel(INPUT_FILE)

    for col in ["Title", "Content", "Description"]:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    print("Loading rules...")
    rules = load_rules(RULE_PATH)
    label_lookup = build_label_lookup(rules)
    
    print(f"Loaded {len(rules)} active rules")

    print("Preparing texts...")
    df["merged_text"] = df.apply(
        lambda r: merge_text(r["Title"], r["Content"], r["Description"]),
        axis=1
    )

    df["dedup_key"] = df["merged_text"].apply(normalize_text)
    unique_texts = df["dedup_key"].unique().tolist()
    
    print(f"Processing {len(unique_texts)} unique texts...")

    cache = await async_classify_texts(
        texts=unique_texts,
        rules=rules,
        label_lookup=label_lookup,
        max_concurrency=MAX_CONCURRENCY
    )

    print("Applying results...")
    df["label_vie"] = df["dedup_key"].apply(lambda x: cache[x]["label_vie"])
    df["label_eng"] = df["dedup_key"].apply(lambda x: cache[x]["label_eng"])

    df.drop(columns=["merged_text", "dedup_key"], inplace=True)
    df.to_excel(OUTPUT_FILE, index=False)

    print(f"✅ Done. Output saved to {OUTPUT_FILE}")

# ==================================================
# Entrypoint
# ==================================================

if __name__ == "__main__":
    asyncio.run(process_excel_async())