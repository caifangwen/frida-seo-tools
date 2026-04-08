# SKILL-07: 内部链接与外部链接植入

**用途**: 在文章中自然植入内部链接和外部权威链接
**适用**: 所有文章类型（横切关注点）

---

## 链接密度规则

### 内部链接
- 每 300-400 字至少 1 个内部链接
- 开篇 2 段必须有 1-2 个链接
- 每个主要章节至少 1 个链接
- 文章结尾必须有 CTA 链接

### 外部链接
- 每 500-800 字可添加 1 个外部权威链接
- 仅链接到标准组织、行业协会、政府网站
- 避免链接到竞争对手网站
- 外部链接使用 `rel="nofollow"` 属性

---

## 链接格式

### 内部链接
```markdown
[链接文字](https://example.com/页面路径/)
```

### 外部链接（带 nofollow）
```markdown
[链接文字](https://authority-site.org/page){: rel="nofollow" target="_blank"}
```

或 HTML 格式：
```html
<a href="https://authority-site.org/page" rel="nofollow" target="_blank">链接文字</a>
```

---

## 内部链接类型

| 类型   | 示例 URL                                         | 优先级 |
| ---- | ---------------------------------------------- | ------ |
| 产品页面 | `https://example.com/stainless-steel-flanges/` | ⭐⭐⭐ |
| 分类页面 | `https://example.com/flange-types/`            | ⭐⭐⭐ |
| 知识页面 | `https://example.com/asme-b16-5-standard/`     | ⭐⭐ |
| 联系页面 | `https://example.com/request-a-quote/`         | ⭐⭐⭐ |
| 选型指南 | `https://example.com/valve-selection-guide/`   | ⭐⭐ |

---

## 外部链接类型（权威来源）

| 类型 | 示例网站 | 用途 |
|------|----------|------|
| 标准组织 | ASME (asme.org), API (api.org), ASTM (astm.org) | 引用标准规范 |
| 政府机构 | OSHA (osha.gov), DOT (dot.gov) | 安全法规引用 |
| 行业协会 | AWS (aws.org), NACE (nace.org) | 行业最佳实践 |
| 技术文档 | NIST (nist.gov), ISO (iso.org) | 技术参数参考 |

---

## 锚文本规范

### 内部链接
```
✅ 正确：[316 stainless steel flanges](https://example.com/316-stainless-flanges/)
✅ 正确：[ASME B16.5 flange dimensions](https://example.com/asme-b16-5-dimensions/)
❌ 错误：[点击这里](https://example.com/316-stainless-flanges/)
❌ 错误：[here](https://example.com/316-stainless-flanges/)
```

### 外部链接
```
✅ 正确：[ASME Section IX welding qualification](https://www.asme.org/codes-standards/find-codes-standards/section-ix){: rel="nofollow" target="_blank"}
✅ 正确：[AWS D1.1 Structural Welding Code](https://www.aws.org/){: rel="nofollow" target="_blank"}
❌ 错误：[check this website](https://www.asme.org/){: rel="nofollow" target="_blank"}
```

规则：锚文本必须是描述性关键词，不使用"click here"或"here"之类的无意义文字。

---

## 自然植入示例

### 内部链接示例

```markdown
Among the various flange materials available, [stainless steel 316](https://example.com/316-stainless-flanges/) offers superior corrosion resistance in chloride environments.

The [ASME B16.5 standard](https://example.com/asme-b16-5-guide/) defines pressure-temperature ratings for steel flanges from Class 150 to Class 2500.

For projects requiring certified components, [API 6D valves](https://example.com/api-6d-valves/) provide reliable performance in pipeline applications.

When selecting flanges for high-pressure systems, consider the [pressure rating chart](https://example.com/flange-pressure-ratings/) to ensure safe operation.

For bulk orders and OEM requirements, [request a quote](https://example.com/request-a-quote/) from our sales team.
```

### 外部链接示例

```markdown
According to [ASME Section IX](https://www.asme.org/codes-standards/find-codes-standards/section-ix){: rel="nofollow" target="_blank"}, welding procedure qualification requires mechanical testing of test coupons.

The [NACE MR0175 standard](https://www.nace.org/standards/standards-detail/mr0175-iso-15156){: rel="nofollow" target="_blank"} specifies material requirements for sour service applications.

For workplace safety guidelines, refer to [OSHA welding safety standards](https://www.osha.gov/welding-cutting-brazing){: rel="nofollow" target="_blank"}.
```

---

## 内部链接网络建议

在文章中优先链接以下高价值页面：

1. `/request-a-quote/` — 每篇文章结尾必须出现
2. 相关产品分类页面 — 法兰/阀门/管件分类页
3. 技术标准解读页面 — ASME/API/ASTM 标准说明
4. 选型指南页面 — 帮助客户选择合适产品
5. 材质说明页面 — 不锈钢/碳钢/合金钢对比

---

## CTA 链接位置

### 文中 CTA（长文章插入）

```markdown
Looking for reliable [stainless steel flanges](https://example.com/stainless-steel-flanges/) suppliers? [Request a free quote](https://example.com/request-a-quote/) for your project.

Need help selecting the right [welding procedure](https://example.com/wps-qualification/)? [Contact our engineering team](https://example.com/request-a-quote/) for technical support.
```

### 结尾 CTA

```markdown
## Conclusion

[Company Name] supplies certified [pipe fittings](https://example.com/pipe-fittings/) and [flanges](https://example.com/flanges/) to industries worldwide. [Contact us today](https://example.com/request-a-quote/) for competitive pricing and fast delivery.

For technical inquiries about [ASME standards](https://example.com/asme-standards-guide/) or custom specifications, our engineering team is ready to assist. [Get a free consultation](https://example.com/request-a-quote/).
```

---

## 链接检查清单

在发布文章前，确认以下链接要求：

- [ ] 开篇 2 段内至少有 1 个内部链接
- [ ] 每个 H2 章节至少有 1 个内部链接
- [ ] 文章结尾有 CTA 链接到询价页面
- [ ] 外部链接仅链接到权威网站（标准组织/政府/协会）
- [ ] 所有外部链接添加 `rel="nofollow"` 和 `target="_blank"`
- [ ] 锚文本是描述性关键词，不是"click here"
- [ ] 内部链接路径正确，无 404 错误
- [ ] 链接密度适中（每 300-400 字 1 个内部链接）

---

## 链接层级优先级

```
P0 - 必须链接（每篇文章）
├── /request-a-quote/ (结尾 CTA)
└── 核心产品分类页

P1 - 优先链接（相关主题）
├── 技术标准解读页面
├── 选型指南页面
└── 材质对比页面

P2 - 可选链接（丰富内容）
├── 相关博客文章
├── 常见问题页面
└── 行业应用案例
```
