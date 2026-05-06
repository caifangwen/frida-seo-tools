#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量获取外链数据（Backlinks）
调用 Ahrefs API v3 - all-backlinks 端点

用法:
    python ahrefs_backlinks_checker.py -i domains.txt -o backlinks.csv
    python ahrefs_backlinks_checker.py --target loadoutroom.com -o backlinks.csv

环境变量:
    AHREFS_API_TOKEN - Ahrefs API Token（必须）
"""

import argparse
import csv
import json
import os
import sys
import time
from urllib.parse import urlencode

import requests

# ======================== 用户配置区域 ========================
# 方式1：直接在此处填写你的 Ahrefs API Token
AHREFS_API_TOKEN = ""

# 方式2：通过环境变量 AHREFS_API_TOKEN 传入（优先级高于上方硬编码）
# ==============================================================

AHREFS_API_BASE = "https://api.ahrefs.com"
DEFAULT_RATE_LIMIT_DELAY = 0.5

# 安全字段列表（确认在 all-backlinks 端点有效）
SAFE_BACKLINK_FIELDS = [
    "url_from", "url_to", "anchor", "title",
    "domain_rating_source", "url_rating_source",
    "is_dofollow", "is_nofollow", "is_ugc", "is_sponsored",
    "first_seen_link", "last_seen", "lost_reason",
    "traffic_domain", "refdomains_source", "links_external",
    "page_type_source", "link_type", "redirect_code"
]


def get_api_token():
    token = os.environ.get("hnU0gd8bikSWyv1oeIQe1T9ZJJ1U3uWF0o8KyNMC", AHREFS_API_TOKEN).strip()
    if not token:
        print("错误: 请设置 Ahrefs API Token")
        print("方式1: 修改脚本第 25 行，将 AHREFS_API_TOKEN = \"\" 改为你的 Token")
        print("方式2: 设置环境变量 AHREFS_API_TOKEN='your_api_token_here'")
        sys.exit(1)
    return token


def get_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


def fetch_backlinks(token, target, limit=50, mode="domain", aggregation="1_per_domain",
                    history="live", order_by="domain_rating_source:desc",
                    select_fields=None, where=None):
    """
    获取指定目标的外链数据
    
    参数:
        token: API Token
        target: 目标域名或 URL（如 loadoutroom.com）
        limit: 返回条数（默认 50，最大 1000）
        mode: domain / subdomains / exact
        aggregation: 1_per_domain / similar_links
        history: live / active / lost / 或日期 YYYY-MM-DD
        order_by: 排序规则，如 "domain_rating_source:desc"
        select_fields: 要获取的字段列表，None 则使用默认安全字段
        where: 过滤条件 JSON 字符串（高级用法）
    
    返回:
        (success: bool, data: dict/list or error_msg)
    """
    if select_fields is None:
        select_fields = SAFE_BACKLINK_FIELDS

    params = {
        "target": target,
        "mode": mode,
        "limit": min(limit, 1000),
        "select": ",".join(select_fields),
        "order_by": order_by,
    }

    if aggregation:
        params["aggregation"] = aggregation
    if history:
        params["history"] = history
    if where:
        params["where"] = where

    url = f"{AHREFS_API_BASE}/v3/site-explorer/all-backlinks"

    try:
        resp = requests.get(url, headers=get_headers(token), params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return True, data

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        try:
            err_body = e.response.json()
            error_msg = f"HTTP {status}: {json.dumps(err_body, ensure_ascii=False)}"
        except Exception:
            error_msg = f"HTTP {status}: {e.response.text[:500]}"
        return False, error_msg

    except requests.exceptions.RequestException as e:
        return False, f"请求异常: {str(e)}"


def flatten_backlinks(api_response, target):
    """将 API 返回的 backlinks 列表展平为 CSV 行"""
    rows = []
    backlinks = []

    if isinstance(api_response, dict):
        backlinks = api_response.get("backlinks", [])
    elif isinstance(api_response, list):
        backlinks = api_response

    for item in backlinks:
        row = {"target": target}
        # 提取所有字段，不存在的填 None
        for key in SAFE_BACKLINK_FIELDS:
            row[key] = item.get(key, "")
        rows.append(row)

    return rows


def batch_fetch(targets, output_file, limit=50, mode="domain", history="live",
                delay=DEFAULT_RATE_LIMIT_DELAY):
    token = get_api_token()
    all_rows = []
    summary = []

    print(f"开始批量查询外链，共 {len(targets)} 个目标")
    print("-" * 70)

    for idx, target in enumerate(targets, 1):
        target = target.strip().rstrip("/")
        if not target:
            continue

        print(f"[{idx}/{len(targets)}] 查询: {target} ...", end=" ", flush=True)

        success, data = fetch_backlinks(
            token=token,
            target=target,
            limit=limit,
            mode=mode,
            history=history,
        )

        if success:
            backlinks = data.get("backlinks", []) if isinstance(data, dict) else []
            rows = flatten_backlinks(data, target)
            all_rows.extend(rows)
            summary.append({
                "target": target,
                "count": len(backlinks),
                "status": "success"
            })
            print(f"成功，获取 {len(backlinks)} 条外链")
        else:
            summary.append({
                "target": target,
                "count": 0,
                "status": f"error: {str(data)[:60]}"
            })
            print(f"失败: {str(data)[:80]}")

        if idx < len(targets):
            time.sleep(delay)

    print("-" * 70)
    success_count = sum(1 for s in summary if s["status"] == "success")
    print(f"查询完成: 成功 {success_count}/{len(targets)}，共获取 {len(all_rows)} 条外链记录")

    # 输出 CSV
    if all_rows:
        fieldnames = ["target"] + SAFE_BACKLINK_FIELDS
        with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in all_rows:
                writer.writerow(row)
        print(f"结果已保存至: {output_file}")
    else:
        print("未获取到任何外链数据，未生成 CSV")

    # 输出摘要
    summary_file = output_file.replace(".csv", "_summary.csv")
    with open(summary_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["target", "count", "status"])
        writer.writeheader()
        writer.writerows(summary)
    print(f"摘要已保存至: {summary_file}")

    return all_rows


def read_targets_from_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            targets = [line.strip() for line in f if line.strip()]
        return targets
    except FileNotFoundError:
        print(f"错误: 找不到文件 {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"读取文件失败: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="批量获取外链数据（Ahrefs API v3）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 批量查外链（从文件读取域名）
  python ahrefs_backlinks_checker.py -i domains.txt -o backlinks.csv

  # 查单个域名外链
  python ahrefs_backlinks_checker.py --target loadoutroom.com -o out.csv

  # 查 URL 级别精确匹配
  python ahrefs_backlinks_checker.py --target example.com/page --mode exact

  # 查丢失的外链
  python ahrefs_backlinks_checker.py -i domains.txt --history lost
        """,
    )

    parser.add_argument("-i", "--input", help="输入文件路径（每行一个域名）")
    parser.add_argument("-o", "--output", default="backlinks.csv", help="输出 CSV 文件路径（默认: backlinks.csv）")
    parser.add_argument("--target", help="单个目标域名或 URL")
    parser.add_argument("--limit", type=int, default=50, help="每条目标返回的外链数量（默认 50，最大 1000）")
    parser.add_argument("--mode", choices=["domain", "subdomains", "exact"], default="domain",
                        help="匹配模式（默认: domain）")
    parser.add_argument("--history", default="live",
                        help="历史类型: live/active/lost/或日期YYYY-MM-DD（默认: live）")
    parser.add_argument("--delay", type=float, default=DEFAULT_RATE_LIMIT_DELAY,
                        help="请求间隔秒数（默认: 0.5）")

    args = parser.parse_args()

    if args.input and args.target:
        print("错误: 不能同时使用 --input 和 --target")
        sys.exit(1)
    elif args.input:
        targets = read_targets_from_file(args.input)
    elif args.target:
        targets = [args.target]
    else:
        print("错误: 请提供 --input 文件或 --target 参数")
        parser.print_help()
        sys.exit(1)

    batch_fetch(
        targets=targets,
        output_file=args.output,
        limit=args.limit,
        mode=args.mode,
        history=args.history,
        delay=args.delay,
    )


if __name__ == "__main__":
    main()
