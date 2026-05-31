# Z_MATRIX_Research_Cockpit_V2_3｜前端工作台纸面工程设计全书

> **项目名称**：Z-MATRIX Research Cockpit V2.3  
> **系统定位**：个人投资研究操作系统前端驾驶舱 / Paper-only Research Cockpit / Agent-Governed Workbench  
> **执行对象**：OpenClaw 天师 / opencode / DeepSeek-v4-Pro / 前端工程 Agent  
> **设计等级**：A+ 纸面工程设计书  
> **版本状态**：V2.3 Design Spec  
> **核心升级**：重构天机引擎为“天机台 / 天机预警 / 天机签 / 天机卜算”；盘中解读改为按需触发；天机警报与系统通知彻底分流；持仓页降密度、高级感增强。  
> **硬边界**：Paper-only / Human Review Required / Broker Runtime Blocked / Real Trade Blocked / Agent Direct Mutation Blocked  

---

## 0. 版本总裁决

V2.3 在 V2.2 基础上做四项关键修正：

```text
1. 天机引擎从“四个并列按钮”升级为“上层路径智能系统”。
2. 盘中实时解读不再常驻实时盯盘，而是按需点击触发。
3. 今日提醒不再混合新闻/系统/市场事件，拆分为：
   - 天机预警：市场/持仓/观察仓强相关事件
   - 系统通知：数据/Agent/后台/验证相关事件
   - 今日待办：需要用户处理的事项汇总
4. 持仓页设计降密度，突出账户状态、资金曲线、正式仓位、三类观察仓与天机引擎。
```

V2.3 的前端核心不是炫技，而是让用户每天打开系统时能快速知道：

```text
今天市场路径如何？
我的持仓是顺风还是逆风？
有没有需要我立刻关注的预警？
哪些诊断已经自动完成？
哪些需要我手动深入？
系统本身有没有异常？
Agent 有没有待审批动作？
```

---

# 1. V2.3 顶层信息架构

```text
Z-MATRIX Research Cockpit V2.3
├── 顶部状态栏
│   ├── 页面标题
│   ├── Paper-only / Human Review / Broker Blocked
│   ├── 系统通知状态点
│   ├── Agent Proposal 数量
│   └── 当前时间 / 数据新鲜度
│
├── 左侧导航
│   ├── Z-MATRIX Logo
│   ├── 用户画像身份卡
│   ├── 持仓管理
│   ├── 投研选股
│   ├── 历史回溯
│   ├── 专业控制台
│   └── 系统设置
│
├── 中央主工作区
│   ├── 持仓管理页
│   ├── 投研选股页
│   ├── 用户画像页
│   ├── 历史回溯页
│   ├── 专业控制台页
│   └── 系统设置页
│
├── 右侧天机栏
│   ├── 天机引擎卡
│   │   ├── 天机台
│   │   ├── 天机预警
│   │   ├── 天机签
│   │   └── 天机卜算入口
│   ├── 今日待办
│   └── 数据与系统状态
│
├── 系统通知条
│   ├── 顶部小横幅 / 底部小横条
│   └── S3/S4 才打扰用户
│
├── Global Drawer
├── Agent Dock
└── Proposal / Skill / Audit 浮层
```

---

# 2. 产品原则

## 2.1 用户任务导航，不做模块展览

用户不需要直接面对 ZC35、R-Matrix、D-Matrix、AutoCaseForge、FactorFactory 等后台名词。前端应回答：

```text
账户怎么样？
持仓顺逆风如何？
今天有什么必须看？
是否需要调仓复核？
哪些机会值得研究？
系统有没有待处理？
```

## 2.2 天机引擎是上层，不是四个普通按钮

V2.3 冻结定义：

```text
天机引擎 = 市场路径智能层
```

它不是：

```text
前夜战报
叙事雷达
盘中解读
普通新闻公告
系统通知
```

它是上层综合器：

```text
天机引擎
├── 自动吸收：前夜环境、叙事状态、持仓结构、观察仓状态、ZC35 催化生命周期、R-Matrix 相对强弱、用户画像、风险预算
├── 按需吸收：盘中解读结果
├── 自动输出：天机台、天机签、天机预警
└── 手动入口：天机卜算
```

## 2.3 系统通知与天机预警必须分流

```text
天机预警：市场 / 持仓 / 观察仓相关
系统通知：数据 / Agent / Verify / ResearchDB / 后台运行相关
今日待办：两者中真正需要用户处理的事项汇总
```

如果混在一起，前端会变成“公告垃圾桶”，这是必须避免的。

---

# 3. 天机引擎 V2.3 命名体系

## 3.1 一级命名冻结

```text
天机引擎
├── 天机台
├── 天机预警
├── 天机签
└── 天机卜算
```

| 一级模块 | 用户感知 | 系统真实含义 | 自动/手动 |
|---|---|---|---|
| 天机台 | 今日总览台 | 每日自动路径报告 | 自动 |
| 天机预警 | 强提醒 | 强相关路径风险/机会事件 | 自动触发 |
| 天机签 | 挂签式摘要 | 自动诊断结果简明卡 | 自动生成，可点开 |
| 天机卜算 | 手动问询 | 深度诊断工具箱 | 用户手动 |

---

## 3.2 天机台

天机台负责每日自动报告，给用户总览。

```text
天机台
├── 今日总势｜看市场水温
├── 持仓风向｜看顺逆风
├── 观察候变｜看观察仓变化
├── 催化水位｜看事件有效期
└── 今日勿为｜看禁止动作
```

首页展示示例：

```text
今日总势：温和偏暖
持仓风向：3 顺 / 2 逆 / 1 中
观察候变：1 升级候选 / 2 继续观察
催化水位：2 有效 / 1 退潮
今日勿为：不追高旧催化
```

天机台生成策略：

```yaml
tianji_daily_report:
  pre_market_auto: true
  post_market_auto: true
  intraday_auto_polling: false
  intraday_on_demand_only: true
  scope:
    - formal_positions
    - observation_warehouses
    - priority_candidates
    - active_catalysts
    - pending_cases
  output:
    - market_temperature
    - position_wind_status
    - observation_changes
    - catalyst_water_level
    - do_not_do_today
```

### 天机台输出规则

天机台只能输出状态和研究判断，不输出交易动作。

允许：

```text
顺风
逆风
中性
继续观察
进入人工复核
等待新证据
不追高旧催化
```

禁止：

```text
立即买入
立即卖出
自动下单
系统建议买入
系统建议卖出
```

---

## 3.3 天机预警

天机预警负责强相关事件提醒，不等于新闻公告。

```text
天机预警
├── 路径偏航｜原剧本失效风险
├── 催化退潮｜利好效力下降
├── 强弱失衡｜个股明显掉队
├── 观察迁移｜观察仓需升降级
└── 破局复核｜核心 thesis 需复核
```

### 天机预警分级

```text
T1：写入天机台，不提醒
T2：进入天机预警列表
T3：进入今日待办，需要确认
T4：强预警，触发明显动效
```

### 动效规则

```text
无 T3/T4：
  不显示强特效按钮，只显示“今日无强预警”。

有 T3：
  天机预警按钮弱呼吸光。

有 T4：
  天机预警按钮强呼吸光 + 右侧栏置顶 + 今日待办出现。
```

### 示例

```text
T4 路径偏航：
双环传动板块修复但个股不跟，进入 thesis review 边缘。

T3 观察迁移：
麦格米特满足黑马观察增强条件，需要确认是否升级观察等级。

T2 催化退潮：
某持仓旧催化残值下降，暂不构成动作，但需继续观察。
```

---

## 3.4 天机签

天机签是每日自动诊断结果的简明摘要卡。

必须做到：

```text
有意境，但不含糊。
有产品感，但不玄学。
一句签文，必须对应明确诊断。
```

```text
天机签
├── 顺风签｜持仓受环境支持
├── 逆风签｜持仓承压
├── 守位签｜逻辑未破，继续观察
├── 退潮签｜催化效力下降
├── 复核签｜需要人工确认
├── 破局签｜原 thesis 可能失效
└── 等待签｜证据不足，不行动
```

### 天机签标准格式

首页简版：

```text
退潮签｜双环旧催化衰减，需复核。
```

展开详情：

```text
签名：退潮签
对象：双环传动
结论：旧催化进入衰减期，不能继续按强催化理解。
依据：催化残值下降 + 板块修复不跟 + 前期预期已透支。
动作：进入人工复核，不自动交易。
```

### 天机签安全规则

禁止：

```text
必涨
必跌
立即买入
立即卖出
自动下单
天机确认上涨
```

允许：

```text
进入人工复核
继续观察
生成研究记录
等待新证据
降级观察
```

---

## 3.5 天机卜算

天机卜算是手动深度诊断工具箱。

```text
天机卜算
├── 问势｜前夜战报
├── 问因｜叙事雷达
├── 问时｜盘中解读
├── 问寿｜催化体检
├── 问真｜信号验真
├── 问尽｜利好出尽
├── 问载｜催化过载
├── 问脉｜行业催化档案
└── 问位｜观察仓动作
```

| 二级名 | 用户理解 | 功能 |
|---|---|---|
| 问势｜前夜战报 | 看盘前环境 | 宏观水温、板块顺逆风、持仓影响 |
| 问因｜叙事雷达 | 看事件/主题真假 | 主题升温、催化真假、利好是否透支 |
| 问时｜盘中解读 | 看当日入场/出场窗口 | 按需读取选中标的，不自动轮询 |
| 问寿｜催化体检 | 看催化还能撑多久 | 半衰期、残值、退潮期 |
| 问真｜信号验真 | 看是真信号还是假信号 | 业务关联、财务验证、周期共振 |
| 问尽｜利好出尽 | 看是否买预期卖事实 | Sell-on-News 检测 |
| 问载｜催化过载 | 看多重利好是否催熟 | 催化叠加、有效窗口压缩 |
| 问脉｜行业催化档案 | 看行业到底吃什么催化 | 行业差异化规律 |
| 问位｜观察仓动作 | 看观察仓是否升降级 | 底仓/轮动/黑马观察状态迁移 |

### 天机卜算触发规则

```text
前夜战报：自动日课 + 手动可查
叙事雷达：自动日课 + 手动可查
盘中解读：手动触发为主
催化体检：自动摘要 + 手动深挖
信号验真：自动摘要 + 手动深挖
利好出尽：自动摘要 + 手动深挖
催化过载：自动摘要 + 手动深挖
行业催化档案：手动查询为主
观察仓动作：自动摘要 + 手动确认
```

---

# 4. 系统通知独立层

## 4.1 系统通知不进入天机引擎

系统通知回答：

```text
系统本身有没有异常？
数据有没有过期？
Agent 有没有待审批？
Verify 有没有失败？
ResearchDB 有没有阻断？
```

它不回答：

```text
市场路径是否偏航？
持仓是否顺风？
观察仓是否升级？
```

## 4.2 系统通知位置

建议：

```text
顶部状态图标
底部小横条
顶部小横幅
系统设置 / 专业控制台通知中心
```

不建议放在右侧天机主栏里抢空间。

## 4.3 系统通知分级

```text
S1：静默记录
S2：状态点
S3：顶部/底部小横条
S4：阻断横幅
```

### 示例

```text
S1：同步完成。
S2：行情数据轻微延迟。
S3：API 限流，盘中解读将使用 5 分钟缓存。
S4：ResearchDB 数据错误，今日天机台不可用。
```

---

# 5. 今日待办定义

今日待办不是新闻公告，也不是系统通知。

它是：

```text
需要用户今天处理的事项汇总。
```

来源：

```text
天机预警 T3/T4
系统通知 S3/S4
Agent Proposal
AutoCaseForge 入库确认
Outcome 到期验证
规则候选晋级
画像月度复核
```

显示位置：

```text
右侧栏第二层
或
顶部 Proposal / 待办入口
```

### 今日待办示例

```text
1. 双环传动路径偏航，需 thesis review。
2. 麦格米特观察仓升级候选，需确认。
3. Agent 生成 2 条案例记忆，需审批入库。
4. Outcome T20 到期，需确认验证结果。
```

---

# 6. 右侧栏 V2.3 结构

首页右侧栏冻结为：

```text
右侧栏
├── 天机引擎卡
│   ├── 天机台
│   ├── 天机预警
│   ├── 天机签
│   └── 天机卜算入口
│
├── 今日待办
│   ├── 待处理数量
│   ├── T4/T3/S3/S4
│   └── 进入详情
│
└── 数据与系统状态
    ├── ResearchDB
    ├── 行情缓存
    ├── Agent Kernel
    ├── Proposal
    ├── Production Blocked
    └── Broker Blocked
```

## 6.1 天机引擎卡首页展示

```text
天机引擎

天机台
今日总势：温和偏暖
持仓风向：3顺 / 2逆 / 1中
催化水位：2有效 / 1退潮
今日勿为：不追高旧催化

天机预警
T4: 0 / T3: 1 / T2: 2
[打开天机预警]  // 有 T3/T4 时显示动效；无强预警则弱化

天机签
顺风签｜德赛西威逻辑未破
退潮签｜双环旧催化衰减
复核签｜麦格米特需人工确认

天机卜算
[进入手动诊断]
```

## 6.2 无强预警状态

```text
天机预警
今日无强预警
```

按钮不闪烁，不强提醒，只显示静态状态点。

---

# 7. 持仓管理页 V2.3 布局修正

## 7.1 页面总结构

```text
持仓管理页 V2.3

左侧 260px
├── Logo
├── 用户画像身份卡
├── 持仓管理
├── 投研选股
├── 历史回溯
├── 专业控制台
└── 系统设置

顶部 72px
├── 页面标题：持仓管理
├── 副标题：全局视角 · 精准配置 · 动态进化
├── Paper-only / Human Review / Broker Blocked
└── 系统通知状态点

中央主区
├── KPI Strip：3强2弱
├── 资金曲线大卡
├── 正式仓位研究表
└── 三类观察仓卡片组

右侧栏
├── 天机引擎卡
├── 今日待办
└── 数据与系统状态
```

## 7.2 密度规则

V2.3 修正重点：

```text
1. 首页不再铺满小模块。
2. 首页不再放常驻盘中实时解读卡。
3. 首页不展示过多导航入口。
4. 橙色发光减少 40%。
5. 强调资金曲线与正式仓位。
6. 三类观察仓提升权重。
```

## 7.3 KPI Strip

强 KPI：

```text
今日盈亏
总资产
持仓 Alpha
```

弱 KPI：

```text
现金比例
最大回撤
```

规则：

```text
强 KPI 可有小折线
弱 KPI 只显示数值与状态，不放小图
```

## 7.4 资金曲线卡

显示：

```text
净值曲线
沪深300 / 行业基准对比
时间范围
累计收益
年化收益
波动率
夏普比率
最大回撤
```

资金曲线为中央视觉主角。

## 7.5 正式仓位研究表

默认字段：

```text
名称
角色
仓位
浮盈亏
Alpha贡献
信号强度
当前动作
```

隐藏字段进入抽屉：

```text
成本价
现价
市值
行业
细分链条
完整交易记录
```

行高：

```text
64px 以上
```

表格定位：

```text
研究型持仓表，不是券商交易终端。
```

## 7.6 三类观察仓

必须提升权重。

```text
底仓观察
轮动观察
黑马观察
```

每张卡显示：

```text
候选数量
核心候选
今日变化
需要确认的动作
```

---

# 8. 投研选股页 V2.3

投研选股页仍保留 V2.2 主结构，但引入天机结果作为辅助判断。

```text
投研选股
├── 全局扫描
├── 七层过滤
├── 10链 × 5力
├── 31板块顺逆风
├── B/R/D Matrix Top
├── 候选矩阵
└── 天机辅助标签
```

## 8.1 天机辅助标签

候选股卡片上可显示：

```text
顺风签
退潮签
等待签
信号验真通过
利好出尽风险
催化过载风险
```

但不能显示：

```text
买入
卖出
自动执行
```

---

# 9. 用户画像入口 V2.3

用户画像仍保持 V2.2 结构：

```text
左侧导航最上方 UserProfileCard
功能等同一级入口
不进入普通菜单列表
```

显示：

```text
Z-Prime
稳健成长型
中长为主 · 纪律优先
风险可控
```

点击进入：

```text
/user-profile
```

用户画像影响：

```text
天机台判断语气
天机签提醒强度
天机预警阈值
盘中解读是否强调“不要做什么”
观察仓动作建议阈值
```

---

# 10. Agent Dock V2.3

Agent Dock 不参与天机自动诊断，只作为受控交互入口。

可执行：

```text
解释当前页面
查看天机日报
打开天机预警
查看今日待办
查看待审批 Proposal
生成今日研究摘要
```

禁止：

```text
直接批准 Proposal
直接修改 ResearchDB
直接触发真实交易
绕过人工确认
```

---

# 11. Global Drawer V2.3

## 11.1 天机引擎抽屉

```text
天机引擎抽屉
├── 天机台｜今日路径报告
│   ├── 今日总势
│   ├── 持仓风向
│   ├── 观察候变
│   ├── 催化水位
│   └── 今日勿为
│
├── 天机预警｜强相关事件
│   ├── 路径偏航
│   ├── 催化退潮
│   ├── 强弱失衡
│   ├── 观察迁移
│   └── 破局复核
│
├── 天机签｜自动诊断摘要
│   ├── 顺风签
│   ├── 逆风签
│   ├── 守位签
│   ├── 退潮签
│   ├── 复核签
│   ├── 破局签
│   └── 等待签
│
└── 天机卜算｜手动深度问询
    ├── 问势｜前夜战报
    ├── 问因｜叙事雷达
    ├── 问时｜盘中解读
    ├── 问寿｜催化体检
    ├── 问真｜信号验真
    ├── 问尽｜利好出尽
    ├── 问载｜催化过载
    ├── 问脉｜行业催化档案
    └── 问位｜观察仓动作
```

## 11.2 盘中解读抽屉

盘中解读必须按需触发。

```text
盘中解读
├── 选择范围
│   ├── 全部正式仓
│   ├── 核心底仓
│   ├── 中期轮动仓
│   ├── 短期事件仓
│   ├── 底仓观察仓
│   ├── 轮动观察仓
│   └── 黑马观察仓
├── 选择标的
├── 读取并解读
├── 数据状态
│   ├── 数据源
│   ├── 更新时间
│   ├── 是否缓存
│   └── API消耗
├── 解读结果
│   ├── 当前状态
│   ├── 我看到
│   ├── 这意味着
│   ├── 你现在不要
│   ├── 接下来盯
│   └── 需要你确认
└── 可记录动作
    ├── 生成入场研究记录
    ├── 生成出场研究记录
    ├── 加入人工复核
    ├── 记录执行偏差
    └── 暂不处理
```

## 11.3 盘中数据策略

```yaml
intraday_interpretation:
  auto_polling: false
  on_demand_only: true
  max_symbols_per_request: 10
  cache_ttl_minutes: 5
  manual_refresh_cooldown_seconds: 60
  fallback_to_last_snapshot: true
```

---

# 12. 前端数据模型

## 12.1 TianjiDashboard

```ts
export type TianjiDashboard = {
  generatedAt: string
  marketTemperature: 'COLD' | 'NEUTRAL' | 'WARM' | 'HOT' | 'VOLATILE'
  positionWind: {
    favorable: number
    unfavorable: number
    neutral: number
  }
  observationChange: {
    upgradeCandidates: number
    downgradeCandidates: number
    keepWatching: number
  }
  catalystWaterLevel: {
    active: number
    decaying: number
    exhausted: number
  }
  doNotDoToday: string[]
  confidence: 'HIGH' | 'MID' | 'LOW'
}
```

## 12.2 TianjiAlert

```ts
export type TianjiAlert = {
  alertId: string
  level: 'T1' | 'T2' | 'T3' | 'T4'
  type: 'PATH_DEVIATION' | 'CATALYST_DECAY' | 'STRENGTH_IMBALANCE' | 'OBSERVATION_MIGRATION' | 'THESIS_REVIEW'
  title: string
  targetType: 'POSITION' | 'OBSERVATION' | 'CANDIDATE' | 'SECTOR' | 'PORTFOLIO'
  targetId: string
  summary: string
  evidenceRefs: string[]
  actionRequired: boolean
  suggestedActions: Array<'VIEW_DETAIL' | 'REQUEST_REVIEW' | 'CREATE_RESEARCH_RECORD' | 'DEFER'>
  createdAt: string
}
```

## 12.3 TianjiSign

```ts
export type TianjiSign = {
  signId: string
  signType: 'TAILWIND' | 'HEADWIND' | 'HOLDING_GROUND' | 'DECAYING' | 'REVIEW' | 'BREAKING' | 'WAITING'
  signName: '顺风签' | '逆风签' | '守位签' | '退潮签' | '复核签' | '破局签' | '等待签'
  targetName: string
  shortText: string
  fullConclusion: string
  evidenceSummary: string[]
  actionText: string
  drawerRef: string
}
```

## 12.4 TianjiDivinationTool

```ts
export type TianjiDivinationTool = {
  toolId: string
  displayName: string
  subtitle: string
  category: 'ENVIRONMENT' | 'NARRATIVE' | 'INTRADAY' | 'CATALYST' | 'SIGNAL' | 'SECTOR' | 'OBSERVATION'
  triggerMode: 'AUTO_INPUT_AND_MANUAL_QUERY' | 'MANUAL_ONLY'
  apiCostLevel: 'LOW' | 'MID' | 'HIGH'
  requiresManualClick: boolean
}
```

## 12.5 SystemNotification

```ts
export type SystemNotification = {
  notificationId: string
  level: 'S1' | 'S2' | 'S3' | 'S4'
  category: 'DATA' | 'AGENT' | 'VERIFY' | 'RESEARCHDB' | 'SECURITY' | 'SYSTEM'
  title: string
  summary: string
  actionRequired: boolean
  displayMode: 'SILENT' | 'STATUS_DOT' | 'TOP_BAR' | 'BLOCKING_BANNER'
  createdAt: string
}
```

## 12.6 TodayTodo

```ts
export type TodayTodo = {
  todoId: string
  sourceType: 'TIANJI_ALERT' | 'SYSTEM_NOTIFICATION' | 'AGENT_PROPOSAL' | 'CASEFORGE' | 'OUTCOME' | 'PROFILE_REVIEW'
  priority: 'LOW' | 'MID' | 'HIGH' | 'CRITICAL'
  title: string
  summary: string
  actions: Array<'VIEW' | 'APPROVE' | 'REJECT' | 'DEFER' | 'REQUEST_EVIDENCE'>
  createdAt: string
}
```

---

# 13. 视觉设计修正

## 13.1 总体风格

```text
深黑底
高级石墨灰
低饱和琥珀金
克制发光
大留白
少边框
卡片分层
主视觉聚焦资金曲线与天机台
```

## 13.2 橙色发光规则

保留发光：

```text
Logo
当前导航
天机引擎主卡
有 T3/T4 的天机预警
资金曲线主线
关键动作按钮
```

不发光：

```text
普通 KPI
普通表格
普通系统状态
普通数据卡
今日待办普通项
```

## 13.3 密度规则

```text
首页不超过 4 个主模块：
1. KPI Strip
2. 资金曲线
3. 正式仓位
4. 三类观察仓

右侧不超过 3 个主模块：
1. 天机引擎卡
2. 今日待办
3. 数据与系统状态
```

---

# 14. 页面验收标准

## 14.1 持仓页

必须完成：

```text
左侧用户画像卡
顶部安全状态
KPI Strip
资金曲线大卡
正式仓位研究表
三类观察仓
右侧天机引擎卡
今日待办
数据与系统状态
系统通知条
```

## 14.2 天机引擎

必须完成：

```text
天机台
天机预警
天机签
天机卜算
天机抽屉
盘中按需解读抽屉
无强警报状态
有强警报动效状态
```

## 14.3 安全边界

禁止用户操作按钮出现：

```text
真实下单
自动买入
自动卖出
券商下单
系统建议买入
系统建议卖出
Production Ready
Broker Ready
```

允许出现：

```text
创建人工建仓记录
生成入场研究记录
生成出场研究记录
进入人工复核
记录执行偏差
继续观察
```

---

# 15. 工程目录更新建议

```text
frontend/src/components/tianji/
  TianjiEngineCard.tsx
  TianjiDashboardPanel.tsx
  TianjiAlertPanel.tsx
  TianjiSignList.tsx
  TianjiSignCard.tsx
  TianjiDivinationEntry.tsx
  TianjiDrawer.tsx
  TianjiDivinationToolbox.tsx
  IntradayInterpretationDrawer.tsx

frontend/src/components/notifications/
  SystemNotificationBar.tsx
  TodayTodoPanel.tsx
  NotificationStatusDot.tsx

frontend/src/types/
  tianji.ts
  notifications.ts
```

---

# 16. OpenClaw 执行批次 V2.3

## Batch 0：Scope Lock

目标：

```text
更新 V2.3 文档和命名体系。
冻结天机引擎结构。
不写复杂交互。
```

## Batch 1：App Shell 降密度

目标：

```text
重做持仓页框架：
左侧导航、顶部状态、中央三段、右侧三段。
```

## Batch 2：天机引擎卡

实现：

```text
TianjiEngineCard
TianjiDashboardPanel
TianjiAlertPanel
TianjiSignList
TianjiDivinationEntry
```

## Batch 3：天机抽屉

实现：

```text
TianjiDrawer
TianjiDivinationToolbox
TianjiSignDetail
TianjiAlertDetail
IntradayInterpretationDrawer
```

## Batch 4：系统通知与今日待办

实现：

```text
SystemNotificationBar
TodayTodoPanel
NotificationStatusDot
S1/S2/S3/S4
T1/T2/T3/T4
```

## Batch 5：持仓页主内容

实现：

```text
KPI Strip
Capital Curve
Formal Position Research Table
Observation Warehouse Cards
Evidence Footer
Data Freshness Badge
```

## Batch 6：质量与安全验证

实现：

```text
verify_cockpit_frontend_v23.sh
forbidden scan
mock data checks
layout screenshot check
build/lint/test
```

---

# 17. Verify 脚本要求

新增：

```text
scripts/verify_cockpit_frontend_v23.sh
```

必须检查：

```text
1. npm run build PASS
2. npm run lint PASS
3. npm test PASS
4. TianjiEngineCard 存在
5. TianjiDashboardPanel 存在
6. TianjiAlertPanel 存在
7. TianjiSignList 存在
8. TianjiDivinationToolbox 存在
9. IntradayInterpretationDrawer 存在
10. SystemNotificationBar 存在
11. TodayTodoPanel 存在
12. forbidden words 不出现在用户操作按钮
13. auto_polling=false 出现在盘中解读配置
14. 今日提醒不作为新闻公告栏
15. 天机预警与系统通知分离
```

---

# 18. 完成报告格式

```text
## Z-MATRIX Research Cockpit V2.3 Frontend 完成报告

commit:
branch:

### V2.3 Core
- TianjiEngineCard:
- TianjiDashboardPanel:
- TianjiAlertPanel:
- TianjiSignList:
- TianjiDivinationToolbox:
- IntradayInterpretationDrawer:
- SystemNotificationBar:
- TodayTodoPanel:

### Layout
- Holdings page density reduced:
- Sidebar simplified:
- UserProfileCard:
- Capital curve primary:
- Observation warehouse promoted:
- Right sidebar restructured:

### Safety
- intraday auto polling:
- broker/runtime:
- real trade:
- auto buy/sell:
- production:
- agent direct mutation:

### Verify
- build:
- lint:
- test:
- verify_cockpit_frontend_v23:

### Final
V2.3_FRONTEND_READY / BLOCKED
```

---

# 19. 最终设计裁决

V2.3 冻结为：

```text
天机引擎 = 每日路径报告 + 强相关预警 + 自动诊断签 + 手动深度卜算
```

它不再是四个普通按钮。

最终结构：

```text
天机引擎
├── 天机台：每日自动报告
├── 天机预警：强相关路径风险/机会提醒
├── 天机签：自动诊断摘要卡
└── 天机卜算：手动深度工具箱
```

系统通知独立：

```text
系统通知
├── 数据源
├── Agent
├── Verify
├── ResearchDB
├── 安全锁
└── 后台状态
```

今日待办负责汇总：

```text
真正需要用户处理的事项。
```

前端最终原则：

```text
天机有锋芒，
系统有边界，
提醒不混流，
盘中不盯盘，
工具可深挖，
报告自动来。
```
