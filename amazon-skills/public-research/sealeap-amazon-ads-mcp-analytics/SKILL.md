---
name: sealeap-amazon-ads-mcp-analytics
description: "用实时工具发现核验 Amazon Ads MCP Lite 能力，规划只读广告报表或 AMC 查询并校验粒度、归因和汇总。用于广告 Agent 接入验收、MCP 动态工具或 AMC Expert 查询审查；不把 Ads 连接当卖家库存利润通道，也不凭生成 SQL 自动改广告。"
metadata:
  verified_at: "2026-10-16"
---

# Ads MCP Lite 与 AMC 智能分析

先证明工具和数据适合业务问题，再让 Agent 查询与解释。

## 工作流

1. 读 [官方基线](references/official-baseline.md)，区分宿主连接、Ads MCP、控制台 Ads Agent、AMC 实例和 Seller Connector。一个登录成功不证明其他连接可用。
2. 固定 advertiser/profile、marketplace、AMC instance、币种、时区、窗口和用户授权。通过当前 tools/list 或宿主等价机制发现 Lite 入口，先搜索能力，再读工具 schema，再调用；不把公告中的“三个工具”当固定工具名。
3. 对账前先检查数据集、权限、报告字段和归因。按 [分析契约](references/analysis-contract.md) 写明行粒度、主键、可加性和指标分母。
4. 若有 AMC Expert 能力，把问题、已验证 schema 和限制交给它生成查询草稿；核验 SQL 的表、join、窗口、过滤、隐私阈值及重复计数。无工具时可人工设计草稿，不伪装成 Expert 输出。
5. 执行前核对查询权限、配额、可能费用与已授权范围。对耗时任务保存唯一请求 ID，轮询原任务至终态，结果未明不重复生成查询。
6. 用最小范围只读结果验证：原始曝光/点击/花费等与相同口径报表核对，再汇总比率。空值、受隐私阈值限制和未返回不能当零。
7. 输出数据支持的诊断与假设。AMC 路径、受众重合或相关增长不自动证明因果；LTS 等模型值与已实现销售分开。
8. 如另有广告变更要求，核对会话授权范围，先保存对象 ID、旧值、最大预算、停止线和回退；写后回读。报表查询成功不能标为广告优化已执行。

## 交付

连接/能力状态、工具 schema 证据、查询或报告定义、执行状态、字段与金额对账、解释和待执行动作。没有实时工具或账户权限时状态为 PREPARATION_ONLY。
