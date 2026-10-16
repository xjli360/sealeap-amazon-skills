# Amazon Listing 官方基线

核对日期：2026-10-16。以下内容用于静态预审，不是永久规则。每次发布前重新读取目标 marketplace 的 Seller Central 提示、账户通知和 Product Type Definition。

## 目录

- [权威顺序](#权威顺序)
- [标题](#标题)
- [要点、描述、属性与后台词](#要点描述属性与后台词)
- [图片](#图片)
- [A+ 与 Brand Story](#a-与-brand-story)
- [生成式 AI](#生成式-ai)
- [Listings API](#listings-api)
- [实验](#实验)
- [高风险内容](#高风险内容)
- [官方来源](#官方来源)

## 权威顺序

按以下顺序解决冲突：

1. 目标账户的 Seller Central 实时错误、政策通知和类目要求；
2. seller + marketplace + product type + parentage 对应的 Product Type Definition；
3. Listings Items API 当前 issues 与 Validation Preview；
4. Amazon 官方 Seller、Ads 和 SP-API 公共资料；
5. 本文件的通用基线。

保存规则来源、获取时间、schema checksum、`requirements`、`requirementsEnforced` 和 `parentageLevel`。规则会持续更新；2026 年仍有大批产品类型属性和枚举变更，因此旧表格或旧课件不能作为发布授权。

## 标题

2026-07-27 起适用的非媒体类目采用模块化标题；实际站点、类目及例外以实时 PTD 和政策为准：

- `item_name` 最多 75 字符，含空格；
- `title_differentiation`（Item Highlights）另有最多 125 字符，双方合计最多 200；使用亮点要求标题不超过 75；
- 亮点用逗号分隔可核验的材质、适用场景、兼容性和规格短语，不重复堆词；
- 非适用站点或媒体类目不得机械套用该结构，必须取得明确的单字段限制；
- 除品牌名中的合法用法外，不允许 `! $ ? _ { } ^ ¬ ¦`；
- 同一单词通常不得出现超过两次，介词、冠词和连词除外。

类目和站点可能更严格，以实时 schema 为准。Amazon Ads 建议约 60 个字符以减少 Sponsored Products 创意中的截断，这只是展示优化建议，不是通用合规长度。标题前段优先表达商品身份和关键真实规格，不为追求 60 字而删掉必要信息。

## 要点、描述、属性与后台词

- 用自然语言回答购买问题；不写价格、促销、配送承诺或无法证明的排名/功效。
- Amazon Ads 的公开优化建议是准备至少三条高质量要点；可用数量和单条长度仍以 product type schema 为准。
- 完整填写准确且有购买价值的结构化属性；属性会影响筛选、比较、系统理解和部分前台展示。不要为了“完整度”填写不适用或猜测值。
- 后台 Search Terms 的公开通用基线为 250 UTF-8 bytes。使用空格分隔；去除标点、重复、停用词，以及标题/品牌等字段已提供的冗余信息。
- 不加入竞品品牌、ASIN、无关高流量词、主观排名词或刻意拼错。多字节语言必须实算 bytes，不能用字符数代替。

## 图片

2026 年 Amazon 官方 Seller Forums 的通用主图基线包括：

- 最长边至少 1000 px 以支持缩放，1600 px 以上为优化建议；
- 纯白背景 `RGB 255,255,255`；
- 商品通常占画面 85%–100%；
- 展示实际销售商品；不添加文字、徽章、水印、边框或未随货提供的道具；
- 保持清晰、完整、不失真，文件格式和大小以当前上传入口与类目规则为准。

类目可能有例外或更严格要求，例如服装模特、套装包装和特定媒体类型。不得为了“好看”用黑色主图背景规避规则；透明商品应通过合规布光、轮廓、阴影或类目允许的表现方式解决。

Amazon Ads 将 4 张以上高质量、可缩放图片作为广告商品优化建议，不是每个类目的法定数量。副图应补充角度、尺寸/适配、使用、细节、包装和限制，不应重复同一信息。

## A+ 与 Brand Story

- Basic A+、Premium A+ 和 Brand Story 的资格及模块以账户当前页面为准；公开指南显示 Basic A+ 可组合文本、图片、品牌标识、比较表和技术规格表。
- 在桌面端和移动端预览后再提交。避免把大量文字嵌入图片；图片缩放后可能模糊，关键规格必须有可读取文本。
- 为图片填写准确、简短的 alt text；不要用 alt text 堆关键词。
- 用规格、比较、使用步骤和 FAQ 降低购买障碍；比较表只比较自有产品，不攻击或点名竞品。
- 不写 `best-selling`、`top-rated`、无证据奖项、价格/促销/配送信息、二维码、外链、联系方式、保修保证或无权使用的素材。奖项或背书需写明机构和年份并保存证明。
- “Hero image” 是创意版面概念，不等于商品主图。生活方式 Hero 应放在允许的副图/A+ 槽位。

## 生成式 AI

Amazon 当前可从简述、商品图片、网页或表格生成 Listing 草稿，也可辅助 A+。这些能力和入口会按站点/账户变化。

把 AI 当成建议生成器：卖家仍负责商品准确性、权利、合规和最终批准。不要沿用旧课件中的固定输入数量；读取当前 UI 限制。上传商品图或网页前确认权利与敏感信息边界。

## Listings API

- 使用 Product Type Definitions API 获取当前 JSON schema。schema 下载链接通常有时效；保存 checksum，但发布前重新获取。
- 独立商品、父体和子体分别用 `parentageLevel=NONE/PARENT/CHILD` 获取适用 schema。
- 更新前用 `getListingsItem` 读取 `attributes`、`issues`、`relationships`、`offers` 和 `fulfillmentAvailability`。
- 部分更新优先使用 `patchListingsItem`；它只支持顶层 Listing 属性，不能直接 patch 嵌套节点。
- 全量 `putListingsItem` 可能覆盖未提交属性；没有完整快照和明确理由不得使用。
- 在 PATCH 请求中设置 `mode=VALIDATION_PREVIEW` 预览错误。Validation Preview 不持久化生产数据，也不能替代写入后的异步检查。
- `ACCEPTED` 只表示请求进入后续处理，不表示前台已生效。写后复读 issues、状态和前台页面。

## 实验

Manage Your Experiments 当前可测试图片、标题、要点、描述、A+ 和 Brand Story，也支持多属性实验。资格通常要求 Professional 账户、Brand Registry 和 Brand Representative 身份，具体以账户为准。

- 为解释单个字段因果，采用单属性实验；
- 为寻找整体最佳组合，可采用多属性实验，但不要拆分归因到单一属性；
- 优先使用 “to significance” 或跑完整周期，不因早期领先提前结束；
- 保留价格、优惠、库存、广告和季节干扰记录。

## 高风险内容

没有目标站点法规、类目许可和商品证据时，不写：

- 治疗、预防疾病、绝对安全或医疗功效；
- `best`、`#1`、`guaranteed`、零风险、永久有效等排名或绝对声明；
- 环保、可降解、有机、无毒、食品接触、儿童/宠物安全等认证性声明；
- 竞品商标、贬损比较、评论引述、外部联系方式、价格/折扣/配送承诺；
- 与实物、包装、变体或站点不一致的尺寸、数量、颜色、兼容性和产地。

静态风险词匹配只能提示复核，不能代替法规、类目和法律判断。

## 官方来源

- 模块化标题：https://developer-docs.amazon/sp-api/docs/submit-modular-titles
- 标题政策更新：https://sellercentral.amazon.com/seller-forums/discussions/t/145b6d0f-999c-4555-896c-c694bda2e470
- 2026 图片基线：https://sellercentral.amazon.com/seller-forums/discussions/t/0149bdb3-2056-42ce-b0bb-9eef94e3d2b8
- Search Terms：https://sellercentral.amazon.com/seller-forums/discussions/t/923d53dc-a182-4475-a164-6b2500dbaf2d
- 广告商品详情页建议：https://advertising.amazon.com/en-gb/library/guides/improve-your-products-for-advertising
- A+ 设计指南：https://sell.amazon.com/blog/a-plus-content-design-guide
- Amazon Listing AI：https://sell.amazon.com/blog/amazon-listing-ai
- Manage Your Experiments：https://sell.amazon.com/tools/manage-your-experiments
- 获取 Product Type Definition：https://developer-docs.amazon.com/sp-api/lang-en_EN/docs/retrieve-a-product-type-definition
- Listings 工作流：https://developer-docs.amazon.com/sp-api/lang-en_EN/docs/building-listings-management-workflows-guide
- PATCH Validation Preview：https://developer-docs.amazon.com/sp-api/lang-zh_CN/docs/preview-errors-before-partially-updating-a-listing
- Listings issues：https://developer-docs.amazon.com/sp-api/lang-zh/docs/manage-listings-issues

## API 过渡兼容与目录回读

官方 API 指南同时保留过渡行为：不提交 Item Highlights 时，76–200 字符的 item_name 仍可被接收，Amazon 可能自动拆成目录中的标题与亮点。不能把它写成必然 API 拒绝。getListingsItem/searchListingsItems 返回原提交值，不足以证明目录和前台未被拆分。

新模块化草稿使用 `title_structure=modular`；只有取得目标范围的当前兼容证据时，才可使用 `api_legacy`（无亮点、最多200）并保留警告。媒体/其他单字段例外使用 `single` 和明确限制。三种模式都要记录规则来源/核验日期；不要把兼容接收当作推荐展示或平台合规认证。
