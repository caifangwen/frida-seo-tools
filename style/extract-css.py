#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Huahao Blog CSS Extractor
提取纯净 CSS - 无注释 - 用于 WordPress Additional CSS
同时提取使用注释到 txt 文件
"""

import re
import os

def extract_css(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'<style>\n(.*?)\n</style>\n\n<!--', content, re.DOTALL)
    return match.group(1) if match else None

def extract_usage_notes(css):
    """提取CSS中的使用注释（所有注释）"""
    # 按注释块分割
    comment_blocks = re.findall(r'/\*(.*?)\*/', css, re.DOTALL)

    notes = []
    for block in comment_blocks:
        # 查找包含 § 的注释块
        section_match = re.search(r'§\s*(\d+[A-Z]?)\s+(.*?)(?:\n|$)', block)
        if not section_match:
            continue

        section_num = section_match.group(1).strip()
        section_name = section_match.group(2).strip()

        # 提取注释块中的所有内容（去除分隔线和section标题行）
        # 移除分隔线
        content = re.sub(r'╌+|═+|─+', '', block)
        # 移除section标题行
        content = re.sub(r'§\s*\d+[A-Z]?\s+.*?\n', '', content, count=1)
        # 清理前后空白
        content = content.strip()

        notes.append({
            'num': section_num,
            'name': section_name,
            'usage': content if content else 'No usage notes'
        })

    return notes

def format_usage_notes(notes):
    """格式化使用注释为文本"""
    lines = []
    lines.append('═' * 70)
    lines.append('  HUAHAO BLOG COMPONENTS - USAGE GUIDE')
    lines.append('═' * 70)
    lines.append('')

    for note in notes:
        lines.append(f"§ {note['num']}  {note['name']}")
        # 直接使用提取的完整内容
        lines.append(f"   {note['usage']}")
        lines.append('-' * 70)

    return '\n'.join(lines)

def clean_css(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    css = css.replace('═', '').replace('─', '').replace('§', '').replace('…', '...')
    css = css.replace('—', '-').replace('→', '->').replace('«', '"').replace('»', '"')

    lines = [line.rstrip() for line in css.split('\n')
             if line.strip() and not line.strip().startswith('/*')]

    result = []
    for line in lines:
        if line.strip() or (result and result[-1].strip()):
            result.append(line)

    return '\n'.join(result)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_file = os.path.join(script_dir, 'huahao-blog-components.html')
    css_file = os.path.join(script_dir, 'huahao.css')
    usage_file = os.path.join(script_dir, 'huahao-usage.txt')

    css = extract_css(html_file)
    if not css:
        print('Error: Cannot extract CSS')
        return

    # 提取使用注释
    usage_notes = extract_usage_notes(css)
    usage_text = format_usage_notes(usage_notes)
    
    with open(usage_file, 'w', encoding='utf-8') as f:
        f.write(usage_text)
    
    # 清理CSS
    css = clean_css(css)

    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css)

    try:
        import pyperclip
        pyperclip.copy(css)
        print(f'Done! CSS: {len(css):,} chars - Copied to clipboard!')
        print(f'Usage notes: {len(usage_notes)} components - Saved to {usage_file}')
    except:
        print(f'Done! CSS saved to {css_file}')
        print(f'Usage notes saved to {usage_file}')

if __name__ == '__main__':
    main()
