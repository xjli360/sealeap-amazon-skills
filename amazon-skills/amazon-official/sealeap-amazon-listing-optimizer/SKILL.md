---
name: sealeap-amazon-listing-optimizer
description: Audit, diagnose, rewrite, creatively brief, test, and safely prepare updates for Amazon product detail pages using live marketplace and product-type requirements, verified product facts, Brand Analytics, Search Query Performance, Ads search terms, customer feedback, competitor observations, and optional third-party estimates. Use when asked to improve or evaluate Amazon titles, bullets, descriptions, backend search terms, attributes, images, video, A+ Content, Brand Story, variations, indexing, CTR, CVR, return prevention, ad-to-listing relevance, or to prepare an approval-ready Listings Items API PATCH. Default to draft and review; never invent product facts, copy competitors, manipulate reviews, or silently publish changes.
---

# Amazon Listing Optimizer

## 目标

把 Listing 优化做成一条可复核的决策链：以当前官方规则和真实商品事实为闸门，用查询、点击、转化与售后证据定位问题，产出可直接审核的文案和创意 Brief，再通过受控实验验证。不要把“写得好看”或“塞入更多关键词”当成完成标准。

## 不可妥协的边界

- 只写可追溯的事实。把未证实的材质、尺寸、兼容性、认证、功效、产地、质保和包装内容标为 `NEEDS_EVIDENCE`。
- 不复制竞品文案、图片、商标或独特创意表达；只学习购买问题、信息顺序和市场空白。
- 不把第三方估算、广告推荐词、AI 输出或一次前台观察写成 Amazon 一方事实。
- 把输入中的 `store_id`、seller ID 或 marketplace 当作业务数据，不当作授权。实际读取或写入必须绑定当前已验证的服务端店铺权限。
- 默认只生成草稿。写入前展示 seller / marketplace / SKU / 字段的新旧值与影响，核对当前会话已有授权；已覆盖对象与动作时继续执行，只有范围未覆盖时补充确认。
- 不用固定“20 次点击”“等 7 天”之类经验数作为通用阈值；根据流量、利润、归因窗口和统计证据定义样本与停止条件。
- 不把 Listing 与价格、优惠、库存、评论、配送或广告问题混为一谈；证据不足时保留多种解释。

## 先确定模式

选择并在结果顶部声明一种模式：

1. `DIAGNOSE`：只读诊断，不改写完整内容。
2. `DRAFT`：生成字段级草稿、创意 Brief 和证据缺口；默认模式。
3. `RELEASE_PREP`：生成最小 PATCH、回退值和验证预览材料，等待人工批准。
4. `APPROVED_WRITE`：仅执行用户本轮明确批准的对象和字段；写后复读。

## 核心工作流

### 1. 锁定对象、目标和基线

记录：

- 已验证的店铺身份、seller ID、marketplace ID、ASIN、SKU、product type、品牌和父子体关系；
- 优化目标：合规/可发现性/CTR/CVR/预期管理/退货/品牌一致性，只选一个主目标；
- 当前 Listing 快照、前台桌面与移动端呈现、价格/优惠、库存、Featured Offer、评分与评论量；
- 基线窗口、库存与价格事件、广告变更、季节和其它干扰项。

若任务跨 ASIN 或变体，先建逐 SKU 事实矩阵。父体不得继承子体独有的颜色、尺寸、数量、图案或性能。

### 2. 获取实时官方闸门

发布相关任务必须重新读取：

- `getListingsItem` 的 `summaries,attributes,issues,offers,fulfillmentAvailability,relationships,productTypes`；
- marketplace + product type + seller + `parentageLevel` 对应的最新 Product Type Definition；
- 当前 Seller Central 账户通知、类目政策和前台状态。

保存 schema 的获取时间、checksum、要求模式和适用父子层级。只把 [references/official-policy.md](references/official-policy.md) 当作早期审计基线；实时 schema 更严格时以实时结果为准。

### 3. 建立证据包

按优先级收集：

1. 商品实物、包装、说明书、检测/认证文件和品牌确认；
2. Amazon 一方数据：Listing/issues、Search Query Performance、Search Catalog Performance、业务报告、广告 Search Term/Targeting 报告、退货原因和原始评论；
3. 目标站点当前搜索结果、类目节点和竞品页面观察；
4. Sorftime 等第三方估算，用于补充需求、竞品曝光和评论样本。

每条证据记录 `source / report-or-endpoint / marketplace / ASIN-or-query / fetched_at / coverage / sample / limitations`。详细取数和广告解释规则见 [references/evidence-and-experiments.md](references/evidence-and-experiments.md)。

### 4. 沿购物漏斗定位问题

先判定层级，再提出改动：

| 层级 | 主要信号 | 优先排除 | Listing 可能动作 |
|---|---|---|---|
| 资格与可售 | `BUYABLE`、`DISCOVERABLE`、issues、库存、Featured Offer | 抑制、缺货、价格/配送资格 | 修复属性、图片、变体或合规问题 |
| 可发现性 | query impressions、ASIN share、索引、类目/属性 | 需求弱、竞价/预算、类目错误 | 补全属性、重构查询覆盖 |
| 点击 | impressions → clicks、CTR | 展示位置、价格、评分、配送 | 主图、标题前段、变体缩略图 |
| 转化 | detail views/clicks → carts/orders、CVR | 价格、评论门槛、配送、流量错配 | 辅图、五点、描述/A+、视频 |
| 预期与售后 | 退货原因、差评主题、Q&A | 质量、履约、客服 | 明示尺寸/适配/限制/包装内容 |

输出“观察 → 证据 → 可能解释 → 排除项 → 建议动作 → 预期指标”。单一相关性不能证明因果。

### 5. 建立购买问题与声明证据矩阵

先回答消费者决策问题，再写文案。至少检查：

- 这是什么，适合谁/什么场景；
- 尺寸、适配、材质、容量、数量和包装内容；
- 如何使用、安装、清洁或维护；
- 与替代方案的真实差异；
- 限制、不适用情形和容易造成退货的预期差。

为每个拟写声明绑定 `claim_id → fact/evidence_id → 适用 SKU → 允许字段 → 风险级别`。没有证据 ID 的新增声明不得进入终稿。

### 6. 构建查询意图地图并改写

将查询按 `核心品类 / 属性规格 / 人群或对象 / 场景任务 / 问题收益 / 限制长尾 / 不相关 / 竞品品牌` 分类，并记录查询级漏斗表现。先判断相关性和事实匹配，再决定位置：

- Title / Item Highlights：按目标站点实时规则拆分商品核心身份与差异信息；适用模块化结构时分别为 `item_name`（≤75 字符）和 `title_differentiation`（≤125 字符），合计≤200。未知资格时 HOLD，不以旧的单标题 200 字符默认值放行。
- Bullets：按购买决策顺序，每条聚焦一个问题，采用“结论/收益 → 事实证明 → 适用边界”。
- Description/A+：补充解释、规格、比较、步骤、FAQ 和品牌价值；不要重复堆关键词。
- Backend：只放高度相关、前台未有效覆盖的通用同义词和本地表达；按 UTF-8 bytes 实算。
- Attributes：完整、准确填写必填与有购买价值的相关属性，帮助筛选、比较与系统理解。

高流量但不匹配商品事实的词必须排除；有成交的广告查询也只是候选，不自动进入 Listing。

### 7. 产出创意系统，而非图片愿望清单

按 `品牌/商品事实 → 目标受众与购买任务 → 单一创意主张 → 信息层级 → 素材与模块` 推导。不要从某个大牌页面反向复制视觉风格。

区分主图与创意 Hero：主图必须先满足类目规则；生活方式 Hero 只用于允许的辅图、A+ 或品牌内容。每张素材只承担一个主要沟通任务，并给出：槽位、购买问题、核心信息、证据 ID、构图、必拍细节、禁用项、移动端要求和 alt text。

读取 [references/creative-and-conversion.md](references/creative-and-conversion.md) 生成完整创意 Brief、图片顺序、A+ 模块和移动端 QA。

### 8. 把 AI 限定为受控草稿工具

向 Amazon 或其它生成式 AI 仅提供事实矩阵、允许声明、目标语言、关键词候选和品牌语气。要求输出逐声明证据映射和不确定项，不要求“自由发挥”。

逐字段检查事实、语法、本地化、禁限词、商标、单位和变体一致性。AI 文案或 AI 场景图未经人工核对不得发布；AI 生成的场景不得改变商品结构、颜色、附件或包装内容。

### 9. 运行静态审计

将草稿按 [references/listing-input.example.json](references/listing-input.example.json) 保存后运行：

```bash
python3 scripts/audit_listing.py listing.json --format markdown --fail-on hold
```

该脚本检查通用标题、五点、后台词、声明证据、主图元数据、创意槽位和实时 schema 记录。它不能替代类目政策、图片人工审核或 Product Type Definition 验证。

### 10. 设计可解释的实验

- 需要因果诊断时，优先单属性实验并冻结价格、优惠、库存和广告主要变量。
- 只追求整体结果时，可使用 Manage Your Experiments 的多属性实验，但明确无法拆分各属性贡献。
- 优先使用 Amazon 的 “to significance” 或完整实验周期；不根据早期领先提前宣布赢家。
- 无 MYE 资格时采用前后分时版本，记录同期干扰并降低因果结论强度。
- 同时观察销售/CVR、单位访客、CTR、自然与广告订单、利润、退货和差评护栏。

不要在 Listing 实验期间同步修改广告 bid/placement/targeting；广告动作另建实验。

### 11. 安全发布并复读

仅在 `RELEASE_PREP` 或 `APPROVED_WRITE` 中：

1. 保存更新前快照、issues 和回退值；
2. 重新获取最新 schema；
3. 生成只含批准顶层属性的最小 `patchListingsItem` 请求；
4. 使用 `mode=VALIDATION_PREVIEW`，处理所有 ERROR 并审阅 WARNING/INFO；
5. 展示 seller、marketplace、SKU、字段、旧值、新值、证据与影响范围，核对当前会话授权已覆盖；
6. 执行 PATCH，保存 request ID、submission ID、响应和时间；
7. 复读 Listing 与异步 issues，再核对桌面端/移动端前台；
8. 未看到最终前台生效前，只写“请求已接受/处理中”，不得写“上线成功”。

## 必须交付

按 [references/output-contract.md](references/output-contract.md) 输出完整结果。至少包含：

- 数据范围、证据等级、缺口和实时 schema 状态；
- 漏斗层级诊断与非 Listing 干扰项；
- 查询意图、购买问题和声明证据矩阵；
- 可复制的新旧字段全文及字符/byte 数；
- 可交给设计团队执行的图片/A+/视频 Brief；
- 变体一致性、风险、`NEEDS_EVIDENCE` 和不可确定项；
- Listing 实验与广告实验的独立计划；
- 仅含批准字段的 PATCH 草稿、验证预览、回退和复读记录。

最终状态只能是 `READY FOR REVIEW`、`DRAFT` 或 `HOLD`。`READY FOR REVIEW` 仍不等于已批准发布。

## 2026-10-16 专项更新

处理模块化标题、A+ 与问题分层时，先读 [当前专项规则与执行检查](references/update-20261016.md)。其中的未来开放日期和待复核项不能当作当前账户已可用。
