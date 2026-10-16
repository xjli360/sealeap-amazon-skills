---
name: sealeap-amazon-full-funnel-growth
description: Plan and diagnose evidence-based Amazon full-funnel growth across awareness, consideration, conversion, and loyalty without collapsing brand media, retail readiness, and performance ads into one metric. Use for 全流域营销, 全漏斗营销, 品牌出海, media mix, non-linear customer journey, CTV/online video/social/search coordination, new-to-brand, high-ticket decision journeys, brand-plus-performance measurement, or turning the authorized 2025 Ipsos/Amazon study into an account-specific plan. Default to read-only analysis and a test plan; current availability, policy, and live media changes require verification and explicit approval.
---

# Amazon 全流域增长规划

## 目标

把“全渠道都投一点”改造成可验证的增长系统：确定业务目标与目标人群，画出非线性决策路径，区分各触点职责，连接零售与品牌信号，并用增量或可归因实验决定下一轮预算，而不是用最后点击代替全程贡献。

先读 [references/source-and-guardrails.md](references/source-and-guardrails.md)。需要消费者旅程与渠道角色时读 [references/journey-and-channel-map.md](references/journey-and-channel-map.md)；设计指标和实验时读 [references/measurement-and-experiment.md](references/measurement-and-experiment.md)。

## 核心原则

- `全流域` 是“认知 → 考虑 → 转化 → 忠诚”的协同，不等于所有广告产品同时开启。
- 消费者路径非线性。搜索、详情页、社媒、在线视频、流媒体电视、达人内容、品牌店和复购触点可能往返出现。
- 电商详情页与品牌店是承接中枢；库存、价格、配送、评价和内容质量不足时，扩大媒体只会放大漏损。
- 每个触点只承担一个首要任务，并拥有匹配的指标。不得用 ACOS 单独评价认知，也不得用曝光量证明销售增量。
- 课程研究数据和 TCL、SOJOS 案例是 `SOURCE_SNAPSHOT` / `TRAINING_CASE`，不是当前账户基准、效果承诺或预算配方。
- 默认只读。预算、受众、竞价、投放状态、素材和详情页写入都要逐对象批准。

## 工作流

### 1. 锁定问题与作用域

记录 marketplace、品牌、ASIN/品类、日期、币种、客单价、复购周期、库存、价格、渠道、归因窗口和数据更新时间。只选一个主要问题：认知不足、考虑流失、转化断点、复购不足或跨触点重复浪费。

### 2. 建立证据表

将输入分为：

- `ACCOUNT_FACT`：当前授权账户和站点的可复核数据；
- `CURRENT_POLICY`：本轮从官方来源确认的能力、资格与规则；
- `SOURCE_SNAPSHOT`：课程研究、历史比例、页面路径和案例；
- `HYPOTHESIS`：待验证的消费者或渠道解释；
- `NEEDS_DATA`：缺失后不能继续下结论的字段。

不把调查相关性写成当前品牌因果，不把行业比例写成当前账户人群比例。

### 3. 画决策旅程

至少覆盖：首次发现、主动研究、商品比较、详情页验证、加购/放弃、购买、复购/推荐。对每一步写清：用户问题、现有触点、证据、漏损、下一触点。高客单价商品单独检查更长的研究周期、多次品牌验证和设备切换。

### 4. 分配触点职责

按 [references/journey-and-channel-map.md](references/journey-and-channel-map.md) 给每个渠道分配一个首要任务：扩大合格触达、建立品牌记忆、推动深度访问、捕捉需求、转化或复购。渠道不可用时标 `NOT_AVAILABLE`，不要替换成同名但不同能力的产品。

### 5. 先修零售承接

检查 Featured Offer、库存、价格/优惠、配送、评分、退货原因、详情页事实完整性、移动端首屏、视频/A+、品牌店导航和广告承诺一致性。承接失败时先 `HOLD_MEDIA_SCALE`。

### 6. 建立指标树

每层保留一个主指标和一组护栏：

| 阶段 | 主指标候选 | 护栏 |
|---|---|---|
| 认知 | 增量触达、视频完成、品牌搜索提升 | 频次、可视成本、无效地域 |
| 考虑 | 品牌店/详情页合格访问、互动、加购 | 跳出、重复触达、价格/库存 |
| 转化 | 增量订单、贡献利润、CVR、ROAS | TACOS、自然替代、退货 |
| 忠诚 | 复购、新客后续价值、交叉购买 | 折扣依赖、联系频次、毛利 |

跨层报告时保留归因窗口与去重规则。

### 7. 设计一个可归因实验

只改变一个主要变量：人群、渠道组合、创意、频次、落地页或预算之一。固定其它主要变量，设置基线、对照、样本门槛、最大花费、成功/停止线、归因成熟时间和回退。若无法建立实验或合理对照，只能写关联性观察。

### 8. 审批与复读

若用户要求执行，先展示账户/站点、活动、对象、旧值、新值、预算上限、证据、停止线和回退。批准后只执行明确对象；写后复读状态与实际值。

## 必须交付

- 业务目标、作用域、证据标签和缺口；
- 一张阶段 × 用户问题 × 触点 × 指标的旅程表；
- 当前最大漏损及其证据强度；
- 零售承接检查与 `GO / HOLD`；
- 一个单变量实验卡；
- `DRAFT`、`READY_FOR_REVIEW`、`APPROVED` 或 `HOLD` 状态。

## 2026-10-16 专项更新

处理Full-Funnel Campaigns 试投与长期指标时，先读 [当前专项规则与执行检查](references/update-20261016.md)。其中的未来开放日期和待复核项不能当作当前账户已可用。
