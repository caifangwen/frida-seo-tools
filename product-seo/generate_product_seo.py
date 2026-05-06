#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Product SEO Content Generator
Supports Kimi (Moonshot) API and other OpenAI-compatible APIs.
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional

import requests

# Configuration
CONFIG_FILE = ".seo_config.json"
CATEGORIES_DIR = Path("categories")
OUTPUT_DIR = Path("output")
BASE_PROMPT_FILE = CATEGORIES_DIR / "prompt_base.md"

DEFAULT_API_URL = "https://api.moonshot.cn/v1/chat/completions"
DEFAULT_MODEL = "moonshot-v1-32k"
DEFAULT_BATCH_SIZE = 15
DEFAULT_RATE_LIMIT = 1.0  # requests per second

# Column mapping
COL_SHORT_DESC = "Short description"
COL_DESCRIPTION = "Description"
COL_FOCUS_KW = "Meta: rank_math_focus_keyword"
COL_SEO_TITLE = "Meta: rank_math_title"
COL_META_DESC = "Meta: rank_math_description"

ALL_COLS = [COL_SHORT_DESC, COL_DESCRIPTION, COL_FOCUS_KW, COL_SEO_TITLE, COL_META_DESC]

# CLI-friendly column names -> actual CSV column names
COL_ALIASES = {
    "short_desc": COL_SHORT_DESC,
    "description": COL_DESCRIPTION,
    "focus_kw": COL_FOCUS_KW,
    "seo_title": COL_SEO_TITLE,
    "meta_desc": COL_META_DESC,
}


def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(config: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def configure_api():
    print("\n=== API Configuration ===")
    config = load_config()
    key = input(f"API Key [{config.get('api_key', '')[:8]}...]: ").strip()
    if key:
        config["api_key"] = key
    url = input(f"API URL [{config.get('api_url', DEFAULT_API_URL)}]: ").strip()
    if url:
        config["api_url"] = url
    model = input(f"Model [{config.get('model', DEFAULT_MODEL)}]: ").strip()
    if model:
        config["model"] = model
    save_config(config)
    print("Configuration saved.")


def read_csv_products(filepath: Path) -> List[Dict[str, str]]:
    products = []
    with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append({k: (v or "") for k, v in row.items()})
    return products


def write_csv_products(filepath: Path, fieldnames: List[str], products: List[Dict[str, str]]):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)


def extract_fieldnames(filepath: Path) -> List[str]:
    with open(filepath, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        return next(reader)


def load_prompt_template(category_dir: Path) -> str:
    base = ""
    if BASE_PROMPT_FILE.exists():
        base = BASE_PROMPT_FILE.read_text(encoding="utf-8")
    cat_prompt = category_dir / "prompt.md"
    cat = ""
    if cat_prompt.exists():
        cat = cat_prompt.read_text(encoding="utf-8")
    prompt = base + "\n\n" + cat if base and cat else (base or cat)
    return prompt


def load_category_variables(category_dir: Path) -> Dict[str, str]:
    config_file = category_dir / "config.json"
    if not config_file.exists():
        return {}
    with open(config_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    vars_dict = {}
    for k, v in data.get("variables", {}).items():
        if isinstance(v, dict):
            vars_dict[k] = v.get("value", "")
        else:
            vars_dict[k] = str(v)
    return vars_dict


def build_output_spec(cols: List[str]) -> str:
    lines = ["## Output Specification", ""]
    lines.append("For each product, return a JSON object with these exact fields:")
    for col in cols:
        if col == COL_SHORT_DESC:
            lines.append('- `short_desc`: HTML <h3>Key Features</h3><ul> with exactly 3 <li> items. 60-80 words total.')
        elif col == COL_DESCRIPTION:
            lines.append('- `description`: Full HTML with <h2>, <p> (150-200 words), <h3>Key Features</h3><ul>, <h3>Specifications</h3><table>.')
        elif col == COL_SEO_TITLE:
            lines.append('- `seo_title`: ≤ 60 characters, include primary keyword.')
        elif col == COL_META_DESC:
            lines.append('- `meta_desc`: ≤ 150 characters, end with CTA like "Order wholesale today."')
        elif col == COL_FOCUS_KW:
            lines.append('- `focus_kw`: One keyword phrase, 2-4 words.')
    lines.append("")
    lines.append("Return a JSON array of objects. No markdown fences, no extra text.")
    return "\n".join(lines)


def build_product_list(products: List[Dict[str, str]]) -> str:
    lines = ["## Products to Generate"]
    for i, p in enumerate(products, 1):
        name = p.get("Name", "").strip()
        sku = p.get("SKU", "").strip()
        cats = p.get("Categories", "").strip()
        lines.append(f"{i}. Name: {name} | SKU: {sku} | Categories: {cats}")
    return "\n".join(lines)


def inject_variables(prompt: str, variables: Dict[str, str]) -> str:
    for k, v in variables.items():
        prompt = prompt.replace(f"{{{{{k}}}}}", str(v))
    return prompt


def ensure_placeholders(prompt: str) -> str:
    if "{{product_list}}" not in prompt:
        prompt += "\n\n## Product List\n{{product_list}}"
    if "{{output_spec}}" not in prompt:
        prompt += "\n\n## Output Specification\n{{output_spec}}"
    return prompt


def call_api(prompt: str, config: dict) -> List[Dict[str, str]]:
    api_key = config.get("api_key", "")
    api_url = config.get("api_url", DEFAULT_API_URL)
    model = config.get("model", DEFAULT_MODEL)

    if not api_key:
        raise RuntimeError("API key not configured.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an SEO copywriting assistant. Output valid JSON only."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    }

    resp = requests.post(api_url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    content = data["choices"][0]["message"]["content"]

    # Strip markdown fences if any
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]
    elif content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
    content = content.strip()

    result = json.loads(content)
    if isinstance(result, dict) and "products" in result:
        result = result["products"]
    if not isinstance(result, list):
        raise ValueError(f"Expected JSON array, got {type(result).__name__}")
    return result


def map_result_to_row(result_item: Dict[str, str], cols: List[str]) -> Dict[str, str]:
    mapping = {
        "short_desc": COL_SHORT_DESC,
        "description": COL_DESCRIPTION,
        "focus_kw": COL_FOCUS_KW,
        "seo_title": COL_SEO_TITLE,
        "meta_desc": COL_META_DESC,
    }
    updates = {}
    for key, col_name in mapping.items():
        if col_name in cols and key in result_item:
            updates[col_name] = result_item[key]
    return updates


def has_existing_content(product: Dict[str, str], cols: List[str]) -> bool:
    for col in cols:
        val = product.get(col, "").strip()
        if not val:
            return False
    return True


def process_csv(
    csv_file: Path,
    category_dir: Path,
    cols: List[str],
    config: dict,
    force: bool = False,
    batch_size: int = DEFAULT_BATCH_SIZE,
    rate_limit: float = DEFAULT_RATE_LIMIT,
):
    products = read_csv_products(csv_file)
    if not products:
        print(f"  [Skip] No products in {csv_file.name}")
        return

    fieldnames = extract_fieldnames(csv_file)
    # Ensure output columns exist
    for col in cols:
        if col not in fieldnames:
            fieldnames.append(col)

    # Determine which products need processing
    indices_to_process = []
    for i, p in enumerate(products):
        if force or not has_existing_content(p, cols):
            indices_to_process.append(i)

    total_need = len(indices_to_process)
    if total_need == 0:
        print(f"  [Skip] All {len(products)} products already have content in {csv_file.name}")
        # Still copy to output if not exists
        out_path = OUTPUT_DIR / csv_file.name
        if not out_path.exists():
            write_csv_products(out_path, fieldnames, products)
        return

    print(f"  Processing {csv_file.name}: {len(products)} products, {total_need} need generation")

    prompt_template = load_prompt_template(category_dir)
    variables = load_category_variables(category_dir)
    prompt_template = inject_variables(prompt_template, variables)
    prompt_template = ensure_placeholders(prompt_template)

    # Process in batches
    batch_count = 0
    for batch_start in range(0, len(indices_to_process), batch_size):
        batch_indices = indices_to_process[batch_start:batch_start + batch_size]
        batch_products = [products[i] for i in batch_indices]

        product_list = build_product_list(batch_products)
        output_spec = build_output_spec(cols)
        prompt = prompt_template.replace("{{product_list}}", product_list).replace("{{output_spec}}", output_spec)

        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                results = call_api(prompt, config)
                if len(results) != len(batch_products):
                    print(f"    Warning: API returned {len(results)} items for {len(batch_products)} products. Adjusting...")
                break
            except Exception as e:
                print(f"    API attempt {attempt}/{max_retries} failed: {e}")
                if attempt == max_retries:
                    print(f"    Skipping batch {batch_start // batch_size + 1}")
                    results = []
                else:
                    time.sleep(2 ** attempt)

        # Apply results
        for idx_in_batch, result_item in enumerate(results):
            if idx_in_batch >= len(batch_indices):
                break
            product_idx = batch_indices[idx_in_batch]
            updates = map_result_to_row(result_item, cols)
            for k, v in updates.items():
                products[product_idx][k] = v

        batch_count += 1
        if rate_limit > 0:
            time.sleep(1.0 / rate_limit)

        # Save progress after each batch
        out_path = OUTPUT_DIR / csv_file.name
        write_csv_products(out_path, fieldnames, products)
        processed = min(batch_start + len(batch_indices), total_need)
        print(f"    Progress: {processed}/{total_need} done")

    print(f"  [Done] {csv_file.name}")


def process_category(category_name: str, cols: List[str], config: dict, force: bool = False):
    category_dir = CATEGORIES_DIR / category_name
    if not category_dir.exists():
        print(f"[Error] Category directory not found: {category_dir}")
        return

    csv_files = sorted(category_dir.glob("products-*.csv"))
    if not csv_files:
        print(f"[Warning] No CSV files found in {category_dir}")
        return

    print(f"\n[Category] {category_name} ({len(csv_files)} files)")
    for csv_file in csv_files:
        process_csv(csv_file, category_dir, cols, config, force=force)


def main():
    parser = argparse.ArgumentParser(description="Generate product SEO content via AI API")
    parser.add_argument("--config", action="store_true", help="Configure API settings")
    parser.add_argument("--all", action="store_true", help="Process all categories")
    parser.add_argument("--single", type=str, help="Process single category by name or number (1-7)")
    parser.add_argument("--cols", nargs="+", choices=list(COL_ALIASES.keys()), help="Columns to generate")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing content")
    parser.add_argument("--batch-size", type=int, default=int(os.getenv("AI_BATCH_SIZE", DEFAULT_BATCH_SIZE)))
    parser.add_argument("--rate-limit", type=float, default=float(os.getenv("AI_RATE_LIMIT", DEFAULT_RATE_LIMIT)))
    args = parser.parse_args()

    if args.config:
        configure_api()
        return

    config = load_config()
    if not config.get("api_key"):
        print("[Error] API key not configured. Run with --config first.")
        sys.exit(1)

    # Resolve columns
    if args.cols:
        cols = [COL_ALIASES[c] for c in args.cols]
    else:
        cols = list(ALL_COLS)

    # Resolve categories
    category_map = {
        "1": "Japanese-Knives",
        "2": "Chinese-Knives",
        "3": "Western-Knives",
        "4": "Cookware",
        "5": "Axes-Outdoor",
        "6": "Accessories",
        "7": "Pocket-Knives",
    }

    categories_to_process = []
    if args.all:
        categories_to_process = sorted([d.name for d in CATEGORIES_DIR.iterdir() if d.is_dir() and d.name != "prompt_base.md"])
    elif args.single:
        single = category_map.get(args.single, args.single)
        categories_to_process = [single]
    else:
        # Default: process all
        categories_to_process = sorted([d.name for d in CATEGORIES_DIR.iterdir() if d.is_dir() and d.name != "prompt_base.md"])

    print(f"\n=== SEO Content Generator ===")
    print(f"API URL: {config.get('api_url', DEFAULT_API_URL)}")
    print(f"Model: {config.get('model', DEFAULT_MODEL)}")
    print(f"Columns: {cols}")
    print(f"Categories: {categories_to_process}")
    print(f"Batch size: {args.batch_size}")
    print("")

    for cat in categories_to_process:
        process_category(cat, cols, config, force=args.force)

    print("\n=== All done ===")


if __name__ == "__main__":
    main()
