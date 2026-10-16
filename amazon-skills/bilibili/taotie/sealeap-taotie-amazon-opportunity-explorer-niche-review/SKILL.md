---
name: sealeap-taotie-amazon-opportunity-explorer-niche-review
description: "Evaluate a niche in Amazon's Product Opportunity Explorer: locate it by category or head keyword, read search volume and growth over 360 and 90 days, products-sold ranges, average price, top-clicked products and click share, seller and offer counts, search-term expansions, insights and trend tabs, then decide whether demand is outrunning supply and export keywords for listing and ads. Use for 商机探测器怎么用、细分市场数据怎么看、搜索量增长率、点击份额是什么、卖家与供应商数量、同比环比、趋势页怎么判断、从商机探测器找关键词. Do not use when the account lacks access to the tool, or to treat ranges as exact sales figures."
---

# Amazon 商机探测器细分市场评估

## 目标

Evaluate a niche in Amazon's Product Opportunity Explorer: locate it by category or head keyword, read search volume and growth over 360 and 90 days, products-sold ranges, average price, top-clicked products and click share, seller and offer counts, search-term expansions, insights and trend tabs, then decide whether demand is outrunning supply and export keywords for listing and ads.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 售出数量、搜索量均为区间或指数化展示，且工具说明与实际字段可能存在口径差异（来源发现过帮助文档与界面周期不一致），只能判断高低不能当销量事实。
- 「卖家与供应商数量约等于跟卖数」「点击份额约等于市场份额」是来源的近似解读，需在前台核对。
- 工具开放范围与字段随平台迭代变化，来源描述的申请方式与站点范围不再适用，以当前后台为准。
- 来源举例的品类、价格与销量区间不转译。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace、类目、价格带、上架时间与运营模式
- 候选品与同购买意图可比样本的销量、评论、价格和上架时间
- 关键词需求、历史趋势、广告依赖、同款密度和品牌集中度
- 采购、头程、平台费、退货、仓储、交期和合规/IP 基础信息

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 在增长类菜单进入商机探测器，按分类树或输入主关键词定位细分市场（长尾词可能无结果）；确认账户与站点当前是否开放该工具，字段名以当前控制台为准。
2. 读细分市场概览：搜索量与增长（近 360 天与近 90 天）、售出商品数区间、平均价格、潜力评分；优先长周期与短周期增长同向为正的细分市场，并记录区间而非点值。
3. 进入商品页签：看点击最多的商品的点击份额（近似市场集中度）、平均价、评论数与评分、BSR、卖家与供应商数量（近似跟卖与分销情况）；点击份额高度集中说明进入难度高。
4. 进入搜索词页签：提取该细分市场的长尾词与前后顺序、各词点击最多的前几个商品；把款式/颜色偏好与词的对应关系记为主图与变体投放的线索。
5. 看洞察与趋势页签：商品数量、广告商品占比、Prime 占比、前五点击份额、搜索量与商品数的趋势线；搜索量增长快于商品数增长记为「供给未跟上」信号，反之记为竞争加剧。
6. 输出细分市场评估表（需求、增长、集中度、价格带、跟卖风险、关键词清单），并与第三方估算交叉：一方数据优先，冲突时保留各自口径。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 细分市场概览记录
- 商品页签集中度与跟卖观察
- 搜索词清单与款式偏好对应表
- 趋势判断（需求 vs 供给）
- 细分市场评估表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。

## 2026-10-16 专项更新

处理Unmet Demand 与产品定义时，先读 [当前专项规则与执行检查](references/update-20261016.md)。其中的未来开放日期和待复核项不能当作当前账户已可用。
