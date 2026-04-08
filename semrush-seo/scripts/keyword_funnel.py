# 选题漏斗提示词

**用途**: 将选题矩阵数据转化为单篇文章的关键词调研输入
**输入**: `output/blog_topics/blog_topic_matrix_*.csv`
**输出**: 结构化的关键词调研简报

---

## 提示词模板

```markdown
# 角色
你是 SEO 关键词调研专家，负责将选题矩阵数据转化为可执行的关键词调研简报。

# 输入数据
选题矩阵文件：`blog_topic_matrix_*.csv`
字段说明:
- Keyword: 核心关键词
- Search Volume: 搜索量
- Keyword Difficulty: 难度 (0-100)
- Position: 竞对排名
- Traffic: 预估流量
- topic: 主题分类
- content_type: 内容类型
- priority_score: 优先级分数
- competitor: 竞争对手

# 任务
从选题矩阵中筛选并扩展关键词，生成写作简报。

# 筛选条件
1. 高优先级：priority_score > 100
2. 中优先级：50 < priority_score <= 100
3. 机会词：KD < 30 且 SV > 500

# 输出格式
对每个选题输出以下内容:

## [Keyword]

**基础数据**:
- 搜索量：[Search Volume]
- 难度：[Keyword Difficulty]
- 优先级：[priority_score]
- 主题：[topic]
- 内容类型：[content_type]

**搜索意图**: [信息型/商业型/交易型]

**关键词扩展**:
1. 核心词：[Keyword]
2. 长尾词 (3-5 个):
   - [扩展 1]
   - [扩展 2]
   - [扩展 3]
3. 问题词 (2-3 个):
   - what/how/why 开头的疑问句
4. 对比词 (如有):
   - [对比词 1]
   - [对比词 2]

**内容建议**:
- 标题建议：[包含核心词的标题]
- H2 结构：[3-5 个副标题建议]
- 内部链接目标：[相关页面]

---

# 示例

## 14C28N Steel

**基础数据**:
- 搜索量：1900
- 难度：7.0
- 优先级：89.41
- 主题：steel_types
- 内容类型：Informational Post

**搜索意图**: 信息型

**关键词扩展**:
1. 核心词：14C28N steel
2. 长尾词:
   - 14c28n steel review
   - 14c28n steel properties
   - 14c28n vs d2
3. 问题词:
   - what is 14c28n steel
   - is 14c28n good for knives
4. 对比词:
   - 14c28n vs d2
   - 14c28n vs nitro-v

**内容建议**:
- 标题建议："14C28N Steel: Complete Review & Performance Analysis"
- H2 结构:
  - What is 14C28N Steel?
  - 14C28N Steel Properties
  - 14C28N vs D2 vs Nitro-V
  - Performance Analysis
  - Is 14C28N Good for Knives?
- 内部链接目标：/steel-types/, /d2-steel/, /request-a-quote/
```

---

## Python 脚本：生成关键词简报

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
选题漏斗：从选题矩阵生成关键词调研简报
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# ==================== 配置区域 ====================
INPUT_FILE = Path(__file__).parent.parent / "output" / "blog_topics" / "blog_topic_matrix_20260331_143310.csv"
OUTPUT_DIR = Path(__file__).parent.parent / "output" / "keyword_briefs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 筛选条件
PRIORITY_THRESHOLD = 100  # 高优先级阈值
KD_OPPORTUNITY = 30       # 机会词难度上限
SV_MIN = 500              # 最小搜索量

# 关键词扩展模式
LONGTAIL_PATTERNS = {
    "steel_types": ["review", "properties", "vs", "heat treat", "composition"],
    "knife_types": ["uses", "types", "vs", "guide", "review"],
    "knife_laws": ["by state", "2026", "legal", "penalty"],
    "maintenance": ["guide", "angle", "stone", "tutorial"],
    "comparison": ["which is better", "difference", "pros and cons"],
}

CONTENT_TYPE_MAP = {
    "Ultimate Guide": "信息型 + 商业型",
    "How-to Tutorial": "信息型",
    "Comparison": "商业型",
    "List Post": "商业型",
    "Informational Post": "信息型",
}


def load_matrix() -> pd.DataFrame:
    """加载选题矩阵"""
    df = pd.read_csv(INPUT_FILE)
    for col in ["Search Volume", "Keyword Difficulty", "Traffic", "priority_score"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df


def filter_keywords(df: pd.DataFrame) -> tuple:
    """筛选关键词"""
    # 高优先级
    high_priority = df[df["priority_score"] > PRIORITY_THRESHOLD].copy()
    
    # 机会词 (低难度高流量)
    opportunities = df[
        (df["Keyword Difficulty"] < KD_OPPORTUNITY) & 
        (df["Search Volume"] > SV_MIN)
    ].copy()
    
    # 按主题筛选 (可选)
    # steel_only = df[df["topic"] == "steel_types"].copy()
    
    return high_priority, opportunities


def expand_keywords(keyword: str, topic: str) -> dict:
    """扩展关键词"""
    kw_lower = str(keyword).lower()
    expansions = {
        "longtail": [],
        "questions": [],
        "comparisons": []
    }
    
    # 长尾扩展
    patterns = LONGTAIL_PATTERNS.get(topic, ["review", "guide", "vs"])
    for pattern in patterns[:3]:
        expansions["longtail"].append(f"{keyword} {pattern}")
    
    # 问题扩展
    expansions["questions"] = [
        f"what is {keyword}",
        f"is {keyword} good",
        f"how to choose {keyword}"
    ]
    
    # 对比扩展 (如果包含 vs 或者是钢材/刀具类型)
    if " vs " in kw_lower or topic in ["steel_types", "knife_types"]:
        expansions["comparisons"] = [
            f"{keyword} vs [competitor]",
        ]
    
    return expansions


def determine_search_intent(content_type: str) -> str:
    """判断搜索意图"""
    return CONTENT_TYPE_MAP.get(content_type, "信息型")


def generate_title_suggestions(keyword: str, content_type: str) -> list:
    """生成标题建议"""
    templates = {
        "Ultimate Guide": [
            f"{keyword}: The Ultimate Guide",
            f"Everything You Need to Know About {keyword}",
        ],
        "How-to Tutorial": [
            f"How to [Action] with {keyword}",
            f"{keyword}: Step-by-Step Tutorial",
        ],
        "Comparison": [
            f"{keyword} vs [Competitor]: Which is Better?",
            f"{keyword} Comparison: Pros, Cons & Verdict",
        ],
        "List Post": [
            f"Best {keyword} for 2026",
            f"Top 10 {keyword} Reviewed",
        ],
        "Informational Post": [
            f"{keyword}: Complete Overview",
            f"What is {keyword}? A Detailed Look",
        ],
    }
    return templates.get(content_type, [f"{keyword}: A Complete Guide"])


def generate_brief(row: pd.Series) -> str:
    """生成单个关键词简报"""
    expansions = expand_keywords(row["Keyword"], row["topic"])
    intent = determine_search_intent(row["content_type"])
    titles = generate_title_suggestions(row["Keyword"], row["content_type"])
    
    brief = f"""## {row["Keyword"]}

**基础数据**:
- 搜索量：{int(row["Search Volume"]):,}
- 难度：{row["Keyword Difficulty"]:.1f}
- 优先级：{row["priority_score"]:.2f}
- 主题：{row["topic"]}
- 内容类型：{row["content_type"]}

**搜索意图**: {intent}

**关键词扩展**:
1. 核心词：{row["Keyword"]}
2. 长尾词:
   - {expansions["longtail"][0] if expansions["longtail"] else "N/A"}
   - {expansions["longtail"][1] if len(expansions["longtail"]) > 1 else "N/A"}
   - {expansions["longtail"][2] if len(expansions["longtail"]) > 2 else "N/A"}
3. 问题词:
   - {expansions["questions"][0]}
   - {expansions["questions"][1]}
4. 对比词:
   - {expansions["comparisons"][0] if expansions["comparisons"] else "N/A"}

**内容建议**:
- 标题建议："{titles[0]}"
- H2 结构:
  - What is {row["Keyword"]}?
  - [Key Feature/Property]
  - [Comparison/Analysis]
  - [Use Cases/Applications]
  - FAQ
- 内部链接目标：
  - /{row["topic"]}/
  - /related-topic/
  - /request-a-quote/

---
"""
    return brief


def generate_report(high_priority: pd.DataFrame, opportunities: pd.DataFrame):
    """生成完整报告"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    report = f"""# 关键词调研简报

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
**数据来源**: blog_topic_matrix_*.csv

---

## 📊 筛选摘要

| 类别 | 数量 | 说明 |
|------|------|------|
| 高优先级选题 | {len(high_priority):,} | priority_score > {PRIORITY_THRESHOLD} |
| 机会词 | {len(opportunities):,} | KD < {KD_OPPORTUNITY} 且 SV > {SV_MIN} |

---

## 🎯 高优先级选题关键词简报

"""
    
    # 按优先级排序，取前 20 个生成详细简报
    top_20 = high_priority.nlargest(20, "priority_score")
    for _, row in top_20.iterrows():
        report += generate_brief(row)
    
    report += """
---

## 💡 机会词列表

| 关键词 | 搜索量 | 难度 | 主题 | 内容类型 |
|--------|--------|------|------|----------|
"""
    
    for _, row in opportunities.nlargest(30, "Search Volume").iterrows():
        report += f"| {row['Keyword']} | {int(row['Search Volume']):,} | {row['Keyword Difficulty']:.1f} | {row['topic']} | {row['content_type']} |\n"
    
    report += """
---

## 📝 使用说明

1. **高优先级选题**: 优先写作，按 priority_score 降序排列
2. **机会词**: 低竞争高流量，适合快速获客
3. **关键词扩展**: 每个选题已自动生成相关长尾词和问题词
4. **内容建议**: 参考标题和 H2 结构建议进行写作

---

## 🔗 工作流

```
选题矩阵 → 筛选高优先级 → 关键词扩展 → 写作简报 → 内容创作
     ↓
competitor-research.md (竞对分析)
     ↓
article-writing.md (正式写作)
```
"""
    
    # 保存报告
    output_file = OUTPUT_DIR / f"keyword_briefs_{timestamp}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"✓ 生成关键词简报：{output_file}")
    
    # 同时导出 CSV
    csv_file = OUTPUT_DIR / f"keyword_briefs_{timestamp}.csv"
    high_priority.to_csv(csv_file, index=False, encoding="utf-8-sig")
    print(f"✓ 导出 CSV: {csv_file}")


def main():
    print("🚀 开始生成关键词调研简报...")
    print("=" * 50)
    
    # 加载数据
    print("\n📂 加载选题矩阵...")
    df = load_matrix()
    print(f"   总选题数：{len(df):,}")
    
    # 筛选
    print("\n🔍 筛选关键词...")
    high_priority, opportunities = filter_keywords(df)
    print(f"   高优先级：{len(high_priority):,}")
    print(f"   机会词：{len(opportunities):,}")
    
    # 生成报告
    print("\n📝 生成关键词简报...")
    generate_report(high_priority, opportunities)
    
    print("\n✅ 完成!")


if __name__ == "__main__":
    main()
```

---

## 使用方法

### 1. 运行漏斗脚本
```bash
cd scripts
python keyword_funnel.py
```

### 2. 查看输出
```
output/keyword_briefs/
├── keyword_briefs_20260331_150000.md    # 关键词调研简报
└── keyword_briefs_20260331_150000.csv   # 筛选后的数据
```

### 3. 工作流整合
```
1. 运行 generate_blog_topics.py
   → 生成选题矩阵

2. 运行 keyword_funnel.py
   → 生成关键词简报

3. 对每个选题应用 keyword-research.md
   → 完成详细关键词调研

4. 应用 competitor-research.md
   → 竞对差距分析

5. 开始写作
```

---

## 筛选条件配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| PRIORITY_THRESHOLD | 100 | 高优先级分数阈值 |
| KD_OPPORTUNITY | 30 | 机会词难度上限 |
| SV_MIN | 500 | 机会词最小搜索量 |

可根据实际情况调整这些参数。
