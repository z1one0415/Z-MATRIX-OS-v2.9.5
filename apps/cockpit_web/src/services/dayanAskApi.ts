import type { AuthSession } from "../auth";
import { createWorkspaceDraft, ensureNoClientTenantFields, MockApiError } from "./mockApi";

export type DayanSafety = {
  paperOnly: true;
  humanReviewRequired: true;
  brokerRuntime: "BLOCKED";
  realTrade: "BLOCKED";
  productionAllowed: false;
  agentDirectMutationAllowed: false;
  registryDirectMutationAllowed: false;
  memoryDirectWriteAllowed: false;
  ruleDirectEnableAllowed: false;
  dataScope: "WORKSPACE_SCOPED";
};

export type SafetyLevel = "READ_ONLY" | "DRAFT_ONLY" | "PROPOSAL_REQUIRED" | "FORBIDDEN";
export type AskMode = "FREE_ASK" | "DEEP_RESEARCH" | "COMMIT_MODE";
export type ResearchScope = "ALL_MARKET" | "CURRENT_HOLDINGS" | "WATCHLIST" | "SINGLE_STOCK" | "CHAIN";
export type MemoryContext = "NONE" | "SHORT_MEMORY" | "LONG_MEMORY" | "FULL_MEMORY";

export type AskAltarState = {
  mode: AskMode;
  modeLabel: string;
  currentTopic: string;
  researchScope: ResearchScope;
  researchScopeLabel: string;
  memoryContext: MemoryContext;
  memoryContextLabel: string;
  safety: DayanSafety;
};

export type AskFormation = {
  id: string;
  name: string;
  description: string;
  promptTemplate: string;
  composedSkillIds: string[];
  safetyLevel: SafetyLevel;
};

export type AskSkill = {
  id: string;
  userVisibleName: string;
  description: string;
  promptTemplate: string;
  outputType: "CHAT" | "REPORT_DRAFT" | "CASE_DRAFT" | "MEMORY_DRAFT" | "RULE_DRAFT" | "PARAMETER_DRAFT" | "AUDIT_CHECK";
  safetyLevel: SafetyLevel;
  requiredInputs: string[];
  backendBinding: {
    registrySkillIds: string[];
    domain: string;
    operation: string;
  };
};

export type AskSkillCategory = {
  id: string;
  name: string;
  description: string;
  skillCount: number;
  safetyLevel: SafetyLevel;
  skills: AskSkill[];
};

export type HermesGuidance = {
  guidanceId: string;
  contextSummary: string;
  suggestions: string[];
  missingInputs: string[];
  recommendedMethods: string[];
  quickQuestions: string[];
  nextActionText: string;
  hermesStatus: "常驻" | "等待输入" | "编排中";
};

export type HermesPlan = {
  planId: string;
  userGoal: string;
  interpretedTask: string;
  recommendedMethods: string[];
  executionSteps: Array<{
    order: number;
    actionName: string;
    userVisiblePurpose: string;
    requiredInput: string[];
    expectedOutput: string;
  }>;
  missingInputs: string[];
  outputTarget: Array<"CHAT_ONLY" | "REPORT_DRAFT" | "CASE_DRAFT" | "MEMORY_DRAFT" | "RULE_DRAFT" | "PARAMETER_DRAFT" | "AUDIT_CHECK">;
  humanReviewRequired: true;
};

export type AdvisoryGroup = {
  id: string;
  title: string;
  description: string;
  entries: string[];
};

export type MethodForgeCandidate = {
  id: string;
  suggestedName: string;
  sourceCombination: string[];
  usageCount: number;
  scenario: string;
  status: "RECOMMENDED" | "NAMING" | "TESTING" | "READY_TO_ADD" | "ADDED" | "IGNORED";
  safetyLevel: SafetyLevel;
};

export type MyMethod = {
  id: string;
  name: string;
  scenario: string;
  promptTemplate: string;
  composedSkills: string[];
  status: "ACTIVE" | "TESTING" | "ARCHIVED";
  lastUsedAt: string;
  usageCount: number;
};

export type MoveReviewItem = {
  id: string;
  date: string;
  researchTopic: string;
  methodCombination: string;
  conclusion: string;
  memoryStatus: "已沉淀" | "待人审" | "仅对话";
};

export type AskMessage = {
  id: string;
  role: "USER" | "HERMES" | "SYSTEM";
  label: "你" | "问天" | "系统";
  content: string;
  createdAt: string;
};

export type AskConversation = {
  conversationId: string;
  topic: string;
  selectedPromptFragments: string[];
  messages: AskMessage[];
};

export type AgentBridgeIntent = {
  id: string;
  label: string;
  output_target: "CHAT_ONLY" | "REPORT_DRAFT" | "AUDIT_CHECK";
  requires_review: boolean;
};

export type AgentBridgeStatus = {
  status: "Z_MATRIX_AGENT_BRIDGE_READY" | "Z_MATRIX_AGENT_BRIDGE_DEGRADED";
  workspace_id: string;
  generated_at: string;
  default_agent: "Hermes";
  interaction_mode: "NATURAL_LANGUAGE_RESEARCH_DRAFT";
  llm_runtime: {
    provider: "ENV_CONFIGURED_BY_USER";
    key_material: "ENV_ONLY";
    response_storage: "DRAFT_LAYER_ONLY";
    external_call_from_backend: "DISABLED_BY_DEFAULT";
  };
  registry: {
    ready: boolean;
    skill_count: number;
    domain_count: number;
    concrete_skill_count: number;
  };
  allowed_intents: AgentBridgeIntent[];
  routing: {
    max_risk_level: "R2_DRAFT";
    proposal_required: boolean;
    human_review_required: boolean;
    direct_command_runtime: "BLOCKED";
    formal_memory_write: "BLOCKED";
    rule_enable: "BLOCKED";
    broker_runtime: "BLOCKED";
    real_trade: "BLOCKED";
  };
  safety: {
    alpha_claim: "BLOCKED";
    promotion: "BLOCKED";
    broker_runtime: "BLOCKED";
    real_trade: "BLOCKED";
    direct_command_runtime: "BLOCKED";
    formal_memory_write: "BLOCKED";
    requires_user_confirmation: boolean;
  };
};

export type AgentResearchDraftPacket = {
  status: "Z_MATRIX_AGENT_DRAFT_READY" | "Z_MATRIX_AGENT_DRAFT_REJECTED";
  workspace_id: string;
  draft_id: string;
  default_agent: "Hermes";
  intent_id: string;
  intent_label: string;
  question_summary: string;
  answer: string;
  user_message: string;
  suggested_next_steps: string[];
  draft_layers: string[];
  selected_fragments: string[];
  human_review_required: true;
  proposal_required: true;
  rejection_reasons?: string[];
  safety: {
    alpha_claim: "BLOCKED";
    promotion: "BLOCKED";
    broker_runtime: "BLOCKED";
    real_trade: "BLOCKED";
    direct_command_runtime: "BLOCKED";
    formal_memory_write: "BLOCKED";
  };
};

export type DayanAction =
  | "插入法门"
  | "生成链路草案"
  | "仅生成草案"
  | "创建法门草案"
  | "保存我的法门草案"
  | "试运行草案"
  | "加入我的法门草案"
  | "忽略熔炼候选"
  | "导出审计包"
  | "清空对话";

export type DayanActionDraft = {
  draftId: string;
  workspaceId: string;
  action: DayanAction;
  status: "DRAFT_CREATED" | "AUDIT_PACK_READY" | "REFERENCE_SAVED" | "DRAFT_REJECTED";
  humanReviewRequired: true;
  auditEvent: string;
  userMessage: string;
  answer?: string;
  intentId?: string;
  suggestedNextSteps?: string[];
};

export type DayanAskPageData = {
  workspaceId: string;
  asOf: string;
  safety: DayanSafety;
  altar: AskAltarState;
  formations: AskFormation[];
  hermesGuidance: HermesGuidance;
  advisoryGroups: AdvisoryGroup[];
  forgeCandidates: MethodForgeCandidate[];
  moveReview: MoveReviewItem[];
  myMethods: MyMethod[];
  skillCategories: AskSkillCategory[];
  currentConversation: AskConversation;
  latestHermesPlan: HermesPlan;
  voice: {
    state: "READY" | "UNAVAILABLE";
    label: string;
    privacyNote: string;
  };
  systemStatus: {
    registeredMethodCount: number;
    concreteDomainCount: number;
    maxRiskLevel: "R2_DRAFT";
    workflowMode: "DRY_RUN_ONLY";
    registryMutation: "BLOCKED";
  };
  agentBridge: AgentBridgeStatus;
  backendMapping: {
    registry: "skill_registry.generated.json";
    contracts: "skill_contract_registry.json";
    invocation: "invoke_skill(command_envelope, context_slice)";
    workflow: "WORKFLOW.RUN_RESEARCH_DRY_CHAIN";
    approval: "Proposal/Human Review";
  };
};

const safety: DayanSafety = {
  paperOnly: true,
  humanReviewRequired: true,
  brokerRuntime: "BLOCKED",
  realTrade: "BLOCKED",
  productionAllowed: false,
  agentDirectMutationAllowed: false,
  registryDirectMutationAllowed: false,
  memoryDirectWriteAllowed: false,
  ruleDirectEnableAllowed: false,
  dataScope: "WORKSPACE_SCOPED"
};

const defaultAgentBridgeStatus: AgentBridgeStatus = {
  status: "Z_MATRIX_AGENT_BRIDGE_DEGRADED",
  workspace_id: "ws_personal_z_prime",
  generated_at: "",
  default_agent: "Hermes",
  interaction_mode: "NATURAL_LANGUAGE_RESEARCH_DRAFT",
  llm_runtime: {
    provider: "ENV_CONFIGURED_BY_USER",
    key_material: "ENV_ONLY",
    response_storage: "DRAFT_LAYER_ONLY",
    external_call_from_backend: "DISABLED_BY_DEFAULT"
  },
  registry: {
    ready: false,
    skill_count: 0,
    domain_count: 0,
    concrete_skill_count: 0
  },
  allowed_intents: [
    { id: "explain-system-status", label: "解释系统状态", output_target: "CHAT_ONLY", requires_review: false },
    { id: "build-research-chain-draft", label: "研究链路草案", output_target: "REPORT_DRAFT", requires_review: true },
    { id: "prepare-audit-reference", label: "审计引用整理", output_target: "AUDIT_CHECK", requires_review: true }
  ],
  routing: {
    max_risk_level: "R2_DRAFT",
    proposal_required: true,
    human_review_required: true,
    direct_command_runtime: "BLOCKED",
    formal_memory_write: "BLOCKED",
    rule_enable: "BLOCKED",
    broker_runtime: "BLOCKED",
    real_trade: "BLOCKED"
  },
  safety: {
    alpha_claim: "BLOCKED",
    promotion: "BLOCKED",
    broker_runtime: "BLOCKED",
    real_trade: "BLOCKED",
    direct_command_runtime: "BLOCKED",
    formal_memory_write: "BLOCKED",
    requires_user_confirmation: true
  }
};

const skillCategories: AskSkillCategory[] = [
  {
    id: "holding-diagnosis",
    name: "持仓问诊",
    description: "账户观察、正式仓体检与逆风复核",
    skillCount: 10,
    safetyLevel: "DRAFT_ONLY",
    skills: [
      {
        id: "holding-wind",
        userVisibleName: "今日持仓风向",
        description: "整理当前持仓顺逆风与待确认点",
        promptTemplate: "请检查当前持仓的顺逆风变化，只输出观察与待确认事项。",
        outputType: "CHAT",
        safetyLevel: "READ_ONLY",
        requiredInputs: ["当前持仓"],
        backendBinding: { registrySkillIds: ["PORTFOLIO.GET_EXPOSURE_TEMPLATE"], domain: "PORTFOLIO", operation: "read_exposure" }
      },
      {
        id: "holding-review",
        userVisibleName: "正式仓体检",
        description: "生成持仓复核草案",
        promptTemplate: "请对正式仓进行复核，重点列出原判断是否仍成立，并生成待确认草案。",
        outputType: "REPORT_DRAFT",
        safetyLevel: "PROPOSAL_REQUIRED",
        requiredInputs: ["当前持仓", "原研究判断"],
        backendBinding: { registrySkillIds: ["PORTFOLIO.BUILD_PORTFOLIO_REVIEW_DRAFT"], domain: "PORTFOLIO", operation: "build_review_draft" }
      }
    ]
  },
  {
    id: "stock-selection",
    name: "选股问策",
    description: "全市场扫描、七层筛选与候选分拣",
    skillCount: 11,
    safetyLevel: "DRAFT_ONLY",
    skills: [
      {
        id: "market-scan",
        userVisibleName: "全市场扫描",
        description: "生成纸面候选池观察",
        promptTemplate: "请从全市场扫描适合继续研究的方向，只输出纸面观察清单。",
        outputType: "REPORT_DRAFT",
        safetyLevel: "DRAFT_ONLY",
        requiredInputs: ["研究范围", "观察周期"],
        backendBinding: { registrySkillIds: ["WORKFLOW.BUILD_RESEARCH_PLAN_DRAFT"], domain: "WORKFLOW", operation: "build_plan_draft" }
      }
    ]
  },
  {
    id: "catalyst",
    name: "催化问因",
    description: "催化强度、残值、退潮与真假信号",
    skillCount: 10,
    safetyLevel: "DRAFT_ONLY",
    skills: [
      {
        id: "catalyst-check",
        userVisibleName: "催化体检",
        description: "判断事件是否仍有研究价值",
        promptTemplate: "请检查目标的催化是否仍有效，区分新增信息、旧催化衰减与待确认风险。",
        outputType: "CHAT",
        safetyLevel: "READ_ONLY",
        requiredInputs: ["目标", "事件线索"],
        backendBinding: { registrySkillIds: ["ZC35.BUILD_REVIEW_DRAFT"], domain: "ZC35", operation: "build_review_draft" }
      }
    ]
  },
  {
    id: "chain-research",
    name: "链上研判",
    description: "产业链位置、价值捕获与风险传导",
    skillCount: 10,
    safetyLevel: "DRAFT_ONLY",
    skills: [
      {
        id: "chain-map",
        userVisibleName: "产业链定位",
        description: "梳理上下游与核心环节",
        promptTemplate: "请梳理目标所在产业链的位置、价值捕获环节与风险传导路径。",
        outputType: "REPORT_DRAFT",
        safetyLevel: "DRAFT_ONLY",
        requiredInputs: ["目标", "产业链"],
        backendBinding: { registrySkillIds: ["RESEARCHDB.BUILD_RESEARCH_RECORD_DRAFT"], domain: "RESEARCHDB", operation: "build_record_draft" }
      }
    ]
  },
  {
    id: "advisory",
    name: "天官问策",
    description: "会审、反方、缺口与高风险复核",
    skillCount: 18,
    safetyLevel: "PROPOSAL_REQUIRED",
    skills: [
      {
        id: "council-review",
        userVisibleName: "全席会审",
        description: "生成多专家复核草案",
        promptTemplate: "请组织多角度会审，输出核心共识、分歧与证据缺口。",
        outputType: "REPORT_DRAFT",
        safetyLevel: "PROPOSAL_REQUIRED",
        requiredInputs: ["研究主题", "证据材料"],
        backendBinding: { registrySkillIds: ["COUNCIL.BUILD_EXPERT_REVIEW_DRAFT"], domain: "COUNCIL", operation: "build_expert_review" }
      }
    ]
  },
  {
    id: "history",
    name: "历史问迹",
    description: "相似案例、错失机会与反例检索",
    skillCount: 12,
    safetyLevel: "READ_ONLY",
    skills: [
      {
        id: "similar-cases",
        userVisibleName: "相似案例检索",
        description: "检索历史相似路径",
        promptTemplate: "请检索历史相似案例，比较当时判断、后续表现与可复用经验。",
        outputType: "CHAT",
        safetyLevel: "READ_ONLY",
        requiredInputs: ["研究主题"],
        backendBinding: { registrySkillIds: ["RESEARCHDB.SEARCH_RECORDS_DRY"], domain: "RESEARCHDB", operation: "search_records" }
      }
    ]
  },
  {
    id: "report",
    name: "报告落盘",
    description: "研究报告、审计轨迹与纸面计划",
    skillCount: 10,
    safetyLevel: "PROPOSAL_REQUIRED",
    skills: [
      {
        id: "research-report",
        userVisibleName: "个股深研报告",
        description: "生成报告草案",
        promptTemplate: "请将当前研究链路整理为个股深研报告草案，等待人工确认。",
        outputType: "REPORT_DRAFT",
        safetyLevel: "PROPOSAL_REQUIRED",
        requiredInputs: ["研究链路", "证据材料"],
        backendBinding: { registrySkillIds: ["REPORT.RENDER_CASEFORGE_REVIEW_DRAFT"], domain: "REPORT", operation: "render_report_draft" }
      }
    ]
  },
  {
    id: "case-replay",
    name: "案例复盘",
    description: "成功、失败、错失与行动偏差案例",
    skillCount: 10,
    safetyLevel: "DRAFT_ONLY",
    skills: [
      {
        id: "case-draft",
        userVisibleName: "案例草案",
        description: "形成复盘案例草案",
        promptTemplate: "请将本次研究整理为复盘案例草案，标注证据链和待复核项。",
        outputType: "CASE_DRAFT",
        safetyLevel: "PROPOSAL_REQUIRED",
        requiredInputs: ["研究结果"],
        backendBinding: { registrySkillIds: ["AUTOCASE.BUILD_CASE_CANDIDATE_DRAFT"], domain: "AUTOCASE", operation: "build_case_candidate" }
      }
    ]
  },
  {
    id: "memory",
    name: "记忆沉淀",
    description: "记忆候选、冲突检查与时效复核",
    skillCount: 9,
    safetyLevel: "PROPOSAL_REQUIRED",
    skills: [
      {
        id: "memory-draft",
        userVisibleName: "记忆入库草案",
        description: "生成待确认记忆候选",
        promptTemplate: "请提炼可复用经验，生成记忆候选草案，不写入正式库。",
        outputType: "MEMORY_DRAFT",
        safetyLevel: "PROPOSAL_REQUIRED",
        requiredInputs: ["研究结论", "证据链"],
        backendBinding: { registrySkillIds: ["MEMORY.BUILD_MONTHLY_MEMORY_CANDIDATE_DRAFT"], domain: "MEMORY", operation: "build_memory_candidate" }
      }
    ]
  },
  {
    id: "rule",
    name: "规则候选",
    description: "候选生成、边界、反例与纸面验证",
    skillCount: 9,
    safetyLevel: "PROPOSAL_REQUIRED",
    skills: [
      {
        id: "rule-draft",
        userVisibleName: "生成规则候选",
        description: "形成待验证规则草案",
        promptTemplate: "请将本次经验转为规则候选草案，列出适用边界和反例。",
        outputType: "RULE_DRAFT",
        safetyLevel: "PROPOSAL_REQUIRED",
        requiredInputs: ["经验结论"],
        backendBinding: { registrySkillIds: ["GOVERNANCE.BUILD_VERIFY_REPORT_DRAFT"], domain: "GOVERNANCE", operation: "build_rule_review" }
      }
    ]
  },
  {
    id: "compass",
    name: "罗盘问治",
    description: "量化参数草案与治理复核入口",
    skillCount: 10,
    safetyLevel: "PROPOSAL_REQUIRED",
    skills: [
      {
        id: "parameter-draft",
        userVisibleName: "参数草案生成",
        description: "送入天机罗盘待审",
        promptTemplate: "请生成参数校准草案，所有变更只进入天机罗盘待审。",
        outputType: "PARAMETER_DRAFT",
        safetyLevel: "PROPOSAL_REQUIRED",
        requiredInputs: ["复盘证据"],
        backendBinding: { registrySkillIds: ["COCKPIT.BUILD_STATUS_DRAFT"], domain: "COCKPIT", operation: "build_parameter_draft" }
      }
    ]
  },
  {
    id: "audit",
    name: "审计护法",
    description: "证据链、风险旗标与审计包导出",
    skillCount: 10,
    safetyLevel: "READ_ONLY",
    skills: [
      {
        id: "audit-pack",
        userVisibleName: "审计包导出",
        description: "整理当前证据链",
        promptTemplate: "请整理当前研究链路审计包，保持只读并等待人工确认。",
        outputType: "AUDIT_CHECK",
        safetyLevel: "READ_ONLY",
        requiredInputs: ["研究链路"],
        backendBinding: { registrySkillIds: ["GOVERNANCE.BUILD_RELEASE_AUDIT_DRAFT"], domain: "GOVERNANCE", operation: "build_audit_draft" }
      }
    ]
  }
];

const zPrimeData: DayanAskPageData = {
  workspaceId: "ws_personal_z_prime",
  asOf: "2026-06-04",
  safety,
  altar: {
    mode: "DEEP_RESEARCH",
    modeLabel: "深度研究模式",
    currentTopic: "AI 驱动下半导体设备国产化机会",
    researchScope: "ALL_MARKET",
    researchScopeLabel: "A股全市场",
    memoryContext: "LONG_MEMORY",
    memoryContextLabel: "长链记忆",
    safety
  },
  formations: [
    { id: "trend-break", name: "趋势破局阵", description: "趋势与拐点", promptTemplate: "请用趋势破局阵拆解当前主题。", composedSkillIds: ["market-scan", "similar-cases"], safetyLevel: "DRAFT_ONLY" },
    { id: "industry", name: "产业洞察阵", description: "产业链与格局", promptTemplate: "请用产业洞察阵梳理产业链格局。", composedSkillIds: ["chain-map", "council-review"], safetyLevel: "DRAFT_ONLY" },
    { id: "value", name: "价值定价阵", description: "估值与安全边际", promptTemplate: "请用价值定价阵评估估值安全边际。", composedSkillIds: ["research-report"], safetyLevel: "PROPOSAL_REQUIRED" },
    { id: "event", name: "事件推演阵", description: "事件与冲击", promptTemplate: "请用事件推演阵判断催化路径。", composedSkillIds: ["catalyst-check"], safetyLevel: "DRAFT_ONLY" },
    { id: "execution", name: "纪律复核阵", description: "纪律与偏差", promptTemplate: "请用纪律复核阵检查研究结论中的行动风险。", composedSkillIds: ["holding-review"], safetyLevel: "PROPOSAL_REQUIRED" },
    { id: "replay", name: "复盘归因阵", description: "复盘与迭代", promptTemplate: "请用复盘归因阵生成可沉淀经验。", composedSkillIds: ["case-draft", "memory-draft"], safetyLevel: "PROPOSAL_REQUIRED" }
  ],
  hermesGuidance: {
    guidanceId: "HG-20260604",
    contextSummary: "当前主题偏宽，建议先明确目标、时间区间、标的范围和约束条件。",
    suggestions: [
      "先说明你要研究的是产业机会、单股风险，还是持仓复核。",
      "可先选择“产业洞察阵”或“趋势破局阵”。",
      "如果需要落盘，请再加入“报告落盘”和“审计护法”。",
      "所有写入动作都会先生成待确认草案。"
    ],
    missingInputs: ["时间区间", "标的范围", "风险约束"],
    recommendedMethods: ["产业洞察阵", "催化体检", "全席会审"],
    quickQuestions: [
      "我应该先选哪个法阵？",
      "这个研究问题还缺什么约束？",
      "帮我组合一条研究链路。",
      "把这次问答沉淀成我的法门草案。"
    ],
    nextActionText: "开始新的研究",
    hermesStatus: "常驻"
  },
  advisoryGroups: [
    { id: "council", title: "十二天官问策", description: "宏观、产业、公司多维推演", entries: ["全席会审", "反方审查", "证据缺口审查"] },
    { id: "catalyst", title: "催化研判", description: "事件强度与传导路径", entries: ["催化体检", "退潮识别", "真假信号"] },
    { id: "industry", title: "产业链研究", description: "上下游格局与演变", entries: ["链主识别", "价值捕获位置", "同链对比"] },
    { id: "execution", title: "纪律复核", description: "纪律可行性与风控检查", entries: ["窗口复核", "流动性复核", "偏差复盘"] }
  ],
  forgeCandidates: [
    {
      id: "forge-001",
      suggestedName: "设备国产化投资框架 v1.0",
      sourceCombination: ["产业洞察阵", "价值定价阵", "审计护法"],
      usageCount: 16,
      scenario: "公司研究",
      status: "READY_TO_ADD",
      safetyLevel: "PROPOSAL_REQUIRED"
    }
  ],
  moveReview: [
    { id: "move-001", date: "2026-06-04", researchTopic: "AI 驱动下设备国产化机会", methodCombination: "产业洞察阵 + 价值定价阵", conclusion: "国产化拐点窗口已出现", memoryStatus: "待人审" },
    { id: "move-002", date: "2026-06-03", researchTopic: "光伏供给侧格局演变", methodCombination: "趋势破局阵 + 复盘归因阵", conclusion: "供给出清进入后半段", memoryStatus: "已沉淀" },
    { id: "move-003", date: "2026-06-02", researchTopic: "创新药出海趋势推演", methodCombination: "催化问因 + 天官问策", conclusion: "关注 BD 与管线兑现", memoryStatus: "已沉淀" }
  ],
  myMethods: [
    { id: "my-001", name: "成长股估值框架", scenario: "公司研究", promptTemplate: "请用成长股估值框架分析目标。", composedSkills: ["价值定价阵", "全席会审"], status: "ACTIVE", lastUsedAt: "2026-06-01", usageCount: 12 },
    { id: "my-002", name: "景气度跟踪模板", scenario: "行业研究", promptTemplate: "请用景气度跟踪模板复核行业。", composedSkills: ["趋势破局阵", "催化体检"], status: "ACTIVE", lastUsedAt: "2026-05-30", usageCount: 9 },
    { id: "my-003", name: "事件影响评估法", scenario: "事件研究", promptTemplate: "请用事件影响评估法整理本次事件。", composedSkills: ["事件推演阵", "审计护法"], status: "TESTING", lastUsedAt: "2026-05-28", usageCount: 5 }
  ],
  skillCategories,
  currentConversation: {
    conversationId: "ask-20260604-001",
    topic: "研究主题：AI 驱动下半导体设备国产化机会",
    selectedPromptFragments: ["产业洞察阵", "价值定价阵"],
    messages: [
      {
        id: "msg-001",
        role: "USER",
        label: "你",
        content: "请分析 AI 驱动下半导体设备国产化的核心机会与关键壁垒，并给出纸面研究框架。",
        createdAt: "09:41"
      },
      {
        id: "msg-002",
        role: "HERMES",
        label: "问天",
        content:
          "已为你构建研究框架：先判断产业链位置，再检查催化是否仍有效，最后用多角度会审识别证据缺口。当前只生成研究草案，不进入正式记忆或规则。",
        createdAt: "09:41"
      }
    ]
  },
  latestHermesPlan: {
    planId: "plan-20260604-001",
    userGoal: "研究半导体设备国产化机会",
    interpretedTask: "产业链机会识别 + 催化有效性检查 + 研究报告草案",
    recommendedMethods: ["产业洞察阵", "催化体检", "全席会审"],
    executionSteps: [
      { order: 1, actionName: "产业链定位", userVisiblePurpose: "确定价值捕获环节", requiredInput: ["产业链范围"], expectedOutput: "产业链位置判断" },
      { order: 2, actionName: "催化体检", userVisiblePurpose: "识别旧催化衰减和新催化", requiredInput: ["事件线索"], expectedOutput: "催化有效性摘要" },
      { order: 3, actionName: "全席会审", userVisiblePurpose: "形成分歧和证据缺口", requiredInput: ["前两步结论"], expectedOutput: "待确认研究草案" }
    ],
    missingInputs: ["标的范围", "观察周期"],
    outputTarget: ["CHAT_ONLY", "REPORT_DRAFT", "AUDIT_CHECK"],
    humanReviewRequired: true
  },
  voice: {
    state: "READY",
    label: "语音输入可用",
    privacyNote: "仅转写到输入框，不上传录音。"
  },
  systemStatus: {
    registeredMethodCount: 104,
    concreteDomainCount: 17,
    maxRiskLevel: "R2_DRAFT",
    workflowMode: "DRY_RUN_ONLY",
    registryMutation: "BLOCKED"
  },
  agentBridge: defaultAgentBridgeStatus,
  backendMapping: {
    registry: "skill_registry.generated.json",
    contracts: "skill_contract_registry.json",
    invocation: "invoke_skill(command_envelope, context_slice)",
    workflow: "WORKFLOW.RUN_RESEARCH_DRY_CHAIN",
    approval: "Proposal/Human Review"
  }
};

function requireSession(session: AuthSession | null): AuthSession {
  if (!session) {
    throw new MockApiError("AUTH_REQUIRED", "dayan ask api requires authenticated session");
  }
  return session;
}

function cloneData(packet: DayanAskPageData, workspaceId: string): DayanAskPageData {
  return {
    ...packet,
    workspaceId,
    safety: { ...packet.safety },
    altar: { ...packet.altar, safety: { ...packet.altar.safety } },
    formations: packet.formations.map((item) => ({ ...item, composedSkillIds: [...item.composedSkillIds] })),
    hermesGuidance: {
      ...packet.hermesGuidance,
      suggestions: [...packet.hermesGuidance.suggestions],
      missingInputs: [...packet.hermesGuidance.missingInputs],
      recommendedMethods: [...packet.hermesGuidance.recommendedMethods],
      quickQuestions: [...packet.hermesGuidance.quickQuestions]
    },
    advisoryGroups: packet.advisoryGroups.map((group) => ({ ...group, entries: [...group.entries] })),
    forgeCandidates: packet.forgeCandidates.map((item) => ({ ...item, sourceCombination: [...item.sourceCombination] })),
    moveReview: packet.moveReview.map((item) => ({ ...item })),
    myMethods: packet.myMethods.map((item) => ({ ...item, composedSkills: [...item.composedSkills] })),
    skillCategories: packet.skillCategories.map((category) => ({
      ...category,
      skills: category.skills.map((skill) => ({
        ...skill,
        requiredInputs: [...skill.requiredInputs],
        backendBinding: {
          ...skill.backendBinding,
          registrySkillIds: [...skill.backendBinding.registrySkillIds]
        }
      }))
    })),
    currentConversation: {
      ...packet.currentConversation,
      selectedPromptFragments: [...packet.currentConversation.selectedPromptFragments],
      messages: packet.currentConversation.messages.map((message) => ({ ...message }))
    },
    latestHermesPlan: {
      ...packet.latestHermesPlan,
      recommendedMethods: [...packet.latestHermesPlan.recommendedMethods],
      missingInputs: [...packet.latestHermesPlan.missingInputs],
      outputTarget: [...packet.latestHermesPlan.outputTarget],
      executionSteps: packet.latestHermesPlan.executionSteps.map((step) => ({ ...step, requiredInput: [...step.requiredInput] }))
    },
    voice: { ...packet.voice },
    systemStatus: { ...packet.systemStatus },
    agentBridge: cloneAgentBridge(packet.agentBridge ?? defaultAgentBridgeStatus, workspaceId),
    backendMapping: { ...packet.backendMapping }
  };
}

function cloneAgentBridge(packet: AgentBridgeStatus, workspaceId: string): AgentBridgeStatus {
  return {
    ...packet,
    workspace_id: workspaceId,
    llm_runtime: { ...packet.llm_runtime },
    registry: { ...packet.registry },
    allowed_intents: packet.allowed_intents.map((intent) => ({ ...intent })),
    routing: { ...packet.routing },
    safety: { ...packet.safety }
  };
}

function getBackendDayanAskPacketUrl(): string | null {
  const configured = import.meta.env.VITE_ZMATRIX_DAYAN_ASK_PACKET_URL as string | undefined;
  if (configured) {
    return configured;
  }
  if (import.meta.env.MODE === "test" || typeof window === "undefined" || typeof fetch !== "function") {
    return null;
  }
  return "/api/cockpit/dayan_ask_packet.json";
}

function getAgentBridgeUrl(): string | null {
  const configured = import.meta.env.VITE_ZMATRIX_AGENT_BRIDGE_URL as string | undefined;
  if (configured) {
    return configured;
  }
  if (import.meta.env.MODE === "test" || typeof window === "undefined" || typeof fetch !== "function") {
    return null;
  }
  return "/api/product/agent_bridge.json";
}

function getAgentDraftUrl(): string | null {
  const configured = import.meta.env.VITE_ZMATRIX_AGENT_DRAFT_URL as string | undefined;
  if (configured) {
    return configured;
  }
  if (import.meta.env.MODE === "test" || typeof window === "undefined" || typeof fetch !== "function") {
    return null;
  }
  return "/api/product/agent_draft.json";
}

async function loadBackendDayanAskPacket(workspaceId: string): Promise<DayanAskPageData | null> {
  const packetUrl = getBackendDayanAskPacketUrl();
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
    const packet = (await response.json()) as DayanAskPageData;
    if (packet.workspaceId !== workspaceId) {
      return null;
    }
    return packet;
  } catch {
    return null;
  }
}

async function createBackendAgentDraft(
  session: AuthSession,
  action: DayanAction,
  payload: Record<string, unknown>,
  auditEvent: string
): Promise<DayanActionDraft | null> {
  const draftUrl = getAgentDraftUrl();
  const question = String(payload.userInput ?? payload.question ?? payload.prompt ?? "").trim();
  if (!draftUrl || !question) {
    return null;
  }
  try {
    const response = await fetch(draftUrl, {
      method: "POST",
      headers: {
        accept: "application/json",
        "content-type": "application/json"
      },
      body: JSON.stringify({
        action,
        question,
        selectedFragments: Array.isArray(payload.selectedFragments) ? payload.selectedFragments : []
      })
    });
    if (!response.ok) {
      return null;
    }
    const packet = (await response.json()) as AgentResearchDraftPacket;
    if (packet.workspace_id && packet.workspace_id !== session.workspaceId) {
      return null;
    }
    return {
      draftId: packet.draft_id || `dayan-draft-${Date.now()}`,
      workspaceId: session.workspaceId,
      action,
      status: packet.status === "Z_MATRIX_AGENT_DRAFT_REJECTED" ? "DRAFT_REJECTED" : "DRAFT_CREATED",
      humanReviewRequired: true,
      auditEvent,
      userMessage: packet.user_message,
      answer: packet.answer,
      intentId: packet.intent_id,
      suggestedNextSteps: Array.isArray(packet.suggested_next_steps) ? [...packet.suggested_next_steps] : []
    };
  } catch {
    return null;
  }
}

async function loadAgentBridgeStatus(workspaceId: string): Promise<AgentBridgeStatus> {
  const bridgeUrl = getAgentBridgeUrl();
  if (!bridgeUrl) {
    return cloneAgentBridge(defaultAgentBridgeStatus, workspaceId);
  }
  try {
    const response = await fetch(bridgeUrl, {
      headers: { accept: "application/json" },
      cache: "no-store"
    });
    if (!response.ok) {
      return cloneAgentBridge(defaultAgentBridgeStatus, workspaceId);
    }
    const packet = (await response.json()) as AgentBridgeStatus;
    if (packet.workspace_id && packet.workspace_id !== workspaceId) {
      return cloneAgentBridge(defaultAgentBridgeStatus, workspaceId);
    }
    return cloneAgentBridge(packet, workspaceId);
  } catch {
    return cloneAgentBridge(defaultAgentBridgeStatus, workspaceId);
  }
}

export async function getDayanAskPageData(session: AuthSession | null): Promise<DayanAskPageData> {
  const current = requireSession(session);
  const [backendPacket, agentBridge] = await Promise.all([
    loadBackendDayanAskPacket(current.workspaceId),
    loadAgentBridgeStatus(current.workspaceId)
  ]);
  if (backendPacket) {
    return cloneData({ ...backendPacket, agentBridge }, current.workspaceId);
  }
  if (current.workspaceId === "ws_personal_z_prime") {
    return cloneData({ ...zPrimeData, agentBridge }, current.workspaceId);
  }

  return {
    ...cloneData({ ...zPrimeData, agentBridge }, current.workspaceId),
    altar: {
      ...zPrimeData.altar,
      currentTopic: "等待研究主题输入",
      modeLabel: "自由问天",
      researchScopeLabel: "未指定",
      memoryContextLabel: "短链记忆"
    },
    currentConversation: {
      ...zPrimeData.currentConversation,
      topic: "等待研究主题输入",
      selectedPromptFragments: [],
      messages: [
        {
          id: "msg-empty",
          role: "HERMES",
          label: "问天",
          content: "请先输入研究目标，随侍童子会帮你挑选法门并生成待确认研究链路。",
          createdAt: "09:41"
        }
      ]
    },
    moveReview: [],
    myMethods: [],
    forgeCandidates: [],
    hermesGuidance: {
      ...zPrimeData.hermesGuidance,
      contextSummary: "当前 workspace 尚未形成个人法门，请先从问天法门或问天法阵开始。",
      missingInputs: ["研究目标", "研究范围"]
    }
  };
}

export async function createDayanActionDraft(
  session: AuthSession | null,
  action: DayanAction,
  payload: Record<string, unknown>
): Promise<DayanActionDraft> {
  const current = requireSession(session);
  ensureNoClientTenantFields(payload);

  const auditEvent =
    action === "导出审计包"
      ? "EXPORT_DAYAN_AUDIT_PACK"
      : action === "插入法门" || action === "清空对话"
        ? "SAVE_DAYAN_REFERENCE"
        : "CREATE_DAYAN_DRAFT";

  const backendDraft = await createBackendAgentDraft(current, action, payload, auditEvent);
  if (backendDraft) {
    return backendDraft;
  }

  const response = await createWorkspaceDraft(current, payload, auditEvent);

  return {
    draftId: `dayan-draft-${Date.now()}`,
    workspaceId: response.workspaceId,
    action,
    status: action === "导出审计包" ? "AUDIT_PACK_READY" : action === "插入法门" || action === "清空对话" ? "REFERENCE_SAVED" : "DRAFT_CREATED",
    humanReviewRequired: true,
    auditEvent: response.auditEvent,
    userMessage:
      action === "插入法门"
        ? "法门提示已插入中宫，可继续编辑。"
        : action === "导出审计包"
          ? "审计包已准备，等待人工确认后导出。"
          : action === "清空对话"
            ? "当前对话已清空为本地草稿状态。"
            : action === "保存我的法门草案"
              ? "个人法门草案已创建，等待你确认后保存。"
              : action === "加入我的法门草案"
                ? "加入我的法门请求已进入人工确认。"
                : action === "忽略熔炼候选"
                  ? "候选已标记为忽略参考，不影响正式库。"
                  : "研究链路草案已创建，等待人审裁定。"
  };
}
