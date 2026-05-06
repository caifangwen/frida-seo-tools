# hub-common.css 使用指南 — 大模型快速理解版

> **文件定位**：`hub-common.css` 是 Leeknives Steel Knowledge Center 的**唯一全局样式表**。  
> **作用域**：`hub.html`（枢纽页）+ 全部 `pillar-*.html`（支柱页）。  
> **设计理念**：语义化类名（`.family-row`、`.metric-card`…）+ CSS 变量（Design Tokens）集中管理，不堆砌原子类。

---

## 一、架构总览（8 层模型）

| 层级 | 区块名 | 职责 | 大模型提示关键词 |
|---|---|---|---|
| **L0** | Design Tokens | 颜色、间距、阴影、圆角、动画常量 | "改品牌色只需改 :root" |
| **L1** | Reset & Base | `box-sizing`、body 字体、平滑滚动 | "已全局 normalization" |
| **L2** | Layout Primitives | `.container`、`.two-col`、`.content-narrow` | "布局骨架" |
| **L3** | Typography | `.section-title`、`.hero-lead`、`.sub-heading` | "排版系统" |
| **L4** | Universal Components | `.btn`、`.tag`、`.chip`、`.progress-bar` | "跨页面复用组件" |
| **L5** | Hub Sections | Header、Family rows、Finder、VS cards… | **仅 hub.html 使用** |
| **L6** | Pillar Components | `.toc-wrap`、`.key-takeaway`、`.deep-dive-block`… | **仅 pillar 页使用** |
| **L7** | Utility Classes | `.u-text-center`、`.u-mt-lg`… | "微调用，不替代语义组件" |
| **L8** | Responsive | `820px` 单断点，多列变单栏 | "移动端自动适配" |

**大模型核心规则**：写新组件时**优先引用 L0 CSS 变量**，不要写死颜色/间距数值。

---

## 二、Design Tokens 速查表（L0）

### 2.1 品牌色
```css
var(--primary)          /* #000  主色/标题/深色背景 */
var(--secondary)        /* #c53030  品牌红/CTA/强调线 */
var(--secondary-hover)  /* #9b1c1c  按钮悬停 */
var(--secondary-bright) /* #e53e3e  渐变亮部 */
```

### 2.2 文本色阶（由深到浅）
```css
var(--ink)       /* #1a1a1a  最深正文 */
var(--text)      /* #333    默认正文 */
var(--muted-900) /* #444 */
var(--muted-800) /* #555 */
var(--muted-700) /* #666 */
var(--muted-500) /* #888 */
var(--muted-400) /* #999 */
var(--muted-300) /* #9ca3af */
var(--muted-200) /* #94a3b8 */
var(--muted-150) /* #b0b0b0 */
var(--muted-100) /* #d0d0d0  深色背景上的次要文字 */
var(--muted-50)  /* #eee    深色背景上的辅助文字 */
```

### 2.3 表面色（Surface）
```css
var(--surface)           /* #fff   卡片/面板底色 */
var(--light-gray)        /* #faf6f6  浅灰背景 */
var(--accent-bg)         /* #fff5f5  强调浅红背景 */
var(--surface-faq)       /* #fafafa  FAQ 区块底色 */
var(--surface-chip)      /* #f4f6f8  chip 标签底色 */
var(--surface-placeholder)/* #f0f2f4 图片占位底色 */
var(--surface-progress)  /* #eceff1 进度条轨道 */
var(--surface-divider)   /* #f2f2f2 分割线 */
```

### 2.4 边框与装饰
```css
var(--border)      /* #ece4e4  默认边框 */
var(--rose-200)    /* #fecaca  装饰边框/Factory insight 边框 */
var(--rose-100)    /* #ffe4e6  data-item 边框 */
```

### 2.5 阴影（由轻到重）
```css
var(--shadow-1)  /* 最轻：卡片 hover 前 / content-note */
var(--shadow-2)  /* TOC 容器 */
var(--shadow-3)  /* metric-card */
var(--shadow-4)  /* key-takeaway */
var(--shadow-5)  /* product-showcase-card 默认 */
var(--shadow-6)  /* product-showcase-card hover */
```

### 2.6 圆角
```css
var(--r-8)   /* 8px   小按钮、select */
var(--r-10)  /* 10px  卡片默认 */
var(--r-12)  /* 12px  大卡片、表格、key-takeaway */
var(--r-14)  /* 14px  FAQ、factory-insight */
var(--r-16)  /* 16px  finder-box */
var(--r-20)  /* 20px  progress 轨道 */
var(--r-30)  /* 30px  实心按钮 .btn */
var(--r-pill-50) /* 50px  tag */
var(--r-pill)    /* 999px  filter-btn、chip */
```

### 2.7 间距（Gap & Padding）
```css
/* gap */
var(--gap-xs)  /* 6px  */
var(--gap-sm)  /* 8px  */
var(--gap-md)  /* 10px */
var(--gap-lg)  /* 14px */
var(--gap-xl)  /* 16px */
var(--gap-2xl) /* 18px */
var(--gap-3xl) /* 20px */
var(--gap-4xl) /* 24px */

/* padding */
var(--pad-card)    /* 18px 卡片内边距 */
var(--pad-card-sm) /* 14px 紧凑型卡片 */
var(--pad-block)   /* 28px FAQ 等区块 */
var(--pad-finder)  /* 45px Finder 面板 */
var(--pad-cta-y)   /* 70px 底部 CTA 上下 */
```

### 2.8 容器宽度
```css
var(--container-max)  /* 1200px 全局最大宽 */
var(--content-max)    /* 900px  叙事文本最大宽 */
var(--content-narrow) /* 860px  副标题/窄内容 */
var(--cta-text-max)   /* 760px  CTA 描述文本 */
var(--table-min)      /* 880px  表格横向滚动阈值 */
```

---

## 三、通用组件百科全书（L3-L4）

### 3.1 按钮 Buttons

| 类名 | 视觉 | 使用场景 |
|---|---|---|
| `.btn` | 红色实心圆角 pill | 主 CTA：Get a Quote、Request samples |
| `.btn-text` | 红色文字+粗体，无背景 | 次级链接：View all articles → |

**最小结构**：
```html
<a href="#" class="btn">Primary Action →</a>
<a href="#" class="btn-text">Secondary Link →</a>
```

---

### 3.2 标签 Tags（价格带/定位标签）

用于标识 Budget / Mid / High-end 定位。

```html
<div class="tier-tags">
  <span class="tag budget">Budget</span>
  <span class="tag mid">Mid</span>
  <span class="tag high">High-end</span>
</div>
```

| 修饰符 | 背景 | 文字色 |
|---|---|---|
| `.budget` | `#fef2f2` | `#991b1b` |
| `.mid` | `#fff1f2` | `#be123c` |
| `.high` | `#ffe4e6` | `#9f1239` |

---

### 3.3 Chips（产品属性小标签）

比 Tag 更小、更轻量，用于产品卡片内展示属性。

```html
<div class="chip-row">
  <span class="chip">Premium Baseline</span>
  <span class="chip">Balanced PM</span>
  <span class="chip">EDC Hero</span>
</div>
```

---

### 3.4 Progress Bar（表格内评分条）

```html
<div class="progress-label">
  <span>82%</span><span>HRC 59-61</span>
</div>
<div class="progress-container">
  <div class="progress-bar" style="width:82%"></div>
</div>
```

**规则**：`style="width:XX%"` 是唯一需要内联的地方，其余全部走类名。

---

### 3.5 排版类 Typography

| 类名 | 用途 | 典型容器 |
|---|---|---|
| `.section-title` | 区块居中主标题，带底部红线装饰 | `<h2>` |
| `.section-sub` | 区块副标题，居中，灰色 | `<p>`，紧跟 `.section-title` |
| `.hero-lead` | Header 内的导语/描述 | `<p>`，位于 `<header>` 内 |
| `.narrative-content` | 长文本正文，自动限制宽度 | `<div>` |
| `.sub-heading` | 两栏布局中的列小标题 | `<h3>` |

---

## 四、Hub 页组件（L5）

> **使用页面**：`hub.html`  
> **大模型规则**：创建新的 Steel Knowledge Center 首页时，直接按以下结构拼装。

### 4.1 Header（全站统一）

```html
<header>
  <div class="container">
    <h1>页面主标题</h1>
    <p class="hero-lead">导语文本，限制在 900px 宽内。</p>
    <div class="stats-strip">
      <div class="stat-item">
        <span class="stat-val">30+</span>
        <span class="stat-title">指标名</span>
        <p class="stat-desc">指标描述，最多 280px 宽。</p>
      </div>
      <!-- 重复 3 个 -->
    </div>
  </div>
</header>
```

**注意**：header 背景为黑色（`var(--primary)`），内部文字默认白色。`.crumbs` 和 `.pillar-kicker` 如放在 header 内，文字也会自动适配。

---

### 4.2 Family Row（ metallurgical family 展示）

```html
<div class="family-list">
  <article class="family-row carbon">   <!-- 修饰符：carbon / stainless / tool / pm / damascus -->
    <div class="family-left">
      <h3>Carbon Steels</h3>
      <div class="family-def">Cr &lt; 1%, non-stainless</div>
      <p>一段描述文本。</p>
    </div>
    <div class="family-right">
      <h4>Featured articles</h4>
      <ul>
        <li><a href="#">文章标题</a></li>
      </ul>
      <div class="tier-tags">…</div>
      <div class="family-actions">
        <a class="btn-text" href="#">Source knives →</a>
        <a class="btn-text" href="pillar-xxx.html">View all →</a>
      </div>
    </div>
  </article>
</div>
```

**左侧统一红色底**：所有 `.family-row.* .family-left` 共享同一深红底 + 暗色遮罩，不区分 family 类型。

---

### 4.3 Comparison Table（可筛选表格）

```html
<div class="table-controls" id="tableFilters">
  <button class="filter-btn active" data-family="all">All</button>
  <button class="filter-btn" data-family="stainless">Stainless</button>
  <!-- 更多筛选按钮 -->
</div>

<div class="table-wrap">
  <table>
    <thead>…</thead>
    <tbody id="comparisonBody">
      <tr data-family="stainless">
        <td>VG-10</td>
        <td>Stainless</td>
        <td>59-61</td>
        <td>
          <!-- progress bar 结构 -->
        </td>
        …
      </tr>
    </tbody>
  </table>
</div>
<div class="table-cta">
  <a class="btn-text" href="#">Compare full dataset →</a>
</div>
```

**交互依赖**：需要外部 JS 监听 `.filter-btn` 的 click，切换 `data-family` 匹配的行显示/隐藏。

---

### 4.4 Steel Finder（交互面板）

```html
<section class="finder-box">
  <h2>Steel Finder</h2>
  <p>简短说明文本。</p>
  <div class="finder-grid">
    <div class="finder-step">
      <h3>Step 1: Product type</h3>
      <select id="finderProduct" class="finder-select">…</select>
    </div>
    <div class="finder-step">
      <h3>Step 2: Price range</h3>
      <select id="finderPrice" class="finder-select">…</select>
    </div>
  </div>
  <div id="finderResult" class="finder-result">
    <div class="result-item"><h4>钢材名</h4><p>推荐理由</p></div>
    <div class="finder-cta">
      <a class="btn" href="#">动作 1</a>
      <a class="btn" href="#">动作 2</a>
    </div>
  </div>
</section>
```

**视觉特征**：深色面板（`var(--primary)` 背景），内部文字白色，结果区为更深灰面板。

---

### 4.5 VS Cards（对比卡片网格）

```html
<div class="vs-grid">
  <a class="vs-card" href="#">
    <h4>8Cr13MoV vs D2</h4>
    <p>简短对比描述。</p>
  </a>
</div>
```

---

### 4.6 Factory Insight（工厂数据区块）

```html
<section class="factory-insight">
  <h2>Factory Insight: Title</h2>
  <p>说明文本。</p>
  <div class="data-grid">
    <div class="data-item">
      <span class="data-label">指标标签</span>
      <span class="data-value">指标值</span>
      <p>补充说明。</p>
    </div>
  </div>
  <div class="factory-cta">
    <a class="btn-text" href="#">Link →</a>
  </div>
</section>
```

---

### 4.7 Product Grid（hub 简易产品卡）

```html
<div class="product-grid">
  <article class="product-card">
    <div class="product-img">Product Image</div>
    <div class="product-info">
      <span class="product-name">8" Chef Knife - 8Cr13MoV</span>
      <span class="product-spec">Stainless · Budget · HRC 56 ± 1</span>
      <a class="btn-text" href="#">Spec sheet →</a>
    </div>
  </article>
</div>
```

---

### 4.8 FAQ

```html
<section class="faq-wrap">
  <div class="faq-category">
    <h3>分类标题</h3>
    <span class="faq-q">问题文本？</span>
    <div class="faq-a">答案文本。</div>
  </div>
</section>
```

---

### 4.9 Bottom CTA（页脚转化区）

```html
<footer class="cta-box">
  <div class="container">
    <h2>Ready to …?</h2>
    <p>描述文本。</p>
    <a href="#" class="btn">Get a Quote →</a>
  </div>
</footer>
```

---

## 五、Pillar 页组件（L6）

> **使用页面**：全部 `pillar-*.html`  
> **大模型规则**：写新的深度文章/支柱页时，按以下结构在 `<header>` 之后组装。

### 5.1 Header 内专属元素

```html
<header>
  <div class="container">
    <div class="crumbs"><a href="hub.html">← Back to Steel Knowledge Center</a></div>
    <span class="pillar-kicker">Metallurgical Family</span>
    <h1>Stainless Steels for Kitchen Knives</h1>
    <p class="hero-lead">…</p>
    <div class="stats-strip">…</div>
  </div>
</header>
```

| 类名 | 用途 |
|---|---|
| `.crumbs` | 面包屑，白字，悬停下划线 |
| `.pillar-kicker` | 小标签（如 "Metallurgical Family"），白色细边框 pill |

---

### 5.2 Intro Narrative（文章开场区）

```html
<section class="intro-narrative">
  <div class="container">
    <div class="key-takeaway">
      <h3>Key Takeaway / At a Glance</h3>
      <p>一段核心结论。</p>
    </div>
    <div class="narrative-content">
      <p>正文段落…</p>
    </div>
    <div class="toc-wrap">
      <h3>Table of Contents</h3>
      <ol>
        <li><a href="#foundation">…</a></li>
      </ol>
    </div>
  </div>
</section>
```

---

### 5.3 Metric Grid（四格数据指标）

```html
<div class="metric-grid">
  <div class="metric-card">
    <span class="metric-label">标签</span>
    <span class="metric-value">数值</span>
    <div class="metric-note">补充说明。</div>
  </div>
</div>
```

**响应式**：`auto-fit, minmax(190px, 1fr)`，窄屏自动换行。

---

### 5.4 Content Note（带阴影的提示卡片）

```html
<div class="content-note">
  <strong>标题</strong>
  <p>内容文本。</p>
</div>
```

**常用于**：`.two-col` 内部左右各放一个，形成对比信息。

---

### 5.5 Deep Dive Block（深度文章区块）

```html
<div class="deep-dive-block">
  <h2 class="section-title" id="dd-s35vn">S35VN PM Steel</h2>
  <p class="deep-dive-lead">导语段落，左侧带红色边框线。</p>
  <div class="two-col">
    <div>
      <h3 class="sub-heading">Why Brands Choose It</h3>
      <p>…</p>
    </div>
    <div>
      <h3 class="sub-heading">Production Watch-Outs</h3>
      <p>…</p>
    </div>
  </div>
  <div class="table-wrap">…</div>
  <div class="content-note">…</div>
</div>
```

**视觉特征**：顶部 2px 分割线 + 上内边距，`.deep-dive-lead` 左侧带 3px 红边。

---

### 5.6 Product Showcase（增强型产品卡片）

与 hub 页 `.product-card` 不同，这是 pillar 页专用、带 hover 浮起效果的精致卡片。

```html
<section class="product-showcase">
  <div class="product-showcase-grid">
    <article class="product-showcase-card">
      <div class="product-cover">Product Preview</div>
      <div class="product-body">
        <span class="product-title">Premium Folder - S35VN</span>
        <span class="product-meta">HRC 61 ±1 · satin stonewash · brand flagship</span>
        <div class="chip-row">
          <span class="chip">Premium Baseline</span>
          <span class="chip">Balanced PM</span>
        </div>
        <a class="btn-text" href="#">Request BOM estimate →</a>
      </div>
    </article>
  </div>
</section>
```

**hover 效果**：`translateY(-3px)` + 更深阴影。

---

### 5.7 Author Meta

```html
<div class="author-meta">
  Last updated: 2026-04-22 · Leeknives Editorial Team
</div>
```

---

## 六、Utility Classes（L7）微调速查

**原则**：这些类仅做**微调**，不替代语义组件。

| 类名 | 作用 |
|---|---|
| `.u-text-center` / `.u-text-left` / `.u-text-right` | 文本对齐 |
| `.u-mt-sm` `.u-mt-md` `.u-mt-lg` `.u-mt-xl` | margin-top |
| `.u-mb-sm` `.u-mb-md` `.u-mb-lg` `.u-mb-xl` | margin-bottom |
| `.u-flex` `.u-flex-col` | display flex / flex-direction: column |
| `.u-items-center` `.u-justify-between` | 对齐 |
| `.u-gap-sm` `.u-gap-md` `.u-gap-lg` | gap |
| `.u-sr-only` | 仅屏幕阅读器可见（无障碍） |

---

## 七、页面组装模板

### 7.1 全新 Hub 页 HTML 骨架

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>… | Leeknives</title>
  <link rel="stylesheet" href="hub-common.css">
</head>
<body>

<header>…</header>

<section class="intro-narrative">…</section>

<div class="container">
  <h2 class="section-title">…</h2>
  <!-- family-list / table / finder / vs-grid / factory-insight / product-grid / nav-grid / faq-wrap -->
</div>

<footer class="cta-box">…</footer>

</body>
</html>
```

### 7.2 全新 Pillar 页 HTML 骨架

```html
<!DOCTYPE html>
<html lang="en">
<head>…<link rel="stylesheet" href="hub-common.css"></head>
<body>

<header>
  <div class="container">
    <div class="crumbs">…</div>
    <span class="pillar-kicker">分类标签</span>
    <h1>支柱页标题</h1>
    <p class="hero-lead">…</p>
    <div class="stats-strip">…</div>
  </div>
</header>

<section class="intro-narrative">
  <div class="container">
    <div class="key-takeaway">…</div>
    <div class="narrative-content">…</div>
    <div class="toc-wrap">…</div>
  </div>
</section>

<div class="container">
  <h2 class="section-title" id="foundation">…</h2>
  <p class="section-sub">…</p>

  <div class="metric-grid">…</div>

  <div class="two-col">
    <div class="content-note">…</div>
    <div class="content-note">…</div>
  </div>

  <div class="table-wrap">…</div>

  <div class="deep-dive-block">…</div>

  <section class="factory-insight">…</section>

  <section class="product-showcase">…</section>

  <section class="faq-wrap">…</section>
</div>

<footer class="cta-box">…</footer>

</body>
</html>
```

---

## 八、大模型 Prompt 模板（直接可用）

### Prompt A：生成新 Pillar 页

```
请基于以下 CSS 组件系统，生成一个完整的 HTML 支柱页。

约束条件：
1. 只使用 hub-common.css 中已有的类名（见下方组件清单），不要发明新类。
2. 颜色、间距、阴影、圆角必须引用 CSS 变量，不要写死数值。
3. 页面结构必须包含：header（带 crumbs + pillar-kicker + stats-strip）→ intro-narrative（key-takeaway + narrative-content + toc-wrap）→ 正文区块（section-title + section-sub + metric-grid + two-col/content-note + deep-dive-block + table-wrap + factory-insight + product-showcase + faq-wrap）→ footer.cta-box。
4. 所有按钮使用 .btn 或 .btn-text。
5. 响应式已由 CSS 处理，无需额外写 media query。

可用语义组件：
- 布局：.container, .two-col, .content-narrow, .content-max
- 标题：.section-title, .section-sub, .hero-lead, .sub-heading, .deep-dive-lead
- 按钮：.btn, .btn-text
- 标签：.tag + .budget/.mid/.high, .chip + .chip-row
- 表格：.table-wrap, .table-controls, .filter-btn, .progress-label/.progress-container/.progress-bar
- 卡片：.product-showcase-card（hover 浮起）, .metric-card, .data-item, .content-note, .vs-card
- 特殊：.key-takeaway, .toc-wrap, .faq-wrap, .factory-insight, .finder-box
- 工具：.u-text-center, .u-mt-*, .u-mb-*

请写关于 [主题] 的支柱页。
```

### Prompt B：生成新 Hub 模块

```
请在现有 hub.html 的 .container 中插入一个新内容区块。

要求：
1. 只使用 hub-common.css 已有类名。
2. 使用 .section-title 作为区块标题。
3. 若需要卡片网格，使用 auto-fit + minmax() 的 grid 类（如 .vs-grid、.product-grid、.nav-grid）。
4. 若需要数据展示，优先使用 .factory-insight > .data-grid > .data-item 结构。
5. 保持视觉一致性：边框用 var(--border)，圆角用 var(--r-12) 或 var(--r-14)。

请生成一个 [功能描述] 的 HTML 结构。
```

### Prompt C：修改主题色

```
请修改 hub-common.css 的 :root 设计令牌，将品牌主色从红黑系改为 [新色系描述]。

规则：
1. 只修改 L0 Design Tokens 中的变量值，不动 HTML 结构。
2. 保持现有变量名不变，确保全部页面自动继承。
3. 需调整的变量至少包括：--secondary, --secondary-hover, --secondary-bright, --family-unified, --tag-*-bg, --tag-*-text, --accent-bg, --cover-grad-a, --cover-grad-b。
4. 确保深色背景（header, finder-box, cta-box）上的文字仍有足够对比度。
```

---

## 九、维护 checklist

- [ ] 新增组件类名前先搜索本文件，确认是否已存在语义等价类。
- [ ] 新增颜色/间距不要写死 px，优先在 `:root` 中声明新变量。
- [ ] Hub 专属组件放 **L5**，Pillar 专属组件放 **L6**，通用组件放 **L4**。
- [ ] 如需 JS 交互（如筛选、Finder），保持类名与现有 `hub.html` 中的 `id`/`class` 一致。
- [ ] 修改后检查 `820px` 断点下的移动端表现。
