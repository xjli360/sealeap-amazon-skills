---
name: sealeap-amazon-acos-diagnostics
description: Diagnose Amazon Ads ACOS with reconciled CTR, CPC, CVR, AOV, ROAS, TACOS, placement, search-term, benchmark, attribution, and contribution-margin evidence, then produce a single-variable optimization experiment. Use for ACOS 高低判断, 广告亏损, CTR/CVR/CPC 异常, 盈亏平衡 ACOS, 广告报告诊断, Benchmark 基准, placement 浪费, 搜索词不精准, Listing 转化问题, 广告利润优化, or converting the authorized Amazon Ads metrics course into an account-specific plan. Default to read-only diagnosis and draft; never change live campaigns without explicit human approval.
---

# Amazon Ads ACOS 核心指标诊断

## 目标

把“ACOS 高不高”改写成一条可复核的问题链：先确认策略目标和经济性，再统一数据口径，重算 ACOS 及其驱动项，定位 CPC、CVR、客单价或流量结构断点，最后只提出一个可归因的实验。

先读 [references/source-and-guardrails.md](references/source-and-guardrails.md)。需要公式与指标口径时读 [references/metric-system.md](references/metric-system.md)，需要完整诊断树时读 [references/diagnostic-tree.md](references/diagnostic-tree.md)。课程案例只能结合 [references/case-study-and-caveats.md](references/case-study-and-caveats.md) 使用；需要 Benchmark 算法与误读防护时读 [references/benchmark-methodology.md](references/benchmark-methodology.md)。

## 核心原则

- `ACOS = 广告花费 ÷ 广告归因销售额 × 100%`，也可在同一口径下拆为 `CPC ÷ (CVR × 广告订单客单价) × 100%`。
- ACOS 是结果指标，不是所有广告目标的唯一评价标准。测试、守位、品牌获客、推排名和成熟品利润的主目标不同。
- 盈亏判断使用“扣除商品成本、平台费用、履约、折扣、退货等广告外可变成本后的贡献毛利率”。缺少完整成本时不得把普通毛利率写成精确盈亏线。
- 广告归因销售额与总销售额不得混用；ACOS、TACOS、ROAS 必须分别命名。
- 不跨 marketplace、profile、币种、广告类型、归因窗口、日期或层级直接拼接。
- Benchmark 是同业参照，不是目标或因果解释。当前可用性、同业组、分位数与指标定义必须在控制台/API 重新确认。
- 默认只读。任何 bid、budget、placement、target、否定词、状态或结构变更均需逐对象人工批准。

## 先声明模式

1. `DIAGNOSE`：重算和定位，不生成变更；默认；
2. `DRAFT`：生成单变量实验草案；
3. `RELEASE_PREP`：生成审批卡、旧值/新值、停止线和回退；
4. `APPROVED_WRITE`：只执行用户本轮明确批准的一个动作，写后复读。

## 核心工作流

### 1. 先问“这轮广告要完成什么”

只选一个主目标：

| 目标 | 首要判断 | ACOS 的位置 |
|---|---|---|
| 测试商品/查询 | 相关性与有效样本 | 护栏，不是首要结果 |
| 防守 | 关键流量是否守住且经济可承受 | 与覆盖、份额、利润并看 |
| 品牌获客 | 品牌新客与后续价值 | 与新客成本、店铺行为并看 |
| 推排名 | 排名/自然贡献是否改善 | 与总利润、TACOS、库存并看 |
| 成熟品利润 | 贡献利润和现金效率 | 关键结果之一 |

若用户只说“把 ACOS 降低”，先确认降低 ACOS 是否会伤害本轮主目标。证据不足时仍可继续只读诊断，但把目标标为 `NEEDS_DATA`。

### 2. 锁定分析作用域

记录：

- 已验证的 seller、marketplace、广告 profile 和授权范围；
- 日期、时区、币种、广告类型、归因窗口、数据更新时间；
- 分析层级：portfolio / campaign / ad group / target / search term / placement / advertised ASIN；
- 当前价格、优惠、库存、Featured Offer、评分、配送和 Listing 变更；
- 单位经济：售价、折扣、COGS、FBA/佣金/履约、退货/退款、其它可变成本。

不要用账户汇总 ACOS 直接解释某个词，也不要用某个词的 CTR 替代 campaign 目标表现。

### 3. 先重算，不信任表格中的派生值

准备 JSON 后运行：

```bash
python3 scripts/acos_diagnose.py --input references/acos-input.example.json
```

至少提供 `impressions / clicks / spend / orders / ad_sales`。脚本会计算 CTR、CPC、CPM、CVR、AOV、CPA、ACOS、ROAS，以及可选 TACOS，并对上报指标做一致性检查。

遇到以下情况先 `HOLD` 或降级结论：

- 广告销售额为 0：ACOS 未定义，不写成 0%；
- 点击为 0：CPC/CVR 未定义；
- 数据为负、订单大于点击、点击大于曝光等明显口径问题；
- `spend ≠ CPC × clicks`、`ad_sales ≠ AOV × orders` 超出舍入误差；
- 归因未成熟、退款未回写或多个币种混合。

### 4. 与经济性对齐

优先计算：

```text
break_even_acos = contribution_margin_before_ads / revenue
ad_contribution_profit = ad_sales × contribution_margin_rate - ad_spend
tacos = ad_spend / total_sales
```

分别报告“广告归因贡献利润”和“全店/ASIN 总贡献”。ACOS 低于盈亏线不自动证明广告增量盈利；仍需考虑自然替代、品牌词截流、退货、库存和边际效果。

### 5. 拆解 ACOS 驱动项

依次回答：

1. ACOS 是否真的影响当前主目标？
2. CPC 是否上升，来自 bid、placement、竞争、匹配结构还是流量迁移？
3. CVR 是否下降，来自搜索词不相关、Listing、价格/优惠、评价、配送、库存还是变体？
4. 广告订单客单价是否变化，来自 SKU 组合、折扣、捆绑或归因结构？
5. 各层汇总是否被少数 placement、target、search term 或 ASIN 淹没？

用 [references/diagnostic-tree.md](references/diagnostic-tree.md) 输出“观察 → 重算 → 可能解释 → 排除证据 → 根因置信度 → 下一步”。不要把同时发生当成因果。

### 6. 使用 Benchmark 只做参照

课程 2026 快照描述了品牌维度 Benchmark，可比较 CTR、CPC、CPM、新客购买占比/购买率/单次购买成本和视频指标，并提到 25/50/75 分位及同行组隐私门槛。

使用前：

1. 在当前 marketplace、广告类型与账户确认可见性；
2. 保存同业组、分位数、日期、指标定义和样本覆盖；
3. 只比较同层级、同时间窗、同广告产品；
4. Benchmark 异常只定位“值得查的指标”，不直接给动作。

课程对“平均值”和“中位数”表述不完全一致；未拿到当前字段定义时标 `NEEDS_DATA`。

### 7. 深挖断点

#### CPC 偏高

- 分 placement、target/search term、match type、日期和设备/素材能力可见维度；
- 检查当前 bid、动态竞价、placement 加价、预算抢量和竞争期；
- 同时看 CVR 与点击价值。高 CPC 但高贡献利润不必机械降低。

#### CTR 偏低

- 先区分流量不匹配与创意/商品卡问题；
- 检查主图、标题前段、价格、优惠、评分、配送、广告位置和竞品差异；
- 不在同一实验同时改主图、标题和竞价。

#### CVR 偏低

- 先看 search term/ASIN 相关性，再看详情页；
- 检查商品事实、图片/视频/A+、价格、评价、配送、变体、退货和库存；
- 不因单个低转化词的少量点击立即否定；按账户利润和归因窗口定义证据要求。

#### 客单价偏低

- 区分促销、低价子体、交叉销售和归因组合变化；
- “提高客单价/捆绑”只是候选策略，必须重算 CVR、利润、库存和合规影响。

### 8. 生成一个单变量实验

一张实验卡只允许一个 `store + campaign + unique ad group + main variable`。必须包含：

- 主目标和战略理由；
- 基线窗口、当前值、数据量、归因成熟度；
- 唯一动作、旧值、新值、最大花费；
- 冻结变量；
- 成功、停止、回退和风险护栏；
- 预期观察指标与不应受损指标；
- 人工确认状态。

若根因在 Listing，广告侧先保持不变，另建 Listing 实验；若根因在竞价，不同时加否词。

### 9. 审批与复读

进入 `RELEASE_PREP` 后逐项展示 profile、campaign、ad group、target/placement、旧值、新值、证据、影响范围、花费上限和回退。只有用户本轮明确确认后才能写。

写后复读 Amazon 返回和控制台/报告状态。请求接受只写“已提交”，复读确认后才写“已生效”。

## 必须交付

按 [references/output-contract.md](references/output-contract.md) 输出：

- 目标、授权、口径、归因成熟度和数据质量；
- 重算指标、经济性和派生值一致性；
- ACOS → CPC/CVR/AOV → placement/target/search term/Listing 的诊断链；
- Benchmark 的适用范围与局限；
- 一个单变量实验卡、审批对象与回退；
- `DRAFT`、`READY_FOR_REVIEW`、`APPROVED` 或 `HOLD`。

## 2026-10-16 专项更新

处理智能诊断与自动优化状态时，先读 [当前专项规则与执行检查](references/update-20261016.md)。其中的未来开放日期和待复核项不能当作当前账户已可用。
