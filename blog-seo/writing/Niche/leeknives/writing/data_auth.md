---
name: steel-data
description: >
  查询和展示钢材成分、硬度、性能等技术数据时使用此 Skill。触发场景包括：
  用户询问某型号钢材的元素成分（C/Cr/V/Mo 等）、硬度指标（HRC/HV/HB）、
  热处理参数、韧性对比、刃具钢选材建议、刀具钢 / 工具钢 / 不锈钢性能比较，
  或需要给出权威引用来源时。无论用户是否明确要求"引用"，只要涉及钢材数据，
  都应激活此 Skill，确保数据来源可溯。

---

## 数据类别与权威引用源

### 1. 钢材元素成分表（Chemical Composition）

| 来源                             | 网址 / 说明                                           | 适用范围                 |
| ------------------------------ | ------------------------------------------------- | -------------------- |
| **ZKnives Steel Chart**        | https://zknives.com/knives/steels/index.shtml     | 刀具钢元素成分总览，社区最广泛引用    |
| **Knife Steel Nerds**          | https://knifesteelnerds.com                       | 深度冶金分析，含元素作用原理       |
| **AZO Materials**              | https://www.azom.com                              | 工业钢材成分与规格，含学术级数据     |
| **Bohler-Uddeholm 官方**         | https://www.bohler.com / https://www.uddeholm.com | 奥地利/瑞典高端工具钢原厂数据表     |
| **Crucible Industries**        | https://www.crucible.com                          | CPM 系列粉末钢原厂成分与性能     |
| **Hitachi Metals (Proterial)** | https://www.proterial.com                         | ZDP-189、HAP 系列等日系钢原厂 |
| **Carpenter Technology**       | https://www.cartech.com                           | CTS 系列及特种不锈钢         |
| **ASSAB (Voestalpine)**        | https://www.assab.com                             | 工具钢 / 模具钢技术数据        |

---

### 2. 硬度指标（Hardness — HRC / HV / HB）

> **原则**：硬度数据应优先来自钢材原厂的技术数据表（TDS / Data Sheet），
> 因为同一牌号的最优热处理参数因炉批和用途而异。

| 来源                                | 说明                                                   |
| --------------------------------- | ---------------------------------------------------- |
| **Bohler Uddeholm TDS PDF**       | 每个牌号有独立 Data Sheet，含淬火/回火曲线与对应 HRC                   |
| **Crucible CPM Data Sheets**      | https://www.crucible.com/eselector — 含 HRC vs 回火温度曲线 |
| **Hitachi Metals Technical Data** | ZDP-189 等可达 67–69 HRC，原厂给出处理窗口                       |
| **Knife Steel Nerds 测试数据**        | 独立测试，含淬火温度、回火次数与实测 HRC，可信度高                          |
| **ZKnives 硬度列 (Typical HRC)**     | 行业通行参考值，注意标注为"典型值"而非厂商保证值                            |
| **Larrin Thomas 著作**              | *Knife Engineering* (2020)，含系统性硬度与韧性实验数据             |

---

### 3. 韧性 / 耐磨性 / 耐腐蚀性（Toughness / Wear Resistance / Corrosion）

| 来源                         | 说明                             |
| -------------------------- | ------------------------------ |
| **Knife Steel Nerds 图表系列** | 含各钢材韧性对比柱状图（查摆锤冲击数据）           |
| **Crucible Selector Tool** | 提供耐磨性/韧性/耐腐蚀的相对评分矩阵            |
| **Bohler 产品选择矩阵**          | 提供工具钢性能雷达图对比                   |
| **CATRA 切割测试**             | 英国刀具研究协会，标准化切割持久性测试（CATRA TCC） |

---

### 4. 热处理参数（Heat Treatment）

| 来源                       | 说明                                                   |
| ------------------------ | ---------------------------------------------------- |
| **各原厂 TDS（首选）**          | Bohler / Crucible / Hitachi 均提供淬火温度、保温时间、回火曲线        |
| **Peters Heat Treating** | https://www.petersheatreating.com — 专业刀具钢热处理服务商，公开指南 |
| **Alpha Knife Supply**   | 含常见刀具钢热处理参数整理                                        |
| **Knife Steel Nerds 文章** | 有各牌号热处理实验与建议                                         |

---

### 5. 标准与规范（Standards）

| 来源                     | 说明                                        |
| ---------------------- | ----------------------------------------- |
| **ASTM International** | https://www.astm.org — 美标工具钢（如 A681、A597） |
| **DIN / EN 标准**        | 欧洲钢材标准，如 DIN 1.4116 对应 X50CrMoV15         |
| **JIS 标准（日本）**         | JIS G 4404 工具钢，如 SKD11 = D2 类             |
| **GB 标准（中国）**          | GB/T 1299 合金工具钢，如 Cr12MoV                 |

---

## 引用规范（Citation Format）

在给出钢材数据时，**必须**按以下格式标注来源：

```
[数据内容]
来源：[来源名称]，[URL 或文档名]，[访问/发布年份（若知）]
```

**示例：**

> S35VN 的典型成分：C 1.45%，Cr 14%，V 3%，Mo 2%，Nb 0.5%  
> 来源：Crucible Industries CPM S35VN Data Sheet，crucible.com，2023

> 在 1066°C 淬火 + 177°C 双回火后，典型 HRC 为 59–61  
> 来源：Crucible CPM S35VN Technical Data Sheet

---

## 数据可靠性分级

```
★★★★★  原厂技术数据表（TDS）—— 最权威
★★★★☆  Knife Steel Nerds（独立实验室数据）
★★★☆☆  ZKnives（行业通行参考，众包整理）
★★☆☆☆  社区 Wiki / 论坛（需交叉验证）
★☆☆☆☆  无来源博客文章（不应引用）
```

---

## 工作流程

1. **识别钢材牌号** — 确认用户意图（成分？硬度？对比？选材？）
2. **选择数据类别** — 对照上方表格选取最佳来源
3. **优先查原厂** — 如有厂商 TDS，优先使用；无法确认时使用 ZKnives / KSN 作为参考
4. **标注引用** — 每条关键数据都注明来源
5. **说明局限** — 若数据为"典型值"而非"保证值"，应明确说明
6. **如数据不确定** — 建议用户访问原厂官网或联系热处理服务商确认

---

## 常见钢材原厂数据表直接入口

```
Bohler M390:    bohler.com → Products → M390 MICROCLEAN
Crucible CPM:   crucible.com/eselector
Uddeholm:       uddeholm.com → Steel Products
Hitachi ZDP-189:proterial.com（原 Hitachi Metals）
Carpenter CTS:  cartech.com → Products → Stainless
Sandvik 14C28N: materials.sandvik → Knife steel
```

---

## 附：常用钢材牌号对照（标准体系）

| 常用名  | 美标     | 欧标 DIN               | 日标 JIS  |
| ---- | ------ | -------------------- | ------- |
| D2   | T30402 | 1.2379 (X153CrMoV12) | SKD11   |
| 440C | S44004 | 1.4125 (X105CrMo17)  | SUS440C |
| O1   | T31501 | 1.2510 (100MnCrW4)   | SKS3    |
| H13  | T20813 | 1.2344 (X40CrMoV5-1) | SKD61   |
| M2   | T11302 | 1.3343 (HS6-5-2)     | SKH51   |
