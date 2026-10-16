# Listing 优化交付合同

不得只给原则、分数或一段“优化后文案”。按以下结构交付；无数据的栏位写 `NOT AVAILABLE`，不能删除后假装完整。

## 1. 结论卡

- 对象：`verified store / seller / marketplace / ASIN / SKU / product type / parentage`
- 模式：`DIAGNOSE | DRAFT | RELEASE_PREP | APPROVED_WRITE`
- 状态：`READY FOR REVIEW | DRAFT | HOLD`
- 主目标：只写一个
- 主问题：最多三项
- 建议首个实验：一项
- 发布阻塞项：没有则写 `None for review; approval still required`

## 2. 数据与规则范围

| Evidence ID | 等级 | 来源/接口 | marketplace / ASIN / query | 日期范围/快照 | 样本 | 限制 |
|---|---|---|---|---|---|---|

同时列出：

- PTD：product type、parentage、requirements、fetched_at、checksum；
- 当前 Listing issues：code、severity、attribute、enforcement；
- 数据缺口与无法访问的账户页面；
- 价格、优惠、库存、评分、配送、广告和季节干扰。

若发布任务未取得实时 PTD，状态必须为 `HOLD: LIVE_SCHEMA_MISSING`。

## 3. 漏斗诊断

| 优先级 | 层级 | 观察 | Evidence ID | 可能解释 | 已排除 | 建议动作 | 预期指标 |
|---|---|---|---|---|---|---|---|

层级使用：`ELIGIBILITY / DISCOVERABILITY / CLICK / CONVERSION / EXPECTATION`。

把事实与推断分开。若存在多个解释，全部列出并说明下一步如何区分。

## 4. 商品事实与声明账本

| Claim ID | 拟写声明 | 事实/证据 ID | 适用 SKU | 允许字段 | 风险 | 状态 |
|---|---|---|---|---|---|---|

状态：`VERIFIED / NEEDS_EVIDENCE / REJECTED`。`NEEDS_EVIDENCE` 和 `REJECTED` 不得进入发布稿。

## 5. 购买问题矩阵

| 优先级 | 消费者问题 | 证据/主题 | 当前是否回答 | 应回答位置 | 预期减少的摩擦 |
|---|---|---|---|---|---|

覆盖身份、尺寸/适配、材质/性能、使用/维护、包装内容、限制和售后预期。

## 6. 查询意图地图

| Query | 站点 | 意图 | 来源/时间 | 展示/点击/订单 | 相关性 | 事实匹配 | 当前覆盖 | 决策 |
|---|---|---|---|---|---|---|---|---|

决策：`TITLE / BULLET / DESCRIPTION-A+ / BACKEND / ATTRIBUTE / AD-ONLY / NEGATIVE-CANDIDATE / EXCLUDE / INSUFFICIENT-SAMPLE`。

## 7. 新旧字段全文

### Title

- 旧值：
- 新值：
- 字符数：`old → new / live max`
- Claim/Evidence IDs：
- Query 映射：
- 移动端/广告前段检查：
- 风险/待确认：

### Item Highlights / title_differentiation

- 单独保留旧值、新值、字符数、事实与关键词映射；不是 bullet points。
- 记录 `title_structure=modular|single|api_legacy`、规则来源、核对日期和适用范围。模块化标题与亮点分别校验并检查总长度；单字段例外必须提供实时限制。api_legacy 仅用于已核验的无亮点 API 兼容路径，保留可能被平台自动拆分的警告与目录回读要求。
- 本地输入可用 `title` / `item_highlights`，或 API 原生名 `item_name` / `title_differentiation`；同义字段并存且值不同必须报错。此处均为抽取后的字符串，不接受 API 的 value 数组；先按 marketplace_id/language_tag 选取正确值，不能把整个数组转成字符串。
- schema、规则范围或结构未知时 HOLD，不自动选用 200 字符。

### Bullets

逐条给出：

| # | 购买问题 | 旧值 | 新值 | Claim/Evidence IDs | 字符数/限制 |
|---|---|---|---|---|---|

### Description / A+ 可读取文本

给出完整正文，不只给模块标题。标出与图片配合的位置和不能写入的声明。

### Backend Search Terms

- 旧值：
- 新值：
- UTF-8 bytes：`old → new / live limit`
- 删除的重复、冗余、竞品或无关词：

### Attributes

| Attribute | 旧值 | 新值 | schema 要求/枚举 | Evidence ID | 是否可编辑 |
|---|---|---|---|---|---|

## 8. 创意 Brief

### 总体方向

- 目标受众与购买任务：
- 单一创意主张：
- 一级/二级信息：
- 品牌语气与视觉规则：
- 禁止项：

### 图片/视频任务卡

| Slot | 目标 | 一个主信息 | Headline/文案 | Evidence IDs | 构图/必拍 | 移动端/alt | 验收标准 |
|---|---|---|---|---|---|---|---|

### A+ / Brand Story

| 顺序 | 模块 | 购买问题 | 可读取文案 | 视觉 | Evidence IDs | 资格/限制 |
|---|---|---|---|---|---|---|

## 9. 变体一致性

| Child SKU | 主题/值 | 标题 | 图片 | 属性 | 价格/库存 | 独有事实 | 问题 |
|---|---|---|---|---|---|---|---|

父体不携带子体独有事实。未取得关系与 schema 时，不建议合并、拆分或改变 variation theme。

## 10. 广告联动（独立于 Listing 实验）

| Query/Target | 窗口与样本 | 成本/订单/销售 | 相关性 | Listing 动作 | Ads 动作 | 审批 |
|---|---|---|---|---|---|---|

写明广告变量冻结范围，以及哪些否定、bid、placement 或 target 动作必须另行审批。

## 11. 静态审计与风险

- `audit_listing.py` 状态与主要检查：
- `NEEDS_EVIDENCE`：
- 类目/法规/商标风险：
- 图片与移动端人工 QA：
- 静态审计无法判断的项目：

## 12. 审批用 PATCH

只有在实时 schema 已获取且属性路径已验证时填写：

```json
{
  "sellerId": "...",
  "sku": "...",
  "marketplaceIds": ["..."],
  "productType": "...",
  "patches": [
    {
      "op": "replace",
      "path": "/attributes/<verified-top-level-attribute>",
      "value": []
    }
  ]
}
```

同时给出：

- 更新前完整值与回退 PATCH；
- 每个 patch 对应的批准字段和 Evidence IDs；
- Validation Preview 状态和 issues；
- 批准人/时间；
- 写入后的 request/submission ID；
- 异步 issues 与前台复读结果。

不要猜属性路径，不要把深层节点当成 PATCH path。

## 13. 实验卡

- 假设：
- 类型：`MYE-SINGLE | MYE-MULTI | SEQUENTIAL | OTHER`
- Version A / B：
- 对象与唯一主变量或组合：
- 基线与归因窗口：
- 最低信息/显著性规则：
- 主指标：
- 护栏：利润、退货、差评等
- 成功/停止/回退规则：
- 冻结变量：价格、优惠、库存、广告、评分事件
- 结论强度：`CAUSAL | DIRECTIONAL | INCONCLUSIVE`

## 最终状态定义

- `READY FOR REVIEW`：草稿、证据和规则检查齐全，可供人审；仍未授权写入。
- `DRAFT`：方向可讨论，但存在非关键数据或素材缺口。
- `HOLD`：实时 schema、授权、关键事实、样本或合规证据不足，不能发布。
