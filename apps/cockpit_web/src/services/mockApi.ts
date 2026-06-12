import type { AuthSession } from "../auth";
import { pageCopy, type CockpitRouteId } from "../data/cockpit";

export type MetricTuple = [string, string, string];
export type RowTuple = [string, string, string, string];

export type CockpitPagePacket = {
  pageId: CockpitRouteId;
  workspaceId: string;
  title: string;
  kicker: string;
  primaryAction: string;
  secondaryAction: string;
  stats: MetricTuple[];
  tableTitle: string;
  rows: RowTuple[];
  audit: {
    paperOnly: true;
    humanReview: true;
    brokerRuntime: "BLOCKED";
    realTrade: "BLOCKED";
    dataScope: "WORKSPACE_SCOPED";
  };
};

export type PrivateWriteResponse = {
  status: "DRAFT_CREATED" | "REFERENCE_SAVED";
  workspaceId: string;
  createdBy: string;
  auditEvent: string;
};

export type DataSourceSecretResponse = {
  status: "REFERENCE_SAVED";
  provider: string;
  workspaceId: string;
  secretRef: string;
  tokenPreview: "***REDACTED***";
};

export type AgentTaskEnvelope = {
  agentId: string;
  taskType: string;
  currentUserId: string;
  workspaceId: string;
  writeLayers: ["workspace_scoped_drafts"];
  production: "BLOCKED";
  brokerRuntime: "BLOCKED";
  realTrade: "BLOCKED";
  payload: Record<string, unknown>;
};

export class MockApiError extends Error {
  code: "AUTH_REQUIRED" | "TENANT_SPOOFING" | "FORBIDDEN_WORKSPACE";

  constructor(code: MockApiError["code"], message: string) {
    super(message);
    this.name = "MockApiError";
    this.code = code;
  }
}

const CLIENT_FORBIDDEN_FIELDS = new Set(["workspace_id", "workspaceId", "owner_user_id", "created_by", "createdBy", "updated_by", "updatedBy"]);

const workspaceRows: Record<string, Partial<Record<CockpitRouteId, RowTuple[]>>> = {
  ws_personal_z_prime: {
    holdings: [
      ["紫金矿业", "800", "-8.40%", "持仓复核"],
      ["双环传动", "1800", "-4.15%", "持仓复核"],
      ["科创创业ETF天弘", "6500", "+5.36%", "只读观察"]
    ],
    selection: [
      ["300308 中际旭创", "人机共识", "投研增强", "创建人工研究记录"],
      ["688256 寒武纪-U", "事件驱动", "观察", "生成研究草案"],
      ["002594 比亚迪", "价值修复", "跟踪", "加入观察记录"]
    ]
  },
  ws_external_reviewer: {
    holdings: [["600519 贵州茅台", "100", "+1.12%", "持仓复核"]],
    selection: [["000858 五粮液", "观察", "只读", "创建人工研究记录"]]
  }
};

function requireSession(session: AuthSession | null): AuthSession {
  if (!session) {
    throw new MockApiError("AUTH_REQUIRED", "mock api requires an authenticated session");
  }
  return session;
}

export function findClientTenantFields(payload: unknown): string[] {
  const found = new Set<string>();

  function visit(value: unknown) {
    if (Array.isArray(value)) {
      value.forEach(visit);
      return;
    }
    if (value && typeof value === "object") {
      for (const [key, nested] of Object.entries(value as Record<string, unknown>)) {
        if (CLIENT_FORBIDDEN_FIELDS.has(key)) {
          found.add(key);
        }
        visit(nested);
      }
    }
  }

  visit(payload);
  return Array.from(found).sort();
}

export function ensureNoClientTenantFields(payload: Record<string, unknown>) {
  const fields = findClientTenantFields(payload);
  if (fields.length > 0) {
    throw new MockApiError("TENANT_SPOOFING", `client tenant fields are forbidden: ${fields.join(", ")}`);
  }
}

function cloneRows(rows: RowTuple[]): RowTuple[] {
  return rows.map((row) => [...row] as RowTuple);
}

export async function getCockpitPagePacket(session: AuthSession | null, pageId: CockpitRouteId): Promise<CockpitPagePacket> {
  const current = requireSession(session);
  const copy = pageCopy[pageId];
  const rows = workspaceRows[current.workspaceId]?.[pageId] ?? copy.rows;

  return {
    pageId,
    workspaceId: current.workspaceId,
    title: copy.title,
    kicker: copy.kicker,
    primaryAction: copy.primaryAction,
    secondaryAction: copy.secondaryAction,
    stats: copy.stats.map((stat) => [...stat] as MetricTuple),
    tableTitle: copy.tableTitle,
    rows: cloneRows(rows),
    audit: {
      paperOnly: true,
      humanReview: true,
      brokerRuntime: "BLOCKED",
      realTrade: "BLOCKED",
      dataScope: "WORKSPACE_SCOPED"
    }
  };
}

export async function createWorkspaceDraft(
  session: AuthSession | null,
  payload: Record<string, unknown>,
  auditEvent: string
): Promise<PrivateWriteResponse> {
  const current = requireSession(session);
  ensureNoClientTenantFields(payload);
  return {
    status: "DRAFT_CREATED",
    workspaceId: current.workspaceId,
    createdBy: current.userId,
    auditEvent
  };
}

export async function saveDataSourceSecret(
  session: AuthSession | null,
  provider: string,
  rawSecret: string
): Promise<DataSourceSecretResponse> {
  const current = requireSession(session);
  if (!rawSecret) {
    throw new MockApiError("AUTH_REQUIRED", "secret value is required");
  }
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(`${current.workspaceId}:${provider}:${rawSecret}`));
  const shortDigest = Array.from(new Uint8Array(digest))
    .slice(0, 8)
    .map((byte) => byte.toString(16).padStart(2, "0"))
    .join("");
  return {
    status: "REFERENCE_SAVED",
    provider,
    workspaceId: current.workspaceId,
    secretRef: `secret://workspace/${current.workspaceId}/${provider}/${shortDigest}`,
    tokenPreview: "***REDACTED***"
  };
}

export function buildAgentTaskEnvelope(
  session: AuthSession | null,
  agentId: string,
  taskType: string,
  payload: Record<string, unknown>
): AgentTaskEnvelope {
  const current = requireSession(session);
  ensureNoClientTenantFields(payload);
  return {
    agentId,
    taskType,
    currentUserId: current.userId,
    workspaceId: current.workspaceId,
    writeLayers: ["workspace_scoped_drafts"],
    production: "BLOCKED",
    brokerRuntime: "BLOCKED",
    realTrade: "BLOCKED",
    payload: { ...payload }
  };
}

export async function attemptWorkspaceRead(session: AuthSession | null, requestedWorkspaceId: string) {
  const current = requireSession(session);
  if (requestedWorkspaceId !== current.workspaceId) {
    throw new MockApiError("FORBIDDEN_WORKSPACE", "requested workspace is not available to this session");
  }
  return { workspaceId: current.workspaceId, status: "ALLOWED" as const };
}
