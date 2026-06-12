import type { AuthSession } from "../auth";
import { createWorkspaceDraft, ensureNoClientTenantFields, MockApiError } from "./mockApi";

export type SelectionKpi = {
  label: string;
  value: string;
  note: string;
  tone: "gold" | "green" | "red" | "muted";
  visual: "bars" | "line" | "donut";
};

export type SelectionFilterStep = {
  step: number;
  title: string;
  detail: string;
  remaining: number;
  dropRatePct: number;
  status: "PASSED" | "REVIEW" | "STRICT";
};

export type SelectionOpportunityGroup = {
  title: string;
  tone: "green" | "red";
  items: Array<{
    rank: number;
    name: string;
    changePct: number;
  }>;
};

export type SelectionMatrixGroup = {
  matrix: "B" | "R" | "D" | "ALL";
  title: string;
  subtitle: string;
  items: Array<{
    symbol: string;
    name: string;
    tags: string[];
  }>;
};

export type SelectionCandidate = {
  symbol: string;
  name: string;
  humanMachineConsensus: "人机共识" | "人机非共识" | "待人工判断";
  recommendedRole: "底仓观察" | "轮动观察" | "黑马观察" | "暂不观察";
  researchStrength: "投研增强" | "投研稳健" | "投研前瞻" | "投研待核";
  eventDriver: string;
  riskProfile: string;
  allocationFit: string;
  fitScore: number;
  keyPoint: string;
  chain: string;
  financialHealth: string;
  catalystStatus: string;
  tianjiDiagnosis: string;
};

export type SelectionActionDraft = {
  draftId: string;
  workspaceId: string;
  symbol: string;
  action:
    | "更新候选池过滤结果"
    | "生成个股研究"
    | "创建人工研究记录"
    | "进入底仓观察仓"
    | "进入轮动观察仓"
    | "进入黑马观察仓"
    | "暂不研究"
    | "导出审计包";
  status: "DRAFT_CREATED" | "AUDIT_PACK_READY";
  humanReviewRequired: true;
  auditEvent: string;
  userMessage: string;
};

export type SelectionDashboardPacket = {
  workspaceId: string;
  asOf: string;
  kpis: SelectionKpi[];
  filterChain: SelectionFilterStep[];
  conclusion: {
    priorityDirection: string;
    confidence: string;
    reasons: string[];
    avoidToday: string[];
  };
  opportunityGroups: SelectionOpportunityGroup[];
  matrixGroups: SelectionMatrixGroup[];
  candidates: SelectionCandidate[];
  todos: Array<{
    time: string;
    title: string;
  }>;
  audit: {
    paperOnly: true;
    humanReview: true;
    brokerRuntime: "BLOCKED";
    realTrade: "BLOCKED";
    dataScope: "WORKSPACE_SCOPED";
  };
};

const zPrimeSelection: SelectionDashboardPacket = {
  workspaceId: "ws_personal_z_prime",
  asOf: "2026-06-04",
  kpis: [
    { label: "范围覆盖", value: "5,281", note: "A股 + 港美映射", tone: "gold", visual: "bars" },
    { label: "初筛候选", value: "612", note: "较昨日 -2.8%", tone: "muted", visual: "line" },
    { label: "高优先级", value: "128", note: "较昨日 +11只", tone: "gold", visual: "line" },
    { label: "集合分流", value: "38 / 55 / 35", note: "近 6 个交易日已入库", tone: "green", visual: "donut" },
    { label: "今日主线", value: "机器人 · AI算力 · 半导体设备", note: "近似集群匹配", tone: "gold", visual: "line" }
  ],
  filterChain: [
    { step: 1, title: "宏观水温过滤", detail: "震荡偏强，风险偏好允许研究扩展", remaining: 3812, dropRatePct: 27.3, status: "PASSED" },
    { step: 2, title: "10链×5力产业链分析", detail: "算力链、机器人链强度靠前", remaining: 1982, dropRatePct: 47.9, status: "PASSED" },
    { step: 3, title: "31板块顺逆风排序", detail: "设备、通信、资源链进入顺风池", remaining: 826, dropRatePct: 58.3, status: "PASSED" },
    { step: 4, title: "财务健康过滤", detail: "剔除现金流和盈利质量弱项", remaining: 342, dropRatePct: 63.5, status: "PASSED" },
    { step: 5, title: "底仓/轮动/黑马角色识别", detail: "按稳定性、弹性、事件驱动分流", remaining: 176, dropRatePct: 65.7, status: "REVIEW" },
    { step: 6, title: "催化有效期与退潮过滤", detail: "旧热点高位分歧，新增催化优先", remaining: 128, dropRatePct: 66.2, status: "STRICT" },
    { step: 7, title: "可执行性与账户适配过滤", detail: "过滤流动性、波动和账户不匹配项", remaining: 128, dropRatePct: 2.1, status: "PASSED" }
  ],
  conclusion: {
    priorityDirection: "科技加速赛道 · 奥型猛催化",
    confidence: "中高",
    reasons: ["机器人", "深冷/AI算力/光模块", "半导体设备"],
    avoidToday: ["分歧超仓信号", "不追退潮/高预期赛道"]
  },
  opportunityGroups: [
    {
      title: "顺风产业链 Top5",
      tone: "green",
      items: [
        { rank: 1, name: "机器人执行器", changePct: 2.41 },
        { rank: 2, name: "AI算力液冷设备", changePct: 2.11 },
        { rank: 3, name: "深冷液氢系统", changePct: 1.93 },
        { rank: 4, name: "半导体设备零部件", changePct: 1.79 },
        { rank: 5, name: "光模块/CPO", changePct: 1.48 }
      ]
    },
    {
      title: "避雷产业链 Top5",
      tone: "red",
      items: [
        { rank: 1, name: "消费电子组装", changePct: -1.62 },
        { rank: 2, name: "传媒内容事件", changePct: -1.26 },
        { rank: 3, name: "低质后疫情饮", changePct: -1.07 },
        { rank: 4, name: "房地产开发链", changePct: -0.98 },
        { rank: 5, name: "航空机场", changePct: -0.86 }
      ]
    },
    {
      title: "顺风板块 Top5",
      tone: "green",
      items: [
        { rank: 1, name: "电力设备", changePct: 2.73 },
        { rank: 2, name: "AI芯片国产化", changePct: 2.31 },
        { rank: 3, name: "致密中心", changePct: 2.01 },
        { rank: 4, name: "工业机器人", changePct: 1.69 },
        { rank: 5, name: "智能汽车", changePct: 1.46 }
      ]
    },
    {
      title: "避风概念 Top5",
      tone: "red",
      items: [
        { rank: 1, name: "可周转塑料", changePct: -1.45 },
        { rank: 2, name: "猪肉养殖", changePct: -1.41 },
        { rank: 3, name: "医美概念", changePct: -1.31 },
        { rank: 4, name: "地产链", changePct: -1.23 },
        { rank: 5, name: "在线教育", changePct: -0.91 }
      ]
    }
  ],
  matrixGroups: [
    {
      matrix: "B",
      title: "B-Matrix Top",
      subtitle: "资金重组度",
      items: [
        { symbol: "300750", name: "宁德时代", tags: ["联权增强", "强势引擎"] },
        { symbol: "688111", name: "金山办公", tags: ["联权增强", "现金共振"] },
        { symbol: "601899", name: "紫金矿业", tags: ["预期增强", "趋势延续"] },
        { symbol: "600309", name: "万华化学", tags: ["定价功能", "现金回流"] },
        { symbol: "300124", name: "汇川技术", tags: ["联权增强", "北向融合"] }
      ]
    },
    {
      matrix: "R",
      title: "R-Matrix Top",
      subtitle: "投强逻辑维度",
      items: [
        { symbol: "300308", name: "中际旭创", tags: ["联权增强", "逻辑共振"] },
        { symbol: "688256", name: "寒武纪-U", tags: ["联权增强", "黑马保留"] },
        { symbol: "002594", name: "比亚迪", tags: ["联权功能", "估值修复"] },
        { symbol: "002384", name: "东山精密", tags: ["联权增强", "事件驱动"] },
        { symbol: "300750", name: "宁德时代", tags: ["联权弱偏", "成长延续"] }
      ]
    },
    {
      matrix: "D",
      title: "D-Matrix Top",
      subtitle: "预期差维度",
      items: [
        { symbol: "301620", name: "万通智控", tags: ["联权增强", "预期联动"] },
        { symbol: "688981", name: "中芯国际", tags: ["联权功能", "全球周期"] },
        { symbol: "300120", name: "经纬辉开", tags: ["联权功能", "低估反转"] },
        { symbol: "002512", name: "达华智能", tags: ["预期增强", "事件驱动"] },
        { symbol: "603986", name: "兆易创新", tags: ["联权弱偏", "估值修复"] }
      ]
    },
    {
      matrix: "ALL",
      title: "综合候选",
      subtitle: "候选分流",
      items: [
        { symbol: "300750", name: "宁德时代", tags: ["联权增强", "强势引擎"] },
        { symbol: "688251", name: "寒武纪-U", tags: ["联权功能", "黑马跃迁"] },
        { symbol: "688041", name: "海光信息", tags: ["联权功能", "低位反转"] },
        { symbol: "601899", name: "紫金矿业", tags: ["预期增强", "底仓联动"] },
        { symbol: "002594", name: "比亚迪", tags: ["联权功能", "估值修复"] }
      ]
    }
  ],
  candidates: [
    {
      symbol: "300308",
      name: "中际旭创",
      humanMachineConsensus: "人机共识",
      recommendedRole: "轮动观察",
      researchStrength: "投研增强",
      eventDriver: "业绩超预期",
      riskProfile: "低/风陷可控",
      allocationFit: "高/82.3",
      fitScore: 82.3,
      keyPoint: "低位人机共识信号",
      chain: "全球算力的AI光通信解决方案提供商，800G需求持续放量。",
      financialHealth: "盈利能力投入/高速光模块需求增长，业绩韧性增强。",
      catalystStatus: "国内服务器客户AI需求波动，客户集中度较高。",
      tianjiDiagnosis: "顺风但不追高，适合进入轮动观察仓并等待复核。"
    },
    {
      symbol: "688256",
      name: "寒武纪-U",
      humanMachineConsensus: "人机非共识",
      recommendedRole: "黑马观察",
      researchStrength: "投研增强",
      eventDriver: "景气拐点",
      riskProfile: "中/需强预期",
      allocationFit: "高/85.7",
      fitScore: 85.7,
      keyPoint: "国产算力核心变量",
      chain: "AI芯片国产替代主线，受政策和订单节奏双重驱动。",
      financialHealth: "收入弹性强但盈利质量仍需跟踪。",
      catalystStatus: "高位预期较满，适合复核不适合追高。",
      tianjiDiagnosis: "题材热度强，必须通过黑马复核签。"
    },
    {
      symbol: "301620",
      name: "万通智控",
      humanMachineConsensus: "人机共识",
      recommendedRole: "黑马观察",
      researchStrength: "投研前瞻",
      eventDriver: "反转预期",
      riskProfile: "中/需强观察",
      allocationFit: "中/76.8",
      fitScore: 76.8,
      keyPoint: "事件黑马初筛通过",
      chain: "汽车电子与智能控制链条，事件催化进入高弹性观察。",
      financialHealth: "财务质量需二次核验。",
      catalystStatus: "催化新鲜但持续性未确认。",
      tianjiDiagnosis: "可以研究，不进入实盘动作。"
    },
    {
      symbol: "688981",
      name: "中芯国际",
      humanMachineConsensus: "待人工判断",
      recommendedRole: "底仓观察",
      researchStrength: "投研增强",
      eventDriver: "业绩超预期",
      riskProfile: "低/闪电可控",
      allocationFit: "高/83.1",
      fitScore: 83.1,
      keyPoint: "半导体设备与国产替代共振",
      chain: "晶圆制造主线，受国产替代和周期修复支撑。",
      financialHealth: "资本开支大，需跟踪毛利率修复节奏。",
      catalystStatus: "周期回暖但海外约束仍在。",
      tianjiDiagnosis: "适合底仓研究，不形成持仓动作。"
    },
    {
      symbol: "002384",
      name: "东山精密",
      humanMachineConsensus: "待人工判断",
      recommendedRole: "轮动观察",
      researchStrength: "投研稳健",
      eventDriver: "事件驱动",
      riskProfile: "中/需跟踪观察",
      allocationFit: "中/74.5",
      fitScore: 74.5,
      keyPoint: "消费电子需求复苏",
      chain: "消费电子与汽车电子双链条。",
      financialHealth: "修复中，现金流仍需观察。",
      catalystStatus: "催化不够强，先进入低优先级研究。",
      tianjiDiagnosis: "可跟踪，不提升优先级。"
    }
  ],
  todos: [
    { time: "09:30", title: "更新候选池过滤结果" },
    { time: "10:00", title: "深研 2 只高优先级候选" },
    { time: "14:30", title: "观察黑马候选变化" }
  ],
  audit: {
    paperOnly: true,
    humanReview: true,
    brokerRuntime: "BLOCKED",
    realTrade: "BLOCKED",
    dataScope: "WORKSPACE_SCOPED"
  }
};

function requireSession(session: AuthSession | null): AuthSession {
  if (!session) {
    throw new MockApiError("AUTH_REQUIRED", "selection api requires authenticated session");
  }
  return session;
}

function clonePacket(packet: SelectionDashboardPacket, workspaceId: string): SelectionDashboardPacket {
  return {
    ...packet,
    workspaceId,
    kpis: packet.kpis.map((kpi) => ({ ...kpi })),
    filterChain: packet.filterChain.map((step) => ({ ...step })),
    conclusion: {
      ...packet.conclusion,
      reasons: [...packet.conclusion.reasons],
      avoidToday: [...packet.conclusion.avoidToday]
    },
    opportunityGroups: packet.opportunityGroups.map((group) => ({
      ...group,
      items: group.items.map((item) => ({ ...item }))
    })),
    matrixGroups: packet.matrixGroups.map((group) => ({
      ...group,
      items: group.items.map((item) => ({
        ...item,
        tags: [...item.tags]
      }))
    })),
    candidates: packet.candidates.map((candidate) => ({ ...candidate })),
    todos: packet.todos.map((todo) => ({ ...todo })),
    audit: { ...packet.audit }
  };
}

export async function getSelectionDashboardPacket(session: AuthSession | null): Promise<SelectionDashboardPacket> {
  const current = requireSession(session);
  if (current.workspaceId === "ws_personal_z_prime") {
    return clonePacket(zPrimeSelection, current.workspaceId);
  }
  return {
    ...clonePacket(zPrimeSelection, current.workspaceId),
    kpis: zPrimeSelection.kpis.map((kpi) => ({ ...kpi, value: "0", note: "等待本 workspace 候选导入" })),
    filterChain: zPrimeSelection.filterChain.map((step) => ({
      ...step,
      remaining: 0,
      dropRatePct: 0,
      detail: "等待本 workspace 候选导入",
      status: "REVIEW"
    })),
    opportunityGroups: zPrimeSelection.opportunityGroups.map((group) => ({ ...group, items: [] })),
    matrixGroups: zPrimeSelection.matrixGroups.map((group) => ({ ...group, items: [] })),
    candidates: [],
    todos: [{ time: "--:--", title: "等待投研候选导入" }]
  };
}

export async function createSelectionActionDraft(
  session: AuthSession | null,
  action: SelectionActionDraft["action"],
  payload: Record<string, unknown>
): Promise<SelectionActionDraft> {
  const current = requireSession(session);
  ensureNoClientTenantFields(payload);
  const auditEvent =
    action === "导出审计包"
      ? "EXPORT_SELECTION_AUDIT_PACK"
      : action === "更新候选池过滤结果"
        ? "REFRESH_SELECTION_FILTER_DRAFT"
        : action === "生成个股研究"
          ? "CREATE_STOCK_RESEARCH_DRAFT"
          : action === "创建人工研究记录"
            ? "CREATE_MANUAL_SELECTION_RESEARCH_RECORD"
            : action === "暂不研究"
              ? "MARK_SELECTION_RESEARCH_DEFERRED"
              : "CREATE_OBSERVATION_WAREHOUSE_PROPOSAL";
  const response = await createWorkspaceDraft(current, payload, auditEvent);
  return {
    draftId: `selection-draft-${Date.now()}`,
    workspaceId: response.workspaceId,
    symbol: String(payload.symbol ?? "SELECTION_POOL"),
    action,
    status: action === "导出审计包" ? "AUDIT_PACK_READY" : "DRAFT_CREATED",
    humanReviewRequired: true,
    auditEvent: response.auditEvent,
    userMessage:
      action === "导出审计包"
        ? "投研问股审计包已准备，等待人工确认。"
        : action === "更新候选池过滤结果"
          ? "候选池过滤结果已进入纸面复核队列。"
          : action === "生成个股研究"
            ? "个股研究草案已生成，等待人工复核。"
            : action === "创建人工研究记录"
              ? "已创建人工研究记录草案。"
              : action === "暂不研究"
                ? "已记录暂不研究原因，保留审计轨迹。"
                : "观察仓提案已生成，等待人工确认。"
  };
}
