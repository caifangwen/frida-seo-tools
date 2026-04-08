# SKILL-00A: 关键词调研

**用途**: 写作前进行关键词研究，确定文章 SEO 方向
**执行时机**: 写作前第一步，在竞对调研（`competitor-research.md`）之前

---

## 1. 关键词类型分类

| 类型 | 说明 | 示例 |
|-----|------|------|
| 核心关键词 | 文章主要目标词 | "best pocket knife steel", "flange types" |
| 长尾关键词 | 3-5 词的具体查询 | "best steel for EDC knife 2026", "class 150 vs 300 flange pressure rating" |
| 对比关键词 | 包含对比意图 | "S30V vs S35VN", "ball valve vs gate valve" |
| 问题关键词 | 疑问句形式 | "what is magnacut steel", "how to install flange" |
| 商业关键词 | 含购买意图 | "buy M390 knife", "wholesale pipe fittings" |

---

## 2. 关键词调研步骤

**步骤 1: 确定主题范围**

```
输入：产品类型/主题
输出：核心关键词列表

示例 - 钢材主题:
- [钢材名] steel
- best steel for [用途]
- [钢材 A] vs [钢材 B]
- what is [钢材名]
- is [钢材名] steel good

示例 - 法兰/阀门主题:
- [产品类型] flanges
- [材质] flange specifications
- [类型 A] vs [类型 B] flange
- what is [法兰类型]
- [法兰] pressure rating chart
```

**步骤 2: 分析搜索意图**

```
信息型 (Informational):
- "what is...", "how to...", "guide to..."
- 适合：科普文章、指南类文章

商业型 (Commercial):
- "best...", "top...", "review..."
- 适合：评测文章、排行榜

交易型 (Transactional):
- "buy...", "wholesale...", "manufacturer..."
- 适合：产品页面、B2B 页面
```

**步骤 3: 关键词难度评估**

```
低难度 (KD 0-30):
- 长尾词、新话题/细分主题
- 示例："magnacut steel review 2026", "duplex 2205 flange properties"

中难度 (KD 30-60):
- 中等竞争词
- 示例："best EDC steel", "flange pressure classes"

高难度 (KD 60+):
- 核心大词
- 示例："best knife steel", "pipe fittings"
```

---

## 3. 关键词策略

**B2B 导向关键词** (优先级高):

```
- wholesale [产品]
- [产品] manufacturer
- OEM [产品] service
- private label [产品]
- custom [产品] maker
- bulk [产品]
- [标准] certified [产品]
```

**产品评测关键词** (流量稳定):

```
- [产品名] review
- is [产品名] good for [用途]
- [产品 A] vs [产品 B]
- best [产品] for [用途]
- [产品] specifications
```

**指南类关键词** (长尾流量):

```
- how to choose [产品]
- guide to [主题]
- types of [类别]
- what is [概念]
- how to maintain/install [产品]
```

**标准相关关键词** (工业品适用):

```
- ASME [标准号] [产品]
- API [标准号] [产品]
- DIN [标准] [产品]
- JIS [标准] [产品]
- ASTM [标准] specifications
```

---

## 4. 关键词布局规则

**标题 (Title)**: 包含核心关键词，长度 50-60 字符

```
✅ "14C28N Steel: Underrated or Overhyped?" (42 字符)
✅ "Class 150 vs Class 300 Flanges: Key Differences Explained" (58 字符)
✅ "What Is a Fixed Blade Knife and How to Choose One?" (52 字符)
```

**开篇段落**: 前 100 词出现核心关键词，自然融入，避免堆砌

```markdown
**14C28N steel** is often mistaken for a "budget substitute," but in reality,
it outperforms many mid-to-high-end steels in several key parameters.

A **weld neck flange** is one of the most widely used flange types in 
industrial piping systems, designed for high-pressure applications.
```

**副标题 (H2/H3)**: 每 300-500 词包含 1 个相关关键词，使用长尾变体

```markdown
## What is 14C28N Steel?
## 14C28N vs Nitro-V
## Performance Analysis of 14C28N Steel
### Toughness
### Corrosion Resistance
### Edge Retention

## Flange Pressure Ratings
## Stainless Steel vs Carbon Steel
## Installation Steps
## Common Applications
```

**图片 Alt**: 描述性文字 + 关键词

```
alt="pocket knife with red handle one rocks"
alt="weld neck flange dimensions ASME B16.5"
alt="ball valve cross section diagram"
```

**内部链接锚文本**: 使用关键词变体

```markdown
[OEM knife manufacturers](https://keganico.com/oem-knife-manufacturer/)
[14C28N steel](https://keganico.com/14c28n-steel/)
[flange pressure class chart](https://example.com/flange-pressure-chart/)
[stainless steel valve suppliers](https://example.com/stainless-steel-valves/)
```

---

## 5. 输出模板

```markdown
## 目标关键词报告

**核心关键词**: [核心词]
**搜索意图**: 信息型/商业型/交易型
**目标受众**: [描述]

### 主要关键词列表
| 关键词 | 类型 | 难度 | 优先级 |
|-------|------|-----|-------|
| [核心词] | 核心 | 高 | P0 |
| [长尾词 1] | 长尾 | 中 | P0 |
| [对比词] | 对比 | 中 | P1 |
| [问题词] | 问题 | 低 | P1 |

### 内容大纲
1. 开篇：引入核心关键词
2. [章节 1]
3. [章节 2]
4. [对比/分析]
5. 购买建议/选型建议 + CTA

### 内部链接目标
- [链接 1]
- [链接 2]
- [链接 3]
- [CTA 页面]
```

---

**下一步** → `competitor-research.md`
