#!/usr/bin/env python3
"""
图片下载脚本 - 用于 SEO 文章
支持从 JSON/CSV 表格批量下载图片

使用方法:
    # 从 JSON 文件批量下载 (推荐)
    python download_images.py --json welding-procedure-specifications-wps-guide-images-list.json --output output/images/

    # 从 CSV 文件批量下载
    python download_images.py --csv welding-procedure-specifications-wps-guide-images-list.csv --output output/images/

    # 单个关键词下载
    python download_images.py --query "关键词" --output output/images/ --count 5

依赖:
    pip install requests Pillow
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

try:
    import requests
    from PIL import Image
    from io import BytesIO
except ImportError as e:
    print(f"缺少依赖：{e}")
    print("请运行：pip install requests Pillow")
    sys.exit(1)


# 图片源 API
IMAGE_SOURCES = {
    "pixabay": {
        "api_url": "https://pixabay.com/api/",
        "api_key": os.environ.get("PIXABAY_API_KEY", ""),
        "enabled": False
    },
    "pexels": {
        "api_url": "https://api.pexels.com/v1/search",
        "api_key": os.environ.get("PEXELS_API_KEY", "iOEv6IqHxu2y142yY0GB1hUa6oW9TIijjUtovDw5PAfOyDmpPhhInfpr"),
        "enabled": True
    },
    "unsplash": {
        "api_url": "https://api.unsplash.com/search/photos",
        "api_key": os.environ.get("UNSPLASH_ACCESS_KEY", ""),
        "enabled": False
    }
}


def sanitize_filename(text):
    """将文本转换为安全的文件名"""
    text = re.sub(r'[^\w\s\u4e00-\u9fff\-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-').lower()


def get_image_size(size_name):
    """获取图片尺寸配置"""
    sizes = {
        'small': {'width': 640, 'height': 480},
        'medium': {'width': 1280, 'height': 720},
        'large': {'width': 1920, 'height': 1080},
        'xlarge': {'width': 2560, 'height': 1440},
    }
    return sizes.get(size_name, sizes['medium'])


def download_from_source(source_name, query, count, size, output_path):
    """通用图片下载函数，支持多个图片源"""
    source = IMAGE_SOURCES.get(source_name)
    if not source or not source["enabled"] or not source["api_key"]:
        return []

    # 简化搜索关键词，提高 API 成功率
    simple_query = simplify_search_keywords(query)
    print(f"  正在使用 {source_name.capitalize()} API 搜索：{simple_query}")

    size_config = get_image_size(size)
    downloaded = []

    headers = {}
    params = {}

    if source_name == "pixabay":
        params = {
            'key': source["api_key"],
            'q': simple_query,
            'image_type': 'photo',
            'per_page': min(count, 40),
            'min_width': size_config['width'],
            'min_height': size_config['height'],
        }
    elif source_name == "pexels":
        headers = {'Authorization': source["api_key"]}
        params = {'query': simple_query, 'per_page': count}
    elif source_name == "unsplash":
        headers = {'Authorization': f'Bearer {source["api_key"]}'}
        params = {'query': simple_query, 'per_page': min(count, 30), 'orientation': 'landscape'}

    try:
        response = requests.get(source["api_url"], headers=headers, params=params, timeout=30)
        response.raise_for_status()

        if source_name == "pixabay":
            results = response.json().get('hits', [])
        elif source_name == "pexels":
            results = response.json().get('photos', [])
        elif source_name == "unsplash":
            results = response.json().get('results', [])

        if not results:
            print(f"  未找到相关图片")
            return downloaded

        for i, item in enumerate(results[:count]):
            try:
                # 获取图片 URL
                if source_name == "pixabay":
                    image_url = item['largeImageURL']
                elif source_name == "pexels":
                    image_url = item['src']['large']
                elif source_name == "unsplash":
                    image_url = item['urls']['regular']

                img_response = requests.get(image_url, timeout=30)
                img_response.raise_for_status()

                img = Image.open(BytesIO(img_response.content))
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')

                # 根据文件扩展名决定保存格式
                ext = Path(output_path).suffix.lower()
                if ext == '.webp':
                    img.save(output_path, 'WEBP', quality=85, method=6)
                else:
                    img.save(output_path, 'JPEG', quality=90, optimize=True)

                downloaded.append(output_path)
                print(f"  ✓ 已保存：{os.path.basename(output_path)} ({os.path.getsize(output_path) // 1024}KB)")
                break  # 成功下载一张后退出

            except Exception as e:
                print(f"  ✗ 下载失败：{e}")
                continue

    except Exception as e:
        print(f"  {source_name.capitalize()} API 请求失败：{e}")

    return downloaded


def simplify_search_keywords(query):
    """简化搜索关键词，提高 API 成功率"""
    # 移除专业术语和标准编号，保留核心视觉词汇
    remove_patterns = [
        r'\bASME\b', r'\bAWS\b', r'\bAPI\b', r'\bISO\b', r'\bNACE\b',
        r'\bSection\s*IX\b', r'\bB31\.3\b', r'\bD1\.1\b',
        r'\bWPS\b', r'\bPQR\b', r'\bWPQ\b',
        r'\bP-Number\b', r'\bF-Number\b',
    ]
    result = query
    for pattern in remove_patterns:
        result = re.sub(pattern, '', result, flags=re.IGNORECASE)
    # 清理多余空格
    result = re.sub(r'\s+', ' ', result).strip()
    # 如果结果为空，返回原始查询
    return result if result else query


def download_single_image(query, output_path, size='medium'):
    """
    下载单张图片，自动尝试多个图片源

    参数:
        query: 搜索关键词
        output_path: 输出文件路径（包含文件名）
        size: 图片尺寸
    """
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # 按优先级尝试多个图片源
    for source_name in ["pixabay", "pexels", "unsplash"]:
        downloaded = download_from_source(source_name, query, 1, size, output_path)
        if downloaded:
            return True

    return False


def download_from_json(json_path, output_base_dir, size='medium', skip_existing=True):
    """
    从 JSON 文件批量下载图片

    参数:
        json_path: JSON 文件路径
        output_base_dir: 输出基础目录
        size: 图片尺寸
        skip_existing: 是否跳过已存在的文件
    """
    json_path = Path(json_path)
    output_base = Path(output_base_dir)

    if not json_path.exists():
        print(f"错误：JSON 文件不存在：{json_path}")
        return []

    # 读取 JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    article_name = data.get('article', 'unknown')
    images = data.get('images', [])

    print(f"\n{'='*60}")
    print(f"SEO 文章图片批量下载器 (JSON 模式)")
    print(f"{'='*60}")
    print(f"文章：{article_name}")
    print(f"JSON 文件：{json_path}")
    print(f"输出目录：{output_base.absolute()}")
    print(f"图片尺寸：{size}")
    print(f"待下载数量：{len(images)}")
    print(f"{'='*60}\n")

    results = []
    success_count = 0
    skip_count = 0
    fail_count = 0

    for i, img in enumerate(images, 1):
        # 从 JSON 读取字段
        seq = img.get('no', i)
        filename = img.get('filename', '')
        search_keywords = img.get('search_keywords', [])
        alt_text = img.get('alt_text', '')
        position = img.get('position', '')
        purpose = img.get('purpose', '')

        # 合并搜索关键词
        search_keyword = ' '.join(search_keywords) if isinstance(search_keywords, list) else search_keywords

        if not filename or not search_keyword:
            print(f"[{i}/{len(images)}] ✗ 跳过：缺少文件名或搜索关键词")
            fail_count += 1
            continue

        # 构建输出路径
        output_path = output_base / filename

        print(f"\n[{i}/{len(images)}] 序号：{seq}")
        print(f"  用途：{purpose}")
        print(f"  位置：{position}")
        print(f"  关键词：{search_keyword}")
        print(f"  输出：{output_path}")

        # 检查是否已存在
        if skip_existing and output_path.exists():
            print(f"  ⊘ 已存在，跳过")
            skip_count += 1
            results.append({
                'image': img,
                'status': 'skipped',
                'path': str(output_path)
            })
            continue

        # 下载图片
        success = download_single_image(
            query=search_keyword,
            output_path=str(output_path),
            size=size
        )

        if success:
            print(f"  ✓ 下载成功")
            success_count += 1
            results.append({
                'image': img,
                'status': 'success',
                'path': str(output_path)
            })
        else:
            print(f"  ✗ 下载失败")
            fail_count += 1
            results.append({
                'image': img,
                'status': 'failed',
                'path': str(output_path)
            })

    # 打印汇总
    print(f"\n{'='*60}")
    print(f"下载完成！")
    print(f"{'='*60}")
    print(f"总计：{len(images)} | 成功：{success_count} | 跳过：{skip_count} | 失败：{fail_count}")
    print(f"{'='*60}\n")

    # 生成 Markdown 引用代码
    if success_count > 0:
        print("Markdown 引用代码:")
        print("```markdown")
        for r in results:
            if r['status'] == 'success':
                img = r['image']
                filename = img.get('filename', '')
                alt_text = img.get('alt_text', '')
                print(f"![{alt_text}]({filename})")
        print("```")
        print()

    return results


def download_from_csv(csv_path, output_base_dir, size='medium', skip_existing=True):
    """
    从 CSV 文件批量下载图片

    参数:
        csv_path: CSV 文件路径
        output_base_dir: 输出基础目录
        size: 图片尺寸
        skip_existing: 是否跳过已存在的文件
    """
    csv_path = Path(csv_path)
    output_base = Path(output_base_dir)

    if not csv_path.exists():
        print(f"错误：CSV 文件不存在：{csv_path}")
        return []

    # 读取 CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"\n{'='*60}")
    print(f"SEO 文章图片批量下载器 (CSV 模式)")
    print(f"{'='*60}")
    print(f"CSV 文件：{csv_path}")
    print(f"输出目录：{output_base.absolute()}")
    print(f"图片尺寸：{size}")
    print(f"待下载数量：{len(rows)}")
    print(f"{'='*60}\n")

    results = []
    success_count = 0
    skip_count = 0
    fail_count = 0

    for i, row in enumerate(rows, 1):
        # 从 CSV 读取字段
        seq = row.get('序号', i)
        filename = row.get('文件名', '')
        search_keyword = row.get('搜索关键词', '')
        alt_text = row.get('Alt 文本', '')
        position = row.get('位置', '')
        purpose = row.get('用途', '')

        if not filename or not search_keyword:
            print(f"[{i}/{len(rows)}] ✗ 跳过：缺少文件名或搜索关键词")
            fail_count += 1
            continue

        # 构建输出路径
        output_path = output_base / filename
        
        print(f"\n[{i}/{len(rows)}] 序号：{seq}")
        print(f"  用途：{purpose}")
        print(f"  位置：{position}")
        print(f"  关键词：{search_keyword}")
        print(f"  输出：{output_path}")

        # 检查是否已存在
        if skip_existing and output_path.exists():
            print(f"  ⊘ 已存在，跳过")
            skip_count += 1
            results.append({
                'row': row,
                'status': 'skipped',
                'path': str(output_path)
            })
            continue

        # 下载图片
        success = download_single_image(
            query=search_keyword,
            output_path=str(output_path),
            size=size
        )

        if success:
            print(f"  ✓ 下载成功")
            success_count += 1
            results.append({
                'row': row,
                'status': 'success',
                'path': str(output_path)
            })
        else:
            print(f"  ✗ 下载失败")
            fail_count += 1
            results.append({
                'row': row,
                'status': 'failed',
                'path': str(output_path)
            })

    # 打印汇总
    print(f"\n{'='*60}")
    print(f"下载完成！")
    print(f"{'='*60}")
    print(f"总计：{len(rows)} | 成功：{success_count} | 跳过：{skip_count} | 失败：{fail_count}")
    print(f"{'='*60}\n")

    # 生成 Markdown 引用代码
    if success_count > 0:
        print("Markdown 引用代码:")
        print("```markdown")
        for r in results:
            if r['status'] == 'success':
                row = r['row']
                filename = row.get('文件名', '')
                alt_text = row.get('Alt 文本', '')
                print(f"![{alt_text}]({filename})")
        print("```")
        print()

    return results


def download_images(query, output_dir, count=5, size='medium'):
    """
    下载单个或多个图片（非 CSV/JSON 模式）
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*50}")
    print(f"SEO 文章图片下载器")
    print(f"{'='*50}")
    print(f"关键词：{query}")
    print(f"输出目录：{output_path.absolute()}")
    print(f"数量：{count}")
    print(f"尺寸：{size}")
    print(f"{'='*50}\n")

    downloaded = []

    for i in range(count):
        filename = f"{sanitize_filename(query)}-{i + 1}.jpg"
        filepath = output_path / filename
        success = download_single_image(query, str(filepath), size)
        if success:
            downloaded.append(filename)

    print(f"\n{'='*50}")
    print(f"下载完成！成功：{len(downloaded)}/{count}")
    print(f"{'='*50}\n")

    if downloaded:
        print("已下载的文件:")
        for f in downloaded:
            print(f"  - {f}")

    return downloaded


def main():
    parser = argparse.ArgumentParser(
        description='下载 SEO 文章相关的免版税图片',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从 JSON 文件批量下载（推荐）
  python download_images.py --json welding-procedure-specifications-wps-guide-images-list.json --output output/images/

  # 从 CSV 文件批量下载
  python download_images.py --csv welding-procedure-specifications-wps-guide-images-list.csv --output output/images/

  # 从 CSV 下载，使用大尺寸
  python download_images.py --csv images.csv --output output/images/ --size large

  # 单个关键词下载
  python download_images.py --query "knife blade close-up" --output output/images/cpm20cv/

  # 下载多个
  python download_images.py --query "chef knife professional" --output output/images/kitchen/ --count 8

CSV 文件格式:
  序号，位置，用途，Alt 文本，文件名，上传路径，搜索关键词
  1,[章节后],开篇主题图，industrial welding...,wps-document.webp,/wp-content/...,welding procedure WPS

JSON 文件格式:
  {
    "article": "article-name",
    "images": [
      {
        "no": 1,
        "position": "After section",
        "purpose": "Description",
        "alt_text": "Alt text",
        "filename": "image.webp",
        "upload_path": "/wp-content/uploads/...",
        "search_keywords": ["keyword1", "keyword2"]
      }
    ]
  }

需要 API 密钥（至少设置一个）:
  - Pixabay: https://pixabay.com/api/docs/
  - Pexels: https://www.pexels.com/api/
  - Unsplash: https://unsplash.com/developers

设置方法:
  export PIXABAY_API_KEY="your_key_here"
  export PEXELS_API_KEY="your_key_here"
        """
    )

    # JSON 模式参数
    parser.add_argument(
        '--json',
        help='JSON 文件路径（包含图片下载参数）'
    )

    # CSV 模式参数
    parser.add_argument(
        '--csv',
        help='CSV 文件路径（包含图片下载参数）'
    )

    # 单图模式参数
    parser.add_argument(
        '--query', '-q',
        help='搜索关键词（中文或英文）'
    )

    parser.add_argument(
        '--output', '-o',
        default='output/images',
        help='输出目录（默认：output/images/）'
    )

    parser.add_argument(
        '--count', '-c',
        type=int,
        default=5,
        help='下载数量（默认：5，最大：20）'
    )

    parser.add_argument(
        '--size', '-s',
        choices=['small', 'medium', 'large', 'xlarge'],
        default='medium',
        help='图片尺寸（默认：medium）'
    )

    parser.add_argument(
        '--skip-existing',
        action='store_true',
        default=True,
        help='跳过已存在的文件（默认开启）'
    )

    parser.add_argument(
        '--no-skip-existing',
        action='store_false',
        dest='skip_existing',
        help='不跳过已存在的文件'
    )

    args = parser.parse_args()

    # 验证参数
    if not args.json and not args.csv and not args.query:
        parser.error("必须指定 --json、--csv 或 --query 参数")

    if sum(bool(x) for x in [args.json, args.csv, args.query]) > 1:
        parser.error("--json、--csv 和 --query 不能同时使用")

    # 执行下载
    if args.json:
        download_from_json(
            json_path=args.json,
            output_base_dir=args.output,
            size=args.size,
            skip_existing=args.skip_existing
        )
    elif args.csv:
        download_from_csv(
            csv_path=args.csv,
            output_base_dir=args.output,
            size=args.size,
            skip_existing=args.skip_existing
        )
    else:
        if args.count > 20:
            print("警告：数量限制为 20")
            args.count = 20

        download_images(
            query=args.query,
            output_dir=args.output,
            count=args.count,
            size=args.size
        )


if __name__ == '__main__':
    main()
