# 图片下载提示词模板

根据图片清单自动生成图片搜索和下载指令

---

## 使用方法

1. 复制下方提示词模板
2. 将 `[图片清单文件路径]` 替换为实际清单路径
3. 将 `[文章 MD 文件路径]` 替换为实际文章路径
4. 发送给 AI 助手执行

---

## 提示词模板

```
请根据图片清单下载并插入图片到文章中。

【图片清单】
[图片清单文件路径]

【目标文章】
[文章 MD 文件路径]

【任务要求】

1. 图片搜索
- 使用清单中的"搜索关键词"列作为搜索词
- 优先从以下来源查找：
  - Wikimedia Commons（可商用，需署名）
  - Unsplash / Pexels（免版权）
  - 行业相关公开资源（ASME、AWS 等标准组织）
- 确保图片与清单"用途"描述匹配

2. 图片下载与命名
- 按清单"文件名"列命名（保持 .webp 格式）
- 保存到目录：output/images/[文章主题]/
- 文章主题从文章标题提取（小写 + 连字符）

3. 图片插入
- 按清单"位置"列插入到对应章节后
- 使用清单"Alt 文本"列作为图片 Alt 属性
- Markdown 格式：![Alt 文本](../../images/[文章主题]/文件名.webp)

4. 上传路径记录
- 在文章 frontmatter 的 image 字段记录首图上传路径
- 格式：/wp-content/uploads/YYYY/MM/文件名.webp

【输出确认】

完成后请提供：
1. 已下载图片列表（文件名 + 来源）
2. 图片插入位置确认
3. 任何未找到图片的说明及替代建议

【注意事项】

- 每张图片必须与清单"用途"描述匹配
- Alt 文本必须与清单完全一致
- 文件名必须与清单完全一致
- 避免下载版权不明的图片
```

---

## 示例（WPS 指南文章）

```
请根据图片清单下载并插入图片到文章中。

### 图片清单
C:\Users\frida\Documents\seo-skill-main\blog-seo\output\hainer\output\posts\welding-procedure-specifications-wps-guide-images-list.md

### 目标文章
C:\Users\frida\Documents\seo-skill-main\blog-seo\output\hainer\output\posts\welding-procedure-specifications-wps-guide.md

### 任务要求

**1. 图片搜索**
- 使用清单中的"搜索关键词"列作为搜索词
- 优先从以下来源查找：
  - Wikimedia Commons（可商用，需署名）
  - Unsplash / Pexels（免版权）
  - 行业相关公开资源（ASME、AWS 等标准组织）
- 确保图片与清单"用途"描述匹配

**2. 图片下载与命名**
- 按清单"文件名"列命名（保持 `.webp` 格式）
- 保存到目录：`output/images/welding-procedure-specifications-wps-guide/`
- 文章主题从文章标题提取（小写 + 连字符）

**3. 图片插入**
- 按清单"位置"列插入到对应章节后
- 使用清单"Alt 文本"列作为图片 Alt 属性
- Markdown 格式：`![Alt 文本](../../images/welding-procedure-specifications-wps-guide/文件名.webp)`

**4. 上传路径记录**
- 在文章 frontmatter 的 `image` 字段记录首图上传路径
- 格式：`/wp-content/uploads/2026/03/文件名.webp`

### 输出确认

完成后请提供：
1. 已下载图片列表（文件名 + 来源）
2. 图片插入位置确认
3. 任何未找到图片的说明及替代建议

### 注意事项

- 每张图片必须与清单"用途"描述匹配
- Alt 文本必须与清单完全一致
- 文件名必须与清单完全一致
- 避免下载版权不明的图片
```

---

## 快速命令（如有 download_images.py 脚本）

```bash
# 批量下载脚本（如项目有提供）
python scripts/download_images.py \
  --list output/hainer/output/posts/welding-procedure-specifications-wps-guide-images-list.md \
  --output output/images/welding-procedure-specifications-wps-guide/
```

---

*最后更新：2026-03-31*
