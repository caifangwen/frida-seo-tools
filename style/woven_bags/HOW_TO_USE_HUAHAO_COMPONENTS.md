# Huahao 样式快捷使用指南

## 方法 1：VS Code 代码片段（推荐 ⭐）

### 安装步骤

1. **打开 VS Code 代码片段设置**
   - 按 `Ctrl+Shift+P` (Windows) 或 `Cmd+Shift+P` (Mac)
   - 输入 `Configure User Snippets`
   - 选择 `HTML` 或 `Markdown`

2. **复制粘贴**
   - 打开 `huahao-snippets.json` 文件
   - 复制全部内容
   - 粘贴到你的 VS Code 用户代码片段中

### 使用方式

在编辑器中输入**前缀**，按 `Tab` 键自动展开：

| 前缀 | 组件 | 效果 |
|------|------|------|
| `hh` | 文章包装器 | `<div class="hh-post">...</div>` |
| `hhero` | 英雄横幅 | 带标题、副标题、统计数据的横幅 |
| `hhsec` | 章节标题 | 带编号和标签的章节头 |
| `hhboxi` | 信息框 | 蓝色信息提示框 |
| `hhboxt` | 提示框 | 绿色专业提示框 |
| `hhboxw` | 警告框 | 黄色警告提示框 |
| `hhcheck` | 勾选列表 | 带勾图标的列表 |
| `hhtable` | 表格 | 样式化数据表格 |
| `hhfaq` | FAQ 项 | 可折叠的问答项 |
| `hhcta` | CTA 横幅 | 底部转化横幅 |
| `hhcards` | 卡片网格 | 多列卡片布局 |
| `hhsteps` | 步骤卡片 | 流程步骤展示 |
| `hhflow` | 流程图 | 垂直流程图 |
| `hhsplit` | 双栏对比 | 左右对比布局 |
| `hhstats` | 统计数据 | 数字统计卡片 |
| `hhbars` | 条形图 | 数据对比条形图 |
| `hhspecs` | 规格卡片 | 产品规格展示 |
| `hhverdict` | 总结表格 | 快速对比总结 |
| `hhtimeline` | 时间线 | 水平时间线 |

### 实际操作示例

```
输入：hhero + Tab

自动生成：
<div class="hh-hero">
  <span class="hh-hero-eyebrow">Guide · 2026</span>
  <h1>Title</h1>
  <p class="hh-hero-sub">Subtitle text...</p>
  <div class="hh-hero-stats">
    <div><span class="hh-hero-stat-num">100+</span><span class="hh-hero-stat-label">Label</span></div>
  </div>
</div>
```

然后**直接编辑占位符内容**即可！

---

## 方法 2：Markdown + markdown-it-attrs（适合静态站点）

### 安装

```bash
npm install markdown-it markdown-it-attrs
```

### 配置

```javascript
// markdown.config.js
const md = require('markdown-it')({ html: true })
  .use(require('markdown-it-attrs'));

module.exports = md;
```

### 使用示例

```markdown
# 标题 {.hh-section-title}

段落文本 {.hh-box-info}

![图片](url.jpg) {.hh-card}

[按钮链接](/contact) {.hh-btn-primary}
```

**缺点**：仍然需要手动输入 class 名，不够快捷。

---

## 方法 3：创建 HTML 模板文件

### 使用步骤

1. 打开 `huahao-template-blank.html`（空白模板）
2. 复制需要的组件代码
3. 粘贴到你的文章文件中
4. 修改内容

---

## 方法 4：浏览器扩展（快速选择器）

创建一个简单的 HTML 选择器页面：

### 使用 `huahao-component-picker.html`

1. 在浏览器中打开此文件
2. 点击需要的组件
3. 自动复制 HTML 代码
4. 粘贴到你的文章中

---

## 完整工作流程示例

### 写一篇新文章

```markdown
<!-- 1. 输入 hhero + Tab -->
<div class="hh-hero">
  <span class="hh-hero-eyebrow">Buyer's Guide 2026</span>
  <h1>How to Order Custom Bags</h1>
  <p class="hh-hero-sub">Complete guide...</p>
</div>

<!-- 2. 输入 hhsec + Tab -->
<div class="hh-section-header">
  <div class="hh-section-num">01</div>
  <div>
    <span class="hh-section-tag">Overview</span>
    <h2 class="hh-section-title">Choose Your Material</h2>
  </div>
</div>

<!-- 3. 写普通段落 -->
<p>Material selection is critical...</p>

<!-- 4. 输入 hhboxi + Tab -->
<div class="hh-box-info">
  <p><span class="hh-box-icon">...</span>Important info here...</p>
</div>

<!-- 5. 输入 hhcheck + Tab -->
<ul class="hh-checklist">
  <li>Feature 1</li>
  <li>Feature 2</li>
</ul>

<!-- 6. 输入 hhtable + Tab -->
<div class="hh-table-wrap">
  <table class="hh-table">
    <!-- 填写表格内容 -->
  </table>
</div>

<!-- 7. 输入 hhcta + Tab（文章结尾） -->
<div class="hh-cta">
  <!-- CTA 内容 -->
</div>
```

---

## 快捷键优化（进阶）

在 VS Code 设置中添加自定义快捷键：

```json
// keybindings.json
[
  {
    "key": "ctrl+alt+h",
    "command": "editor.action.insertSnippet",
    "args": { "name": "Huahao Hero" }
  },
  {
    "key": "ctrl+alt+s",
    "command": "editor.action.insertSnippet",
    "args": { "name": "Huahao Section Header" }
  }
]
```

---

## 常见问题

### Q: 为什么不用 markdown-it-attrs？

A: 它需要你**手动输入 class 名**，如 `{.hh-box .hh-box-info}`，并不比直接写 HTML 快多少。

### Q: 代码片段能在其他编辑器用吗？

A: 代码片段是 VS Code 特有的。其他编辑器：
- **WebStorm**: 使用 Live Templates
- **Sublime Text**: 使用 Snippets
- **Atom**: 使用 Snippets

### Q: 如何自定义代码片段？

A: 编辑 `huahao-snippets.json`，修改 `body` 数组中的内容即可。

---

## 推荐方案

| 需求 | 推荐方案 |
|------|---------|
| 快速写作 | VS Code 代码片段 ⭐⭐⭐⭐⭐ |
| 静态站点 | Markdown + 代码片段 ⭐⭐⭐⭐ |
| 团队协作 | HTML 模板文件 ⭐⭐⭐⭐ |
| 非技术人员 | 可视化选择器 ⭐⭐⭐ |

**最佳实践**：VS Code 代码片段 + HTML 输出
