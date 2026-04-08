# SKILL-05: 产品对比表格

**用途**: 生成对比表格
**适用**: 钢材对比文章、排行榜文章

---

## 结构模板

```markdown
## Comparison Table: [主题 A] vs. [主题 B]

![对比图片](https://img.leeknives.com/wp-content/uploads/YYYY/MM/图片名.jpg)

In the comparison table below, you'll find the features, pros, and cons of [A] and [B].

|  | [主题 A] | [主题 B] |
| --- | --- | --- |
| Features | 特点 1<br>特点 2 | 特点 1<br>特点 2 |
| Pros | 优点 1<br>优点 2 | 优点 1<br>优点 2 |
| Cons | 缺点 1<br>缺点 2 | 缺点 1<br>缺点 2 |
```

---

## 评分表格示例（S30V vs S35VN）

```markdown
|  | **S30V** | **S35VN** |
| --- | --- | --- |
| **Hardness** | 58 - 61 HRc | 58 - 61 HRc |
| **Edge Retention** | 7/10 | 6/10 |
| **Toughness** | 5/10 | 4/10 |
| **Corrosion Resistance** | 7/10 | 4/10 |
| **Sharpening Ease** | 7/10 | 8/10 |
| **Price** | Moderate | Moderate |
```

---

## 完整对比表格模板（M390 vs S30V vs S35VN）

```markdown
## Comparison Table: M390 vs S30V vs S35VN

![M390 vs S30V vs S35VN comparison](https://img.leeknives.com/wp-content/uploads/2024/01/m390-s30v-s35vn-comparison.jpg)

In the comparison table below, you'll find the key differences between M390, S30V, and S35VN stainless steels.

| Feature | M390 | S30V | S35VN |
| --- | --- | --- | --- |
| **Hardness (HRC)** | 60 - 62 | 58 - 61 | 58 - 61 |
| **Edge Retention** | 9/10 | 7/10 | 6/10 |
| **Toughness** | 4/10 | 5/10 | 4/10 |
| **Corrosion Resistance** | 9/10 | 7/10 | 4/10 |
| **Wear Resistance** | 9/10 | 8/10 | 7/10 |
| **Sharpening Ease** | 5/10 | 7/10 | 8/10 |
| **Price Range** | High | Moderate | Moderate |
| **Best For** | Premium EDC | All-around use | Tough tasks |
| **Carbon** | 1.90% | 1.45% | 1.40% |
| **Chromium** | 20.00% | 14.00% | 14.00% |
| **Vanadium** | 4.00% | 4.00% | 3.00% |
```

**数据来源引用（每条数据 1-2 个来源即可）：**

| 数据类型    | 引用来源                                                                                   |
| ------- | -------------------------------------------------------------------------------------- |
| 成分数据    | Bohler M390 TDS: https://www.bohler-edelstahl.com/en/products/m390-microclean/         |
| 成分数据    | Crucible S30V/S35VN: https://nsm-ny.com/content/uploads/2021/07/CPM-S30V-WITH-TAGS.pdf |
| 硬度/性能数据 | Knife Steel Nerds: https://knifesteelnerds.com/                                        |

---

## 引用规范

**原则**：每条数据只引用 1-2 个最权威的来源，优先使用原厂数据表（TDS）。

**格式：**

```markdown
> [数据内容]
> 来源：[来源名称]，[真实有效的 URL]，[年份]
```

**正确示例：**

```markdown
> M390 硬度：60-62 HRC
> 来源：Bohler M390 MICROCLEAN Data Sheet, https://www.bohler-edelstahl.com/en/products/m390-microclean/, 2024

> S30V 成分：C 1.45%, Cr 14%, V 4%
> 来源：Crucible CPM S30V Data Sheet, https://nsm-ny.com/content/uploads/2021/07/CPM-S30V-WITH-TAGS.pdf, 2024
```

**错误示例（避免）：**

```markdown
❌ 来源：crucible.com（URL 不完整）
❌ 来源：https://www.crucible.com/eselector/（链接已失效）
❌ 来源：网络资料（无具体 URL）
```

---

## 数据可靠性分级

| 等级    | 来源类型              | 可信度     |
| ----- | ----------------- | ------- |
| ★★★★★ | 原厂技术数据表（TDS）      | 最权威     |
| ★★★★☆ | Knife Steel Nerds | 独立实验室数据 |
| ★★★☆☆ | ZKnives           | 行业通行参考  |
| ★★☆☆☆ | 社区 Wiki/论坛        | 需交叉验证   |
| ★☆☆☆☆ | 无来源博客             | 不应引用    |

---

## 常用权威来源 URL

| 钢材品牌                | 官方数据源 URL                                                         |
| ------------------- | ----------------------------------------------------------------- |
| Bohler M390         | https://www.bohler-edelstahl.com/en/products/m390-microclean/     |
| Crucible CPM S30V   | https://nsm-ny.com/content/uploads/2021/07/CPM-S30V-WITH-TAGS.pdf |
| Crucible CPM S35VN  | https://nsm-ny.com/content/uploads/2021/07/CPMS35VNds.pdf         |
| Knife Steel Nerds   | https://knifesteelnerds.com/                                      |
| ZKnives Steel Chart | https://zknives.com/knives/steels/index.shtml                     |
