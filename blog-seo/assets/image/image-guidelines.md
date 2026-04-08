# SKILL-06: 图片规范核心指南

**用途**: 规范图片插入位置、格式，及自动化处理流程
**适用**: 所有文章类型（横切关注点）

---

## 1. 图片密度规则

| 规则 | 说明 |
|-----|------|
| 字数密度 | 每 400-500 字至少 1 张图片 |
| 章节密度 | 每个主要章节（`##`）至少 1 张 |
| 开篇规则 | 开篇后第 1 个章节必须有图片 |
| 表格规则 | 对比表格前后各 1 张 |
| 结论规则 | 结论前可有 1 张总结性图片 |

---

## 2. 图片来源优先级

```
第 1 优先：网站现有本地资源（output/images 中已下载的图片）
第 2 优先：从网络下载并本地化（使用 download_images.py）
第 3 优先：外部可信赖来源（Wikimedia、Unsplash 等）
```

⚠️ **禁止虚构图片链接** — 所有图片必须真实存在于服务器或本地。

### 图片存储路径规范

| 场景 | 路径格式 | 示例 |
|-----|---------|------|
| 本地开发 | `output/images/[文章主题]/图片名.webp` | `output/images/class-150-vs-300-flanges/image-1.webp` |
| 文章引用 | `../../images/[文章主题]/图片名.webp` | `../../images/class-150-vs-300-flanges/image-1.webp` |
| 服务器路径 | `/wp-content/uploads/YYYY/MM/图片名.jpg` | `/wp-content/uploads/2026/03/flange-comparison.jpg` |

---

## 3. Markdown 图片格式

### 基础格式

```markdown
![图片描述](https://img.example.com/wp-content/uploads/年份/月份/图片名称.jpg)
```

### Figure 格式（产品展示）

```markdown
<figure>

[![产品图片](https://img.example.com/wp-content/uploads/YYYY/MM/图片.jpg)](https://example.com/产品链接/)

<figcaption>

[产品名称](https://example.com/产品链接/)

</figcaption>

</figure>
```

### 图片来源标注

```markdown
<figure>

[![图片](https://img.example.com/wp-content/uploads/YYYY/MM/图片.jpg)](https://img.example.com/wp-content/uploads/YYYY/MM/图片.jpg)

<figcaption>

ASME B16.5 Flange Dimensions from [Wikimedia](https://commons.wikimedia.org/wiki/Main_Page)

</figcaption>

</figure>
```

### 带数据来源的图片

```markdown
<figure>

![图片](https://img.example.com/wp-content/uploads/YYYY/MM/图片.jpg)

<figcaption>

_Data source: [来源名称](链接)_

</figcaption>

</figure>
```

---

## 4. 图片命名规范

### 命名规则

```
格式：[主题]-[描述]-[可选细节].jpg

规则:
✅ 全部小写字母
✅ 单词间用连字符 - 连接
✅ 避免特殊字符和空格
✅ 保持描述性但简洁 (3-5 个关键词)
✅ 长度不超过 50 字符
```

### 命名示例

```
✅ weld-neck-flange-dimensions.jpg
✅ ball-valve-cross-section.jpg
✅ flange-bolt-tightening-pattern.jpg
✅ hardness-testing-steel-knife.jpg
✅ corrosion-resistance-comparison.jpg

❌ DSC_2847.JPG（无意义）
❌ 法兰图片_2024.jpg（中文 + 特殊字符）
❌ class-150-flange-image-final-v2.jpg（过长）
```

---

## 5. 图片优化最佳实践

| 属性 | 建议 |
|-----|------|
| 格式 - 照片 | JPG |
| 格式 - 图表 | PNG |
| 格式 - 网页优化 | WebP（脚本默认输出） |
| 文件大小 | < 200KB |
| 宽度 | 1200-1920px |
| Alt 文本长度 | 5-15 个单词 |

### Alt 文本规则

```
✅ 正确做法:
- 描述图片内容：the-pressure-rating-chart-for-class-150-flanges
- 包含关键词：weld-neck-flange-dimensions-chart
- 具体描述：stainless-steel-316-flange-closeup

❌ 错误做法:
- 过于简单：image1.jpg, photo.png
- 以"image of"开头
- 缺失或无意义
```

### 推荐工具

| 工具类型 | 推荐工具 |
|---------|---------|
| 批量重命名 | Bulk Rename Utility / Advanced Renamer |
| 在线压缩 | TinyPNG / Squoosh |
| 格式转换 | Convertio / XnConvert |
| 截图/标注 | Snagit / Greenshot / ShareX |

---

## 6. 相关文档

- **图片关键词速查表**: [image-checklist.md](./image-checklist.md)
- **图片下载与插入流程**: [image-download-workflow.md](./image-download-workflow.md)

---

## 7. 发布前检查清单

### 密度检查

```
□ 每 400-500 字至少 1 张图片
□ 每个 H2 章节有配图
□ 开篇后第 1 个章节有图
□ 对比表格前后有图
```

### SEO 检查

```
□ Alt 文本 5-15 个单词
□ Alt 文本描述图片内容
□ Alt 文本包含关键词
□ 避免"image of"开头
□ 文件名含关键词
□ 上传路径正确 (YYYY/MM)
```

### 格式检查

```
□ 所有图片有 Alt 文本
□ Figure 格式正确 (产品图)
□ 图片来源/数据有标注
□ 文件大小已优化 (<200KB)
□ 产品 Figure 链接有效
```

---

*SKILL-06 v1.0 | 最后更新：2026-03-31*
