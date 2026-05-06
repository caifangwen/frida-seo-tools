#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
雷达图生成器 - 从 data 目录的 csv 文件读取数据，自动生成 SVG 雷达图
"""

import csv
import os
import math
from datetime import datetime
from pathlib import Path


def parse_csv_file(file_path):
    """解析 csv 文件，提取维度数据"""
    data = {}
    
    # 尝试不同的编码
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                
                # 检查是否有正确的列名
                if reader.fieldnames is None:
                    continue
                    
                # 自动识别列名（第一列是维度，第二列是得分）
                col_names = [name.strip() for name in reader.fieldnames if name]
                if len(col_names) < 2:
                    continue
                    
                dim_col = col_names[0]
                score_col = col_names[1]
                
                for row in reader:
                    if row.get(dim_col) and row.get(score_col):
                        dimension = row[dim_col].strip()
                        score_str = row[score_col].strip().rstrip(',')
                        if dimension and score_str:
                            try:
                                score = float(score_str)
                                data[dimension] = score
                            except ValueError:
                                continue
                
                if data:  # 如果成功读取了数据
                    return data
                    
        except (UnicodeDecodeError, Exception):
            continue
    
    raise ValueError(f"无法解析文件 {file_path}")


def generate_radar_svg(chart_config, dimensions, data_from_csv=None):
    """生成 SVG 雷达图"""
    title = chart_config['title']

    # 如果提供了从 csv 解析的数据，使用它；否则使用配置中的数据
    if data_from_csv:
        data = data_from_csv
    else:
        data = chart_config['data']

    width = 650
    height = 650
    center_x = width / 2
    center_y = height / 2
    max_radius = 200
    levels = 5  # 雷达图层数

    num_dims = len(dimensions)
    angle_step = (2 * 3.14159265359) / num_dims

    # 开始构建 SVG - 现代简约风格，参考黑色文字、红色强调色系
    svg_parts = []
    svg_parts.append(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="dataGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f44336;stop-opacity:0.25" />
      <stop offset="100%" style="stop-color:#e53935;stop-opacity:0.25" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- 背景 -->
  <rect width="{width}" height="{height}" fill="#ffffff"/>

  <!-- 网格层 - 浅色填充 -->
  <g fill="#fafafa" stroke="#e0e0e0" stroke-width="1">''')

    # 绘制网格层
    import math
    for level in range(1, levels + 1):
        radius = (max_radius / levels) * level
        points = []

        for i in range(num_dims):
            angle = i * angle_step - math.pi / 2
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append(f"{x},{y}")

        points_str = ' '.join(points)
        opacity = 0.3 + (level * 0.1)
        svg_parts.append(f'    <polygon points="{points_str}" fill="#f5f5f5" stroke="#e0e0e0" stroke-width="1" opacity="{opacity}"/>')

    svg_parts.append('  </g>\n\n  <!-- 轴线 -->\n  <g stroke="#bdbdbd" stroke-width="1.5">')

    # 绘制轴线
    for i in range(num_dims):
        angle = i * angle_step - math.pi / 2
        x = center_x + max_radius * math.cos(angle)
        y = center_y + max_radius * math.sin(angle)
        svg_parts.append(f'    <line x1="{center_x}" y1="{center_y}" x2="{x}" y2="{y}"/>')

    svg_parts.append('  </g>\n\n  <!-- 数据区域 -->')

    # 绘制数据
    data_points = []
    label_positions = []

    for i in range(num_dims):
        angle = i * angle_step - math.pi / 2
        dimension = dimensions[i]
        value = data.get(dimension, 0)
        radius = (value / 100) * max_radius

        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        data_points.append(f"{x},{y}")

        # 标签位置（在轴线外侧）
        label_radius = max_radius + 45
        label_x = center_x + label_radius * math.cos(angle)
        label_y = center_y + label_radius * math.sin(angle)
        label_positions.append({'x': label_x, 'y': label_y, 'dimension': dimension, 'angle': angle})

    # 数据填充区域
    data_points_str = ' '.join(data_points)
    svg_parts.append(f'  <polygon points="{data_points_str}" fill="url(#dataGradient)" stroke="#f44336" stroke-width="2.5" filter="url(#glow)"/>')

    # 数据点 - 红色风格
    svg_parts.append('\n  <!-- 数据点 -->\n  <g>')

    for i, point in enumerate(data_points):
        x, y = point.split(',')
        dimension = dimensions[i]
        value = data.get(dimension, 0)
        # 外圈
        svg_parts.append(f'    <circle cx="{x}" cy="{y}" r="6" fill="#ffffff" stroke="#f44336" stroke-width="2.5"/>')
        # 内圈
        svg_parts.append(f'    <circle cx="{x}" cy="{y}" r="3" fill="#f44336"/>')

    svg_parts.append('  </g>\n\n  <!-- 数值标签 -->\n  <g font-size="13" font-weight="bold" fill="#f44336" font-family="Arial, sans-serif">')

    # 添加数值标签 - 放置在数据点上方
    for i in range(num_dims):
        x, y = data_points[i].split(',')
        dimension = dimensions[i]
        value = data.get(dimension, 0)
        # 调整数值标签位置
        angle = i * angle_step - math.pi / 2
        offset_x = math.cos(angle) * 18
        offset_y = math.sin(angle) * 18 - 8
        svg_parts.append(f'    <text x="{float(x) + offset_x}" y="{float(y) + offset_y}" text-anchor="middle">{int(value)}</text>')

    svg_parts.append('  </g>\n\n  <!-- 维度标签 -->\n  <g font-size="13" font-weight="bold" fill="#333333" font-family="Arial, sans-serif">')

    for pos in label_positions:
        x = pos['x']
        y = pos['y']
        dimension = pos['dimension']
        angle = pos['angle']

        # 根据位置调整文本对齐
        if x < center_x - 20:
            text_anchor = 'end'
        elif x > center_x + 20:
            text_anchor = 'start'
        else:
            text_anchor = 'middle'
        
        # 垂直居中对齐
        dy = 0.35  # em单位，使文本垂直居中

        svg_parts.append(f'    <text x="{x}" y="{y}" text-anchor="{text_anchor}" dy="{dy}em">{dimension}</text>')

    # 底部信息 - 图表名称
    svg_parts.append(f'  </g>\n\n  <!-- 底部信息 -->')
    svg_parts.append(f'  <text x="{center_x}" y="{height - 25}" text-anchor="middle" font-size="20" font-weight="bold" fill="#333333" font-family="Arial, sans-serif">{title}</text>\n</svg>')

    return '\n'.join(svg_parts)


def main():
    """主函数"""
    # 获取项目根目录
    base_dir = Path(__file__).parent
    data_dir = base_dir / 'data'
    output_dir = base_dir / 'output'

    # 确保目录存在
    data_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    # 查找所有 csv 文件
    csv_files = list(data_dir.glob('*.csv'))
    
    if not csv_files:
        print("❌ data 目录下没有找到任何 CSV 文件！")
        return

    print(f"找到 {len(csv_files)} 个 CSV 文件\n")
    print('正在生成 SVG 雷达图...\n')

    # 为每个 csv 文件生成雷达图
    for csv_path in csv_files:
        # 从文件名生成输出文件名
        file_stem = csv_path.stem  # 不带扩展名的文件名
        output_filename = f"radar_{file_stem}.svg"
        output_path = output_dir / output_filename

        # 读取 CSV 数据
        data = parse_csv_file(csv_path)
        dimensions = list(data.keys())
        
        if not dimensions:
            print(f"⚠ {csv_path.name} 没有数据，跳过")
            continue

        print(f"处理: {csv_path.name} -> {output_filename}")
        print(f"  维度: {', '.join(dimensions)}")

        # 创建图表配置
        chart_config = {
            'title': file_stem.replace('_', ' ').title()
        }

        # 生成 SVG
        svg_content = generate_radar_svg(chart_config, dimensions, data)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        print(f"✓ 已创建: {output_filename}\n")

    print(f'✅ 所有 SVG 雷达图生成完成！')
    print(f'\n输出目录: {output_dir}')


if __name__ == '__main__':
    main()
