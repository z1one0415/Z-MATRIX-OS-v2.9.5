import { createContext, useContext, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import type { CopyMode, FontScale, ThemeMode } from "../services/settingsApi";

type CopyEntry = Record<CopyMode, string>;

type CockpitPreferencesContextValue = {
  copyMode: CopyMode;
  fontScale: FontScale;
  themeMode: ThemeMode;
  setCopyMode: (mode: CopyMode) => void;
  setFontScale: (scale: FontScale) => void;
  setThemeMode: (mode: ThemeMode) => void;
  copy: (key: string, fallback: string) => string;
};

const copyEntries: Record<string, CopyEntry> = {
  "nav.holdings.label": { tianji: "执仓决断", plain: "持仓检查", english: "Portfolio Review" },
  "nav.holdings.subtitle": { tianji: "账户观察 · 持仓复核", plain: "查看账户 · 检查持仓", english: "Account View · Holdings Check" },
  "nav.selection.label": { tianji: "投研问股", plain: "选股研究", english: "Research Screen" },
  "nav.selection.subtitle": { tianji: "候选分流 · 研究记录", plain: "筛选候选 · 记录研究", english: "Screening · Notes" },
  "nav.dayan.label": { tianji: "大衍天问", plain: "研究助手", english: "Research Assistant" },
  "nav.dayan.subtitle": { tianji: "研究召唤 · 童子编排", plain: "提问研究 · 组合流程", english: "Ask · Compose" },
  "nav.compass.label": { tianji: "天机罗盘", plain: "研究参数", english: "Quant Settings" },
  "nav.compass.subtitle": { tianji: "量化参数 · 人审发布", plain: "参数检查 · 人工确认", english: "Parameters · Review" },
  "nav.history.label": { tianji: "时空回溯", plain: "历史复盘", english: "History Review" },
  "nav.history.subtitle": { tianji: "只读复盘 · 规则沉淀", plain: "查看复盘 · 整理规则", english: "Review · Rules" },
  "nav.settings.label": { tianji: "系统设置", plain: "设置", english: "Settings" },
  "nav.settings.subtitle": { tianji: "数据源 · 安全锁", plain: "数据 · 安全", english: "Data · Safety" },
  "nav.profile.label": { tianji: "操盘者画像", plain: "个人画像", english: "Operator Profile" },
  "nav.profile.subtitle": { tianji: "行为复盘 · 纪律画像", plain: "行为记录 · 个人习惯", english: "Behavior · Discipline" },

  "settings.page.title": { tianji: "系统设置", plain: "设置", english: "Settings" },
  "settings.page.subtitle": { tianji: "基础配置 · 数据连接 · 安全锁", plain: "基础信息 · 数据连接 · 安全", english: "Basics · Data · Safety" },
  "settings.category.account.label": { tianji: "账户显示", plain: "账户信息", english: "Account" },
  "settings.category.account.summary": { tianji: "名称、头像与默认首页", plain: "名称、头像和首页", english: "Name, avatar, home page" },
  "settings.category.data.label": { tianji: "数据源", plain: "数据连接", english: "Data Sources" },
  "settings.category.data.summary": { tianji: "行情、财务与本地导入", plain: "行情、财务和文件导入", english: "Market, finance, imports" },
  "settings.category.llm.label": { tianji: "大模型 API", plain: "模型接口", english: "Model APIs" },
  "settings.category.llm.summary": { tianji: "国内外模型密钥与端点", plain: "模型密钥和连接地址", english: "Keys and endpoints" },
  "settings.category.assistant.label": { tianji: "随侍童子", plain: "帮助助手", english: "Assistant" },
  "settings.category.assistant.summary": { tianji: "问答入口与页面提示", plain: "问答入口和提示", english: "Chat entry and prompts" },
  "settings.category.safety.label": { tianji: "安全锁", plain: "安全保护", english: "Safety Locks" },
  "settings.category.safety.summary": { tianji: "纸面、人审与阻断", plain: "只读、确认和阻断", english: "Read-only, review, blocks" },
  "settings.category.appearance.label": { tianji: "显示设置", plain: "显示设置", english: "Display" },
  "settings.category.appearance.summary": { tianji: "文字表达、字号与主题", plain: "文字、字号和主题", english: "Text, font size, theme" },
  "settings.category.backup.label": { tianji: "备份恢复", plain: "备份恢复", english: "Backup & Restore" },
  "settings.category.backup.summary": { tianji: "配置快照与恢复草案", plain: "配置备份和恢复草稿", english: "Config snapshots and restore drafts" },

  "copy.holdings": { tianji: "执仓决断", plain: "持仓检查", english: "Portfolio Review" },
  "copy.selection": { tianji: "投研问股", plain: "选股研究", english: "Research Screen" },
  "copy.dayan": { tianji: "大衍天问", plain: "研究助手", english: "Research Assistant" },
  "copy.compass": { tianji: "天机罗盘", plain: "研究参数", english: "Quant Settings" },
  "copy.history": { tianji: "时空回溯", plain: "历史复盘", english: "History Review" },
  "copy.settings": { tianji: "系统设置", plain: "设置", english: "Settings" },
  "copy.hermes": { tianji: "童子谏言", plain: "帮助助手", english: "Assistant" },
  "copy.askHermes": { tianji: "问童子", plain: "提问", english: "Ask" },
  "copy.holdingReview": { tianji: "持仓复核", plain: "检查持仓", english: "Review Holdings" },
  "copy.reviewDraft": { tianji: "生成复核草案", plain: "生成检查草稿", english: "Create Review Draft" },
  "copy.auditPack": { tianji: "导出审计包", plain: "导出记录", english: "Export Audit Pack" }
};

const literalEntries: Record<string, CopyEntry> = {
  ...(Object.fromEntries(Object.values(copyEntries).map((entry) => [entry.tianji, entry])) as Record<string, CopyEntry>),

  "全局视角 · 精准配置 · 动态进化": {
    tianji: "全局视角 · 精准配置 · 动态进化",
    plain: "查看账户 · 检查持仓 · 跟踪变化",
    english: "Account view · Holdings check · Live review"
  },
  "仅纸面观察，不触发实盘": {
    tianji: "仅纸面观察，不触发实盘",
    plain: "只做模拟观察，不会交易",
    english: "Observation only, no live trades"
  },
  "人工复核开启": {
    tianji: "人工复核开启",
    plain: "需要人工确认",
    english: "Human review required"
  },
  "券商通道已阻断": {
    tianji: "券商通道已阻断",
    plain: "券商接口已关闭",
    english: "Broker access blocked"
  },
  "创建人工研究记录": {
    tianji: "创建人工研究记录",
    plain: "新增研究记录",
    english: "Add Research Note"
  },
  "所有动作进入人工确认。": {
    tianji: "所有动作进入人工确认。",
    plain: "所有操作都会先等待确认。",
    english: "All actions require review first."
  },
  "今日盈亏": { tianji: "今日盈亏", plain: "今日收益", english: "Today P/L" },
  "浮动盈亏": { tianji: "浮动盈亏", plain: "持仓盈亏", english: "Unrealized P/L" },
  "总资产": { tianji: "总资产", plain: "账户总额", english: "Total Assets" },
  "人民币账户": { tianji: "人民币账户", plain: "人民币账户", english: "CNY Account" },
  "持仓 Alpha": { tianji: "持仓 Alpha", plain: "持仓表现", english: "Holdings Alpha" },
  "导入历史后计算": { tianji: "导入历史后计算", plain: "导入历史后计算", english: "Calculated after history import" },
  "现金比例": { tianji: "现金比例", plain: "现金占比", english: "Cash Ratio" },
  "最大回撤": { tianji: "最大回撤", plain: "最大下跌", english: "Max Drawdown" },
  "待计算": { tianji: "待计算", plain: "待计算", english: "Pending" },
  "近一年": { tianji: "近一年", plain: "最近一年", english: "Last Year" },
  "资金曲线": { tianji: "资金曲线", plain: "账户走势", english: "Equity Curve" },
  "时间筛选": { tianji: "时间筛选", plain: "时间范围", english: "Time Range" },
  "近1月": { tianji: "近1月", plain: "近1个月", english: "1M" },
  "近3月": { tianji: "近3月", plain: "近3个月", english: "3M" },
  "近6月": { tianji: "近6月", plain: "近6个月", english: "6M" },
  "近1年": { tianji: "近1年", plain: "近1年", english: "1Y" },
  "近3年": { tianji: "近3年", plain: "近3年", english: "3Y" },
  "全部": { tianji: "全部", plain: "全部", english: "All" },
  "账户净值与基准的纸面曲线": {
    tianji: "账户净值与基准的纸面曲线",
    plain: "账户和基准走势",
    english: "Portfolio and benchmark curve"
  },
  "组合净值": { tianji: "组合净值", plain: "账户净值", english: "Portfolio NAV" },
  "沪深300": { tianji: "沪深300", plain: "沪深300", english: "CSI 300" },
  "区间表现": { tianji: "区间表现", plain: "区间结果", english: "Period Results" },
  "正式仓位研究表": { tianji: "正式仓位研究表", plain: "持仓研究表", english: "Holdings Review Table" },
  "研究型持仓": { tianji: "研究型持仓", plain: "当前持仓", english: "Reviewed Holdings" },
  "名称": { tianji: "名称", plain: "名称", english: "Name" },
  "角色": { tianji: "角色", plain: "定位", english: "Role" },
  "仓位": { tianji: "仓位", plain: "占比", english: "Weight" },
  "Alpha贡献": { tianji: "Alpha贡献", plain: "表现贡献", english: "Alpha Contribution" },
  "信号强度": { tianji: "信号强度", plain: "信号强弱", english: "Signal Strength" },
  "当前动作": { tianji: "当前动作", plain: "下一步", english: "Next Step" },
  "核心底仓": { tianji: "核心底仓", plain: "核心持仓", english: "Core Holding" },
  "中期轮动": { tianji: "中期轮动", plain: "中期观察", english: "Mid-term Rotation" },
  "事件观察": { tianji: "事件观察", plain: "事件观察", english: "Event Watch" },
  "防御配置": { tianji: "防御配置", plain: "防御持仓", english: "Defensive Holding" },
  "继续研究": { tianji: "继续研究", plain: "继续研究", english: "Continue Research" },
  "观察": { tianji: "观察", plain: "观察", english: "Watch" },
  "Thesis 复核": { tianji: "Thesis 复核", plain: "研究判断复核", english: "Thesis Review" },
  "风险复核": { tianji: "风险复核", plain: "风险检查", english: "Risk Review" },
  "移入观察": { tianji: "移入观察", plain: "转入观察", english: "Move to Watch" },
  "数据不足": { tianji: "数据不足", plain: "数据不足", english: "Insufficient Data" },
  "待归因": { tianji: "待归因", plain: "待分析", english: "Pending Analysis" },
  "低": { tianji: "低", plain: "低", english: "Low" },
  "中": { tianji: "中", plain: "中", english: "Medium" },
  "高": { tianji: "高", plain: "高", english: "High" },
  "催化衰减": { tianji: "催化衰减", plain: "利好变弱", english: "Catalyst Fading" },
  "继续观察": { tianji: "继续观察", plain: "继续观察", english: "Keep Watching" },
  "三类观察仓": { tianji: "三类观察仓", plain: "三类观察列表", english: "Observation Groups" },
  "底仓观察": { tianji: "底仓观察", plain: "核心观察", english: "Core Watch" },
  "轮动观察": { tianji: "轮动观察", plain: "轮动观察", english: "Rotation Watch" },
  "黑马观察": { tianji: "黑马观察", plain: "潜力观察", english: "Breakout Watch" },
  "今日变化": { tianji: "今日变化", plain: "今日变化", english: "Today Change" },
  "待确认": { tianji: "待确认", plain: "待确认", english: "Pending" },
  "无新增": { tianji: "无新增", plain: "无新增", english: "No New Items" },
  "新增复核": { tianji: "新增复核", plain: "新增检查", english: "New Review" },
  "动能转弱": { tianji: "动能转弱", plain: "走势变弱", english: "Momentum Weakening" },
  "关注": { tianji: "关注", plain: "关注", english: "Watch" },
  "空仓": { tianji: "空仓", plain: "空仓", english: "No Position" },
  "稳定": { tianji: "稳定", plain: "稳定", english: "Stable" },
  "查看详情": { tianji: "查看详情", plain: "查看详情", english: "View Details" },

  "童子谏言": { tianji: "童子谏言", plain: "帮助助手", english: "Assistant" },
  "问童子": { tianji: "问童子", plain: "提问", english: "Ask" },
  "常驻": { tianji: "常驻", plain: "在线", english: "Online" },
  "待复核": { tianji: "待复核", plain: "待检查", english: "Needs Review" },
  "原研究判断": { tianji: "原研究判断", plain: "原判断", english: "Original Thesis" },
  "最新催化变化": { tianji: "最新催化变化", plain: "最新变化", english: "Latest Catalyst" },
  "可承受回撤区间": { tianji: "可承受回撤区间", plain: "可承受下跌", english: "Acceptable Drawdown" },
  "正式仓里紫金矿业与双环传动仍需复核，现金比例偏低，先确认原研究判断是否仍成立。": {
    tianji: "正式仓里紫金矿业与双环传动仍需复核，现金比例偏低，先确认原研究判断是否仍成立。",
    plain: "紫金矿业和双环传动需要重新检查，现金占比偏低，先确认原判断是否还成立。",
    english: "Zijin Mining and Shuanghuan Driveline need review. Cash is low; confirm whether the original thesis still holds."
  },

  "右侧天机栏": { tianji: "右侧天机栏", plain: "右侧辅助栏", english: "Right Assistant Rail" },
  "天机引擎": { tianji: "天机引擎", plain: "研究提示", english: "Research Engine" },
  "持仓路径判断": { tianji: "持仓路径判断", plain: "持仓判断", english: "Holdings Path" },
  "天机台": { tianji: "天机台", plain: "状态概览", english: "Status Desk" },
  "今日总势": { tianji: "今日总势", plain: "今日市场", english: "Market Tone" },
  "偏多": { tianji: "偏多", plain: "偏强", english: "Positive" },
  "偏强": { tianji: "偏强", plain: "偏强", english: "Firm" },
  "震荡偏强": { tianji: "震荡偏强", plain: "震荡偏强", english: "Choppy but Firm" },
  "持仓风向": { tianji: "持仓风向", plain: "持仓方向", english: "Holdings Trend" },
  "顺风": { tianji: "顺风", plain: "顺势", english: "Aligned" },
  "主线未破": { tianji: "主线未破", plain: "主线仍在", english: "Trend Intact" },
  "观察候变": { tianji: "观察候变", plain: "观察变化", english: "Watch Changes" },
  "需复核": { tianji: "需复核", plain: "需检查", english: "Needs Review" },
  "催化水位": { tianji: "催化水位", plain: "利好强度", english: "Catalyst Level" },
  "中位": { tianji: "中位", plain: "中等", english: "Mid" },
  "旧催化衰减": { tianji: "旧催化衰减", plain: "旧利好变弱", english: "Old Catalyst Fading" },
  "今日勿为": { tianji: "今日勿为", plain: "今日提醒", english: "Avoid Today" },
  "追高": { tianji: "追高", plain: "追涨", english: "Chasing Highs" },
  "防冲动": { tianji: "防冲动", plain: "避免冲动", english: "Avoid Impulse" },
  "天机预警": { tianji: "天机预警", plain: "风险提醒", english: "Risk Alert" },
  "中度预警": { tianji: "中度预警", plain: "中等风险", english: "Medium Alert" },
  "双环传动路径偏航，板块修复但个股不跟，需 thesis 复核。": {
    tianji: "双环传动路径偏航，板块修复但个股不跟，需 thesis 复核。",
    plain: "双环传动走势偏离，板块修复但个股没有跟上，需要复核原研究判断。",
    english: "Shuanghuan is diverging: the sector recovered, but the stock has not followed. Review the thesis."
  },
  "查看预警详情": { tianji: "查看预警详情", plain: "查看提醒详情", english: "View Alert Details" },
  "天机签": { tianji: "天机签", plain: "判断标签", english: "Decision Tags" },
  "顺风签": { tianji: "顺风签", plain: "顺势标签", english: "Aligned Tag" },
  "组合趋势未破": { tianji: "组合趋势未破", plain: "组合趋势还在", english: "Portfolio Trend Intact" },
  "宜守": { tianji: "宜守", plain: "保持", english: "Hold View" },
  "退潮签": { tianji: "退潮签", plain: "降温标签", english: "Cooling Tag" },
  "高位旧催化衰减": { tianji: "高位旧催化衰减", plain: "高位利好变弱", english: "High-level Catalyst Fading" },
  "慎追": { tianji: "慎追", plain: "谨慎追涨", english: "Do Not Chase" },
  "复核签": { tianji: "复核签", plain: "复核标签", english: "Review Tag" },
  "双环路径需确认": { tianji: "双环路径需确认", plain: "双环需要确认", english: "Shuanghuan Needs Review" },
  "复核": { tianji: "复核", plain: "检查", english: "Review" },
  "天机卜算": { tianji: "天机卜算", plain: "辅助工具", english: "Assistant Tools" },
  "打开天机手册工具箱": { tianji: "打开天机手册工具箱", plain: "打开辅助工具箱", english: "Open Assistant Toolkit" },
  "今日待办": { tianji: "今日待办", plain: "今日待办", english: "Today Tasks" },
  "待处理": { tianji: "待处理", plain: "待处理", english: "Pending" },
  "复核紫金矿业回撤路径": { tianji: "复核紫金矿业回撤路径", plain: "检查紫金矿业下跌原因", english: "Review Zijin drawdown path" },
  "复核双环传动 thesis": { tianji: "复核双环传动 thesis", plain: "复核双环传动研究判断", english: "Review Shuanghuan thesis" },
  "补一条人工研究记录": { tianji: "补一条人工研究记录", plain: "补充一条研究记录", english: "Add one research note" },
  "数据与系统状态": { tianji: "数据与系统状态", plain: "数据和系统状态", english: "Data & System Status" },
  "正常": { tianji: "正常", plain: "正常", english: "Normal" },
  "行情数据": { tianji: "行情数据", plain: "行情数据", english: "Market Data" },
  "财务数据": { tianji: "财务数据", plain: "财务数据", english: "Financial Data" },
  "宏观数据": { tianji: "宏观数据", plain: "宏观数据", english: "Macro Data" },
  "策略引擎": { tianji: "策略引擎", plain: "策略模块", english: "Strategy Engine" },
  "风控引擎": { tianji: "风控引擎", plain: "风控模块", english: "Risk Engine" },
  "数据服务": { tianji: "数据服务", plain: "数据服务", english: "Data Service" },
  "实时": { tianji: "实时", plain: "实时", english: "Live" },
  "查看更多": { tianji: "查看更多", plain: "查看更多", english: "View More" },

  "从全市场拾取发展最合适的研究方向和观察策略": {
    tianji: "从全市场拾取发展最合适的研究方向和观察策略",
    plain: "从全市场筛出值得继续研究的候选方向",
    english: "Screen the market for research-worthy candidates"
  },
  "投研问股概览": { tianji: "投研问股概览", plain: "选股研究概览", english: "Research Screen Overview" },
  "范围覆盖": { tianji: "范围覆盖", plain: "覆盖范围", english: "Coverage" },
  "初筛候选": { tianji: "初筛候选", plain: "初步候选", english: "Initial Candidates" },
  "高优先级": { tianji: "高优先级", plain: "重点候选", english: "High Priority" },
  "集合分流": { tianji: "集合分流", plain: "候选分类", english: "Candidate Split" },
  "今日主线": { tianji: "今日主线", plain: "今日重点", english: "Today Focus" },
  "七层过滤链": { tianji: "七层过滤链", plain: "七步筛选", english: "Seven-step Filter" },
  "从全市场到研究候选": { tianji: "从全市场到研究候选", plain: "从市场筛到候选", english: "Market to candidates" },
  "本轮筛选结论": { tianji: "本轮筛选结论", plain: "本轮筛选结果", english: "Screening Result" },
  "优先方向": { tianji: "优先方向", plain: "优先方向", english: "Priority Direction" },
  "理由": { tianji: "理由", plain: "原因", english: "Reason" },
  "置信度": { tianji: "置信度", plain: "可信度", english: "Confidence" },
  "今日避开": { tianji: "今日避开", plain: "今日回避", english: "Avoid Today" },
  "市场机会热度": { tianji: "市场机会热度", plain: "市场机会", english: "Market Opportunities" },
  "顺风与避雷同步展示": { tianji: "顺风与避雷同步展示", plain: "同时看机会和风险", english: "Opportunities and risks together" },
  "三矩阵选股区": { tianji: "三矩阵选股区", plain: "三类候选区", english: "Three Candidate Groups" },
  "B/R/D 分流只用于研究角色识别": {
    tianji: "B/R/D 分流只用于研究角色识别",
    plain: "三类分组只用于研究定位",
    english: "B/R/D grouping is for research role only"
  },
  "候选矩阵 / 待选分析台": { tianji: "候选矩阵 / 待选分析台", plain: "候选列表 / 分析台", english: "Candidate List / Analysis Desk" },
  "只做研究分拣，不输出交易动作": {
    tianji: "只做研究分拣，不输出交易动作",
    plain: "只做研究整理，不给交易指令",
    english: "Research sorting only, no trade action"
  },
  "候选矩阵": { tianji: "候选矩阵", plain: "候选列表", english: "Candidate List" },
  "序号": { tianji: "序号", plain: "序号", english: "No." },
  "代码": { tianji: "代码", plain: "代码", english: "Code" },
  "股票简称": { tianji: "股票简称", plain: "名称", english: "Stock" },
  "人机识别": { tianji: "人机识别", plain: "综合判断", english: "Joint Read" },
  "投研强度": { tianji: "投研强度", plain: "研究强度", english: "Research Strength" },
  "事件驱动": { tianji: "事件驱动", plain: "事件因素", english: "Event Driver" },
  "风险画像": { tianji: "风险画像", plain: "风险情况", english: "Risk Profile" },
  "适配度": { tianji: "适配度", plain: "适合度", english: "Fit" },
  "候选个股研判": { tianji: "候选个股研判", plain: "候选分析", english: "Candidate Analysis" },
  "基本面亮点": { tianji: "基本面亮点", plain: "基本面亮点", english: "Fundamental Highlights" },
  "人机共识": { tianji: "人机共识", plain: "综合判断", english: "Joint View" },
  "投研逻辑": { tianji: "投研逻辑", plain: "研究逻辑", english: "Research Logic" },
  "风险提示": { tianji: "风险提示", plain: "风险提示", english: "Risk Note" },
  "天机判断": { tianji: "天机判断", plain: "系统判断", english: "System View" },
  "候选评分雷达": { tianji: "候选评分雷达", plain: "候选评分", english: "Candidate Score" },
  "候选安全动作": { tianji: "候选安全动作", plain: "安全操作", english: "Safe Actions" },
  "生成个股研究": { tianji: "生成个股研究", plain: "生成研究草稿", english: "Create Research Draft" },
  "进入观察仓提案": { tianji: "进入观察仓提案", plain: "加入观察草稿", english: "Add Watch Draft" },
  "暂不研究": { tianji: "暂不研究", plain: "暂不研究", english: "Skip for Now" },
  "等待候选输入": { tianji: "等待候选输入", plain: "等待候选", english: "Waiting for Candidate" },
  "候选风向": { tianji: "候选风向", plain: "候选方向", english: "Candidate Trend" },
  "科技主线": { tianji: "科技主线", plain: "科技方向", english: "Tech Theme" },
  "增加": { tianji: "增加", plain: "增加", english: "Increasing" },
  "128只待研": { tianji: "128只待研", plain: "128 只待研究", english: "128 to review" },
  "中位偏上": { tianji: "中位偏上", plain: "中等偏上", english: "Above Mid" },
  "热度防冲": { tianji: "热度防冲", plain: "避免追热", english: "Avoid Hype" },
  "旧热点高位分歧，候选需先进入研究池复核，不触发交易动作。": {
    tianji: "旧热点高位分歧，候选需先进入研究池复核，不触发交易动作。",
    plain: "旧热点开始分化，候选要先进入研究池检查，不触发交易。",
    english: "Old hot themes are diverging. Candidates must enter research review first; no trade action."
  },
  "打开投研问股工具箱": { tianji: "打开投研问股工具箱", plain: "打开选股研究工具", english: "Open Research Screen Tools" },
  "主线强化": { tianji: "主线强化", plain: "主线增强", english: "Theme Strengthening" },
  "宜审": { tianji: "宜审", plain: "适合审查", english: "Review" },
  "旧题材分化": { tianji: "旧题材分化", plain: "旧题材分化", english: "Old Theme Divergence" },
  "黑马条件增强": { tianji: "黑马条件增强", plain: "潜力条件增强", english: "Breakout Conditions Improved" },

  "天机衍算": { tianji: "天机衍算", plain: "参数判断", english: "Parameter Engine" },
  "量化参数判断": { tianji: "量化参数判断", plain: "量化参数判断", english: "Quant Parameter View" },
  "校准台": { tianji: "校准台", plain: "校准概览", english: "Calibration Desk" },
  "参数版本": { tianji: "参数版本", plain: "参数版本", english: "Parameter Version" },
  "量化总览": { tianji: "量化总览", plain: "量化总览", english: "Quant Overview" },
  "成功复盘": { tianji: "成功复盘", plain: "复盘成功率", english: "Review Success" },
  "纸面通过": { tianji: "纸面通过", plain: "模拟通过", english: "Paper Passed" },
  "参数分歧": { tianji: "参数分歧", plain: "参数待确认", english: "Parameter Disputes" },
  "待裁定": { tianji: "待裁定", plain: "待确认", english: "Pending Decision" },
  "快照状态": { tianji: "快照状态", plain: "备份状态", english: "Snapshot Status" },
  "已备份": { tianji: "已备份", plain: "已备份", english: "Backed Up" },
  "可恢复": { tianji: "可恢复", plain: "可恢复", english: "Restorable" },
  "退潮项": { tianji: "退潮项", plain: "降温项", english: "Cooling Items" },
  "旧催化": { tianji: "旧催化", plain: "旧利好", english: "Old Catalysts" },
  "中风险": { tianji: "中风险", plain: "中等风险", english: "Medium Risk" },
  "催化周期门、因子晋级门与 D-Matrix 假预热惩罚待裁定，需保留快照后进入人审。": {
    tianji: "催化周期门、因子晋级门与 D-Matrix 假预热惩罚待裁定，需保留快照后进入人审。",
    plain: "催化周期、因子升级和黑马预热惩罚需要人工确认，先保留备份。",
    english: "Catalyst cycle, factor promotion, and breakout preheat penalty need human review after snapshot backup."
  },
  "查看分歧详情": { tianji: "查看分歧详情", plain: "查看待确认详情", english: "View Dispute Details" },
  "天衍印鉴": { tianji: "天衍印鉴", plain: "参数标签", english: "Parameter Tags" },
  "参数落盘": { tianji: "参数落盘", plain: "参数工具", english: "Parameter Tools" },
  "打开参数校准工具箱": { tianji: "打开参数校准工具箱", plain: "打开参数校准工具", english: "Open Calibration Tools" },
  "稳定印": { tianji: "稳定印", plain: "稳定标签", english: "Stable Tag" },
  "数据、样本与经验内核稳定": {
    tianji: "数据、样本与经验内核稳定",
    plain: "数据、样本和经验较稳定",
    english: "Data, sample, and experience core are stable"
  },
  "校准印": { tianji: "校准印", plain: "校准标签", english: "Calibration Tag" },
  "因子、催化与轮动待校准": {
    tianji: "因子、催化与轮动待校准",
    plain: "因子、催化和轮动待确认",
    english: "Factors, catalysts, and rotation need calibration"
  },
  "禁改印": { tianji: "禁改印", plain: "禁止修改标签", english: "Locked Tag" },
  "禁改域禁止越权": { tianji: "禁改域禁止越权", plain: "禁止越权修改", english: "Locked areas cannot be overridden" },
  "校准": { tianji: "校准", plain: "校准", english: "Calibrate" },
  "禁改": { tianji: "禁改", plain: "禁止修改", english: "Locked" },

  "时空印鉴": { tianji: "时空印鉴", plain: "历史复盘提示", english: "History Seal" },
  "历史学习判断": { tianji: "历史学习判断", plain: "历史复盘判断", english: "History Learning View" },
  "时空印": { tianji: "时空印", plain: "复盘概览", english: "History Desk" },
  "今日报告": { tianji: "今日报告", plain: "今日报告", english: "Today Reports" },
  "报告库": { tianji: "报告库", plain: "报告库", english: "Report Library" },
  "案例库": { tianji: "案例库", plain: "案例库", english: "Case Library" },
  "记忆库": { tianji: "记忆库", plain: "记忆库", english: "Memory Library" },
  "规则库": { tianji: "规则库", plain: "规则库", english: "Rule Library" },
  "审计包": { tianji: "审计包", plain: "审计记录", english: "Audit Pack" },
  "研究库": { tianji: "研究库", plain: "研究库", english: "Research DB" },
  "实盘案例": { tianji: "实盘案例", plain: "复盘案例", english: "Review Cases" },
  "只读复盘": { tianji: "只读复盘", plain: "只读复盘", english: "Read-only Review" },
  "记忆沉淀": { tianji: "记忆沉淀", plain: "记忆整理", english: "Memory Capture" },
  "规则候选": { tianji: "规则候选", plain: "规则草稿", english: "Rule Candidates" },
  "清理记忆": { tianji: "清理记忆", plain: "清理记录", english: "Clean Memories" },
  "时空预鉴": { tianji: "时空预鉴", plain: "历史提醒", english: "History Alert" },
  "H3 预鉴": { tianji: "H3 预鉴", plain: "历史提醒", english: "H3 Alert" },
  "部分历史模式出现失效迹象，3 条记忆即将过期，2 条规则候选待复核。": {
    tianji: "部分历史模式出现失效迹象，3 条记忆即将过期，2 条规则候选待复核。",
    plain: "部分历史经验可能失效，3 条记录快过期，2 条规则草稿待检查。",
    english: "Some historical patterns may be stale. 3 memories are expiring and 2 rule candidates need review."
  },
  "查看预鉴详情": { tianji: "查看预鉴详情", plain: "查看提醒详情", english: "View History Alert" },
  "时空书签": { tianji: "时空书签", plain: "复盘标签", english: "History Tags" },
  "时空工具": { tianji: "时空工具", plain: "复盘工具", english: "History Tools" },
  "打开时空工具箱": { tianji: "打开时空工具箱", plain: "打开复盘工具", english: "Open History Tools" },
  "高胜率": { tianji: "高胜率", plain: "高成功率", english: "High Win Rate" },
  "易失效": { tianji: "易失效", plain: "容易失效", english: "Fragile" },
  "待优化": { tianji: "待优化", plain: "待优化", english: "Needs Optimization" },
  "趋势突破类": { tianji: "趋势突破类", plain: "趋势突破类", english: "Trend Breakout" },
  "高估高位类": { tianji: "高估高位类", plain: "高估高位类", english: "Overvalued Highs" },
  "事件驱动类": { tianji: "事件驱动类", plain: "事件驱动类", english: "Event Driven" },
  "复盘昨日关键案例": { tianji: "复盘昨日关键案例", plain: "复盘昨日案例", english: "Review yesterday's cases" },
  "清理过期系统记忆": { tianji: "清理过期系统记忆", plain: "清理过期记录", english: "Clean expired memories" },
  "规则候选验证复盘": { tianji: "规则候选验证复盘", plain: "复盘规则草稿", english: "Review rule candidates" },

  "设置页统一状态栏": { tianji: "设置页统一状态栏", plain: "设置状态栏", english: "Settings Status Bar" },
  "设置分类": { tianji: "设置分类", plain: "设置分类", english: "Settings Categories" },
  "显示与备份设置": { tianji: "显示设置", plain: "显示设置", english: "Display Settings" },
  "文字表达": { tianji: "文字表达", plain: "文字表达", english: "Copy Mode" },
  "文字表达模式": { tianji: "文字表达模式", plain: "文字表达模式", english: "Copy Mode" },
  "保留当前驾驶舱语气": { tianji: "保留当前驾驶舱语气", plain: "保留当前风格", english: "Keep current cockpit tone" },
  "通用版": { tianji: "通用版", plain: "通用版", english: "Plain" },
  "简洁中文，不用黑话": { tianji: "简洁中文，不用黑话", plain: "简洁中文，不用黑话", english: "Simple Chinese, no jargon" },
  "文字大小": { tianji: "文字大小", plain: "文字大小", english: "Text Size" },
  "小号": { tianji: "小号", plain: "小号", english: "Small" },
  "标准": { tianji: "标准", plain: "标准", english: "Standard" },
  "大号": { tianji: "大号", plain: "大号", english: "Large" },
  "深浅主题": { tianji: "深浅主题", plain: "主题", english: "Theme" },
  "深色": { tianji: "深色", plain: "深色", english: "Dark" },
  "浅色": { tianji: "浅色", plain: "浅色", english: "Light" },
  "外观与备份": { tianji: "显示设置", plain: "显示设置", english: "Display" },
  "显示设置": { tianji: "显示设置", plain: "显示设置", english: "Display" },
  "备份恢复": { tianji: "备份恢复", plain: "备份恢复", english: "Backup & Restore" },
  "备份与恢复": { tianji: "备份与恢复", plain: "备份恢复", english: "Backup & Restore" },
  "配置快照": { tianji: "配置快照", plain: "配置快照", english: "Config Snapshot" },
  "恢复保护": { tianji: "恢复保护", plain: "恢复保护", english: "Restore Protection" },
  "导出审计记录": { tianji: "导出审计记录", plain: "导出审计记录", english: "Export Audit Log" },
  "导出配置快照": { tianji: "导出配置快照", plain: "导出配置快照", english: "Export Config Snapshot" },
  "可导出": { tianji: "可导出", plain: "可导出", english: "Exportable" },
  "创建恢复草案": { tianji: "创建恢复草案", plain: "创建恢复草稿", english: "Create Restore Draft" },
  "导出备份记录": { tianji: "导出配置快照", plain: "导出配置快照", english: "Export Config Snapshot" },
  "保存用户设置快照，不含密钥明文、不含持仓数据、不含研究结论。": {
    tianji: "保存用户设置快照，不含密钥明文、不含持仓数据、不含研究结论。",
    plain: "保存当前设置备份，不包含密钥原文、持仓数据和研究内容。",
    english: "Saves a settings snapshot without raw secrets, holdings data, or research results."
  },
  "恢复前必须生成草案并由人工确认，避免误覆盖当前配置。": {
    tianji: "恢复前必须生成草案并由人工确认，避免误覆盖当前配置。",
    plain: "恢复前先生成草稿并确认，避免覆盖当前设置。",
    english: "Restore first creates a draft for review to avoid overwriting current settings."
  }
};

const copyModes: CopyMode[] = ["tianji", "plain", "english"];
const fontScales: FontScale[] = ["small", "standard", "large"];
const themeModes: ThemeMode[] = ["dark", "light"];

type LocalizationRecord = {
  source: string;
  rendered: string;
};

const textNodeRecords = new WeakMap<CharacterData, LocalizationRecord>();
const attributeRecords = new WeakMap<Element, Map<string, LocalizationRecord>>();
const localizableAttributes = ["aria-label", "title", "placeholder"] as const;

const storageKeys = {
  copyMode: "zmatrix.cockpit.copyMode",
  fontScale: "zmatrix.cockpit.fontScale",
  themeMode: "zmatrix.cockpit.themeMode"
};

const CockpitPreferencesContext = createContext<CockpitPreferencesContextValue | null>(null);

function readStoredValue<T extends string>(key: string, allowed: readonly T[], fallback: T): T {
  if (typeof window === "undefined" || typeof window.localStorage?.getItem !== "function") {
    return fallback;
  }
  try {
    const stored = window.localStorage.getItem(key);
    return allowed.includes(stored as T) ? (stored as T) : fallback;
  } catch {
    return fallback;
  }
}

function writeStoredValue(key: string, value: string) {
  if (typeof window !== "undefined" && typeof window.localStorage?.setItem === "function") {
    try {
      window.localStorage.setItem(key, value);
    } catch {
      // Storage may be unavailable in hardened or test environments.
    }
  }
}

function translateLiteral(value: string, mode: CopyMode): string {
  if (mode === "tianji") {
    return value;
  }
  const match = value.match(/^(\s*)([\s\S]*?)(\s*)$/);
  if (!match) {
    return value;
  }
  const [, prefix, core, suffix] = match;
  const translated = literalEntries[core]?.[mode];
  return translated ? `${prefix}${translated}${suffix}` : value;
}

function shouldLocalizeText(node: CharacterData) {
  const parent = node.parentElement;
  return parent ? !parent.closest("script, style, noscript, textarea, input, select, option, [data-no-localize]") : false;
}

function resolveTextSource(node: CharacterData) {
  const currentValue = node.nodeValue ?? "";
  const record = textNodeRecords.get(node);
  return record && currentValue === record.rendered ? record.source : currentValue;
}

function resolveAttributeSource(element: Element, attribute: string, value: string) {
  let records = attributeRecords.get(element);
  if (!records) {
    records = new Map();
    attributeRecords.set(element, records);
  }
  const record = records.get(attribute);
  return record && value === record.rendered ? record.source : value;
}

function storeAttributeRecord(element: Element, attribute: string, record: LocalizationRecord) {
  let records = attributeRecords.get(element);
  if (!records) {
    records = new Map();
    attributeRecords.set(element, records);
  }
  records.set(attribute, record);
}

function localizeDocument(mode: CopyMode) {
  if (typeof document === "undefined") {
    return;
  }

  if (!document.body) {
    return;
  }

  const walker = document.createTreeWalker(document.body, window.NodeFilter.SHOW_TEXT);
  let current = walker.nextNode();
  while (current) {
    const textNode = current as CharacterData;
    if (shouldLocalizeText(textNode)) {
      const source = resolveTextSource(textNode);
      const nextValue = translateLiteral(source, mode);
      textNodeRecords.set(textNode, { source, rendered: nextValue });
      if (textNode.nodeValue !== nextValue) {
        textNode.nodeValue = nextValue;
      }
    }
    current = walker.nextNode();
  }

  for (const attribute of localizableAttributes) {
    document.querySelectorAll(`[${attribute}]`).forEach((element) => {
      if (element.closest("[data-no-localize]")) {
        return;
      }
      const currentValue = element.getAttribute(attribute);
      if (!currentValue) {
        return;
      }
      const source = resolveAttributeSource(element, attribute, currentValue);
      const nextValue = translateLiteral(source, mode);
      storeAttributeRecord(element, attribute, { source, rendered: nextValue });
      if (currentValue !== nextValue) {
        element.setAttribute(attribute, nextValue);
      }
    });
  }
}

export function CockpitPreferencesProvider({ children }: { children: ReactNode }) {
  const [copyMode, setCopyModeState] = useState<CopyMode>(() => readStoredValue(storageKeys.copyMode, copyModes, "tianji"));
  const [fontScale, setFontScaleState] = useState<FontScale>(() => readStoredValue(storageKeys.fontScale, fontScales, "standard"));
  const [themeMode, setThemeModeState] = useState<ThemeMode>(() => readStoredValue(storageKeys.themeMode, themeModes, "dark"));

  useEffect(() => {
    document.documentElement.dataset.cockpitTheme = themeMode;
    writeStoredValue(storageKeys.themeMode, themeMode);
  }, [themeMode]);

  useEffect(() => {
    document.documentElement.dataset.cockpitFontScale = fontScale;
    writeStoredValue(storageKeys.fontScale, fontScale);
  }, [fontScale]);

  useEffect(() => {
    document.documentElement.dataset.cockpitCopyMode = copyMode;
    writeStoredValue(storageKeys.copyMode, copyMode);
  }, [copyMode]);

  useEffect(() => {
    if (typeof document === "undefined" || typeof MutationObserver === "undefined") {
      return;
    }

    let frame: number | null = null;
    const scheduleLocalization = () => {
      if (frame !== null) {
        return;
      }
      frame = window.requestAnimationFrame(() => {
        frame = null;
        localizeDocument(copyMode);
      });
    };

    scheduleLocalization();
    const observer = new MutationObserver(scheduleLocalization);
    observer.observe(document.body, {
      attributeFilter: [...localizableAttributes],
      attributes: true,
      characterData: true,
      childList: true,
      subtree: true
    });

    return () => {
      if (frame !== null) {
        window.cancelAnimationFrame(frame);
      }
      observer.disconnect();
    };
  }, [copyMode]);

  const value = useMemo<CockpitPreferencesContextValue>(
    () => ({
      copyMode,
      fontScale,
      themeMode,
      setCopyMode: setCopyModeState,
      setFontScale: setFontScaleState,
      setThemeMode: setThemeModeState,
      copy: (key, fallback) => copyEntries[key]?.[copyMode] ?? translateLiteral(fallback, copyMode)
    }),
    [copyMode, fontScale, themeMode]
  );

  return <CockpitPreferencesContext.Provider value={value}>{children}</CockpitPreferencesContext.Provider>;
}

export function useCockpitPreferences() {
  const context = useContext(CockpitPreferencesContext);
  if (!context) {
    throw new Error("useCockpitPreferences must be used inside CockpitPreferencesProvider");
  }
  return context;
}
