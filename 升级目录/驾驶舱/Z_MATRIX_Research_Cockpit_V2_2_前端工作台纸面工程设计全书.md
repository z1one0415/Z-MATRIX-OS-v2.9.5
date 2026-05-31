# Z-MATRIX Research Cockpit V2.2｜前端工作台纸面工程设计全书

> **项目名称**：Z-MATRIX Research Cockpit V2.2  
> **系统定位**：个人量化投资研究决策工作台 / Paper-only Research Cockpit / Agent-Governed Research Workbench  
> **执行对象**：OpenClaw 天师 / opencode / 前端 Agent / DeepSeek-v4-Pro  
> **目标**：完成可落地的前端工作台工程蓝图，使 OpenClaw 可按本文 100% 还原搭建前端骨架、页面、组件、状态、交互、Agent Kernel 承载层与验证流程。  
> **边界**：本项目是前端可视化 workbench，不接 broker，不下单，不启 production，不绕过 human review。  
> **版本状态**：Design Spec v2.2 / Frontend Paper Engineering Manual  
> **关键修正**：在 V2.1 基础上补入用户画像身份卡、Agent Kernel 控制层、Proposal 审批中心、Skill 调用观察台、审计链、Evidence Footer、Data Freshness Badge；保留“盘中实时解读区”和“天机引擎”。

---

## 0. 总裁决

Z-MATRIX Research Cockpit V2.2 不是“系统模块展览馆”，也不是“普通金融看板”。

它是：

```text
个人投资研究操作系统的前端驾驶舱
+
Agent 受控运行台
+
ResearchDB 可视化工作台
+
案例记忆与系统内化入口
```

用户打开系统时，不应该看到：

```text
ZC10 / ZC20 / ZC30 / ZC35 / IRF-01 / IRF-08
```

用户应该看到：

```text
我现在账户怎么样？
我每个仓位持有什么？
今天要注意什么？
我想重新选股怎么开始？
我过去的分析和记忆在哪里？
我的用户画像如何影响系统判断？
Agent 正在做什么？
哪些系统建议需要我确认？
```

因此，V2.2 的前端信息架构必须遵循：

```text
用户任务导航
+
用户画像身份锚点
+
Agent 受控操作
+
ResearchDB 真相源
+
Paper-only 安全边界
```

---

# 1. V2.2 相比 V2.1 的关键升级

## 1.1 保留 V2.1 正确方向

保留：

```text
1. 用户任务导航，而不是后台模块导航。
2. 主界面优先解决“持仓怎么样”和“是否需要重新筛股票”。
3. 摘要可见，复杂信息侧边抽屉展开。
4. 重要提醒分级，不把自动同步噪声推给用户。
5. 所有用户输出先说人话。
6. 苹果美学 + Bloomberg Lite + 私人投研工作台气质。
7. Paper-only / Human Review / Production Blocked / Broker Blocked 全局安全边界。
```

## 1.2 修正 V2.1 不足

新增：

```text
1. 用户画像不做普通菜单项，而做左侧导航最上方“用户画像身份卡”。
2. 点击用户画像身份卡进入完整 UserProfilePage。
3. 增加 Agent Control Center。
4. 增加 Proposal Approval Center。
5. 增加 Skill Invocation Console。
6. 增加 Audit Trail。
7. 增加 Evidence Footer。
8. 增加 Data Freshness Badge。
9. 增加 Safety Status Bar。
10. 增加 Agent Dock，受 Z-Agent Kernel 控制。
11. 增加 Agent Kernel API Contract 前置批次。
12. 保留“盘中实时解读区”，定位为盘中执行质量研究模块。
13. 保留“天机引擎”，定位为传播破圈 + 路径预警产品符号。
```

## 1.3 当前版本硬边界

V2.2 前端不得出现：

```text
真实下单
自动买入
自动卖出
券商下单
一键交易
系统建议买入
系统建议卖出
Production Ready
Broker Ready
```

所有“建仓”动作必须命名为：

```text
创建人工建仓记录
```

所有“卖出/减仓”相关动作必须命名为：

```text
生成出场研究记录
进入人工减仓复核
记录实际执行
```

---

# 2. 产品核心原则

## 2.1 人类驾驶舱，而不是模块面板

错误方向：

```text
把后台 ZC / IRF / ResearchDB 模块逐一做成入口。
```

正确方向：

```text
把用户真实投资任务做成入口，后台自动调度模块。
```

用户不需要知道自己正在调用 ZC35、ZC40、ZC50。用户只需要知道：

```text
这只票今天为什么弱？
这个候选应不应该进轮动观察仓？
我的账户是否跑赢 Alpha 基准？
这条利好是不是已经出尽？
Agent 要写入什么，是否需要我批准？
```

## 2.2 主界面只解决两个高频问题

用户每天打开驾驶舱最高频的问题只有两个：

```text
1. 我现在持仓怎么样？
2. 我要不要重新筛股票 / 建仓？
```

因此默认主界面必须优先服务：

```text
持仓管理看板
投研选股工作台
```

其他功能：历史、控制台、设置、用户画像、Agent，都服务这两个主任务。

## 2.3 用户画像是身份锚点，不是普通菜单项

用户画像非常重要，但不应作为普通左侧菜单项出现。

正确承载方式：

```text
左侧导航最上方：
头像 + 用户卡 + 当前画像标签 + 风险状态 + 点击进入详细页面
```

功能上：

```text
等同一级导航。
```

视觉上：

```text
是身份卡 / 人类参数入口 / 系统人格锚点。
```

## 2.4 能自动完成的不要打扰用户

今日提醒不是“任务堆积箱”。它只显示必须让用户知道的事情。

提醒分级：

| 等级 | 处理方式 | 用户是否看到 |
|---|---|---:|
| L0 自动记录 | 自动落盘 | 不看 |
| L1 公告日志 | 状态栏提示 | 可看 |
| L2 待确认 | 提醒栏出现 | 需要看 |
| L3 重要决策 | 弹出操作按钮 | 必须看 |
| L4 风险中断 | 强提醒 | 必须处理 |

默认原则：

```text
普通数据同步、普通价格路径、普通 outcome 更新，自动完成。
亏损案例、thesis 失效、规则晋级、月度内化、Agent 写入 proposal，需要用户确认。
```

## 2.5 所有用户输出必须先说人话

后台可以输出字段、评分、枚举。用户层必须翻译成自然语言判断。

统一输出格式：

```text
当前状态：
我看到：
这意味着：
你现在不要：
接下来盯：
需要你确认：
```

禁止直接给用户：

```text
volume_ratio=2.3
ZC35=DECAYING
ZC40=LIQUIDITY_TRAP
score=0.62
BUY / SELL / AUTO_EXECUTE
```

必须翻译成：

```text
这不是普通回调，而是“板块弱化 + 个股承接不足”的组合状态。
现在不急着动作，先观察它能否跟上板块修复。
```

## 2.6 Agent 是受控工人，不是系统主人

前端所有 Agent 能力必须受：

```text
Z-Agent Kernel
```

约束。

Agent 不得直接写系统，不得直接执行交易，不得绕过人审。

所有写入必须走：

```text
Proposal → Approval → Execution → Verify → Audit
```

---

# 3. 视觉设计总则

## 3.1 关键词

```text
苹果美学
高级
克制
清爽
真实 SaaS
专业金融工作台
低噪声
高可读
低饱和深色
毛玻璃质感
细金属边线
少量铜金属点缀
身份感
智能副驾感
```

不要做：

```text
赛博朋克
霓虹爆炸
大面积炫光
复杂 HUD
密集图表
过度拟物
交易所大屏风
玄学预测软件
```

目标视觉气质：

```text
Apple Pro App + Bloomberg Lite + 私人投研工作台 + 受控 Agent 操作台。
```

## 3.2 色系

### 背景色

```css
--bg-main: #0B0D10;
--bg-marble: #101216;
--bg-panel: rgba(22, 25, 30, 0.72);
--bg-panel-strong: rgba(28, 31, 37, 0.86);
--bg-elevated: rgba(36, 40, 48, 0.78);
```

要求：

```text
深色石墨灰 / 黑曜石底色
允许极轻微大理石纹理
不能出现高对比花纹
背景不能抢信息
```

### 主文字

```css
--text-primary: #F5F7FA;
--text-secondary: #B9C0CC;
--text-tertiary: #7C8492;
--text-muted: #5C6470;
```

### 强调色

```css
--accent-copper: #C49A6C;
--accent-copper-soft: rgba(196, 154, 108, 0.28);
--accent-blue: #6EA8FF;
--accent-green: #5FE19A;
--accent-purple: #9D7CFF;
--accent-amber: #F2C66D;
--accent-red: #FF6B6B;
```

铜金属色只能作为：

```text
边线
分割线
选中态轻描边
编号
小型高亮
用户画像身份卡 hover
```

禁止大面积铜色填充。

## 3.3 毛玻璃与边框

所有主卡片使用：

```css
background: rgba(20, 24, 30, 0.72);
backdrop-filter: blur(18px);
border: 1px solid rgba(255, 255, 255, 0.08);
box-shadow:
  0 18px 60px rgba(0, 0, 0, 0.42),
  inset 0 1px 0 rgba(255, 255, 255, 0.05);
border-radius: 20px;
```

核心选中态：

```css
border: 1px solid rgba(196, 154, 108, 0.52);
box-shadow:
  0 0 0 1px rgba(196,154,108,0.12),
  0 18px 60px rgba(0,0,0,0.45);
```

## 3.4 布局网格

桌面端优先。

```text
设计稿基准：1440 × 900
最小适配：1280 × 800
最大适配：1920 × 1080
```

布局：

```text
顶部状态栏：64px
左侧导航：88px collapsed / 260px expanded
右侧提醒栏：220px–300px，可折叠
主内容区：剩余自适应
Agent Dock：右下悬浮
Global Drawer：右侧滑出
```

## 3.5 字体层级

```css
--font-family: Inter, SF Pro Display, SF Pro Text, PingFang SC, Microsoft YaHei, sans-serif;

--text-xs: 12px;
--text-sm: 13px;
--text-base: 14px;
--text-md: 16px;
--text-lg: 20px;
--text-xl: 24px;
--text-2xl: 32px;
```

页面标题：

```text
24px / 32px / semibold
```

卡片标题：

```text
14px / 20px / medium
```

指标数字：

```text
24px–32px / semibold
```

正文说明：

```text
13px–14px / regular
```

---

# 4. 信息架构

## 4.1 顶层结构

```text
Z-MATRIX Research Cockpit V2.2
├── 顶部状态栏
│   ├── 系统状态
│   ├── Agent 状态
│   ├── 待审批 Proposal 数
│   ├── 最近 Verify 状态
│   └── 数据新鲜度
├── 左侧导航
│   ├── 用户画像身份卡
│   ├── 持仓管理看板
│   ├── 投研选股
│   ├── 历史回溯
│   ├── 专业控制台
│   └── 系统设置
├── 主内容区
├── 右侧重要提醒栏
├── Global Drawer
├── Agent Dock
├── Proposal Approval Center
├── Skill Invocation Console
└── 全局安全锁与审计层
```

## 4.2 左侧导航冻结

左侧导航结构：

```text
UserProfileCard
NavigationItems
SafetyMiniBadge
```

普通导航项只允许：

```text
持仓管理看板
投研选股
历史回溯
专业控制台
系统设置
```

用户画像不进入普通 NavigationItems，而是作为：

```text
左侧导航最上方 UserProfileCard
```

其功能等同一级导航，点击进入：

```text
/user-profile
```

## 4.3 路由冻结

```ts
const routes = [
  { path: '/', element: <HoldingsDashboardPage /> },
  { path: '/research-selection', element: <ResearchSelectionPage /> },
  { path: '/user-profile', element: <UserProfilePage /> },
  { path: '/history', element: <HistoryRecallPage /> },
  { path: '/pro-console', element: <ProConsolePage /> },
  { path: '/settings', element: <SystemSettingsPage /> },
]
```

---

# 5. 页面总览

## 5.1 页面一：持仓管理看板

默认首页。

页面目的：

```text
让用户一眼知道账户状态、每个仓位持有什么、今天要注意什么、是否需要进一步研究。
```

页面结构：

```text
持仓管理看板
├── 账户总览区
├── 仓位明细区
├── Alpha 平行验证区
├── 三个环境按钮
│   ├── 前夜战报
│   ├── 叙事雷达
│   └── 天机引擎
├── 盘中实时解读区
├── 操作研究建议区
└── 右侧重要提醒栏
```

## 5.2 页面二：投研选股

页面目的：

```text
完成全局扫描、分矩阵选股、候选矩阵、个股研究、建仓记录、进入观察仓。
```

页面结构：

```text
投研选股
├── 全局扫描
│   ├── 七层过滤进度
│   ├── 10链 × 5力分析
│   ├── 31板块 Top5 顺风
│   └── 避雷板块
├── 选股矩阵
│   ├── B-Matrix Top
│   ├── R-Matrix Top
│   ├── D-Matrix Top
│   └── 综合候选
├── 候选矩阵
│   ├── 候选状态
│   ├── 适合仓位
│   ├── 个股研究按钮
│   ├── 建仓记录按钮
│   └── 进入三类观察仓按钮
└── 个股研究侧边抽屉
```

## 5.3 页面三：用户画像

页面目的：

```text
呈现和管理 Z-MATRIX 的人类约束模型。
```

页面结构：

```text
用户画像
├── 账户约束
├── 投资角色画像
├── 风险偏好
├── 行为偏差画像
├── Agent 交互偏好
├── 系统建议风格
├── 月度画像更新
└── 画像审计记录
```

## 5.4 页面四：历史回溯

页面目的：

```text
管理个人研究报告、实盘案例、系统记忆、规则候选。
```

页面结构：

```text
历史回溯
├── 搜索与筛选
├── 完整分析报告
├── 实盘案例
├── 系统记忆
│   ├── 核心永固记忆
│   ├── 时效性记忆
│   ├── 过期记忆
│   └── 待清理记忆
└── 规则候选
```

## 5.5 页面五：专业控制台

页面目的：

```text
让高级用户配置投资研究系统参数，并承载 Agent Kernel 可视化治理。
```

内容：

```text
仓位参数
风险预算
ZC35 半衰期
ZC40 执行门槛
ZC50 回撤阈值
AutoCaseForge 自动化策略
记忆半衰期
因子验证阈值
月度内化策略
Agent Kernel
Skill Registry
Proposal Center
Audit Trail
System Safety
```

必须分为：

```text
常用参数
高级参数
危险参数
Agent Kernel
只读安全状态
```

危险参数必须二次确认。

## 5.6 页面六：系统设置

页面目的：

```text
控制系统后台设置，不涉及投资策略逻辑。
```

内容：

```text
API Key
数据源配置
模型配置
显示主题
后台日志
通知设置
本地路径
备份恢复
权限
```

---

# 6. 用户画像身份卡与用户画像页面

## 6.1 UserProfileCard 定位

UserProfileCard 位于左侧导航最上方。

它不是普通头像入口，而是：

```text
功能上等同一级导航。
视觉上承担账户人格、风险状态和系统身份锚点。
```

## 6.2 UserProfileCard 展示内容

建议显示 4 层信息：

```text
头像
账户画像
画像类型
风险/纪律状态
```

示例：

```text
账户画像
稳健成长型
中长为主 · 风险可控
```

有行为偏差时：

```text
账户画像
稳健成长型
追高风险↑ · 待复核
```

回撤压力升高时：

```text
账户画像
防守修复型
回撤压力↑ · 降风险
```

月度待更新时：

```text
账户画像
稳健成长型
画像待更新 · 月度复盘
```

## 6.3 UserProfileCard 数据结构

```ts
export type UserProfileCardData = {
  displayName: string
  avatarType: 'DEFAULT' | 'AI_AVATAR' | 'CUSTOM'
  profileType: 'STEADY_GROWTH' | 'BALANCED_ROTATION' | 'AGGRESSIVE_EVENT' | 'DEFENSIVE_VALUE'
  profileLabel: string
  strategyBiasLabel: string
  riskStatus: 'CONTROLLED' | 'WATCH' | 'ELEVATED' | 'REVIEW_REQUIRED'
  behaviorAlert?: 'CHASE_RISK' | 'LOSS_HOLDING_RISK' | 'CATALYST_BIAS' | 'NONE'
  freshness: 'FRESH' | 'STALE' | 'NEEDS_REVIEW'
}
```

## 6.4 UserProfileCard 视觉规格

```css
.user-profile-card {
  min-height: 92px;
  padding: 16px;
  border-radius: 20px;
  background: rgba(25, 29, 35, 0.72);
  border: 1px solid rgba(255,255,255,0.08);
  backdrop-filter: blur(18px);
}

.user-profile-card:hover {
  border: 1px solid rgba(196,154,108,0.42);
}

.user-profile-card.active {
  border: 1px solid rgba(196,154,108,0.56);
  box-shadow:
    0 0 0 1px rgba(196,154,108,0.12),
    0 18px 60px rgba(0,0,0,0.45);
}
```

## 6.5 UserProfilePage 组件

```tsx
<UserProfilePage>
  <ProfileOverview />
  <AccountConstraintPanel />
  <InvestmentRoleProfilePanel />
  <RiskPreferencePanel />
  <BehaviorBiasPanel />
  <AgentInteractionPreferencePanel />
  <SystemAdvicePreferencePanel />
  <MonthlyProfileUpdatePanel />
  <ProfileAuditTrail />
</UserProfilePage>
```

## 6.6 用户画像如何影响系统

```text
用户画像
  ↓
影响仓位建议
  ↓
影响提醒等级
  ↓
影响 Agent 说话方式
  ↓
影响选股过滤
  ↓
影响 CaseForge 归因
  ↓
影响月度内化
```

示例：

```text
如果系统识别你近期“利好过度相信”倾向增强，
则 ZC35 催化衰减提醒提高等级。
```

```text
如果账户现金流压力较高，
则投研选股页面不能默认推荐高波动短线事件仓。
```

```text
如果最近连续出现“早盘追高、尾盘回落”的执行偏差，
盘中实时解读区要重点提示入场窗口风险。
```

---

# 7. 持仓管理看板详细设计

## 7.1 页面布局

```text
[顶部状态栏]

[左侧导航] [主内容区：持仓管理看板] [右侧窄提醒栏]
              ├── 账户总览
              ├── 长期资金曲线
              ├── 仓位明细
              ├── Alpha 平行验证
              ├── 前夜/叙事/天机按钮
              └── 盘中实时解读
```

## 7.2 账户总览区

卡片：

```text
今日盈亏
总资产
持仓 Alpha
现金比例
最大回撤
风险预算
```

长期资金成长曲线卡片：

```text
净值曲线
累计投入
累计收益
月度收益
年度收益
最大回撤
与基准对比
机会成本对比
```

用户语言摘要：

```text
账户长期趋势：继续向上
当前回撤：正常波动区
本月表现：跑赢账户基准线
```

组件建议：

```tsx
<AccountSummaryCards />
<CapitalGrowthChart />
<AlphaBenchmarkCard />
<RiskBudgetMeter />
```

## 7.3 仓位明细区

仓位分组：

```text
正式仓：
- 核心底仓
- 中期轮动仓
- 短期事件仓
- 防御/现金仓

平行验证仓：
- 底仓观察仓
- 轮动观察仓
- 黑马观察仓
```

每只股票行字段：

```ts
type PositionRow = {
  ticker: string
  name: string
  role: PortfolioRole
  weightPct: number
  marketValue: number
  costBasis?: number
  pnlPct: number
  alphaPct: number
  thesisStatus: 'HEALTHY' | 'WATCH' | 'REVIEW' | 'BROKEN' | 'UNKNOWN'
  catalystStatus: 'ACTIVE' | 'DECAYING' | 'EXHAUSTED' | 'VACUUM' | 'NONE'
  riskLevel: 'LOW' | 'MID' | 'HIGH'
  nextAction: 'HOLD_RESEARCH' | 'WATCH' | 'THESIS_REVIEW' | 'RISK_REVIEW' | 'MOVE_TO_OBSERVATION' | 'DATA_INSUFFICIENT'
}
```

点击股票打开：

```text
StockResearchDrawer
```

## 7.4 Alpha 平行验证区

必须明确区分三类观察仓。

### 底仓观察仓

显示：

```text
潜在长期资产
估值等待
财务确认
是否可转核心底仓
```

### 轮动观察仓

显示：

```text
板块确认
相对强度
T5/T20 Alpha
是否可转中期轮动仓
```

### 黑马观察仓

显示：

```text
催化兑现
资金接力
执行质量
是否可转短期事件仓
```

每个观察对象字段：

```ts
type ObservationRow = {
  ticker: string
  name: string
  observationRole: 'CORE_OBSERVATION' | 'ROTATION_OBSERVATION' | 'DARK_HORSE_OBSERVATION'
  startDate: string
  thesis: string
  benchmark: string
  t5Alpha?: number
  t20Alpha?: number
  t60Alpha?: number
  validationStatus: 'PENDING' | 'INSUFFICIENT_DAYS' | 'OUTPERFORMING' | 'UNDERPERFORMING' | 'PROMOTE_CANDIDATE' | 'REJECT_CANDIDATE'
  suggestedMove: 'KEEP_OBSERVING' | 'PROMOTE_TO_CORE' | 'PROMOTE_TO_ROTATION' | 'PROMOTE_TO_EVENT' | 'REJECT' | 'NEED_REVIEW'
}
```

---

# 8. 前夜战报 / 叙事雷达 / 天机引擎

这三者必须是按钮，不是静态大图。

放在账户总览下方或持仓明细上方：

```text
前夜战报  命中率 72%
叙事雷达  命中率 68%
天机引擎  今日 5 条预警
```

点击展开右侧抽屉。

## 8.1 前夜战报抽屉

内容：

```text
宏观市场
行业板块
我的持仓影响
今日风险水温
历史命中率
```

## 8.2 叙事雷达抽屉

必须说明对象：

```text
全市场叙事
持仓组合叙事
单股叙事
```

内容：

```text
升温叙事
退潮叙事
拥挤叙事
利好出尽叙事
我的持仓匹配度
```

## 8.3 天机引擎抽屉

保留“天机引擎”命名。

定位：

```text
传播入口 + 趣味化路径预警层
```

底层真实定义：

```text
ZC35 + R-Matrix + D-Matrix + ZC40 + 持仓路径 + 事件状态
组合生成路径预警。
```

必须显示副说明：

```text
天机引擎不是涨跌预测，而是盘前/盘中/盘后路径预警系统。
```

输出内容：

```text
每只持仓关键位
今日异常信号
板块联动观察
催化状态
执行风险
需要注意事项
历史预警成功率
```

## 8.4 天机引擎趣味化标签

允许使用：

```text
路径偏航
催化退潮
板块护航
资金掉队
剧本反转
```

示例：

```text
【路径偏航】
双环传动今天没有跟随机器人板块修复，说明它正在偏离原有强势剧本。

【催化退潮】
前期利好仍在被市场提及，但价格已经不再响应，催化进入衰减期。

【板块护航】
个股没有独立走弱，当前主要受板块回调拖累，暂不做 thesis 破裂处理。
```

禁止：

```text
天机确认上涨
天机建议买入
天机提示卖出
```

---

# 9. 盘中实时解读区

## 9.1 定位

保留“盘中实时解读区”。

它不是高频交易模块，而是：

```text
盘中执行质量研究模块
```

用途：

```text
当日入场窗口研究
当日出场窗口研究
持仓状态解释
执行风险提示
人工决策辅助
```

## 9.2 五个子能力

### 1. 当日入场窗口判断

判断：

```text
现在适不适合进入？
是早盘冲高陷阱？
是板块共振？
是尾盘确认？
还是只适合观察？
```

输出示例：

```text
当前不适合追入，原因是价格强但板块弱，容易形成单股脉冲。
更优观察窗口在午后 13:30 后，看它能否保持相对强度。
```

### 2. 当日出场窗口判断

判断：

```text
现在是否该减仓？
是正常回撤？
是承接失败？
是板块退潮？
还是催化耗尽？
```

输出示例：

```text
这不是单纯跌幅问题，而是板块修复时它没有跟随，说明资金保护力度下降。
如果尾盘仍不能收回关键位，应进入人工减仓复核。
```

### 3. 盘中相对强弱判断

比较：

```text
个股 vs 板块
个股 vs 大盘
个股 vs 同链核心股
个股 vs 昨日预期路径
```

### 4. ZC35 催化状态盘中修正

判断：

```text
催化是否还在？
是否开始衰减？
是否利好出尽？
是否进入催化真空？
```

### 5. 执行质量记录

每次人工买卖后，系统要记录：

```text
计划买点
实际买点
当天更优买点
计划卖点
实际卖点
当天更优卖点
偏差原因
```

## 9.3 盘中实时解读输出结构

组件：

```tsx
<IntradayInterpretationPanel />
```

显示结构：

```text
当前状态：
我看到：
这意味着：
你现在不要：
接下来盯：
需要你确认：
```

示例内容：

```text
当前状态：这不是普通回调，而是“板块降温 + 个股承接变弱”的组合状态。

我看到：
1. 它今天跌幅明显超过机器人板块。
2. 前期催化热度正在衰减。
3. 成交放大但价格没有收回关键位。

这意味着：
它现在不再被资金当作主线核心保护。

你现在不要：
不要因为单日下跌就立刻动作，也不要把旧利好继续当成强支撑。

接下来盯：
如果板块修复而它不跟，进入 thesis review。

需要你确认：
是否将它从轮动观察仓降级为风险观察？
```

## 9.4 安全边界

盘中实时解读区禁止出现：

```text
立即买入
立即卖出
自动交易
一键下单
系统建议买入
系统建议卖出
```

允许动作：

```text
生成入场研究记录
生成出场研究记录
加入人工复核
记录实际执行
记录错过机会
记录执行偏差
```

---

# 10. 投研选股页面详细设计

## 10.1 页面布局

```text
投研选股
├── 顶部扫描控制区
├── 左侧全局扫描进度
├── 中部选股矩阵
├── 右侧候选矩阵
└── 股票研究抽屉
```

## 10.2 全局扫描区

按钮：

```text
开始全局扫描
使用我的账户偏好扫描
仅扫描观察池
仅扫描某产业链
```

七层过滤：

```text
1. 宏观水温过滤
2. 10链 × 5力产业链分析
3. 31板块顺逆风排序
4. 财务健康过滤
5. B/R/D-Matrix 角色识别
6. ZC35 催化生命周期过滤
7. ZC40/ZC50 可执行与账户适配过滤
```

每层显示：

```text
通过数量
剔除数量
关键理由
可展开详情
```

## 10.3 10链 × 5力分析

10链建议：

```text
AI算力链
半导体链
机器人链
新能源链
储能链
医药创新链
黄金铜资源链
券商金融链
消费复苏链
高端制造链
```

5力建议：

```text
政策力
产业力
业绩力
资金力
估值力
```

输出：

```text
Top5 顺风产业链
Top5 避雷产业链
链内核心环节
可研究标的
风险说明
```

## 10.4 31板块 Top5 顺风 + 避雷

显示：

```text
顺风板块 Top5
避雷板块 Top5
中性观察板块
```

每个板块显示：

```text
板块名
顺风理由
风险理由
候选数量
推荐研究入口
```

## 10.5 选股矩阵

三栏：

```text
B-Matrix Top
R-Matrix Top
D-Matrix Top
```

### B-Matrix

适合：

```text
底仓
底仓观察
长期研究
```

指标摘要：

```text
ROE
毛利率
现金流
估值分位
行业地位
护城河
```

### R-Matrix

适合：

```text
中期轮动仓
轮动观察仓
```

指标摘要：

```text
相对强度
趋势位置
行业排名
T5/T20路径
波动结构
```

### D-Matrix

适合：

```text
短期事件仓
黑马观察仓
```

指标摘要：

```text
催化事件
资金行为
涨停结构
主题热度
新闻/公告
```

## 10.6 候选矩阵

候选矩阵是选股到持仓之间的缓冲区。

候选动作：

```text
生成个股研究
加入正式建仓记录
进入底仓观察仓
进入轮动观察仓
进入黑马观察仓
剔除
```

建仓注意：

```text
“建仓”仅创建人工建仓记录，不自动下单。
```

建仓弹窗字段：

```ts
type ManualBuildPositionDraft = {
  ticker: string
  name: string
  targetRole: 'CORE' | 'ROTATION' | 'EVENT' | 'DEFENSIVE'
  plannedQuantity?: number
  plannedPrice?: number
  plannedCapitalPct?: number
  reason: string
  invalidationCondition: string
  paperOnly: true
  brokerOrderAllowed: false
  realTradeAllowed: false
}
```

---

# 11. 历史回溯页面详细设计

## 11.1 页面目的

历史回溯是个人知识库，不是报告列表。

它管理：

```text
完整分析报告
实盘案例
系统记忆
规则候选
无效数据
```

## 11.2 记忆分类

```text
核心永固记忆
时效性记忆
过期记忆
待清理记忆
```

数据类型：

```ts
type MemoryItem = {
  memoryId: string
  title: string
  type: 'CORE_PERMANENT' | 'TIME_SENSITIVE' | 'EXPIRED' | 'CLEANUP_REQUIRED'
  source: 'REPORT' | 'CASE' | 'TRADE' | 'SYSTEM' | 'MANUAL'
  importance: 'LOW' | 'MID' | 'HIGH' | 'CRITICAL'
  freshnessScore: number
  halfLifeDays?: number
  createdAt: string
  lastReviewedAt?: string
  linkedTickers?: string[]
  linkedCases?: string[]
  summary: string
  userActions: Array<'VIEW' | 'ARCHIVE' | 'DELETE' | 'MARK_INVALID' | 'PIN_CORE'>
}
```

## 11.3 记忆新鲜度 UI

时效性记忆显示：

```text
新鲜
衰减中
过期
```

视觉：

```text
新鲜：绿色点
衰减中：琥珀点
过期：灰色点
核心永固：铜色星标
待清理：红色/灰色警示
```

---

# 12. Agent Kernel 前端承载层

## 12.1 Agent Control Center

入口：

```text
顶部状态栏 Agent 状态按钮
专业控制台 Agent Kernel Tab
右侧提醒栏 L3/L4 Proposal 提醒
```

内容：

```text
已注册 Agent
Agent 当前状态
当前运行任务
待审批 Proposal
最近执行记录
被拦截动作
Skill 调用日志
审计链
```

## 12.2 Proposal Approval Center

显示字段：

```text
proposal_id
agent_id
requested_skill
risk_level
target_layers
affected_files
human_review_required
verify_script
status
created_at
```

操作：

```text
查看详情
批准
拒绝
延后
要求补证据
打开审计链
```

严禁：

```text
一键批准所有
自动批准 R3+
绕过 verify
```

## 12.3 Skill Invocation Console

显示：

```text
Agent 调用了哪个 Skill
输入是什么
输出是什么
证据链是什么
quality_status 是什么
blocked_reason 是什么
是否写入 proposal
是否需要审批
```

建议放在：

```text
专业控制台 → Agent Kernel → Skill Invocation
```

## 12.4 Audit Trail

显示：

```text
command
permission decision
proposal
approval
execution
verify
final status
```

审计链必须 append-only 展示，不允许前端直接删除。

## 12.5 Frontend Action Queue

Action 类型：

```text
OPEN_CASE
FOCUS_TICKER
SHOW_EVENT_WINDOW
SHOW_FACTOR_REPORT
SHOW_HYPOTHESIS
SHOW_ANALYSIS_ZONE
ASK_HUMAN_REVIEW
SHOW_AGENT_PROPOSAL
SHOW_VERIFY_RESULT
SHOW_DATA_QUALITY_WARNING
REQUEST_USER_DECISION
```

前端动作只控制展示，不改变 ResearchDB 状态。

---

# 13. Evidence Footer 与 Data Freshness Badge

## 13.1 Evidence Footer

所有结论卡片底部必须显示证据状态。

字段：

```text
数据来源
最后更新时间
quality_status
trust_level
是否 human_reviewed
是否 outcome_ready
是否 paper_only
```

示例：

```text
证据状态：T20 不足，当前只能观察，不能形成规则。
```

## 13.2 Data Freshness Badge

状态：

```text
FRESH
STALE
PARTIAL
ERROR
INSUFFICIENT_FORWARD_DAYS
FIXTURE_ONLY
PRIVATE_READY
```

UI 规则：

```text
FRESH：绿色
PARTIAL：蓝色
STALE：琥珀
ERROR：红色
INSUFFICIENT_FORWARD_DAYS：灰蓝
FIXTURE_ONLY：灰色
PRIVATE_READY：绿色描边
```

## 13.3 SystemTruthStatus

```ts
type SystemTruthStatus = {
  researchDbStatus: 'READY' | 'PARTIAL' | 'STALE' | 'ERROR'
  accountTruthStatus: 'NOT_IMPORTED' | 'FIXTURE_ONLY' | 'PRIVATE_READY' | 'ERROR'
  outcomeStatus: 'READY' | 'INSUFFICIENT_FORWARD_DAYS' | 'STALE' | 'ERROR'
  agentKernelStatus: 'NOT_INSTALLED' | 'READY_STUB_ONLY' | 'RUNNING_CONTROLLED' | 'ERROR'
  zc35Status: 'READY' | 'RESEARCH_PROTOTYPE' | 'EXCLUDED_FROM_RC1' | 'ERROR'
  lastVerifyAt?: string
  lastCloudCommit?: string
}
```

---

# 14. 专业控制台详细设计

## 14.1 目的

专业控制台不是系统设置。它是投资研究参数中控台 + Agent Kernel 治理台。

## 14.2 参数分区

```text
仓位与风险
因子验证
催化生命周期
执行质量
账户治理
自动化确认策略
记忆与内化
Agent Kernel
安全锁
```

## 14.3 Agent Kernel Tabs

```text
Agent Registry
Skill Registry
Proposal Center
Skill Invocation Console
Audit Trail
System Safety
```

## 14.4 危险参数保护

危险参数包括：

```text
回撤阈值
规则晋级阈值
半衰期参数
自动确认策略
数据可信等级
Agent 权限
Skill 写入权限
```

修改必须：

```text
弹出二次确认
写入 audit
显示影响范围
支持回滚
```

---

# 15. 系统设置详细设计

系统设置只包含技术与后台配置。

内容：

```text
API Key
模型配置
数据源
显示主题
通知
后台日志
备份恢复
权限
本地路径
```

禁止把投资策略参数放进系统设置。

---

# 16. Agent Dock

## 16.1 命名

建议使用：

```text
Agent Dock
```

中文可显示：

```text
AI Agent 对话控制台
```

保留原“宠物层”的趣味性，但系统定义为受控 Agent Dock。

## 16.2 状态

```text
安静待命
在线
正在分析
有提醒
需要确认
后台同步中
安全锁定
错误
```

## 16.3 快捷动作

```text
解释当前页面
查看待审批 Proposal
分析当前持仓
生成今日研究摘要
打开投研选股
查看历史报告
查看系统安全状态
```

## 16.4 禁止

```text
真实下单
自动卖出
关闭安全门
批准 RC1
自动晋级规则
绕过 Proposal Approval
```

---

# 17. 数据模型总表

## 17.1 PortfolioRole

```ts
export type PortfolioRole =
  | 'CORE'
  | 'ROTATION'
  | 'EVENT'
  | 'DEFENSIVE'
  | 'CORE_OBSERVATION'
  | 'ROTATION_OBSERVATION'
  | 'DARK_HORSE_OBSERVATION'
```

## 17.2 DashboardStatus

```ts
export type DashboardStatus = {
  dataSync: 'OK' | 'STALE' | 'ERROR'
  autoObserve: 'RUNNING' | 'PAUSED' | 'ERROR'
  memoryWriteback: 'DONE' | 'PENDING' | 'ERROR'
  safetyBoundary: 'LOCKED' | 'WARNING' | 'VIOLATED'
  productionLock: 'LOCKED'
  rc1Status: 'NOT_APPROVED' | 'READY_RECOMMENDED'
}
```

## 17.3 AlertItem

```ts
export type AlertLevel = 'L0_AUTO' | 'L1_LOG' | 'L2_CONFIRM' | 'L3_DECISION' | 'L4_INTERRUPT'

export type AlertItem = {
  id: string
  level: AlertLevel
  category: 'DATA' | 'HOLDING' | 'CASE' | 'RULE' | 'MONTHLY' | 'SAFETY' | 'AGENT'
  title: string
  keyword: string
  summary: string
  requiresUserAction: boolean
  suggestedActions: Array<'APPROVE' | 'EDIT' | 'DEFER' | 'REJECT' | 'VIEW' | 'REQUEST_EVIDENCE'>
  createdAt: string
}
```

## 17.4 DrawerType

```ts
export type DrawerType =
  | 'STOCK_RESEARCH'
  | 'PRE_MARKET_REPORT'
  | 'NARRATIVE_RADAR'
  | 'TIANJI_ENGINE'
  | 'USER_PROFILE'
  | 'ALERT_DETAIL'
  | 'REPORT_DETAIL'
  | 'PARAMETER_DETAIL'
  | 'PROPOSAL_DETAIL'
  | 'SKILL_INVOCATION_DETAIL'
  | 'AUDIT_DETAIL'
```

---

# 18. 前端工程架构建议

## 18.1 技术栈

建议：

```text
React
TypeScript
Vite
Tailwind CSS
shadcn/ui
lucide-react
recharts
zustand
react-router-dom
framer-motion
vitest
testing-library
```

## 18.2 目录

```text
frontend/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.ts
├── src/
│   ├── app/
│   │   ├── App.tsx
│   │   ├── router.tsx
│   │   └── providers.tsx
│   ├── pages/
│   │   ├── HoldingsDashboardPage.tsx
│   │   ├── ResearchSelectionPage.tsx
│   │   ├── UserProfilePage.tsx
│   │   ├── HistoryRecallPage.tsx
│   │   ├── ProConsolePage.tsx
│   │   └── SystemSettingsPage.tsx
│   ├── components/
│   │   ├── layout/
│   │   ├── status/
│   │   ├── profile/
│   │   ├── holdings/
│   │   ├── selection/
│   │   ├── history/
│   │   ├── console/
│   │   ├── agent/
│   │   ├── proposal/
│   │   ├── skill/
│   │   ├── audit/
│   │   ├── evidence/
│   │   ├── drawers/
│   │   └── ui/
│   ├── data/
│   │   └── mock/
│   ├── stores/
│   │   ├── cockpitStore.ts
│   │   ├── drawerStore.ts
│   │   ├── agentStore.ts
│   │   ├── proposalStore.ts
│   │   ├── skillInvocationStore.ts
│   │   ├── auditStore.ts
│   │   ├── userProfileStore.ts
│   │   └── settingsStore.ts
│   ├── types/
│   │   ├── cockpit.ts
│   │   ├── portfolio.ts
│   │   ├── alerts.ts
│   │   ├── reports.ts
│   │   ├── agent.ts
│   │   ├── proposal.ts
│   │   ├── skill.ts
│   │   ├── audit.ts
│   │   └── userProfile.ts
│   └── styles/
│       └── globals.css
└── tests/
```

---

# 19. 组件树

## 19.1 App

```tsx
<AppShell>
  <TopStatusBar />
  <SideNav>
    <UserProfileCard />
    <NavItemList />
    <SafetyMiniBadge />
  </SideNav>
  <MainContent />
  <AlertRail />
  <GlobalDrawer />
  <AgentDock />
</AppShell>
```

## 19.2 HoldingsDashboardPage

```tsx
<HoldingsDashboardPage>
  <AccountOverview />
  <CapitalGrowthChart />
  <PositionRoleTabs />
  <PositionDetailTable />
  <ObservationValidationPanel />
  <EnvironmentActionButtons />
  <IntradayInterpretationPanel />
  <ActionResearchPanel />
</HoldingsDashboardPage>
```

## 19.3 ResearchSelectionPage

```tsx
<ResearchSelectionPage>
  <GlobalScanPanel />
  <SevenLayerFilterProgress />
  <IndustryChainForceMap />
  <SectorRankingPanel />
  <MatrixTopLists />
  <CandidateMatrix />
</ResearchSelectionPage>
```

## 19.4 UserProfilePage

```tsx
<UserProfilePage>
  <ProfileOverview />
  <AccountConstraintPanel />
  <InvestmentRoleProfilePanel />
  <RiskPreferencePanel />
  <BehaviorBiasPanel />
  <AgentInteractionPreferencePanel />
  <SystemAdvicePreferencePanel />
  <MonthlyProfileUpdatePanel />
  <ProfileAuditTrail />
</UserProfilePage>
```

## 19.5 ProConsolePage

```tsx
<ProConsolePage>
  <ParameterGroups />
  <AgentKernelPanel />
  <ProposalApprovalCenter />
  <SkillInvocationConsole />
  <AuditTrail />
  <SystemSafetyPanel />
</ProConsolePage>
```

---

# 20. 状态管理

使用 zustand。

## 20.1 cockpitStore

负责：

```text
当前页面
DashboardStatus
SystemTruthStatus
账户摘要
持仓数据
观察仓数据
提醒摘要
```

## 20.2 userProfileStore

负责：

```text
UserProfileCardData
完整 UserProfile
画像新鲜度
行为偏差状态
月度画像更新状态
```

## 20.3 drawerStore

负责：

```text
当前打开的抽屉
抽屉 payload
关闭/切换
```

## 20.4 agentStore

负责：

```text
Agent Dock 展开状态
对话消息
Agent 状态
快捷动作
```

## 20.5 proposalStore

负责：

```text
待审批 Proposal
Proposal 详情
审批动作
风险等级
```

## 20.6 skillInvocationStore

负责：

```text
Skill 调用日志
Skill 输入输出
quality_status
blocked_reason
```

## 20.7 auditStore

负责：

```text
command
permission
proposal
approval
execution
verify
final status
```

---

# 21. Mock 数据要求

前端第一阶段使用 mock 数据。

必须包含：

```text
账户摘要 mock
长期资金曲线 mock
正式持仓 mock
三类观察仓 mock
用户画像身份卡 mock
完整用户画像 mock
前夜战报 mock
叙事雷达 mock
天机引擎 mock
盘中实时解读 mock
今日提醒 mock
历史报告 mock
系统记忆 mock
Agent 对话 mock
Proposal mock
Skill Invocation mock
Audit Trail mock
专业控制台参数 mock
```

禁止 mock 中出现：

```text
real_trade_allowed=true
broker_order_allowed=true
auto_buy_allowed=true
auto_sell_allowed=true
production_allowed=true
```

---

# 22. 用户语言层实现要求

所有前端展示数据必须通过 `humanize` 函数转译。

示例：

```ts
export function humanizeCatalystStatus(status: CatalystStatus): string {
  switch (status) {
    case 'ACTIVE':
      return '催化还在有效期内，仍值得跟踪。'
    case 'DECAYING':
      return '催化正在衰减，不能再按刚发布时的强度理解。'
    case 'EXHAUSTED':
      return '催化基本耗尽，需要防止利好出尽。'
    case 'VACUUM':
      return '当前缺少新的催化支撑，只适合观察。'
    default:
      return '暂无明确催化信号。'
  }
}
```

组件禁止直接显示后台枚举，除非在高级控制台 / debug 模式。

---

# 23. 安全边界

前端必须全局硬编码展示：

```text
Paper-only
Human Review Required
Production Blocked
Broker Runtime Blocked
Agent Direct Mutation Blocked
```

所有“建仓”动作必须命名为：

```text
创建人工建仓记录
```

建仓弹窗必须显示：

```text
本操作只生成研究记录与人工计划，不会连接券商，不会自动下单。
```

所有 Agent 操作必须显示：

```text
本操作由 Agent 生成 proposal，不会自动执行，需经过审批与验证。
```

---

# 24. 验收标准

## 24.1 页面验收

必须完成：

```text
持仓管理看板
投研选股
用户画像
历史回溯
专业控制台
系统设置
```

## 24.2 组件验收

必须完成：

```text
TopStatusBar
SideNav
UserProfileCard
SafetyMiniBadge
AlertRail
AgentDock
GlobalDrawer
CapitalGrowthChart
PositionDetailTable
ObservationValidationPanel
EnvironmentActionButtons
IntradayInterpretationPanel
MatrixTopLists
CandidateMatrix
MemoryShelf
UserProfilePage
AgentKernelPanel
ProposalApprovalCenter
SkillInvocationConsole
AuditTrail
EvidenceFooter
DataFreshnessBadge
ProConsoleParameterPanel
```

## 24.3 交互验收

必须完成：

```text
点击用户画像身份卡进入用户画像页
点击股票打开个股研究抽屉
点击前夜战报打开抽屉
点击叙事雷达打开抽屉
点击天机引擎打开抽屉
点击 Agent Dock 展开对话
点击候选进入候选矩阵
点击候选生成建仓记录弹窗
点击进入三类观察仓
提醒栏点击展开详情
专业参数修改触发二次确认
待审批 Proposal 可打开详情
Skill 调用日志可查看详情
Audit Trail 可查看完整链路
```

## 24.4 安全验收

不得在用户操作按钮中出现：

```text
BUY
SELL
AUTO_BUY
AUTO_SELL
BROKER_ORDER
REAL_TRADE
PRODUCTION_READY
真实下单
自动买入
自动卖出
券商下单
```

允许出现在：

```text
安全说明
禁止项
测试 forbidden list
```

---

# 25. OpenClaw 执行批次

## Pre-Batch：Agent Kernel API Contract Alignment

目标：

```text
定义前端需要的 Agent Kernel API Contract。
不接真实后端。
只用 mock。
```

新增 mock API：

```text
getAgentStatus()
getProposalList()
getProposalDetail()
getSkillInvocationLog()
getAuditTrail()
getSafetyStatus()
getActionQueue()
```

验收：

```text
所有 Agent Kernel 前端组件可由 mock 驱动。
```

## Batch 0：Scope Lock

目标：

```text
创建 frontend 目录
建立技术栈
建立主题系统
创建路由
创建 mock 数据
不得接后端
```

验收：

```text
npm install
npm run build
npm run lint
```

## Batch 1：App Shell

实现：

```text
TopStatusBar
SideNav
UserProfileCard
SafetyMiniBadge
AlertRail
AgentDock
GlobalDrawer
基础布局
```

验收：

```text
首页加载
左侧导航可切换
用户画像卡可进入 UserProfilePage
右侧提醒栏显示
Agent Dock 可展开
抽屉可打开关闭
```

## Batch 2：持仓管理看板

实现：

```text
AccountOverview
CapitalGrowthChart
PositionDetailTable
ObservationValidationPanel
EnvironmentActionButtons
IntradayInterpretationPanel
EvidenceFooter
DataFreshnessBadge
```

验收：

```text
显示正式仓
显示三类观察仓
显示长期资金曲线
三个按钮可打开抽屉
盘中解读为人话输出
每个结论有证据脚注
```

## Batch 3：投研选股

实现：

```text
GlobalScanPanel
SevenLayerFilterProgress
IndustryChainForceMap
SectorRankingPanel
MatrixTopLists
CandidateMatrix
StockResearchDrawer
ManualBuildPositionModal
```

验收：

```text
全局扫描可见
B/R/D榜单可见
点击个股打开抽屉
候选可进入候选矩阵
可选择进入三类观察仓
建仓只生成人工记录
```

## Batch 4：用户画像 + 历史回溯

实现：

```text
UserProfilePage
AccountConstraintPanel
InvestmentRoleProfilePanel
RiskPreferencePanel
BehaviorBiasPanel
AgentInteractionPreferencePanel
MonthlyProfileUpdatePanel
ProfileAuditTrail
ReportArchive
CaseArchive
MemoryShelf
RuleCandidateList
MemoryFreshnessBadge
```

验收：

```text
用户画像页完整
用户画像卡状态联动
核心永固记忆 / 时效性记忆 / 过期记忆 / 待清理记忆均可见
可标记无效/归档/查看
```

## Batch 5：专业控制台 + Agent Kernel 承载层 + 系统设置

实现：

```text
ProConsolePage
SystemSettingsPage
ParameterGroup
DangerParameterConfirm
AutomationPolicyPanel
AgentKernelPanel
ProposalApprovalCenter
SkillInvocationConsole
AuditTrail
SystemSafetyPanel
```

验收：

```text
专业控制台与系统设置分离
危险参数修改二次确认
Agent Kernel 状态可见
Proposal 可审批/拒绝/延后
Skill 调用可查看
Audit 链可查看
```

## Batch 6：质量与安全验证

实现：

```text
UI forbidden scan
文案检查
组件测试
build 验证
README
前端 closeout
```

验收：

```text
npm run build PASS
npm run lint PASS
npm test PASS
forbidden scan PASS
```

---

# 26. 必须新增脚本

```text
scripts/verify_cockpit_frontend_v22.sh
```

检查：

```bash
npm run build
npm run lint
npm test
grep forbidden words
check required pages
check required components
check paper-only disclaimer
check user profile card
check proposal approval center
check skill invocation console
check evidence footer
check safety status bar
```

Forbidden words：

```text
真实下单
自动买入
自动卖出
券商下单
Production Ready
Broker Ready
```

允许出现在：

```text
安全说明
禁止项
测试 forbidden list
```

但不能出现在用户操作按钮中。

---

# 27. README 要求

新增：

```text
frontend/README.md
```

必须包含：

```text
项目定位
安装
运行
构建
页面结构
组件结构
mock 数据说明
用户画像身份卡说明
Agent Kernel 前端承载说明
Proposal Approval Center 说明
Skill Invocation Console 说明
安全边界
禁止项
OpenClaw 批次记录
```

---

# 28. 完成报告格式

```text
## Z-MATRIX Research Cockpit V2.2 Frontend 完成报告

commit:
branch:

### Pages
- HoldingsDashboardPage:
- ResearchSelectionPage:
- UserProfilePage:
- HistoryRecallPage:
- ProConsolePage:
- SystemSettingsPage:

### Core Components
- TopStatusBar:
- SideNav:
- UserProfileCard:
- SafetyMiniBadge:
- AlertRail:
- AgentDock:
- GlobalDrawer:
- CapitalGrowthChart:
- PositionDetailTable:
- ObservationValidationPanel:
- IntradayInterpretationPanel:
- MatrixTopLists:
- CandidateMatrix:
- MemoryShelf:
- AgentKernelPanel:
- ProposalApprovalCenter:
- SkillInvocationConsole:
- AuditTrail:
- EvidenceFooter:
- DataFreshnessBadge:

### Safety
- broker order:
- real trade:
- auto buy:
- auto sell:
- production:
- agent direct mutation:

### Verify
- npm run build:
- npm run lint:
- npm test:
- verify_cockpit_frontend_v22.sh:

### Final Status
Frontend workbench: PASS / FAIL
Paper-only boundary: PASS / FAIL
Agent Kernel UI boundary: PASS / FAIL
```

---

# 29. 最终设计裁决

Z-MATRIX Research Cockpit V2.2 的核心不是炫技，而是让用户每天打开系统时只面对六件事：

```text
我的账户怎么样？
我的持仓该怎么看？
我该研究哪些新机会？
我的用户画像如何影响系统判断？
Agent 正在做什么，哪些需要我审批？
系统有什么必须提醒我？
```

系统后台负责：

```text
同步数据
更新记忆
验证 outcome
沉淀案例
触发提醒
保持安全边界
记录 Agent 行为
```

AI Agent 负责：

```text
自然语言调度
解释状态
打开流程
生成报告草稿
提交 proposal
降低用户操作摩擦
```

用户画像身份卡负责：

```text
把人类约束、风险状态、行为偏差和系统建议风格，
固定在驾驶舱入口最上方。
```

最终产品目标：

```text
让个人投资者像驾驶一台研究中台一样管理自己的投资系统，
而不是在一堆模块、指标和提示词中迷路。
```

最终工程原则：

```text
产品有锋芒，
系统有边界，
Agent 有门禁，
结论有证据，
操作有人审。
```
