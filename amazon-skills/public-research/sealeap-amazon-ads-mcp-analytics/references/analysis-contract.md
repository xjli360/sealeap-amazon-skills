# 广告与 AMC 分析契约

最小输出字段：task、account/profile/instance、marketplace、currency、timezone、period、attribution_window、date_basis、tool_schema_hash、query_or_report_id、generated_at、coverage、metric_definition、evidence。

检查一行数据是什么：campaign-day、search-term-day、conversion event 或 user-path 的聚合不能随意拼接。曝光/点击事实表与转化表连接前，各按正确唯一键处理；一个点击关联多笔转化时，花费不能复制多次。

计算 ACOS/ROAS 前明确销售是广告归因、点击归因还是总店铺销售；不同窗口不强行相减得到自然销售。AMC 仅输出允许的聚合结果，不请求重识别顾客。

生成 SQL 只标 DRAFT；通过 schema/语义检查标 REVIEWED；执行返回终态和数据标 EXECUTED；与同口径证据对账后标 RECONCILED。未经测试不能越级。对比两周必须同长度、成熟归因并标记改价/断货/预算变更。
