# 多渠道同步契约

商品映射：channel、channel_account、marketplace、listing_id、variant_id、merchant_sku、internal_sku、units_per_offer、bundle_components、currency、mapping_evidence。

订单台账：channel+order_id+line_id 为唯一键；保留源状态、库存预留、履约订单 ID、包裹/追踪、退货退款、最近同步时间及原始事件 ID。包裹分拆和部分退款必须保留数量，不能整单覆盖。

库存：先按权威库存池建立可售数，再扣未纳入源可售数的已承诺订单和安全库存；已扣的预留不重复扣。每渠道发布上限合计不得无条件超过共享可分配库存。事件乱序按版本/时间处理，不用最后到达者覆盖更新版本。

试点通过需同时具备真实源记录、目标回读、事件去重和异常处理证据。模拟只标 SIMULATED。权限不足、未开放、费率缺失或无法排除重复下单分别 HOLD。
