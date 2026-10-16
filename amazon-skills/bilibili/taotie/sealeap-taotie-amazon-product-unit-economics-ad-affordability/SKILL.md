---
name: sealeap-taotie-amazon-product-unit-economics-ad-affordability
description: "Turn a product candidate into unit economics: pull sourcing quotes by feature configuration, set the target price from the market band and coupon practice, run a profit calculator with an explicit ad-cost assumption, then convert the per-unit ad budget into affordable clicks and the conversion rate required at an estimated CPC to decide whether the launch is fundable. Use for 选品利润怎么算、广告费算营业额百分比还是广告订单百分比、低单价能不能做、每单能烧多少广告、需要多少转化率、货源平台报价差异、新品期 ACOS 给多少. Do not use to set live campaign budgets or to replace a full landed-cost model with duties and returns."
---

# Amazon 选品单位经济与广告承受力测算

## 目标

Turn a product candidate into unit economics: pull sourcing quotes by feature configuration, set the target price from the market band and coupon practice, run a profit calculator with an explicit ad-cost assumption, then convert the per-unit ad budget into affordable clicks and the conversion rate required at an estimated CPC to decide whether the launch is fundable.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源示例的售价、成本、利润率、CPC 与 ACOS 数字均为案例经验值，不作阈值；每个数字都要用本类目当前报价与广告数据替换。
- 「新品期广告占比可以很高」「自然单会随广告单上升」是来源经验，自然单占比随类目与阶段变化，需用本店数据校准。
- 利润计算器结果不含退货、长期仓储费、关税变动与汇率，本 Skill 只回答广告承受力，不替代完整落地成本模型。
- 来源的货源平台与工具推广内容不采纳；询价时区分贸易商与厂家只是判断价格水位的方法。

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

1. 先明确目标售价：取头部主流价格带而非最低价，新品可在其基础上留出折扣或优惠券空间；售价用历史价格区间校验，避免拿促销价当常态价。
2. 采购成本按功能配置分别询价（带线/不带线、带支架/不带、带电池/不带、带屏/不带），询价对象区分贸易商与源头厂家；把用户真正买单的核心卖点与其成本增量对应起来，不用最低配报价代表整品。
3. 在利润计算器类工具里填入售价、采购、头程与平台费用，广告成本先按显式假设填写；明确该百分比是「广告花费占总营业额」还是「占广告订单」，两种口径下的利润差异分别列出。
4. 反推广告承受力：每单可分配的广告费 ÷ 估算 CPC = 可购买的点击数，1 ÷ 点击数 = 需要的转化率；把所需转化率与本类目常见转化区间比较，若明显高于可达水平则该价位无法用广告推动。
5. 同一需求下比较不同价位方案：售价更高但销量较小的方案往往每单广告预算更大、成功概率更高；把「每单广告预算」「所需转化率」「当前评分与评论数」三项并列作为取舍依据。
6. 新品期允许广告占比阶段性高于长期目标，但要写明退出条件（自然单比例达到多少、ACOS 回落到盈亏平衡线内）；自然单占比的假设（来源经验为广告单与自然单三七到四六）标为待验证。
7. 输出每个候选的单位经济表与「可推/不可推」判断，附所有假设值；只有通过测算的候选进入打样与合规检查。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取竞品价格区间、估算 CPC 与类目转化参考的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 目标售价与价格带依据
- 分配置采购报价表
- 单位经济计算表（含广告口径说明）
- 广告承受力反推表（点击数/所需转化率）
- 候选可推性判断
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。

## 2026-10-16 专项更新

处理旺季履约费与附加费时，先读 [当前专项规则与执行检查](references/update-20261016.md)。其中的未来开放日期和待复核项不能当作当前账户已可用。
