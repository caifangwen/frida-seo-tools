#!/usr/bin/env python3
"""
批量下载所有 JSON 清单中的图片（包含备用图片）
"""

import json
import os
import sys
from pathlib import Path
from download_images import download_from_json, download_single_image, simplify_search_keywords

# 所有 JSON 清单文件
JSON_FILES = [
    "are-non-woven-bags-eco-friendly-images-list.json",
    "biodegradable-non-woven-bags-images-list.json",
    "custom-logo-non-woven-bags-images-list.json",
    "custom-non-woven-bags-images-list.json",
    "eco-friendly-non-woven-bags-trends-images-list.json",
    "how-to-choose-non-woven-bags-manufacturer-images-list.json",
    "non-woven-bags-wholesale-images-list.json",
    "non-woven-shopping-bags-images-list.json",
    "non-woven-tote-bags-images-list.json",
    "non-woven-vs-plastic-bags-images-list.json",
    "pp-non-woven-bags-images-list.json",
    "what-are-non-woven-bags-images-list.json",
]

def download_backup_images(json_path, output_base_dir, backup_count=2, size='medium'):
    """
    为每个搜索关键词下载备用图片
    
    参数:
        json_path: JSON 文件路径
        output_base_dir: 输出基础目录
        backup_count: 每个关键词的备用图片数量
        size: 图片尺寸
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
    print(f"备用图片下载 - {article_name}")
    print(f"{'='*60}")
    print(f"JSON 文件：{json_path}")
    print(f"输出目录：{output_base.absolute()}")
    print(f"每个关键词备用数量：{backup_count}")
    print(f"{'='*60}\n")
    
    results = []
    success_count = 0
    fail_count = 0
    
    for i, img in enumerate(images, 1):
        seq = img.get('no', i)
        filename = img.get('filename', '')
        search_keywords = img.get('search_keywords', [])
        alt_text = img.get('alt_text', '')
        
        # 合并搜索关键词
        search_keyword = ' '.join(search_keywords) if isinstance(search_keywords, list) else search_keywords
        
        if not filename or not search_keyword:
            continue
        
        # 构建备用图片输出路径
        name_without_ext = Path(filename).stem
        ext = Path(filename).suffix
        
        print(f"\n[{i}/{len(images)}] 为 '{name_without_ext}' 下载 {backup_count} 张备用图片")
        print(f"  关键词：{search_keyword}")
        
        # 为每个关键词下载备用图片
        for j in range(backup_count):
            backup_filename = f"{name_without_ext}-alt-{j+1}{ext}"
            backup_path = output_base / backup_filename
            
            # 检查是否已存在
            if backup_path.exists():
                print(f"  ⊘ 备用 {j+1}: 已存在，跳过")
                continue
            
            # 下载备用图片
            print(f"  正在下载备用 {j+1}: {backup_filename}...")
            success = download_single_image(
                query=search_keyword,
                output_path=str(backup_path),
                size=size
            )
            
            if success:
                print(f"  ✓ 备用 {j+1}: 下载成功")
                success_count += 1
                results.append({
                    'original': img,
                    'backup_no': j + 1,
                    'status': 'success',
                    'path': str(backup_path)
                })
            else:
                print(f"  ✗ 备用 {j+1}: 下载失败")
                fail_count += 1
                results.append({
                    'original': img,
                    'backup_no': j + 1,
                    'status': 'failed',
                    'path': str(backup_path)
                })
    
    # 打印汇总
    print(f"\n{'='*60}")
    print(f"备用图片下载完成！")
    print(f"{'='*60}")
    print(f"成功：{success_count} | 失败：{fail_count}")
    print(f"{'='*60}\n")
    
    return results

def main():
    # 获取当前脚本所在目录
    script_dir = Path(__file__).parent.absolute()
    output_base = script_dir / "output"
    
    print(f"输出目录：{output_base}\n")
    
    # 创建输出目录
    output_base.mkdir(parents=True, exist_ok=True)
    
    total_success = 0
    total_skip = 0
    total_fail = 0
    total_backup_success = 0
    total_backup_fail = 0
    
    for json_file in JSON_FILES:
        json_path = script_dir / json_file
        
        if not json_path.exists():
            print(f"⚠ 文件不存在：{json_file}")
            continue
        
        # 为每个文章创建独立的输出子目录
        article_output_dir = output_base / json_file.replace('-images-list.json', '')
        article_output_dir.mkdir(parents=True, exist_ok=True)
        
        # 下载该文章的所有主图片
        results = download_from_json(
            json_path=json_path,
            output_base_dir=article_output_dir,
            size='medium',
            skip_existing=True
        )
        
        # 统计主图片结果
        for r in results:
            if r['status'] == 'success':
                total_success += 1
            elif r['status'] == 'skipped':
                total_skip += 1
            else:
                total_fail += 1
        
        # 下载备用图片（每个关键词 2 张备用）
        backup_results = download_backup_images(
            json_path=json_path,
            output_base_dir=article_output_dir,
            backup_count=2,
            size='medium'
        )
        
        # 统计备用图片结果
        for r in backup_results:
            if r['status'] == 'success':
                total_backup_success += 1
            else:
                total_backup_fail += 1
    
    # 最终汇总
    print("\n" + "="*60)
    print("所有文章图片下载完成！")
    print("="*60)
    print(f"主图片 - 成功：{total_success} | 跳过：{total_skip} | 失败：{total_fail}")
    print(f"备用图片 - 成功：{total_backup_success} | 失败：{total_backup_fail}")
    print(f"总计 - 成功：{total_success + total_backup_success}")
    print(f"输出目录：{output_base}")
    print("="*60)

if __name__ == '__main__':
    main()
