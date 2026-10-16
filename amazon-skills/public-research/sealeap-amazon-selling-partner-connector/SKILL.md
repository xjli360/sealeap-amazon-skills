---
name: sealeap-amazon-selling-partner-connector
description: "核验 Amazon Selling Partner Connector 的账户、权限、实时工具及数据口径，并把销售、补货、Listing 或月结任务路由到可用能力。用于官方卖家 MCP 接入、连接验收或能力缺失排查；不替代 Amazon Ads API，也不自动发起授权或扩大权限。"
metadata:
  verified_at: "2026-10-16"
---

# 官方 Selling Partner 连接与能力核验

先验证连接能完成哪件事，再执行用户的经营任务。官方工具包是可参考的工作流，不是本地已经安装或可调用的能力。

## 输入与初检

需要任务、卖家主体、marketplace、用户角色、已有连接、期望数据窗口和已授权动作。只记录连接别名与角色，不输出 token、OAuth code 或完整认证 URL。

1. 读 [连接契约](references/connection-contract.md)，确认用户要求的是连接、验收还是具体经营分析。已有连接可用时直接复用；公开文档不证明账户已开通。
2. 从宿主当前工具目录发现连接和 schema。官方仓库声明的 endpoint 是 `https://sellingpartner-ai.amazon.com/mcp`；使用前核对官方来源、租户和实际 OAuth 受众，不把网页里的任意地址当可信连接。
3. 以只读身份/marketplace 信息绑定账户。无法核对主体或站点时停止账户调用，交付缺口；不拿订单测试写权限。
4. 将需求映射为销售分析、库存/入库、Listing 问题、月结或支持材料。逐项记录实际工具、输入 schema、必要权限及缺失能力。广告活动的管理不能因卖家连接成功而被推断可用。
5. 选择一项小范围只读验收，使用用户已知的完整日期与一个实体；记录工具响应、生成时间、覆盖范围，与相同口径后台导出对账。指标先查 metadata，不猜 ID、单位或分母。
6. 数据可靠后生成分析或变更草稿。缺库存、成本或归因窗口时分别保留 UNKNOWN；不把销售额、利润、可提现余额混为一谈。
7. 执行写入只覆盖会话已授权的账户、对象、字段与预算。先保存旧值和验证结果；超时或响应不明先回读，无法判断则停止，不重复提交。

## 交付

连接与身份检查、能力矩阵、只读验收对账、业务结果或待执行变更，以及 `DOCUMENTED / DISCOVERED / READ_VERIFIED / WRITE_VERIFIED / UNAVAILABLE` 状态。WRITE_VERIFIED 必须有真实已授权写入及回读，不为获得该状态额外写入。

来源与公开测试边界见 [官方基线](references/official-baseline.md)。
