import type { AuthSession } from "../auth";
import { createWorkspaceDraft, ensureNoClientTenantFields, MockApiError } from "./mockApi";

export type HermesPageId = "holdings" | "selection" | "dayan" | "compass" | "history" | "settings" | "profile";

export type HermesSafetyBoundary = {
  paperOnly: true;
  humanReviewRequired: true;
  brokerRuntime: "BLOCKED";
  realTrade: "BLOCKED";
  dataScope: "WORKSPACE_SCOPED";
  directMemoryWrite: "BLOCKED";
  directRuleEnable: "BLOCKED";
  directParameterApply: "BLOCKED";
  skillRegistryMutation: "BLOCKED";
};

export type HermesPageContext = {
  pageId: HermesPageId;
  selectedEntity?: string;
  pageSnapshot: string;
  availableActions: string[];
  safetyBoundary: HermesSafetyBoundary;
};

export type HermesAdvisoryPacket = {
  advisoryId: string;
  workspaceId: string;
  pageId: HermesPageId;
  title: "童子谏言";
  status: "常驻" | "等待输入" | "编排中";
  contextSummary: string;
  riskPosture: "稳定" | "待复核" | "待校准" | "待清理";
  missingInputs: string[];
  promptSeeds: string[];
  recommendedActions: string[];
  pageContext: HermesPageContext;
};

export type HermesChatRequest = {
  pageId: HermesPageId;
  question: string;
  selectedEntity?: string;
  pageSnapshot?: string;
};

export type HermesActionRequest = {
  pageId: HermesPageId;
  actionLabel: string;
  selectedEntity?: string;
  pageSnapshot?: string;
};

export type HermesChatResponse = {
  responseId: string;
  workspaceId: string;
  answer: string;
  suggestedNextQuestions: string[];
  draftAction?: string;
  handoffTarget?: "/dayan-ask";
  humanReviewRequired: true;
  auditEvent: "HERMES_CHAT_DRAFT";
};

export type HermesActionDraft = {
  draftId: string;
  workspaceId: string;
  status: "DRAFT_CREATED" | "AUDIT_PACK_READY" | "REFERENCE_SAVED";
  humanReviewRequired: true;
  auditEvent: "CREATE_HERMES_ACTION_DRAFT" | "EXPORT_HERMES_AUDIT_PACK" | "SAVE_HERMES_REFERENCE";
  userMessage: string;
};

const safetyBoundary: HermesSafetyBoundary = {
  paperOnly: true,
  humanReviewRequired: true,
  brokerRuntime: "BLOCKED",
  realTrade: "BLOCKED",
  dataScope: "WORKSPACE_SCOPED",
  directMemoryWrite: "BLOCKED",
  directRuleEnable: "BLOCKED",
  directParameterApply: "BLOCKED",
  skillRegistryMutation: "BLOCKED"
};

const advisoryCopy: Record<
  HermesPageId,
  Omit<HermesAdvisoryPacket, "workspaceId" | "pageContext"> & {
    pageSnapshot: string;
    availableActions: string[];
  }
> = {
  holdings: {
    advisoryId: "hermes-holdings",
    pageId: "holdings",
    title: "童子谏言",
    status: "常驻",
    contextSummary: "正式仓里紫金矿业与双环传动仍需复核，现金比例偏低，先确认原研究判断是否仍成立。",
    riskPosture: "待复核",
    missingInputs: ["原研究判断", "最新催化变化", "可承受回撤区间"],
    promptSeeds: [
      "当前持仓最需要复核的风险是什么？",
      "为什么这只持仓被标记为风险复核？",
      "帮我生成一份持仓复核草案。",
      "把这只持仓带入大衍天问继续研究。"
    ],
    recommendedActions: ["生成持仓复核草案", "创建人工研究记录", "导出审计包"],
    pageSnapshot: "总资产 110,249.84；浮动盈亏 -4,776.77；正式持仓 3 只。",
    availableActions: ["答疑解释", "持仓复核草案", "人工研究记录草案", "审计包"]
  },
  selection: {
    advisoryId: "hermes-selection",
    pageId: "selection",
    title: "童子谏言",
    status: "常驻",
    contextSummary: "候选池已完成七层过滤，当前重点是解释 B/R/D 分流后的证据缺口与研究优先级。",
    riskPosture: "待复核",
    missingInputs: ["目标研究方向", "候选时间窗", "重点行业约束"],
    promptSeeds: [
      "当前候选池最大的筛选瓶颈是什么？",
      "B/R/D 三类候选分别适合怎么继续研究？",
      "为什么这个候选进入高优先级？",
      "生成候选研究草案。"
    ],
    recommendedActions: ["候选研究草案", "候选对比说明", "加入观察记录"],
    pageSnapshot: "范围覆盖 5,281；初筛候选 612；高优先级 128；集合分流 38 / 55 / 35。",
    availableActions: ["答疑解释", "候选研究草案", "观察记录草案", "大衍天问交接"]
  },
  dayan: {
    advisoryId: "hermes-dayan",
    pageId: "dayan",
    title: "童子谏言",
    status: "编排中",
    contextSummary: "当前主题偏宽，建议先收窄目标、选择法阵，再把结果送入落子复盘等待人审。",
    riskPosture: "待复核",
    missingInputs: ["时间区间", "标的范围", "输出目标"],
    promptSeeds: [
      "我应该先选哪个法阵？",
      "这个研究问题还缺什么约束？",
      "帮我组合一条研究链路。",
      "把这次问答沉淀成我的法门草案。"
    ],
    recommendedActions: ["生成链路草案", "保存我的法门草案", "导出审计包"],
    pageSnapshot: "可召法门 104；领域 17；最高边界为草案。",
    availableActions: ["答疑解释", "研究链路草案", "法门草案", "审计包"]
  },
  compass: {
    advisoryId: "hermes-compass",
    pageId: "compass",
    title: "童子谏言",
    status: "常驻",
    contextSummary: "主干量化参数盘里催化周期门与因子信号门待校准，调整前应先确认快照保护。",
    riskPosture: "待校准",
    missingInputs: ["当前参数族", "最近复核证据", "快照编号"],
    promptSeeds: [
      "当前哪个量化参数域最需要人工裁定？",
      "催化周期门为什么待校准？",
      "调整这个参数前需要备份什么？",
      "生成参数校准草案。"
    ],
    recommendedActions: ["参数校准草案", "快照保护检查", "查看审计链"],
    pageSnapshot: "系统健康 82；成功复盘 87.3%；参数分歧 6 项；快照已备份。",
    availableActions: ["答疑解释", "参数校准草案", "快照恢复参考", "审计包"]
  },
  history: {
    advisoryId: "hermes-history",
    pageId: "history",
    title: "童子谏言",
    status: "常驻",
    contextSummary: "时空回溯已有报告、案例与记忆沉淀，当前重点是清理过期记忆和验证规则候选。",
    riskPosture: "待清理",
    missingInputs: ["待复盘事件", "证据链", "沉淀目标"],
    promptSeeds: [
      "哪些历史记忆已经过期或需要清理？",
      "哪些复盘结论可以转成规则候选？",
      "这条历史事件的证据链是否完整？",
      "生成复盘草案。"
    ],
    recommendedActions: ["生成复盘草案", "标记待清理草案", "规则候选草案"],
    pageSnapshot: "累计报告 1,268；实盘案例 842；系统记忆 3,264；规则候选 156。",
    availableActions: ["答疑解释", "复盘草案", "记忆清理草案", "规则候选草案"]
  },
  settings: {
    advisoryId: "hermes-settings",
    pageId: "settings",
    title: "童子谏言",
    status: "常驻",
    contextSummary: "系统设置页重点检查数据源、租户隔离与安全锁；密钥只保存引用，不回显明文。",
    riskPosture: "稳定",
    missingInputs: ["数据源名称", "测试目标", "变更原因"],
    promptSeeds: [
      "当前数据源是否健康？",
      "Tushare token 测试结果怎么解读？",
      "当前用户隔离和安全锁状态如何？",
      "生成配置变更审计草案。"
    ],
    recommendedActions: ["测试数据源", "配置变更草案", "导出审计包"],
    pageSnapshot: "Tushare 可配置；安全锁已锁定；当前 workspace 独立。",
    availableActions: ["答疑解释", "数据源测试参考", "配置草案", "审计包"]
  },
  profile: {
    advisoryId: "hermes-profile",
    pageId: "profile",
    title: "童子谏言",
    status: "常驻",
    contextSummary: "操盘者画像只做个人复盘与纪律提醒，适合记录偏差、复核节奏和生成反思草案。",
    riskPosture: "稳定",
    missingInputs: ["近期决策记录", "复盘对象", "纪律约束"],
    promptSeeds: [
      "我最近的决策偏差是什么？",
      "哪些行为需要纪律复核？",
      "生成一份个人复盘草案。",
      "把这条反思记录加入人工研究记录。"
    ],
    recommendedActions: ["个人复盘草案", "纪律复核记录", "人工研究记录草案"],
    pageSnapshot: "Z-Prime 稳健成长型；中长为主；纪律优先。",
    availableActions: ["答疑解释", "个人复盘草案", "纪律记录草案", "研究记录草案"]
  }
};

function requireSession(session: AuthSession | null): AuthSession {
  if (!session) {
    throw new MockApiError("AUTH_REQUIRED", "hermes advisory api requires authenticated session");
  }
  return session;
}

function clonePacket(packet: HermesAdvisoryPacket): HermesAdvisoryPacket {
  return {
    ...packet,
    missingInputs: [...packet.missingInputs],
    promptSeeds: [...packet.promptSeeds],
    recommendedActions: [...packet.recommendedActions],
    pageContext: {
      ...packet.pageContext,
      availableActions: [...packet.pageContext.availableActions],
      safetyBoundary: { ...packet.pageContext.safetyBoundary }
    }
  };
}

function buildAnswer(pageId: HermesPageId, question: string, snapshot?: string) {
  const packet = advisoryCopy[pageId];
  const usesDraft = /草案|生成|记录|审计|校准|复盘|研究链路|法门/.test(question);
  const base = `${packet.contextSummary} 你可以先补齐「${packet.missingInputs[0]}」，再选择「${packet.recommendedActions[0]}」。`;
  const scope = snapshot ? `我已按当前页面摘要读取：${snapshot}` : `当前页面摘要：${packet.pageSnapshot}`;
  return {
    answer: `${base} ${scope} 全部结果只进入待确认草案或审计引用。`,
    draftAction: usesDraft ? packet.recommendedActions[0] : undefined,
    suggestedNextQuestions: packet.promptSeeds.slice(0, 3)
  };
}

export async function getHermesAdvisoryPacket(session: AuthSession | null, pageId: HermesPageId): Promise<HermesAdvisoryPacket> {
  const current = requireSession(session);
  const copy = advisoryCopy[pageId];

  return clonePacket({
    ...copy,
    workspaceId: current.workspaceId,
    pageContext: {
      pageId,
      pageSnapshot: copy.pageSnapshot,
      availableActions: [...copy.availableActions],
      safetyBoundary
    }
  });
}

export async function createHermesChatResponse(
  session: AuthSession | null,
  request: HermesChatRequest
): Promise<HermesChatResponse> {
  const current = requireSession(session);
  ensureNoClientTenantFields(request as unknown as Record<string, unknown>);

  const answer = buildAnswer(request.pageId, request.question, request.pageSnapshot);
  const response = await createWorkspaceDraft(
    current,
    {
      pageId: request.pageId,
      question: request.question,
      selectedEntity: request.selectedEntity,
      pageSnapshot: request.pageSnapshot
    },
    "HERMES_CHAT_DRAFT"
  );

  return {
    responseId: `hermes-chat-${Date.now()}`,
    workspaceId: response.workspaceId,
    answer: answer.answer,
    suggestedNextQuestions: answer.suggestedNextQuestions,
    draftAction: answer.draftAction,
    handoffTarget: "/dayan-ask",
    humanReviewRequired: true,
    auditEvent: "HERMES_CHAT_DRAFT"
  };
}

export async function createHermesActionDraft(
  session: AuthSession | null,
  request: HermesActionRequest
): Promise<HermesActionDraft> {
  const current = requireSession(session);
  ensureNoClientTenantFields(request as unknown as Record<string, unknown>);

  const isAudit = request.actionLabel.includes("审计");
  const isReference = request.actionLabel.includes("大衍天问");
  const auditEvent = isAudit ? "EXPORT_HERMES_AUDIT_PACK" : isReference ? "SAVE_HERMES_REFERENCE" : "CREATE_HERMES_ACTION_DRAFT";
  const response = await createWorkspaceDraft(current, request as unknown as Record<string, unknown>, auditEvent);

  return {
    draftId: `hermes-action-${Date.now()}`,
    workspaceId: response.workspaceId,
    status: isAudit ? "AUDIT_PACK_READY" : isReference ? "REFERENCE_SAVED" : "DRAFT_CREATED",
    humanReviewRequired: true,
    auditEvent,
    userMessage: isAudit ? "童子已准备审计包，等待人工确认。" : "童子已生成待确认草案，不进入正式库。"
  };
}
