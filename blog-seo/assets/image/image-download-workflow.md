# 图片下载与插入工作流

独立的图片下载、处理和插入流程指南。

---

## 📥 完整工作流程

```
步骤 1: 查找图片 → 步骤 2: 批量下载 → 步骤 3: 重命名 → 步骤 4: 优化压缩 → 步骤 5: 上传服务器 → 步骤 6: 更新文章引用
```

---

## 步骤 1: 查找图片

### 推荐图片源

| 来源 | 类型 | 版权 | 网址 |
|-----|------|------|------|
| Unsplash | 照片/场景 | 免费商用 | https://unsplash.com |
| Pexels | 照片/场景 | 免费商用 | https://pexels.com |
| Pixabay | 照片/插图 | 免费商用 | https://pixabay.com |
| Wikimedia Commons | 图表/技术图 | 需标注来源 | https://commons.wikimedia.org |

### 搜索关键词

根据文章类型选择关键词，参考：[image-checklist.md](./image-checklist.md)

---

## 步骤 2: 批量下载脚本

### 脚本信息

**位置**: `scripts/download_images.py`

**功能**: 从 Unsplash/Pexels/Picsum 批量下载免版税图片，自动压缩为 WebP/JPG 格式

### 安装依赖

```bash
pip install requests Pillow
```

### 环境变量（可选）

```bash
# Windows (PowerShell)
$env:PEXELS_API_KEY="你的 Pexels 密钥"
$env:UNSPLASH_ACCESS_KEY="你的 Unsplash 密钥"

# Linux/Mac
export PEXELS_API_KEY="你的 Pexels 密钥"
export UNSPLASH_ACCESS_KEY="你的 Unsplash 密钥"
```

### 使用示例

```bash
# 下载 5 张关于法兰的图片到 output/images（默认 medium 尺寸）
python scripts/download_images.py --query "industrial flanges pipeline" --count 5 --output output/images/

# 下载到指定文章目录，使用 large 尺寸
python scripts/download_images.py --query "ball valve industrial" --output output/images/ball-valve-guide/ --count 8 --size large

# 使用 Pexels API（需设置 PEXELS_API_KEY）
python scripts/download_images.py --query "steel pipe fittings" --use-api --count 6 --output output/images/
```

### 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|-----|------|------|-------|
| `--query` | `-q` | 搜索关键词（中英文均可） | 必填 |
| `--output` | `-o` | 输出目录（建议使用 output/images/[文章主题]/） | `output/images/` |
| `--count` | `-c` | 下载数量（最多 20） | `5` |
| `--size` | `-s` | 图片尺寸：small/medium/large/xlarge | `medium` |
| `--use-api` | — | 启用 Pexels API | 关闭 |

### 尺寸参考

| 尺寸名 | 分辨率 | 适用场景 |
|-------|--------|---------|
| small | 640×480 | 缩略图/小图 |
| medium | 1280×720 | 文章配图（推荐） |
| large | 1920×1080 | 高清大图 |
| xlarge | 2560×1440 | 超高清展示 |

### 输出示例

```
==================================================
SEO 文章图片下载器
==================================================
关键词：industrial flanges pipeline
输出目录：/project/images
数量：5
尺寸：medium (1280x720)
==================================================

正在从 Picsum 下载图片...
  ✓ 已保存：industrial-flanges-pipeline-1.webp (87KB)
  ✓ 已保存：industrial-flanges-pipeline-2.webp (92KB)
  ✓ 已保存：industrial-flanges-pipeline-3.webp (95KB)
  ✓ 已保存：industrial-flanges-pipeline-4.webp (89KB)
  ✓ 已保存：industrial-flanges-pipeline-5.webp (91KB)

下载完成！成功：5/5
```

---

## 步骤 3: 重命名规范

### 命名格式

```
格式：[主题]-[描述]-[可选细节].jpg

示例:
✅ weld-neck-flange-dimensions.jpg
✅ ball-valve-cross-section.jpg
✅ flange-bolt-tightening-pattern.jpg
✅ hardness-testing-steel-knife.jpg
✅ corrosion-resistance-comparison.jpg
```

### 批量重命名工具

| 工具 | 平台 | 价格 |
|-----|------|------|
| Bulk Rename Utility | Windows | 免费 |
| Advanced Renamer | 跨平台 | 免费 |
| Renamer | Mac | $20 |

---

## 步骤 4: 优化压缩

### 在线工具

| 工具 | 网址 | 特点 |
|-----|------|------|
| TinyPNG | https://tinypng.com | 支持 PNG/JPG，批量处理 |
| Squoosh | https://squoosh.app | Google 出品，实时预览 |
| Convertio | https://convertio.co | 格式转换 + 压缩 |

### 桌面工具

| 工具 | 平台 | 特点 |
|-----|------|------|
| ImageOptim | Mac | 免费，批量优化 |
| RIOT | Windows | 免费，轻量级 |
| XnConvert | 跨平台 | 免费，批量转换 |

### 优化目标

```
文件大小：< 200KB
宽度：1200-1920px
格式：JPG（照片）/ PNG（图表）/ WebP（网页优化）
```

---

## 步骤 5: 上传服务器

### WordPress 上传

```
路径：/wp-content/uploads/YYYY/MM/图片名.jpg
示例：/wp-content/uploads/2026/03/weld-neck-flange.jpg
```

### 上传方式

1. **WordPress 媒体库**: 直接拖拽上传
2. **FTP/SFTP**: 使用 FileZilla 等工具
3. **命令行**: `wp media import`（WP-CLI）

---

## 步骤 6: 更新文章引用脚本

### 脚本信息

**位置**: `scripts/update_article_images.py`

**功能**: 自动将文章中的占位符图片替换为真实下载的图片，或将新图片插入文章合适位置

### 安装依赖

```bash
pip install Pillow
```

### 使用示例

```bash
# 自动替换占位符图片 + 插入新图片
python scripts/update_article_images.py \
  --article output/posts/flange-guide/index.md \
  --images-dir output/images/flange-guide/

# 仅替换占位符图片（不插入新图片）
python scripts/update_article_images.py \
  --article output/posts/flange-guide/index.md \
  --images-dir output/images/flange-guide/ \
  --replace-only

# 在每个 H2 标题后插入图片
python scripts/update_article_images.py \
  --article output/posts/flange-guide/index.md \
  --images-dir output/images/flange-guide/ \
  --pattern after-headings

# 均匀分布图片（每 300 字一张）
python scripts/update_article_images.py \
  --article output/posts/flange-guide/index.md \
  --images-dir output/images/flange-guide/ \
  --pattern evenly

# 查看图片列表和引用示例（不修改文章）
python scripts/update_article_images.py \
  --list \
  --images-dir output/images/flange-guide/ \
  --keyword "industrial flanges"
```

### 参数说明

| 参数 | 简写 | 说明 |
|-----|------|------|
| `--article` | `-a` | Markdown 文章文件路径 |
| `--images-dir` | `-i` | 图片目录（默认：output/images/） |
| `--keyword` | `-k` | 关键词（用于生成 alt 文本） |
| `--pattern` | `-p` | 插入模式（见下表） |
| `--max-images` | `-m` | 最大图片数量 |
| `--list` | — | 仅列出图片，不修改文章 |
| `--replace-only` | — | 仅替换占位符，不插入新图片 |

### 插入模式

| 模式 | 说明 |
|-----|------|
| `after-intro`（默认） | 在第一个 H2 标题后插入 |
| `after-headings` | 在每个 H2 标题后插入 |
| `evenly` | 每 300 字均匀插入一张 |

### 占位符识别

脚本自动识别并替换以下格式的占位符：

```
images/featured-image.jpg
images/image-1.jpg
images/placeholder.jpg
images/TODO.jpg
```

---

## 🔄 典型工作流示例

### 法兰文章完整流程

```bash
# 1. 下载图片到 output/images/[文章主题]/
python scripts/download_images.py \
  --query "industrial flanges pipeline" \
  --output output/images/class-150-vs-300-flanges/ \
  --count 8 \
  --size large

# 2. 重命名下载的图片（手动或使用批量工具）
# industrial-flanges-pipeline-1.webp → weld-neck-flange-dimensions.webp
# industrial-flanges-pipeline-2.webp → flange-pressure-rating-chart.webp
# ...

# 3. 更新文章图片引用
python scripts/update_article_images.py \
  --article output/posts/class-150-vs-300-flanges/index.md \
  --images-dir output/images/class-150-vs-300-flanges/ \
  --keyword "industrial flanges" \
  --pattern after-headings
```

### 钢材评测文章完整流程

```bash
# 1. 下载图片
python scripts/download_images.py \
  --query "M390 steel knife hardness" \
  --output output/images/m390-steel-review/ \
  --count 8 \
  --size large

# 2. 重命名
# m390-steel-knife-hardness-1.webp → m390-steel-composition-chart.webp
# m390-steel-knife-hardness-2.webp → rockwell-hardness-test-m390.webp
# ...

# 3. 更新文章
python scripts/update_article_images.py \
  --article output/posts/m390-steel-review/index.md \
  --images-dir output/images/m390-steel-review/ \
  --keyword "M390 steel" \
  --pattern evenly
```

---

## ✅ 流程检查清单

### 下载前

```
□ 确定文章主题和关键词
□ 选择合适图片源（Unsplash/Pexels/Wikimedia）
□ 准备输出目录 output/images/[文章主题]/
```

### 下载后

```
□ 检查图片数量是否足够
□ 重命名为描述性文件名
□ 压缩优化至<200KB
□ 上传到 WordPress 媒体库
```

### 插入后

```
□ 检查每 400-500 字至少 1 张图
□ 检查每个 H2 章节有配图
□ 检查所有 Alt 文本正确
□ 检查 Figure 格式链接有效
```

---

*SKILL-06-Workflow v1.0 | 最后更新：2026-03-31*
