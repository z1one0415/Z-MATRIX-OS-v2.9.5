import {
  Brain,
  BriefcaseBusiness,
  Clock3,
  Compass,
  Database,
  History,
  Landmark,
  MessageSquareText,
  Radar,
  Settings,
  ShieldCheck,
  UserRoundCog
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

export type CockpitRouteId =
  | "holdings"
  | "selection"
  | "dayan"
  | "compass"
  | "history"
  | "settings"
  | "profile";

export type NavItem = {
  id: CockpitRouteId;
  label: string;
  path: string;
  icon: LucideIcon;
  subtitle: string;
};

export const navItems: NavItem[] = [
  {
    id: "holdings",
    label: "执仓决断",
    path: "/holdings",
    icon: BriefcaseBusiness,
    subtitle: "账户观察 · 持仓复核"
  },
  {
    id: "selection",
    label: "投研问股",
    path: "/selection",
    icon: Radar,
    subtitle: "候选分流 · 研究记录"
  },
  {
    id: "dayan",
    label: "大衍天问",
    path: "/dayan-ask",
    icon: MessageSquareText,
    subtitle: "研究召唤 · 童子编排"
  },
  {
    id: "compass",
    label: "天机罗盘",
    path: "/control-compass",
    icon: Compass,
    subtitle: "量化参数 · 人审发布"
  },
  {
    id: "history",
    label: "时空回溯",
    path: "/history",
    icon: History,
    subtitle: "只读复盘 · 规则沉淀"
  },
  {
    id: "settings",
    label: "系统设置",
    path: "/settings",
    icon: Settings,
    subtitle: "数据源 · 安全锁"
  }
];

export const profileRoute: NavItem = {
  id: "profile",
  label: "操盘者画像",
  path: "/operator-profile",
  icon: UserRoundCog,
  subtitle: "行为画像 · 保护等级"
};

export const securityStates = [
  { label: "Paper-only", tone: "gold", icon: ShieldCheck },
  { label: "Human Review", tone: "gold", icon: UserRoundCog },
  { label: "Broker Blocked", tone: "red", icon: Landmark }
] as const;

export const systemVitals = [
  ["行情数据", "实时"],
  ["财务数据", "T+0"],
  ["宏观数据", "T+0"],
  ["策略引擎", "正常"],
  ["风控引擎", "正常"],
  ["数据服务", "正常"]
];

export const safetyLocks = [
  "Real Trade Blocked",
  "Agent Direct Mutation Blocked",
  "Workspace Scoped",
  "Audit Events On"
];

export const pageCopy: Record<
  CockpitRouteId,
  {
    title: string;
    kicker: string;
    primaryAction: string;
    secondaryAction: string;
    stats: Array<[string, string, string]>;
    tableTitle: string;
    rows: Array<[string, string, string, string]>;
  }
> = {
  holdings: {
    title: "执仓决断",
    kicker: "全局视角 · 精准配置 · 动态进化",
    primaryAction: "持仓复核",
    secondaryAction: "生成复核草案",
    stats: [
      ["总资产", "110,249.84", "人民币账户"],
      ["浮动盈亏", "-4,776.77", "待复核"],
      ["现金比例", "0.10%", "低现金"],
      ["持仓数量", "3", "当前 workspace"]
    ],
    tableTitle: "正式仓位研究表",
    rows: [
      ["紫金矿业", "800", "-8.40%", "持仓复核"],
      ["双环传动", "1800", "-4.15%", "持仓复核"],
      ["科创创业ETF天弘", "6500", "+5.36%", "只读观察"]
    ]
  },
  selection: {
    title: "投研问股",
    kicker: "从全市场拾取发展最合适的研究方向和观察策略",
    primaryAction: "创建人工研究记录",
    secondaryAction: "生成个股研究页",
    stats: [
      ["范围覆盖", "5,281", "A股 + 港美映射"],
      ["初筛候选", "612", "较昨日 -2.8%"],
      ["高优先级", "128", "进入观察池"],
      ["集合分流", "38 / 55 / 35", "B / R / D"]
    ],
    tableTitle: "候选矩阵 / 待选分析台",
    rows: [
      ["300308 中际旭创", "人机共识", "投研增强", "创建人工研究记录"],
      ["688256 寒武纪-U", "事件驱动", "观察", "生成研究草案"],
      ["002594 比亚迪", "价值修复", "跟踪", "加入观察记录"]
    ]
  },
  dayan: {
    title: "大衍天问",
    kicker: "中宫问答 · 八宫召唤 · 随侍童子编排",
    primaryAction: "执行纸面研究",
    secondaryAction: "提交人审",
    stats: [
      ["可召唤法门", "8", "只读技能"],
      ["今日问答", "12", "workspace scoped"],
      ["待审草案", "3", "Human Review"],
      ["童子状态", "常驻", "Hermes"]
    ],
    tableTitle: "研究链草案",
    rows: [
      ["问天对弈", "300750", "运行中", "查看审计"],
      ["归因拆解", "688256", "草案", "提交人审"],
      ["风险复盘", "600519", "完成", "归档到时空回溯"]
    ]
  },
  compass: {
    title: "天机罗盘",
    kicker: "量化参数 · 成功率复盘 · 快照保护",
    primaryAction: "查看参数族",
    secondaryAction: "生成校准草案",
    stats: [
      ["系统健康", "82", "5/8 域稳定"],
      ["成功复盘", "87.3%", "纸面验证"],
      ["参数分歧", "6", "待裁定"],
      ["快照保护", "已备份", "可恢复"]
    ],
    tableTitle: "量化参数校准盘",
    rows: [
      ["催化周期门", "catalyst-cycle v1.2", "待校准", "生成草案"],
      ["因子晋级门", "factor-gate v12.3", "待裁定", "查看参数族"],
      ["R-Matrix 轮动", "r-matrix v1.1", "待校准", "生成草案"]
    ]
  },
  history: {
    title: "时空回溯",
    kicker: "研究复盘 · 系统学习 · 规则沉淀",
    primaryAction: "查看全部报告",
    secondaryAction: "记忆库管理",
    stats: [
      ["累计报告", "1,268", "已沉淀"],
      ["实盘案例", "842", "只读复盘"],
      ["系统记忆", "3,264", "workspace scoped"],
      ["规则候选", "156", "待人审"]
    ],
    tableTitle: "历史事件流 / 复盘时间轴",
    rows: [
      ["宁德时代", "财报分析", "已验证", "只读查看"],
      ["贵州茅台", "实盘案例", "已沉淀", "只读复盘"],
      ["中际旭创", "事件驱动", "规则候选", "提交人审"]
    ]
  },
  settings: {
    title: "系统设置",
    kicker: "基础配置 · 数据连接 · 安全锁",
    primaryAction: "测试数据源",
    secondaryAction: "保存草案",
    stats: [
      ["Tushare", "可配置", "Token 不回显"],
      ["新浪行情", "备用", "只读"],
      ["安全锁", "3", "已锁定"],
      ["备份", "可导出", "当前 workspace"]
    ],
    tableTitle: "数据源与安全状态",
    rows: [
      ["Tushare Token", "已引用化", "可测试", "测试连接"],
      ["Paper-only", "已锁定", "不可关闭", "查看"],
      ["Human Review", "已锁定", "不可关闭", "查看"]
    ]
  },
  profile: {
    title: "操盘者画像",
    kicker: "行为画像 · 保护等级 · 研究节奏",
    primaryAction: "查看画像详情",
    secondaryAction: "导出审计包",
    stats: [
      ["画像完整度", "72%", "继续学习"],
      ["保护等级", "高", "稳健成长型"],
      ["人审偏好", "严格", "高风险拦截"],
      ["研究节奏", "稳态", "月度内化"]
    ],
    tableTitle: "行为画像信号",
    rows: [
      ["回撤敏感", "中高", "保护提示", "查看"],
      ["追高倾向", "低", "保持", "查看"],
      ["复盘纪律", "稳定", "继续", "查看"]
    ]
  }
};

export const commandCards = [
  { title: "天机引擎", icon: Brain, value: "偏强", detail: "顺风 · 追高预警" },
  { title: "今日待办", icon: Clock3, value: "3", detail: "均待处理" },
  { title: "数据状态", icon: Database, value: "正常", detail: "延迟 0s" }
];
