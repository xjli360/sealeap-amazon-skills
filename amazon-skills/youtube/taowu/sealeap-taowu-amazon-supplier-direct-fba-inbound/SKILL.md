---
name: sealeap-taowu-amazon-supplier-direct-fba-inbound
description: "Plan a direct supplier-to-FBA inbound shipment by collecting ship-from, carton, prep and freight facts before creating the shipment plan in Seller Central, then handing the supplier the ship-to address, box labels and unit labels with a verification checklist. Freight cost and carrier choice are checked against current rate cards and quotes rather than assumed. Use for 供应商直发 FBA、工厂直发亚马逊仓、创建货件计划、装箱信息怎么填、FNSKU 标签给工厂、头程发货清单. Do not use to book freight or create shipment plans on a live account without the seller confirming carton data, labels and the ship-to address."
---

# Amazon 供应商直发 FBA 入仓计划

## 目标

Plan a direct supplier-to-FBA inbound shipment by collecting ship-from, carton, prep and freight facts before creating the shipment plan in Seller Central, then handing the supplier the ship-to address, box labels and unit labels with a verification checklist. Freight cost and carrier choice are checked against current rate cards and quotes rather than assumed.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源把“就近分到东/西海岸仓”“ship-from 只用于退件”当作规则；实际分仓、拆仓与入库配置由平台当期规则决定，以当前货件计划页面提示为准，不外推。
- 来源出于对仓库的不信任而坚持全部贴 FNSKU，这是风险偏好而非规定；能否沿用厂商条码取决于当前 Listing 的条码资格与产品属性，逐 SKU 核对。
- 头程方式、箱规与重量上限、运费都随承运商与平台政策变化；本 Skill 不给运费数字，一律按当前费率与承运商报价核对，超规箱先与供应商改箱规。
- 供应商地址、电话、追踪号属于商业敏感数据，只用于货件计划，不写入公开文档或日志。

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

1. 先确认目标 ASIN/SKU 已在目标 marketplace 完成上架且可售；未上架的产品无法建货件计划，先补齐 Listing 再继续。
2. 向供应商收齐五项发货事实：实际发货地址与联系电话、箱标可打印的纸张与打印机类型、承运方式（空运/海运/快递）与承运商、每箱件数与总箱数、每箱尺寸与毛重；把答复原文留档作为填表依据。
3. 在 Seller Central 的补货/发货入口新建货件计划：ship-from 改为供应商地址（用于退件与就近分仓判定），destination 选实际销售站点，核对 SKU 明细，用供应商给的箱规创建可复用的装箱模板（每箱件数、尺寸、重量）。
4. 逐项判定预处理与贴标责任：按产品属性（易碎、液体、尖锐、套装等）选择 prep 类别；按当前品牌角色和商品条件核对厂商条码/FNSKU 资格，不再把已结束的混库作为当前默认理由；美国站已停止 Amazon 代预处理/贴标，安排供应商、卖家或第三方在入仓前完成，其他站点另核验。
5. 填写承运信息前，按当前费率卡与承运商报价核对头程方案：比较承运方式、到仓时效、是否使用平台合作承运；录入运单/追踪号并保存，计划才算完成。
6. 把三样东西回传供应商并要求书面确认：计划里的 ship-to 仓库地址（明确不是卖家地址）、箱标 PDF、按供应商可打印规格（30-up/24-up/A4 等）导出的 FNSKU 标签 PDF；需要标注原产国时一并说明贴放位置。
7. 货件创建后跟踪状态：到仓时间、接收数量与计划数量是否一致，差异按平台的对账/申诉流程处理，并把本次箱规与标签设置沉淀为下次补货的模板。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 供应商发货信息核对表（地址、箱规、件数、承运方式、纸张类型）
- 货件计划填写草案（ship-from、目的站点、SKU、装箱模板、prep 与贴标责任）
- 回传供应商清单（ship-to 地址、箱标 PDF、FNSKU 标签 PDF、原产国标注要求）
- 头程方案比较与承运信息记录（按当前费率与报价核对）
- 到仓核对与差异处理记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。

## 2026-10-16 专项更新

处理FBA 条码与预处理责任时，先读 [当前专项规则与执行检查](references/update-20261016.md)。其中的未来开放日期和待复核项不能当作当前账户已可用。
