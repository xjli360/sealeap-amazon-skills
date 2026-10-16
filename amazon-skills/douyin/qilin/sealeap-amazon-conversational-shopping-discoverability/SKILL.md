---
name: sealeap-amazon-conversational-shopping-discoverability
description: "Map verified product facts to customer shopping missions, structured attributes and localized Amazon listing content, then design observable conversational-shopping tests. Use for Shopping Mission、场景化Listing、Alexa for Shopping、Rufus and AI购物可见性. Never seed reviews or Q&A, fabricate scenarios, or guarantee recommendation placement."
---

# Amazon 对话式购物可发现性

## 目标

让商品事实和真实使用场景更完整、结构化、可验证，使搜索与购物助手更容易理解商品适用性。

## 适用任务

- Listing 属性不完整或场景表达薄弱。
- 准备适配 Rufus、Alexa 或其他对话式购物入口。
- 需要从真实客户问题和反馈中提炼场景内容。

## 开始前要拿到

- 产品规格、说明书、认证、兼容性、限制条件和真实场景证据。
- Listing 当前标题、五点、属性、图片、A+、视频和本地化版本。
- 真实客户搜索词、客服问题、退货原因和评论主题聚合。

缺失的数据要明确列为缺口，并把结论标成事实、估算或假设；不要补造数字。

## 不可妥协的边界

- 不得安排、购买或撰写买家评论与 Q&A，也不得把营销话术伪装成客户内容。
- 所有场景、性能和兼容性声明必须有产品事实或证据支持。
- 不承诺被任何购物助手推荐；推荐机制和展示会变化，需核对当前官方信息。
- 当前 Amazon 官方政策、帮助页、账户资格和后台实际字段优先于本 Skill 中的经验框架；规则可能变化时先核验。
- 默认提供诊断或草案。写入前展示对象、旧值、新值、影响、停止线与回退，核对用户已有授权是否覆盖对象、动作与预算；范围已明确授权时继续执行并回读核验，只有未覆盖或扩大的范围才请求批准。
- 不输出原素材的创作者身份、账号、链接、视频编号或可反查线索；当前业务证据的官方来源、采集时间和口径仍需保留。

## 第三方 MCP 数据

只有在本任务确实需要外部市场、竞品、关键词或公开网页证据时，才读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，并使用 scripts/mcp_research.py。

- 先动态执行 tools/list、search-tools 和 describe，依据实时 inputSchema 构造参数，不照搬历史工具名。
- 凭证只从环境变量读取，不放进命令参数、URL、Skill、结果文件或 Git。
- tools/call 可能计费。调用前展示 Provider、工具名、无密钥参数、预计成本与输出位置，核对已有授权覆盖后才加 --allow-cost；该标志不是费用上限。
- 第三方数据标为估算或代理证据，记录 Provider、工具、无密钥参数、查询时间和原始结果位置；失败一次后记录缺口，不反复消耗额度。
- 脱敏结果用 --output 写到 Skill 包之外的任务私有目录；不假设安装位置受仓库 .gitignore 保护，不把运行结果写入 Skill 包。

## 工作流

### 1. 建立事实底稿

整理结构化规格、兼容性、使用限制、认证和证据来源，先解决内部矛盾。

### 2. 补全属性

填写当前类目允许且适用的属性，不用关键词堆砌替代字段含义。

### 3. 映射真实场景

读取 [购物任务与证据映射](references/shopping-mission.md)，建立支持、条件支持、不支持和未知的任务卡，并按用户指定字段交付。

从搜索词、客服、退货和评论主题聚合出高频任务，用产品事实判断支持、不支持或需条件支持。

### 4. 改造内容

在标题、五点、图片、A+ 和视频中自然表达关键场景、限制和证明，保持可读性并做本地化。

### 5. 处理客户内容边界

只观察真实客户评论和问题的主题；品牌回答保持事实中立，不诱导评价或虚构提问。

### 6. 验证效果

用真实对话式查询做发现性检查，并跟踪会话、转化和退货变化；把结果标为相关观察。

## 判断标准

- 每条卖点和场景能回到事实证据。
- 属性、图片和文案之间一致。
- 不包含任何评论或 Q&A 植入动作。

## 必须交付的结果

- 产品事实与场景矩阵，含任务条件、证据 ID 和字段分配。
- 属性缺口清单。
- Listing 内容改写草稿。
- 对话式查询测试与监控方案。

结尾列出数据窗口、关键假设、证据缺口、风险和下一步；如包含待执行动作，单独放在“待批准变更”中。

## 2026-10-16 专项更新

处理Branded Conversations 准备时，先读 [当前专项规则与执行检查](references/update-20261016.md)。其中的未来开放日期和待复核项不能当作当前账户已可用。
