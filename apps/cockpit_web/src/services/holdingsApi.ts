import type { AuthSession } from "../auth";
import { createWorkspaceDraft, ensureNoClientTenantFields, MockApiError } from "./mockApi";

export type AccountSummary = {
  totalAssets: number;
  floatingPnl: number;
  dayReferencePnl: number;
  marketValue: number;
  cash: number;
  withdrawable: number;
  currency: "CNY";
  accountMask: string;
};

export type HoldingPosition = {
  symbol: string;
  name: string;
  role: "CORE" | "ROTATION" | "EVENT" | "DEFENSIVE";
  marketValue: number;
  weightPct: number;
  floatingPnl: number;
  floatingPnlPct: number;
  alphaContributionPct: number | null;
  signalStrength: "LOW" | "MID" | "HIGH";
  thesisStatus: "HEALTHY" | "WATCH" | "REVIEW" | "BROKEN";
  catalystStatus: "ACTIVE" | "DECAYING" | "EXHAUSTED" | "VACUUM" | "NONE";
  nextAction:
    | "HOLD_RESEARCH"
    | "WATCH"
    | "THESIS_REVIEW"
    | "RISK_REVIEW"
    | "MOVE_TO_OBSERVATION"
    | "DATA_INSUFFICIENT";
  quantity: number;
  available: number;
  costPrice: number;
  currentPrice: number;
  reviewStatus: "待复核" | "只读观察";
  riskTag: "回撤复核" | "正收益观察";
};

export type HoldingReviewDraft = {
  draftId: string;
  workspaceId: string;
  symbol: string;
  action: "持仓复核" | "创建人工研究记录" | "生成复核草案" | "导出审计包";
  status: "DRAFT_CREATED" | "AUDIT_PACK_READY";
  humanReviewRequired: true;
  auditEvent: string;
  userMessage: string;
};

export type HoldingsPacket = {
  workspaceId: string;
  asOf: string;
  account: AccountSummary;
  kpi: {
    todayPnl: number;
    todayPnlPct: number;
    totalAsset: number;
    holdingAlphaAnnualized: number | null;
    cashRatio: number;
    maxDrawdownRecentYear: number | null;
    dataFreshness: "FRESH" | "STALE" | "PARTIAL" | "ERROR";
  };
  curveStats: Array<{
    label: string;
    value: string;
    tone: "gold" | "green" | "red" | "muted";
  }>;
  positions: HoldingPosition[];
  observationWarehouses: Array<{
    warehouseType: "CORE_OBSERVATION" | "ROTATION_OBSERVATION" | "DARK_HORSE_OBSERVATION";
    title: string;
    count: number;
    pendingActionCount: number;
    todayChange: string;
    outcomeStatus: string;
    tone: "green" | "gold" | "red";
    topCandidates: Array<{
      ticker: string;
      name: string;
      oneLineReason: string;
      validationStatus: "PENDING" | "OUTPERFORMING" | "UNDERPERFORMING" | "NEED_REVIEW";
    }>;
  }>;
  todos: Array<{
    time: string;
    title: string;
    tone: "green" | "gold" | "red";
  }>;
  audit: {
    paperOnly: true;
    humanReview: true;
    brokerRuntime: "BLOCKED";
    realTrade: "BLOCKED";
    dataScope: "WORKSPACE_SCOPED";
  };
};

const zPrimeHoldings: HoldingsPacket = {
  workspaceId: "ws_personal_z_prime",
  asOf: "2026-06-04",
  account: {
    totalAssets: 110249.84,
    floatingPnl: -4776.77,
    dayReferencePnl: 3733.5,
    marketValue: 110137,
    cash: 112.84,
    withdrawable: 112.84,
    currency: "CNY",
    accountMask: "550***06"
  },
  positions: [
    {
      symbol: "601899",
      name: "紫金矿业",
      role: "CORE",
      marketValue: 25264,
      weightPct: 22.91,
      floatingPnl: -2317.42,
      floatingPnlPct: -8.4,
      alphaContributionPct: null,
      signalStrength: "MID",
      thesisStatus: "REVIEW",
      catalystStatus: "DECAYING",
      nextAction: "RISK_REVIEW",
      quantity: 800,
      available: 800,
      costPrice: 34.477,
      currentPrice: 31.58,
      reviewStatus: "待复核",
      riskTag: "回撤复核"
    },
    {
      symbol: "002472",
      name: "双环传动",
      role: "ROTATION",
      marketValue: 71964,
      weightPct: 65.27,
      floatingPnl: -3116.61,
      floatingPnlPct: -4.15,
      alphaContributionPct: null,
      signalStrength: "LOW",
      thesisStatus: "REVIEW",
      catalystStatus: "DECAYING",
      nextAction: "THESIS_REVIEW",
      quantity: 1800,
      available: 1800,
      costPrice: 41.711,
      currentPrice: 39.98,
      reviewStatus: "待复核",
      riskTag: "回撤复核"
    },
    {
      symbol: "588860",
      name: "科创创业ETF天弘",
      role: "DEFENSIVE",
      marketValue: 12909,
      weightPct: 11.71,
      floatingPnl: 657.26,
      floatingPnlPct: 5.36,
      alphaContributionPct: null,
      signalStrength: "MID",
      thesisStatus: "WATCH",
      catalystStatus: "ACTIVE",
      nextAction: "WATCH",
      quantity: 6500,
      available: 6500,
      costPrice: 1.885,
      currentPrice: 1.986,
      reviewStatus: "只读观察",
      riskTag: "正收益观察"
    }
  ],
  kpi: {
    todayPnl: 3733.5,
    todayPnlPct: 3.39,
    totalAsset: 110249.84,
    holdingAlphaAnnualized: null,
    cashRatio: 0.1,
    maxDrawdownRecentYear: null,
    dataFreshness: "FRESH"
  },
  curveStats: [
    { label: "累计收益", value: "待导入", tone: "muted" },
    { label: "年化收益", value: "待归因", tone: "muted" },
    { label: "波动率", value: "待计算", tone: "muted" },
    { label: "夏普比率", value: "待计算", tone: "muted" },
    { label: "最大回撤", value: "待计算", tone: "muted" }
  ],
  observationWarehouses: [
    {
      warehouseType: "CORE_OBSERVATION",
      title: "底仓观察",
      count: 3,
      pendingActionCount: 2,
      todayChange: "新增复核 2 项",
      outcomeStatus: "稳定",
      tone: "green",
      topCandidates: [
        { ticker: "601899", name: "紫金矿业", oneLineReason: "资源底仓回撤复核", validationStatus: "NEED_REVIEW" },
        { ticker: "588860", name: "科创创业ETF天弘", oneLineReason: "指数仓继续观察", validationStatus: "OUTPERFORMING" },
        { ticker: "ACCOUNT", name: "现金水位", oneLineReason: "现金比例偏低", validationStatus: "PENDING" }
      ]
    },
    {
      warehouseType: "ROTATION_OBSERVATION",
      title: "轮动观察",
      count: 1,
      pendingActionCount: 1,
      todayChange: "动能转弱",
      outcomeStatus: "关注",
      tone: "gold",
      topCandidates: [
        { ticker: "002472", name: "双环传动", oneLineReason: "轮动催化衰减", validationStatus: "NEED_REVIEW" }
      ]
    },
    {
      warehouseType: "DARK_HORSE_OBSERVATION",
      title: "黑马观察",
      count: 0,
      pendingActionCount: 0,
      todayChange: "无新增",
      outcomeStatus: "空仓",
      tone: "gold",
      topCandidates: [
        { ticker: "PENDING", name: "等待投研问股输入", oneLineReason: "由候选池进入观察", validationStatus: "PENDING" }
      ]
    }
  ],
  todos: [
    { time: "09:30", title: "复核紫金矿业回撤路径", tone: "red" },
    { time: "10:00", title: "复核双环传动 thesis", tone: "red" },
    { time: "14:30", title: "补一条人工研究记录", tone: "gold" }
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
    throw new MockApiError("AUTH_REQUIRED", "holdings api requires authenticated session");
  }
  return session;
}

function clonePacket(packet: HoldingsPacket, workspaceId: string): HoldingsPacket {
  return {
    ...packet,
    workspaceId,
    account: { ...packet.account },
    positions: packet.positions.map((position) => ({ ...position })),
    kpi: { ...packet.kpi },
    curveStats: packet.curveStats.map((stat) => ({ ...stat })),
    observationWarehouses: packet.observationWarehouses.map((warehouse) => ({
      ...warehouse,
      topCandidates: warehouse.topCandidates.map((candidate) => ({ ...candidate }))
    })),
    todos: packet.todos.map((todo) => ({ ...todo })),
    audit: { ...packet.audit }
  };
}

function getBackendHoldingsPacketUrl(): string | null {
  const configured = import.meta.env.VITE_ZMATRIX_HOLDINGS_PACKET_URL as string | undefined;
  if (configured) {
    return configured;
  }
  if (import.meta.env.MODE === "test" || typeof window === "undefined" || typeof fetch !== "function") {
    return null;
  }
  return "/api/cockpit/holdings_packet.json";
}

async function loadBackendHoldingsPacket(workspaceId: string): Promise<HoldingsPacket | null> {
  const packetUrl = getBackendHoldingsPacketUrl();
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
    const packet = (await response.json()) as HoldingsPacket;
    if (packet.workspaceId !== workspaceId) {
      return null;
    }
    return packet;
  } catch {
    return null;
  }
}

export async function getHoldingsPacket(session: AuthSession | null): Promise<HoldingsPacket> {
  const current = requireSession(session);
  const backendPacket = await loadBackendHoldingsPacket(current.workspaceId);
  if (backendPacket) {
    return clonePacket(backendPacket, current.workspaceId);
  }
  if (current.workspaceId === "ws_personal_z_prime") {
    return clonePacket(zPrimeHoldings, current.workspaceId);
  }
  return {
    ...clonePacket(zPrimeHoldings, current.workspaceId),
    account: {
      ...zPrimeHoldings.account,
      totalAssets: 0,
      floatingPnl: 0,
      dayReferencePnl: 0,
      marketValue: 0,
      cash: 0,
      withdrawable: 0
    },
    positions: [],
    kpi: {
      ...zPrimeHoldings.kpi,
      todayPnl: 0,
      todayPnlPct: 0,
      totalAsset: 0,
      cashRatio: 0,
      dataFreshness: "PARTIAL"
    },
    curveStats: zPrimeHoldings.curveStats.map((stat) => ({ ...stat, value: "待导入" })),
    observationWarehouses: zPrimeHoldings.observationWarehouses.map((warehouse) => ({
      ...warehouse,
      count: 0,
      pendingActionCount: 0,
      todayChange: "等待导入",
      outcomeStatus: "未启用",
      topCandidates: []
    })),
    todos: [{ time: "--:--", title: "等待账户快照导入", tone: "gold" }]
  };
}

export async function createHoldingActionDraft(
  session: AuthSession | null,
  action: HoldingReviewDraft["action"],
  payload: Record<string, unknown>
): Promise<HoldingReviewDraft> {
  const current = requireSession(session);
  ensureNoClientTenantFields(payload);
  const auditEvent =
    action === "创建人工研究记录"
      ? "CREATE_MANUAL_RESEARCH_RECORD"
      : action === "导出审计包"
        ? "EXPORT_HOLDINGS_AUDIT_PACK"
        : "CREATE_HOLDING_REVIEW_DRAFT";
  const response = await createWorkspaceDraft(current, payload, auditEvent);
  return {
    draftId: `holdings-draft-${Date.now()}`,
    workspaceId: response.workspaceId,
    symbol: String(payload.symbol ?? "ACCOUNT"),
    action,
    status: action === "导出审计包" ? "AUDIT_PACK_READY" : "DRAFT_CREATED",
    humanReviewRequired: true,
    auditEvent: response.auditEvent,
    userMessage:
      action === "导出审计包"
        ? "审计包已准备，可在人工复核后导出。"
        : action === "创建人工研究记录"
          ? "已创建人工研究记录草案，等待你补充判断。"
          : action === "生成复核草案"
            ? "复核草案已生成，等待人工确认。"
            : "持仓复核已进入人工确认队列。"
  };
}
