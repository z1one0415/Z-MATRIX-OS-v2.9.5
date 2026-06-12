import type { AuthSession } from "../auth";
import { createWorkspaceDraft, ensureNoClientTenantFields, MockApiError } from "./mockApi";

export type HistoryTone = "gold" | "green" | "red" | "muted";
export type HistoryStatus = "READY" | "PARTIAL" | "ERROR";

export type HistoryKpi = {
  label: string;
  value: string;
  note: string;
  delta: string;
  tone: HistoryTone;
};

export type LearningPipelineNode = {
  nodeId: "REPORT" | "CASE" | "MEMORY" | "RULE_CANDIDATE" | "FROZEN_RULE";
  displayName: string;
  count: number;
  monthlyDelta: number;
  status: HistoryStatus | "PENDING";
};

export type MonthlyHistoryStats = {
  month: string;
  newItems: number;
  verified: number;
  falsified: number;
  crystallized: number;
  promotable: number;
};

export type HistoryEvent = {
  eventId: string;
  date: string;
  targetName: string;
  targetCode: string;
  eventType: "基本面研报" | "事件复盘" | "技术复盘" | "策略复盘" | "主题复盘";
  conclusion: string;
  outcomeStatus: "已验证" | "已证伪" | "部分验证" | "待验证" | "数据不足";
  memoryStatus: "已沉淀" | "时效性记忆" | "待清理" | "未入记忆";
  ruleStatus: "规则候选" | "优质规则" | "次优规则" | "观察中" | "无";
  evidenceStatus: "证据完整" | "缺证据" | "待人审" | "审计包";
};

export type HistoryLibraryItem = {
  itemId: string;
  date: string;
  title: string;
  type: string;
  status: "已沉淀" | "已验证" | "部分验证" | "待复核" | "候选" | "观察";
};

export type MemoryRuleSummary = {
  memories: Array<{
    label: "核心永固记忆" | "时效性记忆" | "待清理记忆";
    count: number;
  }>;
  rules: Array<{
    label: "待验证" | "验证中" | "待复核" | "可晋级";
    count: number;
  }>;
};

export type SpaceTimeSealData = {
  summary: Array<{
    label: string;
    value: string;
    detail: string;
    tone: HistoryTone;
  }>;
  alert: {
    title: string;
    level: "H1" | "H2" | "H3" | "H4";
    summary: string;
  };
  bookmarks: Array<{
    title: string;
    body: string;
    verdict: string;
    tone: "green" | "gold" | "red";
  }>;
};

export type HistoryTodo = {
  time: string;
  title: string;
  status: "待处理" | "已完成" | "延后";
};

export type HistoryDataSystemStatus = {
  reportIndex: HistoryStatus;
  caseRegistry: HistoryStatus;
  memoryRegistry: HistoryStatus;
  ruleRegistry: HistoryStatus;
  auditPack: HistoryStatus;
  researchDb: HistoryStatus;
  lastUpdatedAt: string;
};

export type HistoryActionDraft = {
  draftId: string;
  workspaceId: string;
  targetId: string;
  action:
    | "查看详情"
    | "查看全部报告"
    | "生成复盘草案"
    | "创建人工研究记录"
    | "请求专家复盘"
    | "标记待清理草案"
    | "提交入记忆草案"
    | "生成规则候选草案"
    | "继续纸面验证"
    | "导出审计包"
    | "打开时空工具箱";
  status: "DRAFT_CREATED" | "AUDIT_PACK_READY" | "REFERENCE_SAVED";
  humanReviewRequired: true;
  auditEvent: string;
  userMessage: string;
};

export type HistoryPageData = {
  workspaceId: string;
  asOf: string;
  safety: {
    paperOnly: true;
    humanReviewRequired: true;
    brokerRuntime: "BLOCKED";
    realTrade: "BLOCKED";
    agentDirectMutationAllowed: false;
    dataScope: "WORKSPACE_SCOPED";
  };
  kpis: HistoryKpi[];
  learningPipeline: LearningPipelineNode[];
  monthlyStats: MonthlyHistoryStats;
  events: HistoryEvent[];
  reportLibrary: HistoryLibraryItem[];
  caseLibrary: HistoryLibraryItem[];
  memoryRuleSummary: MemoryRuleSummary;
  spaceTimeSeal: SpaceTimeSealData;
  todos: HistoryTodo[];
  systemStatus: HistoryDataSystemStatus;
  backendMapping: {
    reportLibrary: "ReportRenderer";
    auditEvidence: "OutputEnvelope/AuditEvent/AuditExportPack";
    evidenceChain: "research_os_rc.evidence_chain_auditor";
    caseRegistry: "data/research_db/cases/case_registry_v1.json";
    replay: "historical_replay";
    memoryDraft: "MemoryCandidate Preview";
    ruleCandidate: "Rule Candidate Miner";
  };
};

const zPrimeHistory: HistoryPageData = {
  workspaceId: "ws_personal_z_prime",
  asOf: "2026-06-04",
  safety: {
    paperOnly: true,
    humanReviewRequired: true,
    brokerRuntime: "BLOCKED",
    realTrade: "BLOCKED",
    agentDirectMutationAllowed: false,
    dataScope: "WORKSPACE_SCOPED"
  },
  kpis: [
    { label: "累计报告", value: "1,256", note: "较昨日 +5.12%", delta: "+12", tone: "gold" },
    { label: "实盘案例", value: "428", note: "只读复盘资产", delta: "+8", tone: "gold" },
    { label: "系统记忆", value: "1,024", note: "可复用经验", delta: "+25", tone: "green" },
    { label: "规则候选", value: "186", note: "等待人审验证", delta: "+4", tone: "gold" },
    { label: "待清理记忆", value: "96", note: "时效性需复核", delta: "-3", tone: "red" }
  ],
  learningPipeline: [
    { nodeId: "REPORT", displayName: "分析报告", count: 1256, monthlyDelta: 128, status: "READY" },
    { nodeId: "CASE", displayName: "实盘案例", count: 428, monthlyDelta: 18, status: "PARTIAL" },
    { nodeId: "MEMORY", displayName: "系统记忆", count: 1024, monthlyDelta: 25, status: "PARTIAL" },
    { nodeId: "RULE_CANDIDATE", displayName: "规则候选", count: 186, monthlyDelta: 14, status: "PARTIAL" },
    { nodeId: "FROZEN_RULE", displayName: "固化规则", count: 72, monthlyDelta: 6, status: "PENDING" }
  ],
  monthlyStats: {
    month: "2026-06",
    newItems: 128,
    verified: 76,
    falsified: 21,
    crystallized: 54,
    promotable: 9
  },
  events: [
    {
      eventId: "HE-20260604-001",
      date: "2026-06-04",
      targetName: "宁德时代",
      targetCode: "300750",
      eventType: "基本面研报",
      conclusion: "业绩超预期，估值修复空间仍需跟踪",
      outcomeStatus: "已验证",
      memoryStatus: "已沉淀",
      ruleStatus: "无",
      evidenceStatus: "审计包"
    },
    {
      eventId: "HE-20260603-002",
      date: "2026-06-03",
      targetName: "贵州茅台",
      targetCode: "600519",
      eventType: "事件复盘",
      conclusion: "批价回升但需求边际仍需二次确认",
      outcomeStatus: "部分验证",
      memoryStatus: "时效性记忆",
      ruleStatus: "次优规则",
      evidenceStatus: "待人审"
    },
    {
      eventId: "HE-20260602-003",
      date: "2026-06-02",
      targetName: "中际旭创",
      targetCode: "300308",
      eventType: "技术复盘",
      conclusion: "关键阻力突破后趋势延续，需检查拥挤度",
      outcomeStatus: "已验证",
      memoryStatus: "已沉淀",
      ruleStatus: "优质规则",
      evidenceStatus: "证据完整"
    },
    {
      eventId: "HE-20260601-004",
      date: "2026-06-01",
      targetName: "五粮液",
      targetCode: "000858",
      eventType: "策略复盘",
      conclusion: "配置性价比提升，但催化不足",
      outcomeStatus: "待验证",
      memoryStatus: "未入记忆",
      ruleStatus: "观察中",
      evidenceStatus: "证据完整"
    },
    {
      eventId: "HE-20260531-005",
      date: "2026-05-31",
      targetName: "新易盛",
      targetCode: "300502",
      eventType: "主题复盘",
      conclusion: "订单加速预期被验证，估值弹性增强",
      outcomeStatus: "已验证",
      memoryStatus: "已沉淀",
      ruleStatus: "规则候选",
      evidenceStatus: "审计包"
    }
  ],
  reportLibrary: [
    { itemId: "RPT-001", date: "2026-06-04", title: "宁德时代基本面复核", type: "个股研究报告", status: "已沉淀" },
    { itemId: "RPT-002", date: "2026-06-03", title: "中际旭创趋势验证", type: "策略验证报告", status: "已验证" },
    { itemId: "RPT-003", date: "2026-06-02", title: "估值修复因子增强策略", type: "因子验证报告", status: "待复核" }
  ],
  caseLibrary: [
    { itemId: "CASE-001", date: "2026-06-03", title: "贵州茅台批价回升复盘", type: "复盘案例", status: "部分验证" },
    { itemId: "CASE-002", date: "2026-06-02", title: "五粮液配置回归案例", type: "只读复盘", status: "待复核" },
    { itemId: "CASE-003", date: "2026-05-31", title: "新易盛订单弹性案例", type: "复盘案例", status: "已验证" }
  ],
  memoryRuleSummary: {
    memories: [
      { label: "核心永固记忆", count: 1842 },
      { label: "时效性记忆", count: 1380 },
      { label: "待清理记忆", count: 96 }
    ],
    rules: [
      { label: "待验证", count: 62 },
      { label: "验证中", count: 48 },
      { label: "待复核", count: 46 },
      { label: "可晋级", count: 9 }
    ]
  },
  spaceTimeSeal: {
    summary: [
      { label: "今日报告", value: "12", detail: "新增", tone: "gold" },
      { label: "实盘案例", value: "8", detail: "只读复盘", tone: "gold" },
      { label: "记忆沉淀", value: "25", detail: "新增", tone: "green" },
      { label: "规则候选", value: "4", detail: "待处理", tone: "gold" },
      { label: "清理记忆", value: "6", detail: "待处理", tone: "red" }
    ],
    alert: {
      title: "时空预鉴",
      level: "H3",
      summary: "部分历史模式出现失效迹象，3 条记忆即将过期，2 条规则候选待复核。"
    },
    bookmarks: [
      { title: "高胜率", body: "趋势突破类", verdict: "标签", tone: "green" },
      { title: "易失效", body: "高估高位类", verdict: "标签", tone: "gold" },
      { title: "待优化", body: "事件驱动类", verdict: "标签", tone: "gold" }
    ]
  },
  todos: [
    { time: "09:30", title: "复盘昨日关键案例", status: "待处理" },
    { time: "10:00", title: "清理过期系统记忆", status: "待处理" },
    { time: "14:30", title: "规则候选验证复盘", status: "待处理" }
  ],
  systemStatus: {
    reportIndex: "READY",
    caseRegistry: "PARTIAL",
    memoryRegistry: "PARTIAL",
    ruleRegistry: "PARTIAL",
    auditPack: "READY",
    researchDb: "READY",
    lastUpdatedAt: "09:42:31"
  },
  backendMapping: {
    reportLibrary: "ReportRenderer",
    auditEvidence: "OutputEnvelope/AuditEvent/AuditExportPack",
    evidenceChain: "research_os_rc.evidence_chain_auditor",
    caseRegistry: "data/research_db/cases/case_registry_v1.json",
    replay: "historical_replay",
    memoryDraft: "MemoryCandidate Preview",
    ruleCandidate: "Rule Candidate Miner"
  }
};

function requireSession(session: AuthSession | null): AuthSession {
  if (!session) {
    throw new MockApiError("AUTH_REQUIRED", "history api requires authenticated session");
  }
  return session;
}

function cloneHistoryData(packet: HistoryPageData, workspaceId: string): HistoryPageData {
  return {
    ...packet,
    workspaceId,
    safety: { ...packet.safety },
    kpis: packet.kpis.map((kpi) => ({ ...kpi })),
    learningPipeline: packet.learningPipeline.map((node) => ({ ...node })),
    monthlyStats: { ...packet.monthlyStats },
    events: packet.events.map((event) => ({ ...event })),
    reportLibrary: packet.reportLibrary.map((item) => ({ ...item })),
    caseLibrary: packet.caseLibrary.map((item) => ({ ...item })),
    memoryRuleSummary: {
      memories: packet.memoryRuleSummary.memories.map((memory) => ({ ...memory })),
      rules: packet.memoryRuleSummary.rules.map((rule) => ({ ...rule }))
    },
    spaceTimeSeal: {
      summary: packet.spaceTimeSeal.summary.map((item) => ({ ...item })),
      alert: { ...packet.spaceTimeSeal.alert },
      bookmarks: packet.spaceTimeSeal.bookmarks.map((bookmark) => ({ ...bookmark }))
    },
    todos: packet.todos.map((todo) => ({ ...todo })),
    systemStatus: { ...packet.systemStatus },
    backendMapping: { ...packet.backendMapping }
  };
}

function getBackendHistoryPacketUrl(): string | null {
  const configured = import.meta.env.VITE_ZMATRIX_HISTORY_PACKET_URL as string | undefined;
  if (configured) {
    return configured;
  }
  if (import.meta.env.MODE === "test" || typeof window === "undefined" || typeof fetch !== "function") {
    return null;
  }
  return "/api/cockpit/history_packet.json";
}

async function loadBackendHistoryPacket(workspaceId: string): Promise<HistoryPageData | null> {
  const packetUrl = getBackendHistoryPacketUrl();
  if (!packetUrl) {
    return null;
  }
  try {
    const response = await fetch(packetUrl, {
      headers: { accept: "application/json" },
      cache: "no-store"
    });
    if (!response.ok) {
      return null;
    }
    const packet = (await response.json()) as HistoryPageData;
    if (packet.workspaceId !== workspaceId) {
      return null;
    }
    return packet;
  } catch {
    return null;
  }
}

export async function getHistoryPageData(session: AuthSession | null): Promise<HistoryPageData> {
  const current = requireSession(session);
  const backendPacket = await loadBackendHistoryPacket(current.workspaceId);
  if (backendPacket) {
    return cloneHistoryData(backendPacket, current.workspaceId);
  }
  if (current.workspaceId === "ws_personal_z_prime") {
    return cloneHistoryData(zPrimeHistory, current.workspaceId);
  }
  return {
    ...cloneHistoryData(zPrimeHistory, current.workspaceId),
    kpis: zPrimeHistory.kpis.map((kpi) => ({ ...kpi, value: "0", note: "等待历史资产导入", delta: "0", tone: "muted" })),
    learningPipeline: zPrimeHistory.learningPipeline.map((node) => ({ ...node, count: 0, monthlyDelta: 0, status: "PENDING" })),
    monthlyStats: {
      ...zPrimeHistory.monthlyStats,
      newItems: 0,
      verified: 0,
      falsified: 0,
      crystallized: 0,
      promotable: 0
    },
    events: [],
    reportLibrary: [],
    caseLibrary: [],
    memoryRuleSummary: {
      memories: zPrimeHistory.memoryRuleSummary.memories.map((memory) => ({ ...memory, count: 0 })),
      rules: zPrimeHistory.memoryRuleSummary.rules.map((rule) => ({ ...rule, count: 0 }))
    },
    todos: [{ time: "--:--", title: "等待历史资产索引导入", status: "待处理" }],
    systemStatus: {
      ...zPrimeHistory.systemStatus,
      reportIndex: "PARTIAL",
      caseRegistry: "PARTIAL",
      memoryRegistry: "PARTIAL",
      ruleRegistry: "PARTIAL",
      auditPack: "PARTIAL",
      researchDb: "PARTIAL"
    }
  };
}

export async function createHistoryActionDraft(
  session: AuthSession | null,
  action: HistoryActionDraft["action"],
  payload: Record<string, unknown>
): Promise<HistoryActionDraft> {
  const current = requireSession(session);
  ensureNoClientTenantFields(payload);
  const auditEvent =
    action === "导出审计包"
      ? "EXPORT_HISTORY_AUDIT_PACK"
      : action === "查看详情" || action === "查看全部报告"
        ? "SAVE_HISTORY_REFERENCE"
        : action === "打开时空工具箱"
          ? "OPEN_SPACE_TIME_TOOLBOX_REFERENCE"
          : "CREATE_HISTORY_REVIEW_DRAFT";
  const response = await createWorkspaceDraft(current, payload, auditEvent);
  return {
    draftId: `history-draft-${Date.now()}`,
    workspaceId: response.workspaceId,
    targetId: String(payload.targetId ?? payload.eventId ?? "HISTORY"),
    action,
    status: action === "导出审计包" ? "AUDIT_PACK_READY" : action === "查看详情" || action === "查看全部报告" || action === "打开时空工具箱" ? "REFERENCE_SAVED" : "DRAFT_CREATED",
    humanReviewRequired: true,
    auditEvent: response.auditEvent,
    userMessage:
      action === "导出审计包"
        ? "历史审计包已准备，等待人工确认后导出。"
        : action === "查看详情"
          ? "历史事件详情已打开，证据链保持只读。"
          : action === "查看全部报告"
            ? "报告库索引已打开，保持只读复盘。"
            : action === "创建人工研究记录"
              ? "人工研究记录草案已创建，等待你补充判断。"
              : action === "生成复盘草案"
                ? "复盘草案已生成，等待人工确认。"
                : action === "打开时空工具箱"
                  ? "时空工具箱已打开，所有动作保持草案状态。"
                  : "历史学习动作已进入人工确认队列。"
  };
}
