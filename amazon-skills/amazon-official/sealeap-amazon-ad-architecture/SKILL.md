---
name: sealeap-amazon-ad-architecture
description: "Build and diagnose a profit-aware Amazon advertising architecture by working backward from stage-level sales and profit goals into inventory, keyword priorities, campaign roles, budgets, and measurable experiments across SP, SB, SBV, SD, keyword targeting, product targeting, and seasonal launch phases. Use for 精品广告架构, 亚马逊广告架构搭建, ASIN 推广计划, 季节性新品预算, 销量利润倒推, 关键词分层/竞争度/SPR/CPR, SP SB SBV SD 组合, 红海类目投放, 广告预算分配, 关键词首页计划, 周复盘, 或根据《如何搭建一个精品的广告架构》形成可审批方案. Default to analysis and draft; do not change live campaigns or claim organic-rank causality without verified account evidence and human approval."
---

# SeaLeap 亚马逊广告架构

围绕阶段销量和退货后利润构建广告组合，而不是按广告类型堆 Campaign。先算经营上限，再选择关键词和各广告活动的职责，最后用周复盘和单变量实验调整。

## 强制边界

- 把源 PPTX 中的日期、客单价、利润率、退货/仓储占比、搜索量区间、SPR/CPR、PPC、预算比例、订单和 ACOS 标记为 `TRAINING_CASE`，不得直接套入当前 ASIN。
- 不承诺“投广告即可把关键词推上首页”。自然排名受相关性、转化、销量、竞争和平台机制共同影响，只能把排名变化设为伴随指标。
- 使用当前账户的广告报告、业务报告、库存、退货、价格、费用和 Listing 证据；数据不足时输出 `HOLD / NEEDS_DATA`，不编数。
- 对不明确的缩写（如材料中的 SPM、SPA、KT、LW、MD、BP/BPE、CT）先建立数据字典，不猜测后执行。
- 广告可用性、归因、竞价策略、placement 和政策以当前站点/控制台为准。
- profile/store/ASIN/SKU 是业务对象，不是授权。生产写入必须绑定服务端已验证 scope，并逐项人工确认。
- 一张实验卡只改一个主变量；不要同时改 Listing、价格、Coupon、预算、竞价、匹配方式和创意后声称因果。

阅读 [references/source-and-guardrails.md](references/source-and-guardrails.md) 获取 PPTX 页码映射、案例口径与限制。

## 工作流

### 1. 固定对象和目标

记录 marketplace、profile、ASIN/SKU/父子体、品类、生命周期/季节、价格、销量目标、利润目标、旺季截止、库存、补货周期和负责人。

将目标按阶段拆开，每阶段只保留：日期、目标单位数、最低利润/最大可接受亏损、关键词/人群任务和停止条件。不要只写“提高销量”。

### 2. 倒推经济上限

用真实费用计算净收入、退货后贡献利润、盈亏平衡 ACOS/CPA 和最大广告花费。广告预算不得超过经营上限、库存上限或季节剩余机会中的最小值。

使用 [references/economics-and-stages.md](references/economics-and-stages.md) 的公式和三阶段模板。源材料的 $50 季节品案例只用于演示算法。

### 3. 建关键词/商品机会表

从搜索词、Search Query Performance/Brand Analytics、广告报告和当前可用的第三方研究取得证据。逐个验证相关性、意图、搜索量、CPC、CVR、竞争、自然/广告位置和利润容量。

按核心/中等/长尾/场景/竞品意图分层，不用固定 10 万/1 万搜索量阈值。使用 [references/keyword-plan.md](references/keyword-plan.md)。

### 4. 为每个阶段分配广告职责

按任务选择广告类型：

- SP 自动用于发现，SP 手动用于验证关键词/商品定向；
- SB/SBV 用于品牌入口、视频卖点和额外搜索承接；
- SD 用于当前可用的商品/受众再营销或扩展；
- 只有具备资格、素材、落地页和可归因目标时才分配预算。

用 [references/campaign-portfolio.md](references/campaign-portfolio.md) 设计 Campaign/Ad Group、匹配与预算，不复制案例百分比。

### 5. 处理红海/高竞争场景

当核心大词的 SP 成本超过利润容量时，不用更高出价掩盖问题。先验证 Listing/价格/评论/库存，再比较 SB/SBV、商品定向、长尾和 SD 是否带来可盈利增量。

阅读 [references/red-ocean-playbook.md](references/red-ocean-playbook.md)；材料中“SB 带来 210 单、占广告订单 40%”只属于一个 2023 年讲师案例。

### 6. 形成可审批架构

输出阶段目标、经济模型、关键词任务、Campaign map、预算、样本门槛、单变量动作卡与回退值。使用 [references/output-contract.md](references/output-contract.md)。

### 7. 周复盘与降档

- 同时看广告销售、自然销售、总销售、TACOS、退货后利润、库存和关键词位置；不要只看 ACOS。
- 标记价格、优惠、评论、断货、竞品、季节和归因延迟等干扰项。
- 依据预设样本/日期判断 `KEEP`、`ITERATE`、`ROLLBACK` 或 `STOP`。
- 旺季剩余时间短于学习/补货/回收窗口时停止扩量并执行降档。

## 必须交付

- 对象、授权、数据窗口、数据覆盖和口径；
- 分阶段销量、利润、库存和季节截止；
- 最大广告花费、盈亏平衡 ACOS/CPA 与计算假设；
- 关键词/商品定向优先级及每个词的阶段任务；
- SP/SB/SBV/SD 的职责、Campaign map、预算和资格；
- `ACCOUNT_FACT`、`CURRENT_POLICY`、`TRAINING_CASE`、`HYPOTHESIS` 分离；
- 单变量实验、逐项审批、停止条件、回退值和未解决风险。

信息不足时交付取数清单与 `HOLD`，不要为了填满架构而制造 Campaign。

## 2026-10-16 专项更新

处理智能诊断与自动优化状态时，先读 [当前专项规则与执行检查](references/update-20261016.md)。其中的未来开放日期和待复核项不能当作当前账户已可用。
