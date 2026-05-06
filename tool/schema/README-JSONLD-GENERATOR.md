# 🚀 JSON-LD Schema 批量生成器

从 `input-files/` 文件夹中的文档自动生成多种 JSON-LD 结构化数据。

## 📁 工作流程

```
input-files/                    JSON-LD 生成器              output-jsonld/
┌────────────────────┐         ┌──────────────┐         ┌─────────────────────┐
│  article1.html     │         │              │         │  article1/          │
│  article2.md       │  ────▶  │ generate-    │  ────▶  │  ├── *-schema.json  │
│  article3.html     │         │ jsonld.js    │         │  ├── all-schemas.json│
└────────────────────┘         └──────────────┘         │  └── *.html         │
                                                         └─────────────────────┘
```

## 🚀 快速开始

### 1️⃣ 放入待转换文件

将 HTML 或 Markdown 文件放到 `input-files/` 文件夹：

```bash
# 支持的文件格式
✓ .html - HTML 文档
✓ .md   - Markdown 文档
✓ .txt  - 文本文档
```

### 2️⃣ 运行生成器

```bash
npm run jsonld
```

或

```bash
node generate-jsonld.js
```

### 3️⃣ 查看输出

生成的文件在 `output-jsonld/` 文件夹中。

## 📊 生成的 JSON-LD Schema 类型

### 1. Article Schema
- 用于文章、博客、指南等内容
- 包含标题、描述、作者、日期等

### 2. FAQ Schema
- 自动从 HTML 中提取 FAQ 内容
- 适用于 Google FAQ 富片段

### 3. BreadcrumbList Schema
- 面包屑导航结构化数据
- 帮助搜索引擎理解网站结构

### 4. WebPage Schema
- 网页基本信息
- 标题、描述、URL 等

### 5. Organization Schema
- 组织/公司信息
- Logo、社交媒体链接等

## 📁 每个文件生成的输出

对于每个输入文件，会生成：

```
output-jsonld/your-article/
├── article-schema.json          # Article Schema
├── faq-schema.json              # FAQ Schema（如果有 FAQ）
├── breadcrumb-schema.json       # BreadcrumbList Schema
├── webpage-schema.json          # WebPage Schema
├── organization-schema.json     # Organization Schema
├── all-schemas.json             # 所有 Schema 的合并文件
├── jsonld-scripts.html          # 可直接嵌入的脚本标签
└── complete-example.html        # 完整的 HTML 示例
```

## 💡 使用方式

### 方式 1: 直接使用 JSON 文件

将生成的 `*-schema.json` 文件集成到你的网站：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  ...
}
</script>
```

### 方式 2: 使用合并文件

使用 `all-schemas.json` 一次性获取所有 Schema：

```javascript
const schemas = require('./all-schemas.json');
```

### 方式 3: 使用 HTML 示例

直接使用 `complete-example.html` 作为模板：

```html
<!DOCTYPE html>
<html>
<head>
  <!-- JSON-LD 已集成 -->
  <script type="application/ld+json">
  ...
  </script>
</head>
<body>
  ...
</body>
</html>
```

### 方式 4: 使用脚本标签文件

`jsonld-scripts.html` 包含所有 JSON-LD 脚本标签，可以直接复制到你的 HTML 中。

## 🎯 示例输出

### Article Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Wholesale Canvas Bags: Complete B2B Buying Guide 2026",
  "description": "Looking for wholesale canvas bags?...",
  "datePublished": "2026-04-11",
  "dateModified": "2026-04-11",
  "author": {
    "@type": "Organization",
    "name": "Canvas Bag Manufacturer"
  }
}
```

### FAQ Schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is the typical MOQ for wholesale canvas bags?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Most factories offer MOQs starting at 100–200 units..."
      }
    }
  ]
}
```

## 🔧 自定义配置

编辑 `jsonld-generator.js` 可以：

- 修改 Organization 信息
- 调整 URL 和 Logo
- 添加 Product Schema
- 自定义 Schema 属性

## 📈 SEO 好处

✅ **Article Schema** - 文章富片段展示  
✅ **FAQ Schema** - Google FAQ 直接展示在搜索结果  
✅ **BreadcrumbList** - 更好的网站结构理解  
✅ **WebPage Schema** - 基本结构化数据  
✅ **Organization Schema** - 品牌知识图谱  

## 💡 最佳实践

1. **验证输出** - 使用 [Google 结构化数据测试工具](https://search.google.com/test/rich-results) 验证
2. **自定义信息** - 修改默认的 URL、Logo、Organization 信息
3. **定期更新** - 内容更新时重新生成 JSON-LD
4. **监控效果** - 在 Google Search Console 中监控富片段表现

## 📝 注意事项

- FAQ 只从 HTML 中已有的 JSON-LD 提取
- URL 和 Logo 等需要手动修改为实际值
- 建议根据实际内容调整生成的 Schema
