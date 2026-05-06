#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ahrefs API v3 - all-backlinks 诊断工具
分析用户提供的 URL 并测试调用
"""

import json
import os
import sys
from urllib.parse import parse_qs, unquote, urlparse

import requests

# ========== 请在此处填入你的 API Token ==========
AHREFS_API_TOKEN = ""
# ==============================================


def get_token():
    token = os.environ.get("AHREFS_API_TOKEN", AHREFS_API_TOKEN).strip()
    if not token:
        return None
    return token


def analyze_url(url):
    """静态分析 URL 参数，列出潜在问题"""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    print("=" * 60)
    print("URL 静态分析")
    print("=" * 60)
    print(f"端点: {parsed.path}")
    print(f"目标 (target): {params.get('target', ['未设置'])[0]}")
    print("-" * 60)

    issues = []
    warnings = []

    target = params.get("target", [""])[0]
    if target.endswith("/"):
        issues.append(f"target 末尾带了斜杠: '{target}' -> 建议改为 '{target.rstrip('/')}'")

    if "mode" not in params:
        warnings.append("缺少 mode 参数 (domain/subdomains/exact)，部分端点可能默认 domain")

    history = params.get("history", [""])[0]
    if history.startswith("since:"):
        warnings.append(
            f"history='{history}' - 'since:' 语法在 v3 部分端点中有效，"
            "但 all-backlinks 通常建议用 'live'/'active'/'lost' 或纯日期 'YYYY-MM-DD'"
        )

    select_fields = params.get("select", [""])[0].split(",")
    known_backlinks_fields = {
        "url_from", "url_to", "anchor", "title", "is_dofollow", "is_nofollow",
        "is_ugc", "is_sponsored", "is_content", "domain_rating_source",
        "url_rating_source", "traffic_domain", "refdomains_source",
        "linked_domains_source_page", "links_external", "page_type_source",
        "page_category_source", "first_seen_link", "last_seen", "lost_reason",
        "drop_reason", "http_code", "discovered_status", "snippet_left",
        "snippet_right", "language", "link_type", "redirect_code", "redirect_kind",
        "url_redirect", "last_visited", "is_root_source", "is_spam",
        "root_name_source", "traffic", "positions", "js_crawl", "http_crawl",
        "broken_redirect_source", "broken_redirect_new_target", "broken_redirect_reason",
        "link_group_count", "languages", "powered_by", "source_page_author",
    }

    unknown_fields = [f for f in select_fields if f and f not in known_backlinks_fields]
    if unknown_fields:
        warnings.append(f"select 中可能存在不支持的字段: {unknown_fields}")

    order_by = params.get("order_by", [""])[0]
    if "traffic:desc" in order_by:
        warnings.append(
            "order_by 包含 'traffic:desc' - 'traffic' 在 backlinks 端点中通常指来源页流量，"
            "排序字段建议用 'domain_rating_source' 或 'url_rating_source'"
        )

    limit = params.get("limit", [""])[0]
    if limit and int(limit) > 1000:
        issues.append(f"limit={limit} 超过最大允许值 1000")

    if issues:
        print("\n[严重问题]")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")

    if warnings:
        print("\n[警告/建议]")
        for i, warn in enumerate(warnings, 1):
            print(f"  {i}. {warn}")

    if not issues and not warnings:
        print("未检测到明显问题")

    print("=" * 60)
    return issues, warnings


def build_fixed_url(original_url):
    """基于分析结果生成一个修正后的简化 URL"""
    parsed = urlparse(original_url)
    params = parse_qs(parsed.query, keep_blank_values=True)

    # 修复 target
    if "target" in params:
        target = params["target"][0].rstrip("/")
        params["target"] = [target]

    # 简化 select 字段，只保留最常见且确认存在的字段
    safe_fields = [
        "url_from", "url_to", "anchor", "title",
        "domain_rating_source", "url_rating_source",
        "is_dofollow", "is_nofollow", "first_seen_link", "last_seen"
    ]
    params["select"] = [",".join(safe_fields)]

    # 简化 order_by
    params["order_by"] = ["domain_rating_source:desc"]

    # 去掉有问题的 history 或改为 live
    if "history" in params:
        history_val = params["history"][0]
        if history_val.startswith("since:"):
            params["history"] = ["live"]

    # 添加 mode 如果缺失
    if "mode" not in params:
        params["mode"] = ["domain"]

    # 重建查询字符串
    from urllib.parse import urlencode
    query = urlencode(params, doseq=True)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{query}"


def call_api(url, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    print("\n正在发送请求...")
    print(f"URL: {url[:120]}...")
    print(f"Headers: Authorization: Bearer {token[:8]}...")
    print("-" * 60)

    try:
        resp = requests.get(url, headers=headers, timeout=30)
        print(f"状态码: {resp.status_code}")

        if resp.status_code == 200:
            data = resp.json()
            print("请求成功！")
            if isinstance(data, dict):
                keys = list(data.keys())
                print(f"返回顶层字段: {keys}")
                if "backlinks" in data and isinstance(data["backlinks"], list):
                    print(f"外链数量: {len(data['backlinks'])}")
                    if data["backlinks"]:
                        print("第一条数据示例:")
                        print(json.dumps(data["backlinks"][0], indent=2, ensure_ascii=False)[:800])
            return True, data
        else:
            print(f"\n请求失败 - 状态码 {resp.status_code}")
            print("-" * 60)
            if resp.status_code == 401:
                print("诊断: Token 无效或已过期")
            elif resp.status_code == 403:
                print("诊断: 权限不足 - 当前套餐可能不支持该端点或 API units 已用完")
            elif resp.status_code == 400:
                print("诊断: 参数错误 - 请检查 select/order_by/history 字段是否正确")
            elif resp.status_code == 429:
                print("诊断: 请求过于频繁，触发速率限制")
            elif resp.status_code == 404:
                print("诊断: 端点或目标不存在")

            try:
                err = resp.json()
                print(f"\n响应体:\n{json.dumps(err, indent=2, ensure_ascii=False)}")
            except Exception:
                print(f"\n原始响应:\n{resp.text[:1000]}")
            return False, resp.text

    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {e}")
        return False, str(e)


def main():
    # 用户提供的原始 URL
    original_url = (
        "https://api.ahrefs.com/v3/site-explorer/all-backlinks"
        "?aggregation=1_per_domain"
        "&history=since%3A2026-03-25"
        "&limit=50"
        "&order_by=traffic%3Adesc%2Curl_rating_source%3Adesc"
        "&select=url_from%2Clink_group_count%2Ctitle%2Clanguages%2Cpowered_by%2Clink_type"
        "%2Credirect_code%2Cfirst_seen_link%2Clost_reason%2Cdrop_reason%2Chttp_code"
        "%2Cdiscovered_status%2Csource_page_author%2Cis_dofollow%2Cis_nofollow"
        "%2Cis_ugc%2Cis_sponsored%2Cis_content%2Cdomain_rating_source%2Ctraffic_domain"
        "%2Cis_root_source%2Cis_spam%2Croot_name_source%2Ctraffic%2Cpositions"
        "%2Clinked_domains_source_page%2Clinks_external%2Cpage_type_source"
        "%2Cpage_category_source%2Curl_rating_source%2Clast_visited%2Crefdomains_source"
        "%2Csnippet_left%2Canchor%2Csnippet_right%2Curl_to%2Cjs_crawl%2Chttp_crawl"
        "%2Credirect_kind%2Curl_redirect%2Cbroken_redirect_source"
        "%2Cbroken_redirect_new_target%2Cbroken_redirect_reason%2Clast_seen"
        "&target=loadoutroom.com%2F"
    )

    print("\n" + "=" * 60)
    print("Ahrefs API v3 - all-backlinks 诊断工具")
    print("=" * 60)

    # 1. 静态分析
    issues, warnings = analyze_url(original_url)

    # 2. 生成修正版 URL
    fixed_url = build_fixed_url(original_url)
    print("\n[建议的修正版 URL]")
    print(fixed_url)
    print("=" * 60)

    # 3. 尝试调用 API
    token = get_token()
    if not token:
        print("\n未配置 API Token，跳过实际调用测试。")
        print("如需测试，请修改脚本第 16 行的 AHREFS_API_TOKEN 变量")
        print("或设置环境变量: $env:AHREFS_API_TOKEN='your_token'")
        return

    print("\n" + "=" * 60)
    print("测试 A: 使用原始 URL")
    print("=" * 60)
    call_api(unquote(original_url), token)

    print("\n" + "=" * 60)
    print("测试 B: 使用修正版 URL")
    print("=" * 60)
    success, data = call_api(fixed_url, token)

    if success:
        print("\n修正版 URL 调用成功！建议在生产环境中使用修正版参数。")
    else:
        print("\n修正版 URL 也失败了。请检查 Token 权限和套餐限制。")


if __name__ == "__main__":
    main()
