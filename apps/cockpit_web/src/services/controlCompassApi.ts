import type { AuthSession } from "../auth";
import { createWorkspaceDraft, ensureNoClientTenantFields, MockApiError } from "./mockApi";

export type GovernanceDomainId =
  | "DATA_QUALITY"
  | "SAMPLE_POOL"
  | "FACTOR_SIGNAL"
  | "CATALYST_CYCLE"
  | "B_MATRIX"
  | "R_MATRIX"
  | "D_MATRIX"
  | "EXPERIENCE_INTERNALIZATION";

export type GovernanceStatus = "STABLE" | "NEED_CALIBRATION" | "UNDER_REVIEW" | "BLOCKED" | "PENDING_APPROVAL";
export type GovernanceRiskLevel = "LOW" | "MID" | "HIGH" | "CRITICAL";
export type OptimizationSnapshotStatus = "READY" | "REQUIRED" | "MISSING";

export type CompassKpi = {
  governanceDomainCount: number;
  healthyDomainCount: number;
  healthScore: number;
  latestPaperHitRatePct: number;
  weakenedSignalCount: number;
  pendingAdjudicationCount: number;
  optimizationSnapshotStatus: OptimizationSnapshotStatus;
  pendingChangeCount: number;
  blockedChangeCount: number;
  monthlyInternalizationPct: number;
  auditCompletenessPct: number;
  configVersion: string;
  dataFreshness: "FRESH" | "STALE" | "PARTIAL" | "ERROR";
};

export type GovernanceDomainStatus = {
  domainId: GovernanceDomainId;
  index: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8;
  displayName: string;
  ringIndex: number;
  status: GovernanceStatus;
  pendingChanges: number;
  riskLevel: GovernanceRiskLevel;
  lastReviewedAt: string;
};

export type DerivationDetail = {
  selectedDomainId: GovernanceDomainId;
  selectedDomainName: string;
  currentValue: {
    label: string;
    value: string | number;
  };
  suggestedValue: {
    label: string;
    value: string | number;
  };
  impactScope: {
    relatedParameterCount: number;
    affectedModuleCount: number;
    affectedPages: string[];
  };
  validationStatus: {
    paperValidationPassed: boolean;
    confidencePct: number;
    method: string;
  };
  auditStatus: {
    status: "NOT_STARTED" | "PENDING_EXPERT_REVIEW" | "PASSED" | "FAILED";
    expectedFinishAt?: string;
  };
};

export type DerivationSandbox = {
  draft: {
    draftId: string;
    domainId: GovernanceDomainId;
    affectedParameterCount: number;
    version: string;
  };
  impact: {
    impactLevel: "LOW" | "MID" | "HIGH";
    coverage: "LOW" | "MID" | "HIGH";
    strategyImpact: string;
    internalizationImpactPct: number;
  };
  risk: {
    riskLevel: GovernanceRiskLevel;
    potentialImpact: string;
    varianceRange: [number, number];
    blockingCount: number;
  };
  paperValidation: {
    method: string;
    sampleSize: number;
    passRatePct: number;
    conclusion: "PASSED" | "FAILED" | "INSUFFICIENT";
  };
  humanReview: {
    status: "NOT_SUBMITTED" | "PENDING" | "APPROVED" | "REJECTED";
    requiredReviewerCount: number;
    estimatedMinutes: number;
  };
};

export type DerivationRuling = {
  draftId: string;
  evidenceChain: {
    linkedEvidenceCount: number;
    completenessPct: number;
  };
  expertReview: {
    required: number;
    passed: number;
    expectedFinishAt?: string;
  };
  auditResult: {
    status: "PENDING" | "PASSED" | "FAILED";
    completenessPct?: number;
  };
  rulingStatus: {
    status: "PENDING" | "APPROVED" | "REJECTED" | "DEFERRED";
    changeWindowOpen: boolean;
  };
};

export type CalibrationParameterFamily = {
  familyId: string;
  domainId: GovernanceDomainId;
  label: string;
  scope: string;
  backendMapping: string;
  currentVersion: string;
  systemOptimizedVersion: string;
  currentSignal: string;
  optimizationAdvice: string;
  paperReview: string;
  driftStatus: "STABLE" | "DRIFTING" | "WEAKENED" | "LOW_SAMPLE" | "BLOCKED";
  editableMode: "DRAFT_ONLY" | "READ_ONLY" | "LOCKED";
  snapshotRequired: true;
  restoreAvailable: boolean;
};

export type CalibrationDispute = {
  disputeId: string;
  domainId: GovernanceDomainId;
  title: string;
  reason: string;
  severity: GovernanceRiskLevel;
  humanReviewRequired: true;
};

export type TianjiDerivationPanelData = {
  dashboard: {
    configVersion: string;
    pendingApprovalCount: number;
    blockedCount: number;
    internalizationPct: number;
    doNotChangeTodayCount: number;
  };
  riftAlerts: Array<{
    alertId: string;
    level: "L1" | "L2" | "L3" | "L4";
    title: string;
    summary: string;
    affectedDomainIds: GovernanceDomainId[];
    actionRequired: boolean;
  }>;
  seals: Array<{
    sealType: "STABLE" | "CALIBRATION" | "FORBIDDEN";
    title: "稳定印" | "校准印" | "禁改印";
    summary: string;
    targetDomainIds: GovernanceDomainId[];
  }>;
};

export type ControlCompassTodo = {
  todoId: string;
  sourceType: "PARAMETER_CHANGE" | "RISK_REVIEW" | "MEMORY_CLEANUP" | "CATALYST_CALIBRATION" | "AUDIT_REVIEW" | "MONTHLY_INTERNALIZATION";
  priority: "LOW" | "MID" | "HIGH" | "CRITICAL";
  title: string;
  dueTime?: string;
  status: "PENDING" | "DONE" | "DEFERRED";
};

export type ControlCompassActionDraft = {
  draftId: string;
  workspaceId: string;
  action:
    | "查看治理域全景详情"
    | "查看参数族详情"
    | "查看推衍详情"
    | "创建校准草案"
    | "发起人审提交"
    | "查看审计链详情"
    | "打开衍算手工工具箱"
    | "导出审计包"
    | "恢复系统自优化结果"
    | "放弃草案";
  status: "DRAFT_CREATED" | "AUDIT_PACK_READY" | "REFERENCE_SAVED";
  humanReviewRequired: true;
  auditEvent: string;
  userMessage: string;
};

export type ControlCompassPageData = {
  workspaceId: string;
  asOf: string;
  safety: {
    paperOnly: true;
    humanReviewRequired: true;
    realTradeAllowed: false;
    brokerOrderAllowed: false;
    productionAllowed: false;
    agentDirectMutationAllowed: false;
  };
  kpi: CompassKpi;
  governanceDomains: GovernanceDomainStatus[];
  selectedDomain: DerivationDetail;
  sandbox: DerivationSandbox;
  ruling: DerivationRuling;
  optimizationSummary: {
    systemVersion: string;
    suggestedVersion: string;
    latestCycleId: string;
    headline: string;
    evidence: string;
    snapshotId: string;
    snapshotStatus: OptimizationSnapshotStatus;
    restoreAvailable: boolean;
  };
  parameterFamilies: CalibrationParameterFamily[];
  calibrationDisputes: CalibrationDispute[];
  derivationPanel: TianjiDerivationPanelData;
  todos: ControlCompassTodo[];
  systemStatus: {
    marketData: "READY" | "PARTIAL" | "ERROR";
    financialData: "READY" | "PARTIAL" | "ERROR";
    macroData: "READY" | "PARTIAL" | "ERROR";
    strategyEngine: "READY" | "PARTIAL" | "ERROR";
    riskEngine: "READY" | "PARTIAL" | "ERROR";
    dataService: "READY" | "PARTIAL" | "ERROR";
    configRegistry: "READY" | "PARTIAL" | "ERROR";
    auditService: "READY" | "PARTIAL" | "ERROR";
    lastUpdatedAt: string;
  };
};

const compassMock: ControlCompassPageData = {
  workspaceId: "ws_personal_z_prime",
  asOf: "2026-06-04",
  safety: {
    paperOnly: true,
    humanReviewRequired: true,
    realTradeAllowed: false,
    brokerOrderAllowed: false,
    productionAllowed: false,
    agentDirectMutationAllowed: false
  },
  kpi: {
    governanceDomainCount: 8,
    healthyDomainCount: 5,
    healthScore: 82,
    latestPaperHitRatePct: 87.3,
    weakenedSignalCount: 8,
    pendingAdjudicationCount: 6,
    optimizationSnapshotStatus: "READY",
    pendingChangeCount: 6,
    blockedChangeCount: 2,
    monthlyInternalizationPct: 56,
    auditCompletenessPct: 92.4,
    configVersion: "v2.6.0",
    dataFreshness: "FRESH"
  },
  governanceDomains: [
    { domainId: "DATA_QUALITY", index: 1, displayName: "数据质量门", ringIndex: 8, status: "STABLE", pendingChanges: 0, riskLevel: "LOW", lastReviewedAt: "2026-06-04 09:10" },
    { domainId: "SAMPLE_POOL", index: 2, displayName: "样本池韧性", ringIndex: 7, status: "STABLE", pendingChanges: 0, riskLevel: "LOW", lastReviewedAt: "2026-06-04 09:12" },
    { domainId: "FACTOR_SIGNAL", index: 3, displayName: "因子信号门", ringIndex: 6, status: "NEED_CALIBRATION", pendingChanges: 3, riskLevel: "MID", lastReviewedAt: "2026-06-04 09:15" },
    { domainId: "CATALYST_CYCLE", index: 4, displayName: "催化周期门", ringIndex: 5, status: "NEED_CALIBRATION", pendingChanges: 2, riskLevel: "MID", lastReviewedAt: "2026-06-04 09:17" },
    { domainId: "B_MATRIX", index: 5, displayName: "B-Matrix 底仓", ringIndex: 4, status: "STABLE", pendingChanges: 0, riskLevel: "LOW", lastReviewedAt: "2026-06-04 09:18" },
    { domainId: "R_MATRIX", index: 6, displayName: "R-Matrix 轮动", ringIndex: 3, status: "NEED_CALIBRATION", pendingChanges: 1, riskLevel: "MID", lastReviewedAt: "2026-06-04 09:19" },
    { domainId: "D_MATRIX", index: 7, displayName: "D-Matrix 黑马", ringIndex: 2, status: "UNDER_REVIEW", pendingChanges: 1, riskLevel: "MID", lastReviewedAt: "2026-06-04 09:20" },
    { domainId: "EXPERIENCE_INTERNALIZATION", index: 8, displayName: "经验内化", ringIndex: 1, status: "STABLE", pendingChanges: 0, riskLevel: "LOW", lastReviewedAt: "2026-06-04 09:22" }
  ],
  selectedDomain: {
    selectedDomainId: "CATALYST_CYCLE",
    selectedDomainName: "催化周期门",
    currentValue: { label: "当前版本", value: "catalyst-cycle v1.2" },
    suggestedValue: { label: "自优化建议", value: "旧催化残值与过载阈值收紧" },
    impactScope: {
      relatedParameterCount: 8,
      affectedModuleCount: 4,
      affectedPages: ["执仓决断", "投研问股", "时空回溯", "天机罗盘"]
    },
    validationStatus: {
      paperValidationPassed: true,
      confidencePct: 87.3,
      method: "近 6 个月纸面验证"
    },
    auditStatus: {
      status: "PENDING_EXPERT_REVIEW",
      expectedFinishAt: "2026-06-05 14:00"
    }
  },
  sandbox: {
    draft: {
      draftId: "D-20260604-03",
      domainId: "CATALYST_CYCLE",
      affectedParameterCount: 8,
      version: "catalyst-cycle v1.2"
    },
    impact: {
      impactLevel: "MID",
      coverage: "MID",
      strategyImpact: "旧催化衰减和催化真空识别更谨慎",
      internalizationImpactPct: 4
    },
    risk: {
      riskLevel: "MID",
      potentialImpact: "可能降低事件黑马召回，需要更多纸面周期确认",
      varianceRange: [-1.2, 0.8],
      blockingCount: 2
    },
    paperValidation: {
      method: "渐进式纸面验证",
      sampleSize: 12,
      passRatePct: 87.3,
      conclusion: "PASSED"
    },
    humanReview: {
      status: "NOT_SUBMITTED",
      requiredReviewerCount: 3,
      estimatedMinutes: 100
    }
  },
  ruling: {
    draftId: "D-20260604-03",
    evidenceChain: {
      linkedEvidenceCount: 5,
      completenessPct: 100
    },
    expertReview: {
      required: 2,
      passed: 1,
      expectedFinishAt: "2026-06-05 14:00"
    },
    auditResult: {
      status: "PENDING",
      completenessPct: 92.4
    },
    rulingStatus: {
      status: "PENDING",
      changeWindowOpen: false
    }
  },
  optimizationSummary: {
    systemVersion: "quant-param v2.6.0",
    suggestedVersion: "v2.6.1 草案",
    latestCycleId: "V12.4 第2轮",
    headline: "系统建议收紧旧催化残值与因子晋级门槛，保持数据与样本池门槛。",
    evidence: "V12.2 复盘：弱化 8 项 / 样本不足 4 项 / 确认 0 项",
    snapshotId: "OPT-SNAP-20260604-01",
    snapshotStatus: "READY",
    restoreAvailable: true
  },
  parameterFamilies: [
    {
      familyId: "PF-DATA-QUALITY",
      domainId: "DATA_QUALITY",
      label: "数据健康与泄漏门",
      scope: "新鲜度、覆盖率、泄漏审计、缺失样本处理",
      backendMapping: "数据健康 / 泄漏审计 / 覆盖率审计",
      currentVersion: "data-gate v1.8",
      systemOptimizedVersion: "data-gate v1.8",
      currentSignal: "实时 · T+0",
      optimizationAdvice: "保持当前门槛",
      paperReview: "覆盖稳定，无泄漏报警",
      driftStatus: "STABLE",
      editableMode: "DRAFT_ONLY",
      snapshotRequired: true,
      restoreAvailable: true
    },
    {
      familyId: "PF-SAMPLE-POOL",
      domainId: "SAMPLE_POOL",
      label: "候选池韧性与矩阵时钟",
      scope: "池规模、零池率、小池率、B/R/D 时钟一致性",
      backendMapping: "候选池韧性 / 矩阵时钟一致性",
      currentVersion: "pool-clock v3.5.7",
      systemOptimizedVersion: "pool-clock v3.5.7",
      currentSignal: "候选池韧性通过",
      optimizationAdvice: "保持当前 TTL 与 pool resilience hardgate",
      paperReview: "walk-forward 覆盖 3/3",
      driftStatus: "STABLE",
      editableMode: "DRAFT_ONLY",
      snapshotRequired: true,
      restoreAvailable: true
    },
    {
      familyId: "PF-FACTOR-SIGNAL",
      domainId: "FACTOR_SIGNAL",
      label: "因子信号与晋级门",
      scope: "RankIC、decay、horizon、promote/reject、live paper 反馈",
      backendMapping: "因子工厂 / 纸面跟踪 / Z9 复盘反馈",
      currentVersion: "factor-gate v12.3",
      systemOptimizedVersion: "factor-gate v12.4-draft",
      currentSignal: "8 个因子首轮弱化",
      optimizationAdvice: "收紧首轮弱化因子晋级，至少补 2 个纸面跟踪周期",
      paperReview: "确认 0 项 / 弱化 8 项 / 样本不足 4 项",
      driftStatus: "WEAKENED",
      editableMode: "DRAFT_ONLY",
      snapshotRequired: true,
      restoreAvailable: true
    },
    {
      familyId: "PF-CATALYST-CYCLE",
      domainId: "CATALYST_CYCLE",
      label: "催化周期门",
      scope: "叙事水温、催化半衰期、残值、退潮、真空、过载、事件结果回链",
      backendMapping: "催化生命周期 / 叙事水温 / 主题热度 / 事件结果回链",
      currentVersion: "catalyst-cycle v1.2",
      systemOptimizedVersion: "catalyst-cycle v1.3-draft",
      currentSignal: "旧催化退潮 2 项 / 真空 1 项",
      optimizationAdvice: "收紧旧催化残值阈值，保留高热主题冷却观察",
      paperReview: "2 个退潮样本与 D-Matrix 假预热重叠",
      driftStatus: "DRIFTING",
      editableMode: "DRAFT_ONLY",
      snapshotRequired: true,
      restoreAvailable: true
    },
    {
      familyId: "PF-B-MATRIX",
      domainId: "B_MATRIX",
      label: "B-Matrix 底仓质量门",
      scope: "评级 cap、质量陷阱、估值上下文、Thesis Stop",
      backendMapping: "B-Matrix v2.1.1 / 评级上限 / 质量陷阱",
      currentVersion: "b-matrix v2.1.1",
      systemOptimizedVersion: "b-matrix v2.1.1",
      currentSignal: "稳定",
      optimizationAdvice: "保持底仓质量门，暂不放松",
      paperReview: "底仓候选无需新增草案",
      driftStatus: "STABLE",
      editableMode: "DRAFT_ONLY",
      snapshotRequired: true,
      restoreAvailable: true
    },
    {
      familyId: "PF-R-MATRIX",
      domainId: "R_MATRIX",
      label: "R-Matrix 轮动/震荡门",
      scope: "Hurst、半衰期、箱体幅度、支撑阻力、波动衰减",
      backendMapping: "R-Matrix v1.1 / 震荡王评分",
      currentVersion: "r-matrix v1.1",
      systemOptimizedVersion: "r-matrix v1.1-review",
      currentSignal: "轮动信号偏弱",
      optimizationAdvice: "复核半衰期与波动衰减阈值",
      paperReview: "需与因子弱化共同裁定",
      driftStatus: "DRIFTING",
      editableMode: "DRAFT_ONLY",
      snapshotRequired: true,
      restoreAvailable: true
    },
    {
      familyId: "PF-D-MATRIX",
      domainId: "D_MATRIX",
      label: "D-Matrix 黑马源点门",
      scope: "黑马基因、产业点火、主题种子、假预热惩罚、M1 数据质量",
      backendMapping: "D-Matrix v2.2 / M1 覆盖 / 假预热惩罚",
      currentVersion: "d-matrix v2.2",
      systemOptimizedVersion: "d-matrix v2.2-review",
      currentSignal: "假预热惩罚待复核",
      optimizationAdvice: "保持 WATCH_ONLY 上限，禁止提高执行级别",
      paperReview: "需补 M1 覆盖证据",
      driftStatus: "LOW_SAMPLE",
      editableMode: "DRAFT_ONLY",
      snapshotRequired: true,
      restoreAvailable: true
    },
    {
      familyId: "PF-EXPERIENCE-INTERNALIZATION",
      domainId: "EXPERIENCE_INTERNALIZATION",
      label: "经验内化",
      scope: "账户生存线、安全硬门、V3 压测、Z9 反馈、月度经验内化",
      backendMapping: "账户生存线 / 安全硬门 / Z9 校准 / 月度经验内化",
      currentVersion: "experience-internalization v2.6",
      systemOptimizedVersion: "experience-internalization v2.6",
      currentSignal: "经验内化 56%",
      optimizationAdvice: "保持纸面观察和人审门，禁止自动调参",
      paperReview: "待审 5 项，阻断 2 项",
      driftStatus: "STABLE",
      editableMode: "DRAFT_ONLY",
      snapshotRequired: true,
      restoreAvailable: true
    }
  ],
  calibrationDisputes: [
    {
      disputeId: "DISPUTE-FACTOR-001",
      domainId: "FACTOR_SIGNAL",
      title: "因子晋级门收紧",
      reason: "首轮 live paper 中 8 个因子 weakened，系统建议延后推广。",
      severity: "MID",
      humanReviewRequired: true
    },
    {
      disputeId: "DISPUTE-CATALYST-001",
      domainId: "CATALYST_CYCLE",
      title: "旧催化残值阈值收紧",
      reason: "近期退潮样本与假预热重叠，系统建议降低旧催化继续加分的权重。",
      severity: "MID",
      humanReviewRequired: true
    },
    {
      disputeId: "DISPUTE-DMATRIX-001",
      domainId: "D_MATRIX",
      title: "假预热惩罚是否过严",
      reason: "M1 覆盖证据不足，不允许直接放松黑马源点门。",
      severity: "MID",
      humanReviewRequired: true
    }
  ],
  derivationPanel: {
    dashboard: {
      configVersion: "v2.6.0",
      pendingApprovalCount: 8,
      blockedCount: 2,
      internalizationPct: 56,
      doNotChangeTodayCount: 3
    },
    riftAlerts: [
      {
        alertId: "RIFT-20260604-01",
        level: "L3",
        title: "因子弱化反馈待裁定",
        summary: "首轮纸面跟踪中 8 个因子弱化，旧催化退潮样本需同步校准。",
        affectedDomainIds: ["FACTOR_SIGNAL", "CATALYST_CYCLE"],
        actionRequired: true
      }
    ],
    seals: [
      { sealType: "STABLE", title: "稳定印", summary: "数据、样本与经验内核稳定", targetDomainIds: ["DATA_QUALITY", "SAMPLE_POOL", "EXPERIENCE_INTERNALIZATION"] },
      { sealType: "CALIBRATION", title: "校准印", summary: "因子、催化与轮动待校准", targetDomainIds: ["FACTOR_SIGNAL", "CATALYST_CYCLE", "R_MATRIX"] },
      { sealType: "FORBIDDEN", title: "禁改印", summary: "高风险域禁止越权修改", targetDomainIds: ["D_MATRIX"] }
    ]
  },
  todos: [
    { todoId: "todo-experience-01", sourceType: "RISK_REVIEW", priority: "HIGH", title: "复核经验内化草案", dueTime: "09:30", status: "PENDING" },
    { todoId: "todo-catalyst-01", sourceType: "CATALYST_CALIBRATION", priority: "MID", title: "确认催化周期门校准", dueTime: "10:15", status: "PENDING" },
    { todoId: "todo-audit-01", sourceType: "AUDIT_REVIEW", priority: "MID", title: "补齐量化审计证据", dueTime: "14:00", status: "PENDING" }
  ],
  systemStatus: {
    marketData: "READY",
    financialData: "READY",
    macroData: "READY",
    strategyEngine: "READY",
    riskEngine: "READY",
    dataService: "READY",
    configRegistry: "READY",
    auditService: "READY",
    lastUpdatedAt: "2026-06-04 09:42:31"
  }
};

function requireSession(session: AuthSession | null): AuthSession {
  if (!session) {
    throw new MockApiError("AUTH_REQUIRED", "control compass api requires authenticated session");
  }
  return session;
}

function cloneData(data: ControlCompassPageData, workspaceId: string): ControlCompassPageData {
  return {
    ...data,
    workspaceId,
    safety: { ...data.safety },
    kpi: { ...data.kpi },
    governanceDomains: data.governanceDomains.map((domain) => ({ ...domain })),
    selectedDomain: {
      ...data.selectedDomain,
      currentValue: { ...data.selectedDomain.currentValue },
      suggestedValue: { ...data.selectedDomain.suggestedValue },
      impactScope: {
        ...data.selectedDomain.impactScope,
        affectedPages: [...data.selectedDomain.impactScope.affectedPages]
      },
      validationStatus: { ...data.selectedDomain.validationStatus },
      auditStatus: { ...data.selectedDomain.auditStatus }
    },
    sandbox: {
      draft: { ...data.sandbox.draft },
      impact: { ...data.sandbox.impact },
      risk: { ...data.sandbox.risk, varianceRange: [...data.sandbox.risk.varianceRange] as [number, number] },
      paperValidation: { ...data.sandbox.paperValidation },
      humanReview: { ...data.sandbox.humanReview }
    },
    ruling: {
      draftId: data.ruling.draftId,
      evidenceChain: { ...data.ruling.evidenceChain },
      expertReview: { ...data.ruling.expertReview },
      auditResult: { ...data.ruling.auditResult },
      rulingStatus: { ...data.ruling.rulingStatus }
    },
    optimizationSummary: { ...data.optimizationSummary },
    parameterFamilies: data.parameterFamilies.map((family) => ({ ...family })),
    calibrationDisputes: data.calibrationDisputes.map((dispute) => ({ ...dispute })),
    derivationPanel: {
      dashboard: { ...data.derivationPanel.dashboard },
      riftAlerts: data.derivationPanel.riftAlerts.map((alert) => ({
        ...alert,
        affectedDomainIds: [...alert.affectedDomainIds]
      })),
      seals: data.derivationPanel.seals.map((seal) => ({
        ...seal,
        targetDomainIds: [...seal.targetDomainIds]
      }))
    },
    todos: data.todos.map((todo) => ({ ...todo })),
    systemStatus: { ...data.systemStatus }
  };
}

function getBackendControlCompassPacketUrl(): string | null {
  const configured = import.meta.env.VITE_ZMATRIX_CONTROL_COMPASS_PACKET_URL as string | undefined;
  if (configured) {
    return configured;
  }
  if (import.meta.env.MODE === "test" || typeof window === "undefined" || typeof fetch !== "function") {
    return null;
  }
  return "/api/cockpit/control_compass_packet.json";
}

async function loadBackendControlCompassPacket(workspaceId: string): Promise<ControlCompassPageData | null> {
  const packetUrl = getBackendControlCompassPacketUrl();
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
    const packet = (await response.json()) as ControlCompassPageData;
    if (packet.workspaceId !== workspaceId) {
      return null;
    }
    return packet;
  } catch {
    return null;
  }
}

export async function getControlCompassPageData(session: AuthSession | null): Promise<ControlCompassPageData> {
  const current = requireSession(session);
  const backendPacket = await loadBackendControlCompassPacket(current.workspaceId);
  if (backendPacket) {
    return cloneData(backendPacket, current.workspaceId);
  }
  if (current.workspaceId === "ws_personal_z_prime") {
    return cloneData(compassMock, current.workspaceId);
  }
  return {
    ...cloneData(compassMock, current.workspaceId),
    kpi: {
      ...compassMock.kpi,
      healthyDomainCount: 0,
      healthScore: 0,
      latestPaperHitRatePct: 0,
      weakenedSignalCount: 0,
      pendingAdjudicationCount: 0,
      optimizationSnapshotStatus: "MISSING",
      pendingChangeCount: 0,
      blockedChangeCount: 0,
      monthlyInternalizationPct: 0,
      auditCompletenessPct: 0,
      dataFreshness: "PARTIAL"
    },
    governanceDomains: compassMock.governanceDomains.map((domain) => ({
      ...domain,
      status: "PENDING_APPROVAL",
      pendingChanges: 0,
      lastReviewedAt: "等待本档案治理数据导入"
    })),
    todos: [{ todoId: "todo-empty", sourceType: "PARAMETER_CHANGE", priority: "LOW", title: "等待治理数据导入", status: "PENDING" }]
  };
}

export async function createControlCompassActionDraft(
  session: AuthSession | null,
  action: ControlCompassActionDraft["action"],
  payload: Record<string, unknown>
): Promise<ControlCompassActionDraft> {
  const current = requireSession(session);
  ensureNoClientTenantFields(payload);
  const auditEvent =
    action === "导出审计包"
      ? "EXPORT_CONTROL_COMPASS_AUDIT_PACK"
      : action === "恢复系统自优化结果"
        ? "RESTORE_SYSTEM_OPTIMIZATION_DRAFT"
        : action === "创建校准草案"
          ? "CREATE_CALIBRATION_PARAMETER_DRAFT"
          : action === "发起人审提交"
            ? "SUBMIT_CONTROL_COMPASS_PROPOSAL_REVIEW"
            : action === "放弃草案"
              ? "DEFER_CONTROL_COMPASS_DRAFT"
              : "CREATE_CONTROL_COMPASS_REVIEW_DRAFT";
  const response = await createWorkspaceDraft(current, payload, auditEvent);
  return {
    draftId: `control-compass-draft-${Date.now()}`,
    workspaceId: response.workspaceId,
    action,
    status: action === "导出审计包" ? "AUDIT_PACK_READY" : action === "打开衍算手工工具箱" ? "REFERENCE_SAVED" : "DRAFT_CREATED",
    humanReviewRequired: true,
    auditEvent: response.auditEvent,
    userMessage:
      action === "导出审计包"
        ? "天机罗盘审计包已准备，等待人工确认。"
        : action === "恢复系统自优化结果"
          ? "系统自优化恢复草案已生成，等待人审与审计。"
          : action === "创建校准草案"
            ? "参数校准草案已生成，已保留自优化快照。"
            : action === "发起人审提交"
              ? "人审提案草案已生成，等待你确认提交。"
              : action === "放弃草案"
                ? "已记录放弃草案决定，保留审计轨迹。"
                : action === "打开衍算手工工具箱"
                  ? "衍算手工工具箱入口已打开为只读草案。"
                  : "参数复核草案已生成，等待人工确认。"
  };
}
