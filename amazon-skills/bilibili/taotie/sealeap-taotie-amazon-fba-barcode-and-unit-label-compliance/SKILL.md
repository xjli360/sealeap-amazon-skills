---
name: sealeap-taotie-amazon-fba-barcode-and-unit-label-compliance
description: "Decide between manufacturer barcode and Amazon FNSKU labeling for an FBA SKU by checking the commingling and eligibility rules, then verify unit-label placement, legacy barcode coverage, label size and print quality before shipping. Field names and fee values follow the current Seller Central console. Use for FBA 条码用哪种、制造商条码和亚马逊条码区别、FNSKU 标签怎么贴、旧条码要不要覆盖、标签纸尺寸、热敏打印机选择、入库问题件原因. Do not use to purchase or validate GS1 UPC codes, or to decide carton-level shipment labels (see the shipment skill)."
---

# Amazon FBA 条码类型与商品标签合规核对

## 目标

Decide between manufacturer barcode and Amazon FNSKU labeling for an FBA SKU by checking the commingling and eligibility rules, then verify unit-label placement, legacy barcode coverage, label size and print quality before shipping. Field names and fee values follow the current Seller Central console.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 混库相关经验只适用于对应历史规则，不作为 2026-03-31 起新发库存的当前判断；当前条码资格按品牌角色、商品与站点确认。
- 标签与包装边缘间距、标签尺寸区间、贴标费用等具体数值随站点与政策更新，来源数字仅作参考，以当前 FBA 帮助页面与控制台为准。
- 来源推荐的打印机品牌型号不采纳；只保留「热敏优先、可扫描」的判断标准。
- 标题与标签名称不一致是否必然导致问题件属待验证假设，但在途期间冻结标题修改是低成本的稳妥做法。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、库存阶段、补货与到仓时间
- 断货或备货前后的销量、流量、广告、自然位置和转化基线
- COGS、头程、仓储、平台费、退货和清仓成本
- 可比产品的成熟度、销量区间和需求趋势

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 在库存或发货设置里读取当前 SKU 的条码类型偏好：默认通常为制造商条码，需在设置中改为亚马逊条码；先确认商品是否属于必须用亚马逊条码的类别（有效期商品、消耗品、条码无法扫描或需预处理的商品等），入口与类别清单以当前控制台为准。
2. 按发货日期与当前规则判断条码资格：2026-03-31 起的新发库存不再沿用旧混库逻辑。具有 Brand Representative 身份且商品有制造商条码的品牌方，与经销商和无制造商条码商品分别核验；不能把「UPC 正规」当作经销商免贴 Amazon 条码的充分条件。
3. 核对贴标位置：FNSKU 标签必须覆盖或用贴纸遮住包装上所有可见的旧条码（UPC/EAN 等），贴在最外层（气泡膜或塑料袋外侧），避开弯折与边角，与包装边缘保持当前要求的最小间距；服装类塑料袋另贴窒息警告标签。
4. 核对标签内容：标签上的商品名称应与当前 Listing 标题一致，条码格式采用平台可识别的一维码规范；货件在途期间不修改标题，改名放到入库完成之后。
5. 确认打印方案：优先热敏打印，避免激光打印碳粉受热受潮模糊；商品标签纸与外箱标签纸分开采购，尺寸落在当前允许区间内且不大于商品可平贴面；打印后抽样用手机扫码验证可读性。
6. 美国站 FBA 已于 2026-01-01 停止预处理与商品贴标服务，须在入仓前安排卖家、工厂或第三方完成；美国入库接口不再接受 prepOwner/labelOwner=AMAZON。其他站点逐一核验当前政策，不能直接推广美国时间表。保存责任方、验收与交期并回读货件。
7. 把「条码类型、贴标方、覆盖旧码、最外层、名称一致、扫码抽检」做成发货前检查表，未通过项不放行；入库出现问题件时先按此表反查原因再联系支持。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 条码类型决策记录
- 贴标位置与覆盖旧码核对表
- 标签规格与打印方案
- 发货前标签检查表
- 问题件反查记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。

## 2026-10-16 专项更新

处理FBA 条码与预处理责任时，先读 [当前专项规则与执行检查](references/update-20261016.md)。其中的未来开放日期和待复核项不能当作当前账户已可用。
