# 连接与任务契约

## 能力矩阵

每行记录 task、connection_alias、seller_id、marketplace_id、role、live_tool、schema_hash、required_scope、observed_result、checked_at、evidence_id。schema_hash 是本次实际发现 schema 的摘要，不是自造凭证。

销售任务须绑定指标定义和完整时间窗；月结任务须区分订单日期、结算期、付款状态与用户提供的银行入账；补货任务须区分可售、预留、在途和接收中库存。跨 marketplace 不直接合计币种。

## 验收标准

- 工具出现在目录：DISCOVERED；实际请求成功且对账通过：READ_VERIFIED。
- 认证成功但权限不够：记录 permission gap；空结果先排除错站点、过滤、报告延迟，不能当零业务。
- 本地 Skill 与官方工具包均不能授予账户权限。二级用户的角色需由有权管理员确认。
- 不把官方插件示例工具名移植成任意宿主的 API；先发现实时能力。缺失时接受用户导出或只给材料清单。
- 授权回调、token 与原始含个人信息数据不进入公开交付或 Skill 包。
