---
name: sealeap-suanni-amazon-fba-fee-size-tier
description: "Classify a product into its Amazon FBA size tier from verified packaged dimensions and weight, compute the fulfilment fee from the current marketplace rate card, and flag packaging changes that would push the unit into a costlier tier. Use for FBA 配送费怎么算、尺寸分段判断、体积重与实重、包装尺寸优化、配送费为什么变贵、改包装能省多少. Do not use as a substitute for the official fee preview in Seller Central, or for marketplaces and product classes whose current rate table has not been loaded."
---

# Amazon FBA 配送费与尺寸分段测算

## 目标

Classify a product into its Amazon FBA size tier from verified packaged dimensions and weight, compute the fulfilment fee from the current marketplace rate card, and flag packaging changes that would push the unit into a costlier tier.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 体积重除数、各分段的边长与重量上限、重量取整档位和费率数字都随站点与年份调整，来源中的具体数值仅作示例，每次计算前以当前费率表为准。
- “包装尺寸多出一点就跨档、费用明显上升”是普遍机制，但跨档的具体位置与差价必须用当前费率表复算，不能沿用旧经验值。
- 手工计算的价值在于建立包装意识与复核能力，不能替代后台费用预览；两者不一致时以官方数值为准并记录差异原因。
- 供应商提供的尺寸重量常与入仓实测不一致，平台以自身测量为准；缺少样品实测时把结果标为估算。

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

1. 先确认站点与当前生效的 FBA 费率表版本，并判断产品适用哪一张费率表（普通品、服装类、危险品各有各的表）；类别依据产品事实与后台分类结果，不凭印象。
2. 用实测的包装后尺寸与重量（不是供应商报的裸品数据）换算成站点单位；按当前费率表的体积重公式算出体积重，与实重取较大值作为计费重量，并记录本品是实重货还是体积货。
3. 按最长边、次长边、最短边与计费重量逐条对照当前尺寸分段的上限，全部满足才归入该档；任一维度超限即落到下一档，并记录触发越级的是哪一个维度。
4. 在对应分段内按费率表的重量档位向上取整，基础费加超出部分的递增费得到配送费；再与后台费用预览或收入计算器交叉核对，不一致时以官方数值为准并查找原因（单位换算、取整、费率版本）。
5. 做包装敏感性分析：把每个维度各加减少量，看是否跨越分段边界，标出离越级还剩多少余量，把余量写进给供应商和包装设计的规格要求。
6. 把配送费与售价、类目佣金放在一起看占比；占比异常高时优先考虑改包装或改规格，而不是直接提价。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 尺寸分段判定表（三边、计费重量与对照结果）
- 配送费计算过程与结果
- 包装越级余量分析与规格建议
- 与官方费用预览的核对记录
- 配送费占售价比例与改包装建议
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。

## 2026-10-16 专项更新

处理旺季履约费与附加费时，先读 [当前专项规则与执行检查](references/update-20261016.md)。其中的未来开放日期和待复核项不能当作当前账户已可用。
