#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量获取外链权威度（Domain Rating / URL Rating）
调用 Ahrefs API v3

用法:
    python ahrefs_authority_checker.py --input urls.txt --output results.csv
    python ahrefs_authority_checker.py --urls example.com google.com --output results.csv

环境变量:
    AHREFS_API_TOKEN - Ahrefs API Token（必须）
"""

import argparse
import csv
import os
import sys
import time
from urllib.parse import quote

import requests

# ======================== 用户配置区域 ========================
# 方式1：直接在此处填写你的 Ahrefs API Token
AHREFS_API_TOKEN = "hnU0gd8bikSWyv1oeIQe1T9ZJJ1U3uWF0o8KyNMC"

# 方式2：通过环境变量 AHREFS_API_TOKEN 传入（优先级高于上方硬编码）
# ==============================================================

AHREFS_API_BASE = "https://apiv3.ahrefs.com"
DEFAULT_RATE_LIMIT_DELAY = 0.5  # 请求间隔（秒）


def get_api_token():
    """获取 API Token，优先环境变量，其次硬编码"""
    token = os.environ.get("https://api.ahrefs.com/v3/site-explorer/all-backlinks?aggregation=1_per_domain&history=since%3A2026-03-25&limit=50&order_by=traffic%3Adesc%2Curl_rating_source%3Adesc&select=url_from%2Clink_group_count%2Ctitle%2Clanguages%2Cpowered_by%2Clink_type%2Credirect_code%2Cfirst_seen_link%2Clost_reason%2Cdrop_reason%2Chttp_code%2Cdiscovered_status%2Csource_page_author%2Cis_dofollow%2Cis_nofollow%2Cis_ugc%2Cis_sponsored%2Cis_content%2Cdomain_rating_source%2Ctraffic_domain%2Cis_root_source%2Cis_spam%2Croot_name_source%2Ctraffic%2Cpositions%2Clinked_domains_source_page%2Clinks_external%2Cpage_type_source%2Cpage_category_source%2Curl_rating_source%2Clast_visited%2Crefdomains_source%2Csnippet_left%2Canchor%2Csnippet_right%2Curl_to%2Cjs_crawl%2Chttp_crawl%2Credirect_kind%2Curl_redirect%2Cbroken_redirect_source%2Cbroken_redirect_new_target%2Cbroken_redirect_reason%2Clast_seen&target=loadoutroom.com%2F", AHREFS_API_TOKEN).strip()
    if not token:
        print("错误: 请设置 Ahrefs API Token")
        print("方式1: 修改脚本第 22 行，将 AHREFS_API_TOKEN = \"\" 改为你的 Token")
        print("方式2: 设置环境变量 AHREFS_API_TOKEN='your_api_token_here'")
        sys.exit(1)
    return token


def get_headers(token):
    """生成请求头"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def get_domain_rating(token, target, mode="domain"):
    """
    获取 Domain Rating (DR)
    
    参数:
        token: Ahrefs API Token
        target: 目标域名或 URL
        mode: 'domain' 或 'subdomains' 或 'exact'
    
    返回:
        dict: 包含 dr, ahrefs_rank, backlinks, ref_domains 等字段
        None: 请求失败
    """
    encoded_target = quote(target, safe="")
    url = f"{AHREFS_API_BASE}/v3/site-explorer/domain-rating"
    params = {
        "target": target,
        "mode": mode,
    }

    try:
        response = requests.get(url, headers=get_headers(token), params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if "domain_rating" in data:
            return {
                "target": target,
                "domain_rating": data["domain_rating"].get("dr", 0),
                "ahrefs_rank": data["domain_rating"].get("ahrefs_rank", 0),
                "backlinks": data["domain_rating"].get("backlinks", 0),
                "ref_domains": data["domain_rating"].get("ref_domains", 0),
                "status": "success",
            }
        else:
            return {
                "target": target,
                "domain_rating": None,
                "ahrefs_rank": None,
                "backlinks": None,
                "ref_domains": None,
                "status": "no_data",
            }

    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP {e.response.status_code}"
        try:
            err_data = e.response.json()
            if "error" in err_data:
                error_msg = f"{error_msg} - {err_data['error']}"
        except Exception:
            pass
        return {
            "target": target,
            "domain_rating": None,
            "ahrefs_rank": None,
            "backlinks": None,
            "ref_domains": None,
            "status": f"error: {error_msg}",
        }
    except requests.exceptions.RequestException as e:
        return {
            "target": target,
            "domain_rating": None,
            "ahrefs_rank": None,
            "backlinks": None,
            "ref_domains": None,
            "status": f"error: {str(e)}",
        }


def get_url_rating(token, target):
    """
    获取 URL Rating (UR) - 通过 overview 端点
    
    参数:
        token: Ahrefs API Token
        target: 目标 URL
    
    返回:
        dict: 包含 ur, dr, backlinks, ref_domains 等字段
        None: 请求失败
    """
    url = f"{AHREFS_API_BASE}/v3/site-explorer/overview"
    params = {
        "target": target,
        "mode": "exact",
    }

    try:
        response = requests.get(url, headers=get_headers(token), params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if "metrics" in data:
            metrics = data["metrics"]
            return {
                "target": target,
                "url_rating": metrics.get("ur", 0),
                "domain_rating": metrics.get("dr", 0),
                "backlinks": metrics.get("backlinks", 0),
                "ref_domains": metrics.get("ref_domains", 0),
                "organic_traffic": metrics.get("organic_traffic", 0),
                "organic_keywords": metrics.get("organic_keywords", 0),
                "status": "success",
            }
        else:
            return {
                "target": target,
                "url_rating": None,
                "domain_rating": None,
                "backlinks": None,
                "ref_domains": None,
                "organic_traffic": None,
                "organic_keywords": None,
                "status": "no_data",
            }

    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP {e.response.status_code}"
        try:
            err_data = e.response.json()
            if "error" in err_data:
                error_msg = f"{error_msg} - {err_data['error']}"
        except Exception:
            pass
        return {
            "target": target,
            "url_rating": None,
            "domain_rating": None,
            "backlinks": None,
            "ref_domains": None,
            "organic_traffic": None,
            "organic_keywords": None,
            "status": f"error: {error_msg}",
        }
    except requests.exceptions.RequestException as e:
        return {
            "target": target,
            "url_rating": None,
            "domain_rating": None,
            "backlinks": None,
            "ref_domains": None,
            "organic_traffic": None,
            "organic_keywords": None,
            "status": f"error: {str(e)}",
        }


def batch_check(targets, output_file=None, check_type="domain", mode="domain", delay=DEFAULT_RATE_LIMIT_DELAY):
    """
    批量查询权威度
    
    参数:
        targets: 目标列表（域名或 URL）
        output_file: 输出 CSV 文件路径，None 则只打印到控制台
        check_type: 'domain' 查 DR, 'url' 查 UR
        mode: 'domain' / 'subdomains' / 'exact'（仅对 domain 类型有效）
        delay: 请求间隔秒数
    """
    token = get_api_token()
    results = []

    print(f"开始批量查询，共 {len(targets)} 个目标，类型: {check_type}")
    print("-" * 70)

    for idx, target in enumerate(targets, 1):
        target = target.strip()
        if not target:
            continue

        print(f"[{idx}/{len(targets)}] 查询: {target} ...", end=" ", flush=True)

        if check_type == "url":
            result = get_url_rating(token, target)
            if result["status"] == "success":
                print(f"UR={result.get('url_rating', 'N/A')} | DR={result.get('domain_rating', 'N/A')}")
            else:
                print(f"失败: {result['status']}")
        else:
            result = get_domain_rating(token, target, mode=mode)
            if result["status"] == "success":
                print(f"DR={result.get('domain_rating', 'N/A')} | AR={result.get('ahrefs_rank', 'N/A')}")
            else:
                print(f"失败: {result['status']}")

        results.append(result)

        # 速率控制：最后一个请求后不 sleep
        if idx < len(targets):
            time.sleep(delay)

    print("-" * 70)
    print(f"查询完成，成功 {sum(1 for r in results if r['status'] == 'success')} / {len(results)}")

    # 输出到 CSV
    if output_file:
        if check_type == "url":
            fieldnames = ["target", "url_rating", "domain_rating", "backlinks", "ref_domains",
                          "organic_traffic", "organic_keywords", "status"]
        else:
            fieldnames = ["target", "domain_rating", "ahrefs_rank", "backlinks", "ref_domains", "status"]

        with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in results:
                # 过滤掉 CSV 中不存在的字段
                clean_row = {k: v for k, v in row.items() if k in fieldnames}
                writer.writerow(clean_row)

        print(f"结果已保存至: {output_file}")

    return results


def read_targets_from_file(filepath):
    """从文件读取目标列表"""
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
        description="批量获取外链权威度（Ahrefs API）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 批量查域名 DR（从文件读取）
  python ahrefs_authority_checker.py -i domains.txt -o results.csv

  # 直接命令行传入域名
  python ahrefs_authority_checker.py --urls example.com google.com github.com

  # 批量查 URL 的 UR
  python ahrefs_authority_checker.py -i urls.txt --type url -o url_results.csv

  # 指定 subdomains 模式并增加请求间隔
  python ahrefs_authority_checker.py -i domains.txt --mode subdomains --delay 1.0
        """,
    )

    parser.add_argument("-i", "--input", help="输入文件路径（每行一个域名/URL）")
    parser.add_argument("-o", "--output", default="ahrefs_results.csv", help="输出 CSV 文件路径（默认: ahrefs_results.csv）")
    parser.add_argument("--urls", nargs="+", help="直接在命令行传入域名/URL 列表")
    parser.add_argument("--type", choices=["domain", "url"], default="domain",
                        help="查询类型: domain=Domain Rating, url=URL Rating（默认: domain）")
    parser.add_argument("--mode", choices=["domain", "subdomains", "exact"], default="domain",
                        help="域名匹配模式（仅对 --type domain 有效，默认: domain）")
    parser.add_argument("--delay", type=float, default=DEFAULT_RATE_LIMIT_DELAY,
                        help=f"请求间隔秒数，防止触发速率限制（默认: {DEFAULT_RATE_LIMIT_DELAY}）")

    args = parser.parse_args()

    # 获取目标列表
    if args.input and args.urls:
        print("错误: 不能同时使用 --input 和 --urls")
        sys.exit(1)
    elif args.input:
        targets = read_targets_from_file(args.input)
    elif args.urls:
        targets = args.urls
    else:
        print("错误: 请提供 --input 文件或 --urls 参数")
        parser.print_help()
        sys.exit(1)

    if not targets:
        print("错误: 目标列表为空")
        sys.exit(1)

    # 执行批量查询
    batch_check(
        targets=targets,
        output_file=args.output,
        check_type=args.type,
        mode=args.mode,
        delay=args.delay,
    )


if __name__ == "__main__":
    main()
