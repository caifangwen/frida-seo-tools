#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch runner: processes one CSV file at a time to avoid long-running tasks.
"""
import argparse
import sys
from pathlib import Path
from generate_product_seo import (
    process_csv, load_config, ALL_COLS,
    CATEGORIES_DIR, OUTPUT_DIR
)


def get_pending_files():
    pending = []
    for category_dir in sorted(CATEGORIES_DIR.iterdir()):
        if not category_dir.is_dir() or category_dir.name == "prompt_base.md":
            continue
        for csv_file in sorted(category_dir.glob("products-*.csv")):
            out_path = OUTPUT_DIR / csv_file.name
            if out_path.exists():
                import csv
                in_count = sum(1 for _ in csv.DictReader(open(csv_file, "r", encoding="utf-8-sig", newline="")))
                out_count = sum(1 for _ in csv.DictReader(open(out_path, "r", encoding="utf-8-sig", newline="")))
                if out_count >= in_count:
                    continue
            pending.append((category_dir, csv_file))
    return pending


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--next", action="store_true", help="Process only the next pending file")
    parser.add_argument("--list", action="store_true", help="List pending files")
    args = parser.parse_args()

    pending = get_pending_files()

    if args.list:
        print(f"Pending files: {len(pending)}")
        for cat_dir, csv_file in pending:
            print(f"  {cat_dir.name}/{csv_file.name}")
        return

    if not pending:
        print("All products are already generated!")
        return

    if args.next:
        cat_dir, csv_file = pending[0]
        print(f">>> Processing {cat_dir.name}/{csv_file.name} ...")
        config = load_config()
        process_csv(csv_file, cat_dir, ALL_COLS, config, force=False, batch_size=20, rate_limit=2.0)
        print("[Done]")
    else:
        config = load_config()
        if not config.get("api_key"):
            print("[Error] API key not configured.")
            sys.exit(1)
        print(f"Pending files: {len(pending)}")
        for cat_dir, csv_file in pending:
            print(f"\n>>> Processing {csv_file.name} ...")
            try:
                process_csv(csv_file, cat_dir, ALL_COLS, config, force=False, batch_size=15, rate_limit=1.0)
            except Exception as e:
                print(f"[Error] {csv_file.name}: {e}")
        print("\n=== Batch run complete ===")


if __name__ == "__main__":
    main()
