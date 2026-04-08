#!/usr/bin/env python3
"""
图片转 WebP 脚本

功能：批量将 JPG/PNG 图片转换为 WebP 格式，自动优化文件大小
支持：单文件转换、目录批量转换、递归子目录转换
"""

import argparse
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from PIL import Image
except ImportError:
    print("错误：需要安装 Pillow 库")
    print("运行：pip install Pillow")
    sys.exit(1)


class WebPConverter:
    """WebP 图片转换器"""

    def __init__(self, quality: int = 80, method: int = 6, keep_original: bool = False):
        """
        初始化转换器

        Args:
            quality: WebP 质量 (1-100)，默认 80
            method: 压缩方法 (0-6)，数字越大压缩越好但越慢，默认 6
            keep_original: 是否保留原文件，默认 False
        """
        self.quality = quality
        self.method = method
        self.keep_original = keep_original
        self.stats = {
            "success": 0,
            "failed": 0,
            "original_size": 0,
            "converted_size": 0,
        }

    def convert_file(self, input_path: str, output_dir: str = None) -> tuple[bool, str]:
        """
        转换单个文件

        Args:
            input_path: 输入文件路径
            output_dir: 输出目录（None 则保存到原目录）

        Returns:
            (成功标志，消息)
        """
        input_path = Path(input_path)

        if not input_path.exists():
            return False, f"文件不存在：{input_path}"

        if input_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"]:
            return False, f"不支持的格式：{input_path.suffix}"

        # 确定输出路径
        if output_dir:
            output_path = Path(output_dir) / f"{input_path.stem}.webp"
        else:
            output_path = input_path.with_suffix(".webp")

        try:
            # 获取原文件大小
            original_size = input_path.stat().st_size

            # 打开并转换图片
            with Image.open(input_path) as img:
                # 处理 RGBA 模式（PNG 透明背景）
                if img.mode in ("RGBA", "LA") or (
                    img.mode == "P" and "transparency" in img.info
                ):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")

                # 保存为 WebP
                img.save(
                    output_path,
                    "WEBP",
                    quality=self.quality,
                    method=self.method,
                    lossless=False,
                )

            # 获取新文件大小
            converted_size = output_path.stat().st_size

            # 计算压缩率
            compression_ratio = (1 - converted_size / original_size) * 100

            # 更新统计
            self.stats["success"] += 1
            self.stats["original_size"] += original_size
            self.stats["converted_size"] += converted_size

            # 如果不保留原文件，删除它
            if not self.keep_original and output_path != input_path:
                input_path.unlink()

            return True, f"✓ {input_path.name} → {output_path.name} ({compression_ratio:+.1f}%)"

        except Exception as e:
            self.stats["failed"] += 1
            return False, f"✗ {input_path.name}: {str(e)}"

    def convert_directory(
        self,
        input_dir: str,
        output_dir: str = None,
        recursive: bool = False,
        max_workers: int = 4,
        preserve_structure: bool = False,
    ) -> None:
        """
        批量转换目录中的图片

        Args:
            input_dir: 输入目录
            output_dir: 输出目录（None 则保存到原目录）
            recursive: 是否递归子目录
            max_workers: 最大线程数
            preserve_structure: 是否保持目录结构（默认保持）
        """
        input_dir = Path(input_dir)

        if not input_dir.exists():
            print(f"错误：目录不存在：{input_dir}")
            return

        # 收集所有图片文件
        image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"}
        image_files = []

        if recursive:
            for ext in image_extensions:
                image_files.extend(input_dir.rglob(f"*{ext}"))
                image_files.extend(input_dir.rglob(f"*{ext.upper()}"))
        else:
            for ext in image_extensions:
                image_files.extend(input_dir.glob(f"*{ext}"))
                image_files.extend(input_dir.glob(f"*{ext.upper()}"))

        # 排除已有的 WebP 文件
        image_files = [f for f in image_files if f.suffix.lower() != ".webp"]

        if not image_files:
            print(f"未找到可转换的图片文件")
            return

        print(f"找到 {len(image_files)} 个图片文件")
        print(f"开始转换（线程数：{max_workers}）...\n")

        # 创建输出目录
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

        # 多线程转换
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for img_file in image_files:
                # 如果保持目录结构，计算相对路径
                if preserve_structure and output_dir:
                    try:
                        rel_path = img_file.relative_to(input_dir)
                        file_output_dir = Path(output_dir) / rel_path.parent
                        file_output_dir.mkdir(parents=True, exist_ok=True)
                        target_output_dir = str(file_output_dir)
                    except ValueError:
                        target_output_dir = output_dir
                else:
                    target_output_dir = output_dir

                futures[
                    executor.submit(self.convert_file, str(img_file), target_output_dir)
                ] = img_file

            for future in as_completed(futures):
                success, message = future.result()
                print(message)

        # 打印统计
        self.print_stats()

    def print_stats(self) -> None:
        """打印转换统计信息"""
        print("\n" + "=" * 50)
        print("转换完成！")
        print("=" * 50)
        print(f"成功：{self.stats['success']} 个")
        print(f"失败：{self.stats['failed']} 个")

        if self.stats["original_size"] > 0:
            original_mb = self.stats["original_size"] / (1024 * 1024)
            converted_mb = self.stats["converted_size"] / (1024 * 1024)
            compression_ratio = (
                1 - self.stats["converted_size"] / self.stats["original_size"]
            ) * 100

            print(f"\n原始大小：{original_mb:.2f} MB")
            print(f"转换后大小：{converted_mb:.2f} MB")
            print(f"压缩率：{compression_ratio:+.1f}%")
            print(f"节省空间：{(original_mb - converted_mb):.2f} MB")


def main():
    parser = argparse.ArgumentParser(
        description="图片转 WebP 脚本 - 批量转换 JPG/PNG 为 WebP 格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 转换单个文件
  python convert_to_webp.py image.jpg

  # 转换目录中的所有图片
  python convert_to_webp.py ./images/

  # 递归转换子目录，输出到新目录
  python convert_to_webp.py ./images/ -o ./webp-images/ -r

  # 使用更高质量（90），保留原文件
  python convert_to_webp.py ./images/ -q 90 --keep-original

  # 使用 8 个线程加速转换
  python convert_to_webp.py ./images/ -w 8
        """,
    )

    parser.add_argument("input", help="输入文件或目录路径")
    parser.add_argument(
        "-o", "--output", help="输出目录（默认保存到原目录）", default=None
    )
    parser.add_argument(
        "-q", "--quality", type=int, default=80, help="WebP 质量 1-100（默认：80）"
    )
    parser.add_argument(
        "-m",
        "--method",
        type=int,
        default=6,
        help="压缩方法 0-6（默认：6，数字越大压缩越好但越慢）",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="递归转换子目录",
    )
    parser.add_argument(
        "--keep-original",
        action="store_true",
        help="保留原文件（默认删除）",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=4,
        help="最大线程数（默认：4）",
    )
    parser.add_argument(
        "--preserve-structure",
        action="store_true",
        default=True,
        help="保持输入目录结构（默认开启）",
    )
    parser.add_argument(
        "--no-preserve-structure",
        action="store_true",
        help="不保持目录结构，所有文件输出到同一目录",
    )

    args = parser.parse_args()

    # 验证参数
    if args.quality < 1 or args.quality > 100:
        print("错误：质量必须在 1-100 之间")
        sys.exit(1)

    if args.method < 0 or args.method > 6:
        print("错误：压缩方法必须在 0-6 之间")
        sys.exit(1)

    if args.workers < 1 or args.workers > 16:
        print("错误：线程数必须在 1-16 之间")
        sys.exit(1)

    # 确定是否保持目录结构
    preserve_structure = args.preserve_structure and not args.no_preserve_structure

    # 创建转换器并执行
    converter = WebPConverter(
        quality=args.quality,
        method=args.method,
        keep_original=args.keep_original,
    )

    input_path = Path(args.input)

    if input_path.is_file():
        # 转换单个文件
        success, message = converter.convert_file(str(input_path), args.output)
        print(message)
        converter.print_stats()
    elif input_path.is_dir():
        # 转换目录
        converter.convert_directory(
            str(input_path),
            args.output,
            recursive=args.recursive,
            max_workers=args.workers,
            preserve_structure=preserve_structure,
        )
    else:
        print(f"错误：路径不存在：{input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
