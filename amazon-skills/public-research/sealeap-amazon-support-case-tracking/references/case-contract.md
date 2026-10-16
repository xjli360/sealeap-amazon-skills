# 工单记录与验收

每个工单保存 case_id、account_alias、marketplace、subject、platform_status、created_at、updated_at、history_coverage、business_resolution、next_action、deadline、deadline_source、evidence_ids。

沟通记录保留时间、渠道、发言角色、要点及平台原始引用位置。业务交付只保留必要摘要；完整往来和附件存入任务私有目录，不能放进公开 Skill 包。附件记录名称、哈希、真实性状态和关联要求；文件名本身不证明内容。

重复工单不直接合并或关闭：先按 ASIN/SKU、问题、时间判断关联，保留各自的状态与回复。

验收用例：工单关闭但库存仍不可售 => 工单已关/业务未解决；客服没有期限 => SLA 未知；同一条回复重复出现 => 按真实记录 ID 去重，不能只按正文删相似沟通；缺页 => 时间线不完整。
