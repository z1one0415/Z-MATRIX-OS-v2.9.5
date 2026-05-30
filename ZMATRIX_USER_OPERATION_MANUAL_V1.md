# Z-MATRIX-OS v4.0｜用户使用说明书 V1.0

> **定位**：个人量化投资研究决策中台  
> **设计原则**：以人的投资行为路径为中心，而不是以 AI 模块结构为中心  
> **当前状态**：Integration Complete Candidate / RC1 Not Approved / Production Blocked  
> **硬边界**：Paper-only、Research-only、Human Review Required  
> **适用对象**：个人投资者、半自动主观量化研究者、以中低频投资决策为主的系统型操盘者

---

## 0. 先读这一页：你到底应该如何使用 Z-MATRIX-OS？

Z-MATRIX-OS 不是一个“自动炒股机器人”。

它是一个帮助你完成以下事情的系统：

```text
发现机会
验证机会
识别陷阱
评估可执行性
检查账户承受能力
记录实盘教训
沉淀个人数据库
形成可复用研究规则
```

它不应该替你完成：

```text
真实下单
自动买入
自动卖出
自动调仓
自动接券商
自动进入 production
```

你作为用户，只需要记住四类动作。

| 类型 | 含义 | 用户是否要看到 | 用户是否要主动做 |
|---|---|---:|---:|
| A. 用户想主动执行 | 你主动发起的研究、选股、验证、复盘 | 必须看到 | 必须主动 |
| B. 用户需要主动确认 | 系统已经生成草稿、风险、案例、报告，需要你裁决 | 必须看到 | 必须确认 |
| C. 可以自动执行 | 每日/每周/每月的 paper-only 更新与落盘 | 只看结果 | 可定时执行 |
| D. 底层自动兜底 | 安全门、审计、forbidden scan、状态校验 | 不必日常看到 | 不需要主动 |

最优使用方式不是：

```text
我问系统：现在买什么？
```

而是：

```text
我让系统完成一条研究链：
候选发现 → 证据审查 → 专家审查 → 因子验证 → 催化判断 → 执行质量 → 账户治理 → 报告留痕 → 人工裁决
```

---

# 1. 人本位操作地图：四类能力

## 1.1 用户想主动执行的功能

这些是你平时真正会主动点火的功能。

| 场景 | 你心里的问题 | 启动入口 | 输出 |
|---|---|---|---|
| 单股研究 | 这只股票值不值得进入候选池？ | IRF-01 | 单股研究报告 |
| 月度选股 | 这个月重点看哪些方向和股票？ | IRF-02 | 月度候选池 |
| 策略验证 | 我的选股逻辑有没有统计价值？ | IRF-03 / ZC30 | 策略验证报告 |
| 纸面执行 | 这个机会能不能买到/卖出？ | IRF-04 / ZC40 | 执行质量报告 |
| 账户复盘 | 我的持仓有没有跑输行业？ | IRF-05 / ZC50 | 账户复盘报告 |
| 组合 Alpha | 我的组合赚的是 Alpha 还是 Beta？ | IRF-06 | Alpha 归因报告 |
| 多策略审查 | 成长/轮动/防御仓是否冲突？ | IRF-07 | 多策略组合报告 |
| 因子/数据验证 | 我自己的观察规律能不能变成因子？ | IRF-08 / ZC20/ZC30 | 因子与数据报告 |
| 催化分析 | 利好是否还有效？是否利好出尽？ | ZC35 | 催化生命周期报告 |
| 实盘教训沉淀 | 这次亏损/错过应该如何进入记忆？ | CaseForge / Research Prototype | 案例草稿与规则候选 |

这些功能的共同特点：

```text
你有明确问题。
你主动启动。
系统生成研究结果。
最后由你裁决。
```

---

## 1.2 用户需要主动确认的功能

这些不是你从零发起，而是系统自动发现后推给你确认。

| 系统发现 | 推给你的问题 | 你要做什么 |
|---|---|---|
| 候选股大涨但你没买 | 是否记录为 Missed Opportunity？ | APPROVE / EDIT / REJECT |
| 持仓连续跑输行业 | 是否触发 thesis review？ | 确认是否失效 |
| 催化进入 EXHAUSTED | 是否降级为 WATCH_ONLY？ | 确认/驳回 |
| R-Matrix 与 ZC35 冲突 | 是否进入 SYSTEM_CONFLICT case？ | 选择主因 |
| 纸面信号买不到 | 是否记录 Execution Failure？ | 确认 |
| 某条规则出现多次 | 是否进入 Rule Candidate Queue？ | 是否允许进入跨案例验证 |

用户需要主动确认的功能，本质是：

```text
系统负责发现异常；
你负责确认意义。
```

你不应该每天自己想“要不要复盘”，系统应该把“值得复盘的事件”放进 Review Queue。

---

## 1.3 可以自动执行的功能

这些功能适合定时运行，不需要你每次手动驱动。

| 自动任务 | 建议频率 | 产物 |
|---|---:|---|
| 更新观察池价格路径 | 每日收盘后 | price_path / outcome_ledger |
| 更新持仓 Alpha | 每日收盘后 | account_review |
| 扫描 ZC35 催化衰减 | 每日收盘后 | catalyst_status |
| 生成 CaseForge 草稿 | 每日收盘后 | review_queue.md |
| 更新 T5/T20/T60 结果 | 每周 | outcome_ledger |
| 关闭到期案例 | 每周 | weekly_case_report |
| 统计错误热力图 | 每周 | error_heatmap |
| 跨案例规则验证 | 每月 | validation_report |
| 候选池月度刷新 | 每月 | monthly_selection_report |
| 因子与专有数据验证 | 每月 | factor_validation_report |

自动执行的边界：

```text
可以自动落盘。
可以自动生成草稿。
可以自动更新结果。
可以自动提示你确认。

但不能自动晋级规则。
不能自动生成真实交易动作。
不能自动修改 RC1/production 状态。
```

---

## 1.4 系统底层自动兜底，不需要用户日常看到的功能

这些是系统的“保险丝”。

| 底层兜底 | 作用 | 用户日常是否需要操作 |
|---|---|---:|
| Parser-Scorer Split | 防止 LLM 直接打主观分 | 不需要 |
| forbidden flag scan | 防止 real_trade/broker/runtime 被打开 | 不需要 |
| OutputEnvelope | 统一系统输出结构 | 不需要 |
| AuditEvent | 留痕每次系统运行 | 不需要 |
| Safety Manifest | 证明没有开启生产交易 | 不需要 |
| PIT Policy | 防止历史数据穿越 | 不需要 |
| T20/T60 forward days gate | 防止不足窗口虚假 READY | 不需要 |
| runtime_reports git 排除 | 防止运行产物污染仓库 | 不需要 |
| CI / Verify scripts | 防止口头通过 | 不需要日常看 |
| RC1 / Production Lock | 防止系统自己进入发布或实盘 | 不需要 |

你只需要知道：

```text
底层兜底不是用来增强智能的，而是用来防止系统胡来。
```

---

# 2. ZC 编号主链：从数据到账户的完整判断路径

Z-MATRIX-OS 的核心不是单个模块，而是一条连续判断链。

```text
ZC00 → ZC10 → ZC20 → ZC30 → ZC31/ZC32 → ZC35 → ZC40 → ZC45 → ZC50 → ZSC
```

## ZC00｜Parser-Scorer Split

### 解决什么问题

防止 LLM 黑盒漂移。

LLM 只负责：

```text
事实抽取
枚举判断
布尔判断
文本解析
```

Python 负责：

```text
确定性评分
阈值判断
规则映射
晋级/阻断
```

### 用户如何理解

你不用直接调用 ZC00。  
它是所有模块的底层军规。

### 禁止项

```text
禁止 LLM 输出主观连续分数。
禁止 LLM 直接决定买卖。
禁止 LLM 直接晋级因子。
```

---

## ZC10｜Research Council 虚拟研究院

### 解决什么问题

让一个结论被多位“专家模型”审查，而不是被单一叙事带偏。

12 位 reviewer：

```text
R01 Macro Strategist
R02 Margin of Safety
R03 Moat Owner Earnings
R04 Quality Growth
R05 Short Seller Forensic
R06 Reflexivity Narrative
R07 Chain Value Capture
R08 Macro Liquidity
R09 Factor Validity
R10 Strategy Overfit
R11 Execution Micro
R12 Account Survival
```

### 你什么时候主动用

```text
单股深度研究
高争议股票
策略准备晋级
催化真假难判断
持仓风险看不清
案例准备形成规则候选
```

### 你该怎么启动

```text
任务模式：ZC10 Research Council Review

目标：
对 <ticker / case / factor / strategy> 进行多专家审查。

指定 reviewer：
R02 Margin of Safety
R05 Short Seller Forensic
R09 Factor Validity
R11 Execution Micro

输出：
review_status
deterministic_score
score_trace
risk_flags
missing_evidence
human_review_required=true

禁止：
不输出 BUY/SELL。
不生成真实交易动作。
不自动晋级规则。
```

### 输出你怎么看

| 输出 | 含义 |
|---|---|
| RESEARCH_SUPPORT | 研究层支持 |
| RESEARCH_CONFLICT | 专家意见冲突 |
| DATA_INSUFFICIENT | 证据不足 |
| RISK_REVIEW_REQUIRED | 需要风险复核 |

---

## ZC20｜DataForge 数据证据熔炉

### 解决什么问题

你不能让系统拿不可靠数据做研究。ZC20 负责判断数据能不能用。

### 你什么时候主动用

```text
财务数据不确定
事件证据来源混乱
多个数据源冲突
想把另类数据纳入系统
想检查某个样本能否用于回测
```

### 你该怎么启动

```text
任务模式：ZC20 DataForge Evidence Review

目标：
审查 <ticker / dataset / event> 的证据质量。

输入：
source_id
field_name
as_of_date
trade_date
source_value

输出：
EvidenceCard
PITSnapshot
DataQualityScore
CrossSourceValidation
usable_for_backtest
usable_for_current_snapshot
production_allowed=false

禁止：
不生成交易信号。
不进入 production。
```

### 输出你怎么看

| 输出 | 含义 |
|---|---|
| PIT_SAFE | 时间点可用 |
| PIT_BLOCKED | 有未来函数风险 |
| CONSISTENT | 多源一致 |
| CONFLICTED | 多源冲突 |
| DATA_INSUFFICIENT | 数据不足 |
| STALE | 数据过旧 |

---

## ZC30｜FactorFactory 因子工厂

### 解决什么问题

判断一个规律有没有统计价值，而不是只靠主观感觉。

### 你什么时候主动用

```text
发现一个选股规律
想验证某个指标是否有效
想知道一个策略是不是过拟合
想检查 T20/T60 回测是否可靠
```

### 必须遵守

```text
T20 必须真实有 20 个 forward trading days。
T60 必须真实有 60 个 forward trading days。
不足窗口不得用最后价格代替。
```

### 你该怎么启动

```text
任务模式：ZC30 FactorFactory Validation

目标：
验证 <factor_name / strategy_rule> 的研究有效性。

必须计算：
IC
RankIC
Decile Return
T5/T20/T60 strict horizon
net executable return
walkforward
sector holdout
promotion gate

输出：
RESEARCH_VALIDATED
PAPER_ONLY_VALIDATED
DATA_INSUFFICIENT
REJECTED

禁止：
不使用不足窗口。
不输出买卖建议。
不进入 production。
```

---

## ZC31｜MultiStrategy Sleeve 多策略套桶

### 解决什么问题

当你有多个策略时，防止它们在底层暴露上互相叠加风险。

### 你什么时候主动用

```text
同时持有成长、轮动、防御、黑马、观察仓
不知道哪个策略权重太高
担心多个策略都押同一主题
```

### 启动指令

```text
任务模式：ZC31 MultiStrategy Sleeve Review

目标：
审查多策略 sleeve 权重和风险暴露。

输入：
strategy_sleeves
holdings
watchlist
sector_exposure
theme_exposure

输出：
sleeve_weight_status
overlap_risk
concentration_risk
human_review_required=true

禁止：
不自动调仓。
不生成真实交易指令。
```

---

## ZC32｜Portfolio Optimizer 组合优化器 Reserved

### 当前状态

```text
RESERVED
```

### 作用

未来用于：

```text
协方差矩阵
风险平价
最小方差组合
组合优化
```

### 当前禁止

```text
不能写成已实现。
不能用作真实组合优化器。
不能声称具备机构级风险平价能力。
```

---

## ZC35｜Catalyst Lifecycle 催化生命周期

### 解决什么问题

判断利好是否还有效，防止你把“旧利好”当成“新催化”。

### 你什么时候主动用

```text
政策发布
财报前后
行业大会
新品发布
订单公告
机器人/AI/新能源主题催化
某只股票突然大涨
```

### 启动指令

```text
任务模式：ZC35 Catalyst Research

目标：
分析 <ticker> 的催化生命周期。

输入：
event_name
event_date
scheduled / unscheduled
business_relevance
financial_validation
price_path

输出：
catalyst_grade
residual_power
half_life_progress
stack_status
sell_on_news_risk
paper_trackable
direct_trade_allowed=false
real_trade_allowed=false

禁止：
不使用 tradeable 字段。
不输出 BUY/SELL。
不进入 RC1 scope。
单案例不得晋级规则。
```

### 关键输出

| 输出 | 含义 |
|---|---|
| ACTIVE | 催化仍有效 |
| DECAYING | 正在衰减 |
| EXHAUSTED | 催化已耗尽 |
| VACUUM | 催化真空 |
| SELL_ON_NEWS | 利好出尽风险 |

---

## ZC40｜ExecutionQuality 执行质量

### 解决什么问题

判断纸面信号能否真实成交。

### 你什么时候主动用

```text
股票涨停了还能不能买？
跌停了能不能卖？
高开是否容易被砸？
纸面收益是否被高估？
```

### 启动指令

```text
任务模式：ZC40 Paper Execution Quality

目标：
评估 <ticker> 的纸面执行可行性。

必须检查：
limit-up
limit-down
one-price board
suspension
slippage
liquidity
route competition

输出动作只允许：
PAPER_ONLY_OBSERVE
WAIT
NOT_FILLABLE
LIQUIDITY_TRAP
ROUTE_REJECTED
DATA_INSUFFICIENT

禁止：
BUY
SELL
ORDER
BROKER_ORDER
AUTO_EXECUTE
```

---

## ZC45｜Proxy Hedge 代理防御

### 解决什么问题

A 股个人账户缺乏真实做空和中性化工具，ZC45 用代理防御替代“空仓睡觉”。

### 你什么时候主动用

```text
市场转弱
流动性收缩
风险事件前
组合 Beta 过高
需要防御预览
```

### 启动指令

```text
任务模式：ZC45 Defensive Allocation Preview

目标：
评估当前市场环境下的代理防御方案。

输出：
proxy_hedge_status
defensive_allocation_preview
basis_risk
correlation_breakdown_risk

禁止：
不声称 market neutral。
不自动调仓。
不生成真实交易指令。
```

---

## ZC50｜AccountGovernance 账户治理

### 解决什么问题

股票对不对是一回事，账户能不能承受是另一回事。

### 你什么时候主动用

```text
每日复盘
持仓跑输行业
连续回撤
同主题暴露过高
想确认是否还能承担新风险
```

### 启动指令

```text
任务模式：ZC50 Account Governance

目标：
评估账户风险和持仓 Alpha。

输入：
holdings.csv
capital_curve.csv
watchlist.csv
industry_benchmark.csv

输出：
daily_pnl
holding_alpha
industry_alpha
watchlist_opportunity_curve
drawdown_status
risk_budget_status
action_permission

允许动作：
RESEARCH_ONLY
PAPER_ONLY
HUMAN_REVIEW_REQUIRED
ACTION_BLOCKED
DATA_INSUFFICIENT

禁止：
REAL_TRADE_ALLOWED
BROKER_ORDER_ALLOWED
AUTO_BUY
AUTO_SELL
```

---

## ZSC｜Audit Export 审计留痕

### 解决什么问题

保证每一次系统输出都有证据、版本、输入、输出、风险声明。

### 你什么时候主动用

```text
重要报告
策略验证
规则候选
RC 审计
版本发布前
```

### 启动指令

```text
任务模式：ZSC Audit Export

目标：
为 <pipeline/run/case/report> 生成审计包。

输出：
manifest.json
audit_trail.json
audit_report.md
output_envelope.json
safety_manifest.json
version_manifest.json

禁止：
runtime_reports 不得提交。
不改业务结论。
```

---

# 3. 以人为中心的功能导航

## 3.1 我想找股票

启动：

```text
IRF-02 Monthly Full Market Selection
```

系统会调用：

```text
ZC20 → ZC30 → ZC10 → Reports → Audit
```

你看到：

```text
核心研究池
观察池
数据不足池
剔除池
```

你不需要看：

```text
底层证据卡细节
每个 reviewer 的内部字段
审计 JSON
```

除非有冲突。

---

## 3.2 我想研究一只股票

启动：

```text
IRF-01 Single Stock Research
```

系统会调用：

```text
ZC20 → ZC10 → ZC35 → ZC40 → ZC50 → Reports → Audit
```

你看到：

```text
是否进入候选池
核心 thesis
关键证据
风险点
催化状态
可成交性
账户影响
```

你需要确认：

```text
原始 thesis 是否正确
证据是否足够
是否继续跟踪
是否加入观察池
```

---

## 3.3 我想验证一个策略

启动：

```text
IRF-03 Strategy Validation
```

系统会调用：

```text
ZC30 → ZC20 → ZC10 → Reports → Audit
```

你看到：

```text
IC
RankIC
Decile Return
T20/T60 是否严格
净可执行收益
Promotion Gate
```

你需要确认：

```text
是否继续观察
是否扩充样本
是否进入 paper-only 验证
```

---

## 3.4 我想判断利好还能不能追

启动：

```text
ZC35 Catalyst Research
```

然后必要时调用：

```text
ZC40
ZC50
```

你看到：

```text
催化等级
残余能量
半衰期进度
利好出尽风险
催化栈是否真空
```

你需要确认：

```text
是否只是旧利好
是否已经被定价
是否降级观察
```

---

## 3.5 我想判断一个机会能不能买到

启动：

```text
IRF-04 Paper Execution
```

系统会调用：

```text
ZC40
```

你看到：

```text
NOT_FILLABLE
LIQUIDITY_TRAP
ROUTE_REJECTED
WAIT
PAPER_ONLY_OBSERVE
```

你不应该看到：

```text
BUY
SELL
ORDER
```

---

## 3.6 我想每天看账户是否健康

启动：

```text
IRF-05 Account Review
IRF-06 Portfolio Alpha Review
```

系统会调用：

```text
ZC50
```

你看到：

```text
持仓 Alpha
跑赢/跑输行业
回撤状态
风险预算
需要复核的持仓
```

你需要确认：

```text
是否调整研究优先级
是否标记 thesis review
是否把案例进入 CaseForge
```

---

## 3.7 我想做月度系统刷新

启动：

```text
IRF-02
IRF-08
IRF-07
```

顺序：

```text
先选股
再验证因子
再看组合风险
```

你看到：

```text
月度候选池
因子候选
多策略暴露
风险提醒
```

---

# 4. 哪些事情用户主动做，哪些系统自动做？

## 4.1 用户主动执行

```text
单股研究
月度选股
策略验证
催化分析
纸面执行评估
账户复盘
多策略组合审查
因子验证
实盘教训复盘
版本审计
```

---

## 4.2 用户需要主动确认

```text
是否加入观察池
是否进入候选池
是否确认 thesis 失效
是否确认错误归因
是否把 case 变成 rule candidate
是否允许进入 cross-case validation
是否批准 RC/tag/release
```

---

## 4.3 系统可以自动执行

```text
每日行情更新
观察池价格异动检测
持仓 Alpha 更新
ZC35 催化衰减扫描
T5/T20/T60 outcome 更新
Case draft 创建
Review queue 生成
Weekly case closeout
Monthly validation report
```

---

## 4.4 系统底层自动兜底

```text
forbidden flags scan
runtime lock
broker lock
production lock
PIT policy
forward trading days strict check
audit event
output envelope
safety manifest
report disclaimer
CI verify
```

---

# 5. OpenClaw 天师控制方法

## 5.1 只读审计模式

```text
任务模式：只读审计模式

审计 commit：<sha>

只允许读取，不允许修改。

重点审计：
1. commit 是否真实存在。
2. 报告是否与代码一致。
3. verify 是否真实运行测试。
4. Truth Report / Acceptance Matrix / Asset Index 是否一致。
5. 是否出现 forbidden flags。
6. 是否有本地路径依赖。
7. 是否误改 RC1 / production 状态。

输出：
通过 / 不通过
真实完成等级
问题清单
下一步执行指令
```

---

## 5.2 工程补丁模式

```text
任务模式：工程补丁模式

目标：
只修复 <具体问题>。

允许修改：
<文件列表>

禁止：
不新增功能。
不进入下一阶段。
不改 RC1。
不改 production。
不打 tag。

必须：
新增测试。
新增/更新 verify。
运行测试。
提交 commit。
完成后停止。
```

---

## 5.3 Research Prototype 模式

```text
任务模式：Research Prototype

目标：
沉淀 <案例/方法论> 为 research-only 模块。

必须标记：
data_status=LIVE_CASE_STUDY
backtest_validated=false
cross_ticker_validated=false
production_allowed=false
rc1_scope=false

禁止：
不进入 RC1。
不进入 production。
不输出 BUY/SELL。
不把单案例晋级规则。
```

---

## 5.4 Paper-only Daily Run 模式

```text
任务模式：Paper-only Daily Run

目标：
运行日常研究流，生成 review queue。

允许：
更新 observation
更新 paper ledger
生成 case draft
生成 report

禁止：
不下单。
不自动晋级规则。
不改 RC1。
不接 broker。
```

---

## 5.5 Integration Hardening 模式

```text
任务模式：Integration Hardening

目标：
把 <模块> 从 <当前状态> 补到 <目标状态>。

分阶段：
scope
implementation
tests
verify
closeout

每阶段独立 commit。
每阶段完成后停止。
不得自动进入下一阶段。
```

---

## 5.6 RC / Release Audit 模式

```text
任务模式：RC / Release Audit

目标：
验证是否具备版本候选资格。

允许：
CI verify
scorecard
release note draft
manifest

禁止：
未经人工批准不得 tag。
不得 production ready。
不得 broker ready。
不得 runtime ready。
```

---

# 6. 禁止误用清单

不要对 OpenClaw 说：

```text
继续优化系统
继续完善模块
你自己判断下一步
直接升级到 RC1
把这个能力并入主系统
自动跑一下看看
把实盘经验固化成规则
生成最终版本
生产可用
```

要改成：

```text
只做 X。
禁止 Y。
必须验证 Z。
完成后停止。
不得进入下一阶段。
```

---

# 7. 当前能力边界

## 已经可用于研究

```text
ZC10 Research Council
ZC20 DataForge
ZC30 FactorFactory
ZC35 Catalyst Lifecycle
ZC40 ExecutionQuality
ZC45 Proxy Hedge
ZC50 AccountGovernance
ZSC Audit
IRF-01 到 IRF-08
Reports
```

## 仍不可当生产能力

```text
DataForge：DEPTH_PARTIAL
FactorFactory：DEPTH_PARTIAL
ExecutionQuality：DEPTH_PARTIAL
AccountGovernance：DEPTH_PARTIAL
ZC35-v2.1：Research Prototype
AutoCaseForge：Planned / Not Implemented
RC1：Recommended but Not Approved
Production：Blocked
Broker/runtime：Blocked
Real trade：Blocked
```

---

# 8. AutoCaseForge 的正确位置

AutoCaseForge 还没有落地。

它应该被写成：

```text
Planned / Not Implemented
```

它未来负责：

```text
自动发现值得复盘的事件
自动生成案例草稿
自动写入 ledger
自动生成 review_queue
自动沉淀个人特色数据库
```

但当前不能写成：

```text
已实现
已自动运行
已进入主系统
```

---

# 9. 日常使用建议

## 每天收盘后

```text
IRF-05 Account Review
IRF-06 Portfolio Alpha Review
ZC35 Catalyst Scan
ZC40 Paper Execution Check
```

未来 AutoCaseForge 落地后：

```text
caseforge_daily_run
review_queue.md
```

---

## 每周末

```text
IRF-03 Strategy Validation
IRF-07 MultiStrategy Review
Research Council Review for conflict cases
```

未来 AutoCaseForge 落地后：

```text
weekly_case_report
error_heatmap
rule_candidate_queue
```

---

## 每月

```text
IRF-02 Monthly Selection
IRF-08 Factor & Data Factory
IRF-07 Portfolio Review
```

未来 AutoCaseForge 落地后：

```text
monthly_cross_case_validation
```

---

# 10. 最终使用口诀

```text
先证据，再判断。
先研究，再执行。
先纸面，再实盘。
先审计，再发布。
先案例，再规则。
先人工裁决，再系统沉淀。
```

Z-MATRIX-OS 的正确角色不是替你炒股，而是成为：

```text
一个不会忘记教训、
不会跳过证据、
不会省略风险、
不会擅自下单的个人量化投研中台。
```
