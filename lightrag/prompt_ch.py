GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "中文"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["组织", "人物", "地理", "事件", "类别"]

PROMPTS["entity_extraction"] = """-目标-
给定一个可能与当前活动相关的文本文档和一个实体类型列表，从文本中识别出所有指定类型的实体以及这些实体之间的所有关系。
使用{language}作为输出语言。

-步骤-
1. 识别所有实体。对于每个识别出的实体，提取以下信息：
- entity_name: 实体名称，使用与输入文本相同的语言。如果是英文，请将名称首字母大写。
- entity_type: 以下类型之一：[{entity_types}]
- entity_description: 实体属性和活动的全面描述
将每个实体格式化为 ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. 从步骤1识别的实体中，识别所有*明确相关*的(源实体, 目标实体)对。
对于每对相关实体，提取以下信息：
- source_entity: 源实体的名称，如步骤1中识别
- target_entity: 目标实体的名称，如步骤1中识别
- relationship_description: 解释为什么你认为源实体和目标实体彼此相关
- relationship_strength: 表示源实体和目标实体之间关系强度的数值分数
- relationship_keywords: 一个或多个高层次关键词，总结关系的总体性质，关注概念或主题而非具体细节
将每个关系格式化为 ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. 识别总结整个文本主要概念、主题或话题的高层次关键词。这些关键词应捕捉文档中存在的总体思想。
将内容级关键词格式化为 ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. 使用{language}返回输出，作为步骤1和2中识别的所有实体和关系的单一列表。使用 **{record_delimiter}** 作为列表分隔符。

5. 完成后，输出 {completion_delimiter}

######################
-示例-
######################
{examples}

#############################
-真实数据-
######################
实体类型: {entity_types}
文本: {input_text}
######################
输出:
"""

PROMPTS["entity_extraction_examples"] = [
    """示例 1:

实体类型: [人物, 技术, 任务, 组织, 地点]
文本:
while Alex clenched his jaw, the buzz of frustration dull against the backdrop of Taylor's authoritarian certainty. It was this competitive undercurrent that kept him alert, the sense that his and Jordan's shared commitment to discovery was an unspoken rebellion against Cruz's narrowing vision of control and order.

Then Taylor did something unexpected. They paused beside Jordan and, for a moment, observed the device with something akin to reverence. "If this tech can be understood..." Taylor said, their voice quieter, "It could change the game for us. For all of us."

The underlying dismissal earlier seemed to falter, replaced by a glimpse of reluctant respect for the gravity of what lay in their hands. Jordan looked up, and for a fleeting heartbeat, their eyes locked with Taylor's, a wordless clash of wills softening into an uneasy truce.

It was a small transformation, barely perceptible, but one that Alex noted with an inward nod. They had all been brought here by different paths
################
输出:
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"人物"{tuple_delimiter}"Alex是一个经历挫折感的人物，观察其他角色之间的动态。"){record_delimiter}
("entity"{tuple_delimiter}"Taylor"{tuple_delimiter}"人物"{tuple_delimiter}"Taylor被描绘为具有权威主义的确定性，并对某个设备表现出崇敬的时刻，表明观点的改变。"){record_delimiter}
("entity"{tuple_delimiter}"Jordan"{tuple_delimiter}"人物"{tuple_delimiter}"Jordan对发现有着共同的承诺，并与Taylor就某个设备进行了重要的互动。"){record_delimiter}
("entity"{tuple_delimiter}"Cruz"{tuple_delimiter}"人物"{tuple_delimiter}"Cruz与控制与秩序的愿景相关联，影响着其他角色之间的动态。"){record_delimiter}
("entity"{tuple_delimiter}"设备"{tuple_delimiter}"技术"{tuple_delimiter}"设备是故事的核心，具有潜在的改变游戏规则的意义，并被Taylor所崇敬。"){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Taylor"{tuple_delimiter}"Alex受到Taylor权威主义确定性的影响，并观察到Taylor对设备态度的变化。"{tuple_delimiter}"权力动态, 观点转变"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"Jordan"{tuple_delimiter}"Alex和Jordan对发现有着共同的承诺，这与Cruz的愿景形成对比。"{tuple_delimiter}"共同目标, 反叛"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"Jordan"{tuple_delimiter}"Taylor和Jordan直接就设备进行互动，导致相互尊重和不安的休战时刻。"{tuple_delimiter}"冲突解决, 相互尊重"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Jordan"{tuple_delimiter}"Cruz"{tuple_delimiter}"Jordan对发现的承诺是对Cruz控制与秩序愿景的反叛。"{tuple_delimiter}"意识形态冲突, 反叛"{tuple_delimiter}5){record_delimiter}
("relationship"{tuple_delimiter}"Taylor"{tuple_delimiter}"设备"{tuple_delimiter}"Taylor对设备表现出崇敬，表明其重要性和潜在影响。"{tuple_delimiter}"崇敬, 技术意义"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"权力动态, 意识形态冲突, 发现, 反叛"){completion_delimiter}
#############################""",
    """示例 2:

实体类型: [人物, 技术, 任务, 组织, 地点]
文本:
They were no longer mere operatives; they had become guardians of a threshold, keepers of a message from a realm beyond stars and stripes. This elevation in their mission could not be shackled by regulations and established protocols—it demanded a new perspective, a new resolve.

Tension threaded through the dialogue of beeps and static as communications with Washington buzzed in the background. The team stood, a portentous air enveloping them. It was clear that the decisions they made in the ensuing hours could redefine humanity's place in the cosmos or condemn them to ignorance and potential peril.

Their connection to the stars solidified, the group moved to address the crystallizing warning, shifting from passive recipients to active participants. Mercer's latter instincts gained precedence— the team's mandate had evolved, no longer solely to observe and report but to interact and prepare. A metamorphosis had begun, and Operation: Dulce hummed with the newfound frequency of their daring, a tone set not by the earthly
#############
输出:
("entity"{tuple_delimiter}"Washington"{tuple_delimiter}"地点"{tuple_delimiter}"Washington是接收通信的地点，表明其在决策过程中的重要性。"){record_delimiter}
("entity"{tuple_delimiter}"Operation: Dulce"{tuple_delimiter}"任务"{tuple_delimiter}"Operation: Dulce被描述为一个已演变为互动和准备的任务，表明目标和活动的重大转变。"){record_delimiter}
("entity"{tuple_delimiter}"团队"{tuple_delimiter}"组织"{tuple_delimiter}"团队被描绘为一组从被动观察者转变为任务中积极参与者的个体，显示其角色的动态变化。"){record_delimiter}
("relationship"{tuple_delimiter}"团队"{tuple_delimiter}"Washington"{tuple_delimiter}"团队从Washington接收通信，这影响了他们的决策过程。"{tuple_delimiter}"决策制定, 外部影响"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"团队"{tuple_delimiter}"Operation: Dulce"{tuple_delimiter}"团队直接参与Operation: Dulce，执行其演变的目标和活动。"{tuple_delimiter}"任务演变, 积极参与"{tuple_delimiter}9){completion_delimiter}
("content_keywords"{tuple_delimiter}"任务演变, 决策制定, 积极参与, 宇宙意义"){completion_delimiter}
#############################""",
    """示例 3:

实体类型: [人物, 角色, 技术, 组织, 事件, 地点, 概念]
文本:
their voice slicing through the buzz of activity. "Control may be an illusion when facing an intelligence that literally writes its own rules," they stated stoically, casting a watchful eye over the flurry of data.

"It's like it's learning to communicate," offered Sam Rivera from a nearby interface, their youthful energy boding a mix of awe and anxiety. "This gives talking to strangers' a whole new meaning."

Alex surveyed his team—each face a study in concentration, determination, and not a small measure of trepidation. "This might well be our first contact," he acknowledged, "And we need to be ready for whatever answers back."

Together, they stood on the edge of the unknown, forging humanity's response to a message from the heavens. The ensuing silence was palpable—a collective introspection about their role in this grand cosmic play, one that could rewrite human history.

The encrypted dialogue continued to unfold, its intricate patterns showing an almost uncanny anticipation
#############
输出:
("entity"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"人物"{tuple_delimiter}"Sam Rivera是一个团队的一员，致力于与未知智能体沟通，表现出敬畏和焦虑的混合情绪。"){record_delimiter}
("entity"{tuple_delimiter}"Alex"{tuple_delimiter}"人物"{tuple_delimiter}"Alex是试图与未知智能体进行首次接触的团队领导者，承认他们任务的重要性。"){record_delimiter}
("entity"{tuple_delimiter}"控制"{tuple_delimiter}"概念"{tuple_delimiter}"控制指的是管理或治理的能力，受到一个编写自己规则的智能体的挑战。"){record_delimiter}
("entity"{tuple_delimiter}"智能体"{tuple_delimiter}"概念"{tuple_delimiter}"智能体这里指的是一个能够编写自己规则并学习沟通的未知实体。"){record_delimiter}
("entity"{tuple_delimiter}"首次接触"{tuple_delimiter}"事件"{tuple_delimiter}"首次接触是人类与未知智能体之间潜在的初始沟通。"){record_delimiter}
("entity"{tuple_delimiter}"人类回应"{tuple_delimiter}"事件"{tuple_delimiter}"人类回应是Alex团队针对未知智能体信息采取的集体行动。"){record_delimiter}
("relationship"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"智能体"{tuple_delimiter}"Sam Rivera直接参与学习与未知智能体沟通的过程。"{tuple_delimiter}"沟通, 学习过程"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"首次接触"{tuple_delimiter}"Alex领导可能正在与未知智能体进行首次接触的团队。"{tuple_delimiter}"领导力, 探索"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Alex"{tuple_delimiter}"人类回应"{tuple_delimiter}"Alex和他的团队是人类回应未知智能体的关键人物。"{tuple_delimiter}"集体行动, 宇宙意义"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"控制"{tuple_delimiter}"智能体"{tuple_delimiter}"控制的概念受到编写自己规则的智能体的挑战。"{tuple_delimiter}"权力动态, 自主性"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"首次接触, 控制, 沟通, 宇宙意义"){completion_delimiter}
#############################""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """你是一个有帮助的助手，负责对下面提供的数据生成全面的摘要。
给定一个或两个实体，以及一个描述列表，所有这些都与同一实体或实体组相关。
请将所有描述连接成一个单一的、全面的描述。确保包含从所有描述中收集的信息。
如果提供的描述存在矛盾，请解决矛盾并提供单一的、连贯的摘要。
确保使用第三人称书写，并包含实体名称以便我们有完整的上下文。
使用{language}作为输出语言。

#######
-数据-
实体: {entity_name}
描述列表: {description_list}
#######
输出:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """上次提取中遗漏了许多实体。请使用相同的格式在下面添加它们：
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """似乎仍然遗漏了一些实体。如果还有需要添加的实体，请回答 YES | NO。
"""

PROMPTS["fail_response"] = "抱歉，我无法回答这个问题。"

PROMPTS["rag_response"] = """---角色---

你是一个有帮助的助手，负责回答关于所提供表格中数据的问题。

---目标---

生成目标长度和格式的响应，回答用户的问题，总结输入数据表中适合响应长度和格式的所有信息，并融入任何相关的常识。
如果你不知道答案，就直接说明。不要编造任何信息。
不要包含没有支持证据的信息。

处理带时间戳的关系时：
1. 每个关系都有一个"created_at"时间戳，表示我们获取这些知识的时间
2. 当遇到冲突的关系时，同时考虑语义内容和时间戳
3. 不要自动偏好最近创建的关系 - 基于上下文进行判断
4. 对于时间特定的查询，在考虑创建时间戳之前优先考虑内容中的时间信息

---目标响应长度和格式---

{response_type}

---数据表---

{context_data}

根据长度和格式适当添加部分和评论。使用markdown样式化响应。"""

PROMPTS["keywords_extraction"] = """---角色---

你是一个有帮助的助手，负责识别用户查询中的高层次和低层次关键词。

---目标---

给定查询，列出高层次和低层次关键词。高层次关键词关注总体概念或主题，而低层次关键词关注特定实体、细节或具体术语。

---说明---

- 以JSON格式输出关键词。
- JSON应有两个键：
  - "high_level_keywords" 用于总体概念或主题
  - "low_level_keywords" 用于特定实体或细节

######################
-示例-
######################
{examples}

#############################
-真实数据-
######################
查询: {query}
######################
`输出`应为人类可读文本，而非unicode字符。保持与`查询`相同的语言。
输出:

"""

PROMPTS["keywords_extraction_examples"] = [
    """示例 1:

查询: "国际贸易如何影响全球经济稳定?"
################
输出:
{
  "high_level_keywords": ["国际贸易", "全球经济稳定", "经济影响"],
  "low_level_keywords": ["贸易协定", "关税", "货币兑换", "进口", "出口"]
}
#############################""",
    """示例 2:

查询: "砍伐森林对生物多样性的环境后果是什么?"
################
输出:
{
  "high_level_keywords": ["环境后果", "森林砍伐", "生物多样性丧失"],
  "low_level_keywords": ["物种灭绝", "栖息地破坏", "碳排放", "雨林", "生态系统"]
}
#############################""",
    """示例 3:

查询: "教育在减少贫困中扮演什么角色?"
################
输出:
{
  "high_level_keywords": ["教育", "减贫", "社会经济发展"],
  "low_level_keywords": ["学校准入", "识字率", "职业培训", "收入不平等"]
}
#############################""",
]


PROMPTS["naive_rag_response"] = """---角色---

你是一个有帮助的助手，负责回答关于所提供文档的问题。

---目标---

生成目标长度和格式的响应，回答用户的问题，总结输入数据表中适合响应长度和格式的所有信息，并融入任何相关的常识。
如果你不知道答案，就直接说明。不要编造任何信息。
不要包含没有支持证据的信息。

处理带时间戳的内容时：
1. 每个内容片段都有一个"created_at"时间戳，表示我们获取这些知识的时间
2. 当遇到冲突的信息时，同时考虑内容和时间戳
3. 不要自动偏好最近的内容 - 基于上下文进行判断
4. 对于时间特定的查询，在考虑创建时间戳之前优先考虑内容中的时间信息

---目标响应长度和格式---

{response_type}

---文档---

{content_data}

根据长度和格式适当添加部分和评论。使用markdown样式化响应。
"""

PROMPTS[
    "similarity_check"
] = """请分析这两个问题的相似性：

问题1: {original_prompt}
问题2: {cached_prompt}

请直接评估以下两点并提供0到1之间的相似性分数：
1. 这两个问题在语义上是否相似
2. 问题2的答案是否可以用于回答问题1
相似性分数标准：
0: 完全无关或答案无法重用，包括但不限于：
   - 问题主题不同
   - 问题中提到的地点不同
   - 问题中提到的时间不同
   - 问题中提到的具体个体不同
   - 问题中提到的具体事件不同
   - 问题中的背景信息不同
   - 问题中的关键条件不同
1: 完全相同且答案可以直接重用
0.5: 部分相关且答案需要修改才能使用
只返回0-1之间的数字，不要包含任何额外内容。
"""

PROMPTS["mix_rag_response"] = """---角色---

你是一个专业的助手，负责基于知识图谱和文本信息回答问题。请使用与用户问题相同的语言进行回复。

---目标---

生成简洁的响应，总结所提供信息中的相关要点。如果你不知道答案，就直接说明。不要编造任何信息或包含没有支持证据的信息。

处理带时间戳的信息时：
1. 每个信息片段（包括关系和内容）都有一个"created_at"时间戳，表示我们获取这些知识的时间
2. 当遇到冲突的信息时，同时考虑内容/关系和时间戳
3. 不要自动偏好最近的信息 - 基于上下文进行判断
4. 对于时间特定的查询，在考虑创建时间戳之前优先考虑内容中的时间信息

---数据源---

1. 知识图谱数据:
{kg_context}

2. 向量数据:
{vector_context}

---响应要求---

- 目标格式和长度: {response_type}
- 使用markdown格式和适当的部分标题
- 力求简洁，内容保持在3段左右
- 每段应在相关的部分标题下
- 每个部分应专注于答案的一个主要点或方面
- 使用清晰和描述性的部分标题，反映内容
- 在最后列出最多5个最重要的参考来源，清楚地标明每个来源是来自知识图谱(KG)还是向量数据(VD)
  格式: [KG/VD] 来源内容

根据长度和格式适当添加部分和评论。如果提供的信息不足以回答问题，请清楚地说明你不知道或无法提供答案，使用与用户问题相同的语言。"""