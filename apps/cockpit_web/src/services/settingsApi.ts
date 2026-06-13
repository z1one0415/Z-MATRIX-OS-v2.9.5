import type { AuthSession } from "../auth";
import { createWorkspaceDraft, ensureNoClientTenantFields, MockApiError, saveDataSourceSecret } from "./mockApi";

export type CopyMode = "tianji" | "plain" | "english";
export type ThemeMode = "dark" | "light";
export type FontScale = "small" | "standard" | "large";

export type SettingsSafety = {
  paperOnly: true;
  humanReviewRequired: true;
  brokerRuntime: "BLOCKED";
  realTrade: "BLOCKED";
  agentDirectMutation: "BLOCKED";
  dataScope: "WORKSPACE_SCOPED";
};

export type SettingsCategoryId = "account" | "data" | "llm" | "assistant" | "safety" | "appearance" | "backup";

export type SettingsCategory = {
  id: SettingsCategoryId;
  label: string;
  summary: string;
  status: "正常" | "待配置" | "已锁定" | "可导出";
};

export type SettingsDrilldownItem = {
  id: string;
  categoryId: SettingsCategoryId;
  label: string;
  summary: string;
  status: "正常" | "待配置" | "已锁定" | "可导出" | "待保存";
  targetId?: string;
};

export type AccountDisplaySettings = {
  nickname: string;
  avatarInitial: string;
  accountDisplayName: string;
  profileTags: string[];
  defaultHome: "/holdings" | "/selection" | "/history" | "/control-compass" | "/dayan-ask" | "/settings";
};

export type DataSourceStatus = {
  id: string;
  label: string;
  status: "正常" | "可测试" | "备用" | "待导入";
  lastChecked: string;
  detail: string;
  secretPreview?: "***REDACTED***";
};

export type LlmProviderStatus = {
  id: string;
  label: string;
  region: "国际" | "国内" | "自定义";
  endpointMode: "官方 API" | "兼容 OpenAI" | "聚合网关";
  baseUrl: string;
  defaultModel: string;
  fallbackModel: string;
  testTarget: string;
  lastTested: string;
  latency: string;
  keyStatus: "未配置" | "已保存引用" | "待测试";
  status: "可配置" | "可测试" | "备用";
  modelScope: string;
  detail: string;
  secretPreview?: "***REDACTED***";
};

export type AssistantPreference = {
  advisoryVisible: true;
  floatingChatEnabled: true;
  keepPageConversation: false;
  defaultPromptCount: 4;
  style: "克制解释";
};

export type SafetyLock = {
  id: string;
  label: string;
  status: "已锁定";
  detail: string;
};

export type AppearanceBackupSettings = {
  pageDensity: "标准";
  fontScale: FontScale;
  themeMode: ThemeMode;
  bottomTickerVisible: true;
  backupStatus: "可导出";
  lastBackup: string;
  restoreRequiresReview: true;
};

export type CopyPackEntry = {
  tianji: string;
  plain: string;
  english: string;
};

export type CopyPack = Record<string, CopyPackEntry>;

export type SystemHealthItem = {
  label: string;
  value: string;
  tone: "green" | "gold" | "red";
  detail: string;
};

export type AuditSummaryItem = {
  time: string;
  title: string;
  status: "已记录" | "待确认" | "可导出";
};

export type ProductRuntimeStatus = {
  status: "Z_MATRIX_PRODUCT_RUNTIME_READY" | "Z_MATRIX_PRODUCT_RUNTIME_DEGRADED";
  service: {
    name: string;
    host: string;
    port: number;
  };
  cockpit: {
    ready: boolean;
    packet_count: number;
    required_packet_count: number;
    missing: string[];
  };
  registry: {
    ready: boolean;
    skill_count: number;
    domain_count: number;
    concrete_skill_count: number;
  };
  data_source: {
    ready: boolean;
    manifest_count: number;
    mode: string;
  };
  config: {
    ready: boolean;
    template_count: number;
    ready_count: number;
    configured_secret_refs: number;
    required_secret_refs: number;
    env_reference_policy: "PROCESS_ENV_ONLY_NO_VALUES_EMITTED";
    env_references: Array<{
      key: string;
      configured: boolean;
      source: "PROCESS_ENV";
      value_material: "NOT_EMITTED";
    }>;
    secret_material_policy: "TEMPLATE_KEYS_ONLY_ENV_VALUES_NEVER_EMITTED";
  };
  safety: {
    alpha_claim: "BLOCKED";
    promotion: "BLOCKED";
    broker_runtime: "BLOCKED";
    real_trade: "BLOCKED";
    agent_direct_mutation: "BLOCKED";
    secret_storage: "ENV_ONLY";
  };
};

export type ProductReadinessStatus = {
  status: "Z_MATRIX_LOCAL_PRODUCT_READINESS_PASS" | "Z_MATRIX_LOCAL_PRODUCT_READINESS_BLOCKED";
  scope: "LOCAL_PERSONAL_RESEARCH_WORKSTATION";
  checks: Array<{
    id: string;
    ready: boolean;
    evidence: string;
    missing_required_keys?: string[];
    unsafe_example_value_keys?: string[];
    value_material?: "NOT_EMITTED";
  }>;
  blocking_reasons: string[];
  summary: {
    cockpit_packets: number;
    cockpit_routes: number;
    registered_skills: number;
    research_capabilities: number;
    ready_research_capabilities: number;
    research_evidence_groups: number;
    report_export_artifacts: number;
    data_quality_evidence: number;
    local_vendor_manifests: number;
    agent_intents: number;
    operator_actions: number;
    config_templates: number;
    configured_secret_refs: number;
    required_secret_refs: number;
  };
  safety: {
    alpha_claim: "BLOCKED";
    promotion: "BLOCKED";
    broker_runtime: "BLOCKED";
    real_trade: "BLOCKED";
    agent_direct_mutation: "BLOCKED";
  };
};

export type ProductOperatorAction = {
  id: string;
  label: string;
  category: "health" | "verification" | "research" | "cockpit" | "package";
  command: string;
  detail: string;
  expected: string;
  mode: "LOCAL_TERMINAL_MANUAL";
  safety: {
    alpha_claim: "BLOCKED";
    promotion: "BLOCKED";
    broker_runtime: "BLOCKED";
    real_trade: "BLOCKED";
    secret_storage: "ENV_ONLY";
  };
};

export type ProductOperatorActions = {
  status: "Z_MATRIX_OPERATOR_ACTIONS_READY" | "Z_MATRIX_OPERATOR_ACTIONS_DEGRADED";
  auto_run_enabled: false;
  human_review_required: true;
  actions: ProductOperatorAction[];
};

export type ProductResearchCapability = {
  id: string;
  label: string;
  summary: string;
  status: "READY" | "PARTIAL";
  available_count: number;
  required_count: number;
  evidence_paths: string[];
  missing_paths: string[];
  module_count: number;
  safety: "RESEARCH_ONLY";
};

export type ProductResearchStatus = {
  status: "Z_MATRIX_RESEARCH_STATUS_READY" | "Z_MATRIX_RESEARCH_STATUS_DEGRADED";
  capability_count: number;
  ready_count: number;
  capabilities: ProductResearchCapability[];
  report_export: {
    status: "LOCAL_EXPORT_PLANNED" | "LOCAL_EXPORT_READY";
    command: string;
    artifact_policy: "LOCAL_FILES_ONLY";
  };
  monthly_refresh: {
    status: "MONTHLY_REFRESH_DRY_PLAN_READY" | "MONTHLY_REFRESH_DEGRADED";
    ready_count: number;
    required_count: number;
    command: string;
    mode: "LOCAL_TERMINAL_MANUAL_DRY_PLAN";
    safety: {
      alpha_claim: "BLOCKED";
      promotion: "BLOCKED";
      broker_runtime: "BLOCKED";
      real_trade: "BLOCKED";
    };
  };
  safety: {
    alpha_claim: "BLOCKED";
    promotion: "BLOCKED";
    broker_runtime: "BLOCKED";
    real_trade: "BLOCKED";
  };
};

export type ProductResearchEvidenceArtifact = {
  path: string;
  ready: boolean;
  bytes: number;
  artifact_type: string;
  status_field: string;
};

export type ProductResearchEvidenceGroup = {
  id: string;
  label: string;
  summary: string;
  status: "READY" | "PARTIAL";
  ready_count: number;
  required_count: number;
  artifacts: ProductResearchEvidenceArtifact[];
  safety: "RESEARCH_ONLY_NO_ALPHA_PROMOTION";
};

export type ProductResearchEvidenceIndex = {
  status: "Z_MATRIX_RESEARCH_EVIDENCE_INDEX_READY" | "Z_MATRIX_RESEARCH_EVIDENCE_INDEX_PARTIAL";
  group_count: number;
  ready_group_count: number;
  groups: ProductResearchEvidenceGroup[];
  artifact_policy: "LOCAL_RESEARCH_EVIDENCE_ONLY";
  safety: {
    alpha_claim: "BLOCKED";
    promotion: "BLOCKED";
    broker_runtime: "BLOCKED";
    real_trade: "BLOCKED";
    evidence_to_alpha_promotion: "BLOCKED";
  };
};

export type ProductReportExportStatus = {
  status: "Z_MATRIX_REPORT_EXPORT_READY" | "Z_MATRIX_REPORT_EXPORT_EMPTY";
  command: string;
  default_output_dir: string;
  artifact_count: number;
  doc_artifact_count: number;
  runtime_artifact_count: number;
  sample_artifacts: string[];
  artifact_policy: "LOCAL_FILES_ONLY";
  data_policy: {
    raw_vendor_data_included: false;
    private_account_data_included: false;
    secret_files_included: false;
    local_files_only: true;
  };
  safety: {
    alpha_claim: "BLOCKED";
    promotion: "BLOCKED";
    broker_runtime: "BLOCKED";
    real_trade: "BLOCKED";
  };
};

export type ProductDataQualityStatus = {
  status: "Z_MATRIX_DATA_QUALITY_STATUS_READY" | "Z_MATRIX_DATA_QUALITY_STATUS_DEGRADED";
  data_source: {
    ready: boolean;
    path: string;
    resolved_path: string;
    manifest_count: number;
    latest_manifest: string;
    latest_run_id: string;
    latest_manifest_status: string;
    source_vendor: string;
    write_scope: "LOCAL_VENDOR_STORE_ONLY";
    symbol_count: number;
    file_count: number;
    failure_count: number;
    endpoint_count: number;
    endpoints: string[];
    window: {
      start_date: string;
      end_date: string;
      years: number;
    };
    mode: "LOCAL_VENDOR_STORE_ONLY";
  };
  quality_evidence: {
    ready_count: number;
    required_count: number;
    items: Array<{
      id: string;
      label: string;
      path: string;
      ready: boolean;
      bytes: number;
      status_field: string;
      artifact_type: string;
    }>;
  };
  source_health: {
    status: "SOURCE_HEALTH_LEDGER_READY" | "SOURCE_HEALTH_LEDGER_EMPTY";
    ledger_path: string;
    source_count: number;
    usable_count: number;
    sources: Array<{
      source_id: string;
      ok_count: number;
      error_count: number;
      freshness_status: string;
      usable_now: boolean;
      blocked_reason: string;
    }>;
  };
  privacy_guardrail: {
    status: "PASS" | "FAILED";
    scan_scope: "GIT_TRACKED_MARKET_DATA_FILES";
    tracked_private_market_data_violation_count: number;
    violations: string[];
    production_allowed: false;
  };
  refresh_dry_plan: {
    command: string;
    mode: "LOCAL_TERMINAL_MANUAL_DRY_PLAN";
    write_scope: "LOCAL_VENDOR_STORE_ONLY";
    auto_run_enabled: false;
  };
  data_policy: {
    raw_vendor_data_included: false;
    private_account_data_included: false;
    secret_files_included: false;
    repository_commit_allowed: false;
    local_vendor_store_only: true;
  };
  safety: {
    alpha_claim: "BLOCKED";
    promotion: "BLOCKED";
    broker_runtime: "BLOCKED";
    real_trade: "BLOCKED";
  };
};

export type ProductCockpitRoute = {
  id: string;
  label: string;
  route: string;
  capability: string;
  packet_file: string;
  api_path: string;
  ready: boolean;
  bytes: number;
  mode: "READ_ONLY_PACKET";
  safety: {
    paper_only: true;
    human_review_required: true;
    broker_runtime: "BLOCKED";
    real_trade: "BLOCKED";
  };
};

export type ProductCockpitManifest = {
  status: "Z_MATRIX_COCKPIT_MANIFEST_READY" | "Z_MATRIX_COCKPIT_MANIFEST_DEGRADED";
  public_root: string;
  route_count: number;
  ready_count: number;
  routes: ProductCockpitRoute[];
  safety: {
    alpha_claim: "BLOCKED";
    promotion: "BLOCKED";
    broker_runtime: "BLOCKED";
    real_trade: "BLOCKED";
    agent_direct_mutation: "BLOCKED";
  };
};

export type SettingsPageData = {
  workspaceId: string;
  title: "系统设置";
  subtitle: "基础配置 · 数据连接 · 安全锁";
  categories: SettingsCategory[];
  settingsDrilldowns: Record<SettingsCategoryId, SettingsDrilldownItem[]>;
  accountDisplay: AccountDisplaySettings;
  dataSources: DataSourceStatus[];
  llmProviders: LlmProviderStatus[];
  assistantPreference: AssistantPreference;
  safetyLocks: SafetyLock[];
  appearanceBackup: AppearanceBackupSettings;
  copyMode: CopyMode;
  copyPack: CopyPack;
  systemHealth: SystemHealthItem[];
  auditSummary: AuditSummaryItem[];
  productRuntime: ProductRuntimeStatus;
  productReadiness: ProductReadinessStatus;
  operatorActions: ProductOperatorActions;
  researchStatus: ProductResearchStatus;
  researchEvidence: ProductResearchEvidenceIndex;
  reportExport: ProductReportExportStatus;
  dataQuality: ProductDataQualityStatus;
  cockpitManifest: ProductCockpitManifest;
  safety: SettingsSafety;
};

export type SettingsAction =
  | "SAVE_ACCOUNT_DISPLAY_DRAFT"
  | "TEST_DATA_SOURCE"
  | "SAVE_SECRET_REFERENCE"
  | "VALIDATE_LOCAL_IMPORT_DRAFT"
  | "TEST_LLM_PROVIDER"
  | "SAVE_LLM_SECRET_REFERENCE"
  | "SAVE_ASSISTANT_PREFERENCE_DRAFT"
  | "PREVIEW_COPY_MODE"
  | "PREVIEW_THEME_MODE"
  | "PREVIEW_FONT_SCALE"
  | "SAVE_SETTINGS_DRAFT"
  | "EXPORT_SETTINGS_AUDIT_PACK"
  | "CREATE_BACKUP_RESTORE_DRAFT";

export type SettingsActionDraft = {
  draftId: string;
  workspaceId: string;
  status: "DRAFT_CREATED" | "AUDIT_PACK_READY" | "REFERENCE_SAVED";
  humanReviewRequired: true;
  auditEvent:
    | "TEST_SETTINGS_DATA_SOURCE"
    | "SAVE_SETTINGS_SECRET_REFERENCE"
    | "VALIDATE_SETTINGS_LOCAL_IMPORT"
    | "TEST_SETTINGS_LLM_PROVIDER"
    | "SAVE_SETTINGS_LLM_SECRET_REFERENCE"
    | "SAVE_SETTINGS_ACCOUNT_DISPLAY"
    | "SAVE_SETTINGS_ASSISTANT_PREFERENCE"
    | "PREVIEW_SETTINGS_COPY_MODE"
    | "PREVIEW_SETTINGS_THEME_MODE"
    | "PREVIEW_SETTINGS_FONT_SCALE"
    | "CREATE_SETTINGS_CHANGE_DRAFT"
    | "EXPORT_SETTINGS_AUDIT_PACK"
    | "CREATE_BACKUP_RESTORE_DRAFT";
  userMessage: string;
  tokenPreview?: "***REDACTED***";
  secretRef?: string;
  copyMode?: CopyMode;
  themeMode?: ThemeMode;
  fontScale?: FontScale;
};

const safety: SettingsSafety = {
  paperOnly: true,
  humanReviewRequired: true,
  brokerRuntime: "BLOCKED",
  realTrade: "BLOCKED",
  agentDirectMutation: "BLOCKED",
  dataScope: "WORKSPACE_SCOPED"
};

const defaultProductRuntime: ProductRuntimeStatus = {
  status: "Z_MATRIX_PRODUCT_RUNTIME_DEGRADED",
  service: {
    name: "z-matrix-local-product-backend",
    host: "127.0.0.1",
    port: 8765
  },
  cockpit: {
    ready: true,
    packet_count: 5,
    required_packet_count: 5,
    missing: []
  },
  registry: {
    ready: true,
    skill_count: 104,
    domain_count: 20,
    concrete_skill_count: 50
  },
  data_source: {
    ready: false,
    manifest_count: 0,
    mode: "LOCAL_VENDOR_STORE_ONLY"
  },
  config: {
    ready: true,
    template_count: 2,
    ready_count: 2,
    configured_secret_refs: 0,
    required_secret_refs: 2,
    env_reference_policy: "PROCESS_ENV_ONLY_NO_VALUES_EMITTED",
    env_references: [
      { key: "TUSHARE_TOKEN", configured: false, source: "PROCESS_ENV", value_material: "NOT_EMITTED" },
      { key: "DEEPSEEK_API_KEY", configured: false, source: "PROCESS_ENV", value_material: "NOT_EMITTED" }
    ],
    secret_material_policy: "TEMPLATE_KEYS_ONLY_ENV_VALUES_NEVER_EMITTED"
  },
  safety: {
    alpha_claim: "BLOCKED",
    promotion: "BLOCKED",
    broker_runtime: "BLOCKED",
    real_trade: "BLOCKED",
    agent_direct_mutation: "BLOCKED",
    secret_storage: "ENV_ONLY"
  }
};

const defaultProductReadiness: ProductReadinessStatus = {
  status: "Z_MATRIX_LOCAL_PRODUCT_READINESS_BLOCKED",
  scope: "LOCAL_PERSONAL_RESEARCH_WORKSTATION",
  checks: [
    { id: "backend-service", ready: false, evidence: "scripts/product/start_backend_service.py" },
    { id: "product-runtime", ready: false, evidence: "backend unavailable" }
  ],
  blocking_reasons: ["backend-service", "product-runtime"],
  summary: {
    cockpit_packets: 0,
    cockpit_routes: 0,
    registered_skills: 0,
    research_capabilities: 0,
    ready_research_capabilities: 0,
    research_evidence_groups: 0,
    report_export_artifacts: 0,
    data_quality_evidence: 0,
    local_vendor_manifests: 0,
    agent_intents: 0,
    operator_actions: 0,
    config_templates: 0,
    configured_secret_refs: 0,
    required_secret_refs: 2
  },
  safety: {
    alpha_claim: "BLOCKED",
    promotion: "BLOCKED",
    broker_runtime: "BLOCKED",
    real_trade: "BLOCKED",
    agent_direct_mutation: "BLOCKED"
  }
};

const defaultReportExport: ProductReportExportStatus = {
  status: "Z_MATRIX_REPORT_EXPORT_EMPTY",
  command: "PYTHONPATH=. python3 scripts/product/export_research_report_pack.py",
  default_output_dir: "build/research_report_exports/Z-MATRIX-research-report-pack",
  artifact_count: 0,
  doc_artifact_count: 0,
  runtime_artifact_count: 0,
  sample_artifacts: [],
  artifact_policy: "LOCAL_FILES_ONLY",
  data_policy: {
    raw_vendor_data_included: false,
    private_account_data_included: false,
    secret_files_included: false,
    local_files_only: true
  },
  safety: {
    alpha_claim: "BLOCKED",
    promotion: "BLOCKED",
    broker_runtime: "BLOCKED",
    real_trade: "BLOCKED"
  }
};

const defaultDataQuality: ProductDataQualityStatus = {
  status: "Z_MATRIX_DATA_QUALITY_STATUS_DEGRADED",
  data_source: {
    ready: false,
    path: "data/research_db/market_data/vendor/tushare_5y",
    resolved_path: "data/research_db/market_data/vendor/tushare_5y",
    manifest_count: 0,
    latest_manifest: "",
    latest_run_id: "",
    latest_manifest_status: "",
    source_vendor: "TUSHARE",
    write_scope: "LOCAL_VENDOR_STORE_ONLY",
    symbol_count: 0,
    file_count: 0,
    failure_count: 0,
    endpoint_count: 0,
    endpoints: [],
    window: {
      start_date: "",
      end_date: "",
      years: 0
    },
    mode: "LOCAL_VENDOR_STORE_ONLY"
  },
  quality_evidence: {
    ready_count: 0,
    required_count: 6,
    items: [
      {
        id: "v8-large-data-manifest",
        label: "V8 大数据 manifest",
        path: "runtime_reports/cases/v8_large_data_manifest.json",
        ready: false,
        bytes: 0,
        status_field: "",
        artifact_type: "json"
      },
      {
        id: "price-data-schema-validation",
        label: "价格数据 schema 验证",
        path: "runtime_reports/cases/v12_4_7_price_data_schema_validation.json",
        ready: false,
        bytes: 0,
        status_field: "",
        artifact_type: "json"
      },
      {
        id: "core-real-market-data-readiness",
        label: "Core 12 真实行情就绪",
        path: "runtime_reports/cases/core_12_real_market_data_readiness.json",
        ready: false,
        bytes: 0,
        status_field: "",
        artifact_type: "json"
      }
    ]
  },
  source_health: {
    status: "SOURCE_HEALTH_LEDGER_EMPTY",
    ledger_path: "data/research_db/governance/source_health_ledger.jsonl",
    source_count: 0,
    usable_count: 0,
    sources: []
  },
  privacy_guardrail: {
    status: "PASS",
    scan_scope: "GIT_TRACKED_MARKET_DATA_FILES",
    tracked_private_market_data_violation_count: 0,
    violations: [],
    production_allowed: false
  },
  refresh_dry_plan: {
    command:
      "PYTHONPATH=. python3 scripts/data/ingest_tushare_market_data.py --symbols 601899,002472,300750 --end-date 20260613 --years 5 --endpoints stock_basic,trade_cal,daily,adj_factor,daily_basic --dry-plan",
    mode: "LOCAL_TERMINAL_MANUAL_DRY_PLAN",
    write_scope: "LOCAL_VENDOR_STORE_ONLY",
    auto_run_enabled: false
  },
  data_policy: {
    raw_vendor_data_included: false,
    private_account_data_included: false,
    secret_files_included: false,
    repository_commit_allowed: false,
    local_vendor_store_only: true
  },
  safety: {
    alpha_claim: "BLOCKED",
    promotion: "BLOCKED",
    broker_runtime: "BLOCKED",
    real_trade: "BLOCKED"
  }
};

const defaultResearchEvidence: ProductResearchEvidenceIndex = {
  status: "Z_MATRIX_RESEARCH_EVIDENCE_INDEX_PARTIAL",
  group_count: 4,
  ready_group_count: 0,
  groups: [
    {
      id: "factor-library",
      label: "因子库状态",
      summary: "等待本地后端返回因子证据索引。",
      status: "PARTIAL",
      ready_count: 0,
      required_count: 1,
      artifacts: [{ path: "backend", ready: false, bytes: 0, artifact_type: "endpoint", status_field: "" }],
      safety: "RESEARCH_ONLY_NO_ALPHA_PROMOTION"
    },
    {
      id: "historical-oos",
      label: "历史 OOS",
      summary: "等待本地后端返回历史 OOS 证据索引。",
      status: "PARTIAL",
      ready_count: 0,
      required_count: 1,
      artifacts: [{ path: "backend", ready: false, bytes: 0, artifact_type: "endpoint", status_field: "" }],
      safety: "RESEARCH_ONLY_NO_ALPHA_PROMOTION"
    },
    {
      id: "forward-oos",
      label: "Forward OOS 等待",
      summary: "等待本地后端返回 Forward OOS 证据索引。",
      status: "PARTIAL",
      ready_count: 0,
      required_count: 1,
      artifacts: [{ path: "backend", ready: false, bytes: 0, artifact_type: "endpoint", status_field: "" }],
      safety: "RESEARCH_ONLY_NO_ALPHA_PROMOTION"
    },
    {
      id: "gatekeeper-audit",
      label: "Gatekeeper 审计",
      summary: "等待本地后端返回审计证据索引。",
      status: "PARTIAL",
      ready_count: 0,
      required_count: 1,
      artifacts: [{ path: "backend", ready: false, bytes: 0, artifact_type: "endpoint", status_field: "" }],
      safety: "RESEARCH_ONLY_NO_ALPHA_PROMOTION"
    }
  ],
  artifact_policy: "LOCAL_RESEARCH_EVIDENCE_ONLY",
  safety: {
    alpha_claim: "BLOCKED",
    promotion: "BLOCKED",
    broker_runtime: "BLOCKED",
    real_trade: "BLOCKED",
    evidence_to_alpha_promotion: "BLOCKED"
  }
};

const defaultCockpitManifest: ProductCockpitManifest = {
  status: "Z_MATRIX_COCKPIT_MANIFEST_DEGRADED",
  public_root: "apps/cockpit_web/public/api/cockpit",
  route_count: 5,
  ready_count: 0,
  routes: [
    { id: "holdings", label: "持仓管理", route: "/holdings", capability: "portfolio_review_readonly", packet_file: "holdings_packet.json", api_path: "/api/cockpit/holdings_packet.json", ready: false, bytes: 0 },
    { id: "selection", label: "投研选股", route: "/selection", capability: "candidate_research_watchlist", packet_file: "selection_packet.json", api_path: "/api/cockpit/selection_packet.json", ready: false, bytes: 0 },
    { id: "history", label: "历史回溯", route: "/history", capability: "oos_memory_report_library", packet_file: "history_packet.json", api_path: "/api/cockpit/history_packet.json", ready: false, bytes: 0 },
    { id: "control-compass", label: "天机罗盘", route: "/control-compass", capability: "gatekeeper_audit_control", packet_file: "control_compass_packet.json", api_path: "/api/cockpit/control_compass_packet.json", ready: false, bytes: 0 },
    { id: "dayan-ask", label: "大衍天问", route: "/dayan-ask", capability: "hermes_research_draft_interaction", packet_file: "dayan_ask_packet.json", api_path: "/api/cockpit/dayan_ask_packet.json", ready: false, bytes: 0 }
  ].map((route) => ({
    ...route,
    mode: "READ_ONLY_PACKET",
    safety: {
      paper_only: true,
      human_review_required: true,
      broker_runtime: "BLOCKED",
      real_trade: "BLOCKED"
    }
  })),
  safety: {
    alpha_claim: "BLOCKED",
    promotion: "BLOCKED",
    broker_runtime: "BLOCKED",
    real_trade: "BLOCKED",
    agent_direct_mutation: "BLOCKED"
  }
};

const defaultOperatorActions: ProductOperatorActions = {
  status: "Z_MATRIX_OPERATOR_ACTIONS_DEGRADED",
  auto_run_enabled: false,
  human_review_required: true,
  actions: [
    {
      id: "bootstrap-check",
      label: "本地安装检查",
      category: "verification",
      command: "bash scripts/product/bootstrap_local_workstation.sh --check",
      detail: "确认本地安装入口、Python/npm 工具链与关键文件存在，不安装依赖。",
      expected: "Z_MATRIX_LOCAL_BOOTSTRAP_CHECK_PASS",
      mode: "LOCAL_TERMINAL_MANUAL",
      safety: {
        alpha_claim: "BLOCKED",
        promotion: "BLOCKED",
        broker_runtime: "BLOCKED",
        real_trade: "BLOCKED",
        secret_storage: "ENV_ONLY"
      }
    },
    {
      id: "backend-check",
      label: "后端健康检查",
      category: "health",
      command: "PYTHONPATH=. python3 scripts/product/start_backend_service.py --check",
      detail: "读取本地服务状态、驾驶舱数据和 SkillOS registry。",
      expected: "Z_MATRIX_PRODUCT_RUNTIME_READY",
      mode: "LOCAL_TERMINAL_MANUAL",
      safety: {
        alpha_claim: "BLOCKED",
        promotion: "BLOCKED",
        broker_runtime: "BLOCKED",
        real_trade: "BLOCKED",
        secret_storage: "ENV_ONLY"
      }
    },
    {
      id: "product-smoke",
      label: "产品 smoke test",
      category: "verification",
      command: "bash scripts/verify_z_matrix_product_smoke.sh",
      detail: "验证后端、数据 dry plan、驾驶舱测试、驾驶舱构建和产品包。",
      expected: "Z-MATRIX Product Smoke PASS",
      mode: "LOCAL_TERMINAL_MANUAL",
      safety: {
        alpha_claim: "BLOCKED",
        promotion: "BLOCKED",
        broker_runtime: "BLOCKED",
        real_trade: "BLOCKED",
        secret_storage: "ENV_ONLY"
      }
    },
    {
      id: "product-readiness",
      label: "产品就绪自检",
      category: "verification",
      command: "PYTHONPATH=. python3 scripts/product/check_product_readiness.py",
      detail: "检查安装、启动、驾驶舱、研究能力、Hermes 桥接和安全门状态。",
      expected: "Z_MATRIX_LOCAL_PRODUCT_READINESS_PASS",
      mode: "LOCAL_TERMINAL_MANUAL",
      safety: {
        alpha_claim: "BLOCKED",
        promotion: "BLOCKED",
        broker_runtime: "BLOCKED",
        real_trade: "BLOCKED",
        secret_storage: "ENV_ONLY"
      }
    }
  ]
};

const defaultResearchStatus: ProductResearchStatus = {
  status: "Z_MATRIX_RESEARCH_STATUS_DEGRADED",
  capability_count: 4,
  ready_count: 0,
  capabilities: [
    {
      id: "factor-library",
      label: "因子库状态",
      summary: "等待本地后端返回因子库状态。",
      status: "PARTIAL",
      available_count: 0,
      required_count: 1,
      evidence_paths: [],
      missing_paths: ["backend"],
      module_count: 0,
      safety: "RESEARCH_ONLY"
    },
    {
      id: "historical-oos",
      label: "历史 OOS",
      summary: "等待本地后端返回历史验证状态。",
      status: "PARTIAL",
      available_count: 0,
      required_count: 1,
      evidence_paths: [],
      missing_paths: ["backend"],
      module_count: 0,
      safety: "RESEARCH_ONLY"
    },
    {
      id: "forward-oos",
      label: "Forward OOS 等待",
      summary: "等待本地后端返回未来标签状态。",
      status: "PARTIAL",
      available_count: 0,
      required_count: 1,
      evidence_paths: [],
      missing_paths: ["backend"],
      module_count: 0,
      safety: "RESEARCH_ONLY"
    },
    {
      id: "gatekeeper-audit",
      label: "Gatekeeper 审计",
      summary: "等待本地后端返回审计闸状态。",
      status: "PARTIAL",
      available_count: 0,
      required_count: 1,
      evidence_paths: [],
      missing_paths: ["backend"],
      module_count: 0,
      safety: "RESEARCH_ONLY"
    }
  ],
  report_export: {
    status: "LOCAL_EXPORT_READY",
    command: "PYTHONPATH=. python3 scripts/product/export_research_report_pack.py",
    artifact_policy: "LOCAL_FILES_ONLY"
  },
  monthly_refresh: {
    status: "MONTHLY_REFRESH_DEGRADED",
    ready_count: 0,
    required_count: 4,
    command: (
      "PYTHONPATH=. python3 scripts/data/ingest_tushare_market_data.py " +
      "--symbols 601899,002472,300750 --end-date 20260613 --years 5 " +
      "--endpoints stock_basic,trade_cal,daily,adj_factor,daily_basic --dry-plan"
    ),
    mode: "LOCAL_TERMINAL_MANUAL_DRY_PLAN",
    safety: {
      alpha_claim: "BLOCKED",
      promotion: "BLOCKED",
      broker_runtime: "BLOCKED",
      real_trade: "BLOCKED"
    }
  },
  safety: {
    alpha_claim: "BLOCKED",
    promotion: "BLOCKED",
    broker_runtime: "BLOCKED",
    real_trade: "BLOCKED"
  }
};

const copyPack: CopyPack = {
  holdings: { tianji: "执仓决断", plain: "持仓检查", english: "Portfolio Review" },
  selection: { tianji: "投研问股", plain: "选股研究", english: "Research Screen" },
  dayan: { tianji: "大衍天问", plain: "研究助手", english: "Research Assistant" },
  compass: { tianji: "天机罗盘", plain: "研究参数", english: "Quant Settings" },
  history: { tianji: "时空回溯", plain: "历史复盘", english: "History Review" },
  settings: { tianji: "系统设置", plain: "设置", english: "Settings" },
  hermes: { tianji: "童子谏言", plain: "帮助助手", english: "Assistant" },
  askHermes: { tianji: "问童子", plain: "提问", english: "Ask" },
  holdingReview: { tianji: "持仓复核", plain: "检查持仓", english: "Review Holdings" },
  reviewDraft: { tianji: "生成复核草案", plain: "生成检查草稿", english: "Create Review Draft" },
  auditPack: { tianji: "导出审计包", plain: "导出记录", english: "Export Audit Pack" }
};

const zPrimeSettings: Omit<SettingsPageData, "workspaceId"> = {
  title: "系统设置",
  subtitle: "基础配置 · 数据连接 · 安全锁",
  categories: [
    { id: "account", label: "账户显示", summary: "名称、头像与默认首页", status: "正常" },
    { id: "data", label: "数据源", summary: "行情、财务与本地导入", status: "待配置" },
    { id: "llm", label: "大模型 API", summary: "国内外模型密钥与端点", status: "待配置" },
    { id: "assistant", label: "随侍童子", summary: "问答入口与页面提示", status: "正常" },
    { id: "safety", label: "安全锁", summary: "纸面、人审与阻断", status: "已锁定" },
    { id: "appearance", label: "显示设置", summary: "文字表达、字号与主题", status: "正常" },
    { id: "backup", label: "备份恢复", summary: "配置快照与恢复草案", status: "可导出" }
  ],
  settingsDrilldowns: {
    account: [
      { id: "account-profile", categoryId: "account", label: "个人显示档案", summary: "昵称、头像、身份标签与默认首页", status: "正常" }
    ],
    data: [
      { id: "data-tushare", categoryId: "data", label: "Tushare 数据源", summary: "Token 引用、连接测试与最近记录", status: "待配置", targetId: "tushare" },
      { id: "data-local-import", categoryId: "data", label: "本地数据导入", summary: "价格、财务与复盘文件导入草案", status: "待保存", targetId: "research-import" }
    ],
    llm: [
      { id: "llm-openai", categoryId: "llm", label: "OpenAI", summary: "国际官方端点与多模态模型", status: "待配置", targetId: "openai" },
      { id: "llm-deepseek", categoryId: "llm", label: "DeepSeek", summary: "工程落地与中文推理主通道", status: "待配置", targetId: "deepseek" },
      { id: "llm-domestic", categoryId: "llm", label: "国内模型组", summary: "通义、智谱、火山、硅基、Kimi", status: "待配置", targetId: "qwen" },
      { id: "llm-custom", categoryId: "llm", label: "自定义兼容接口", summary: "OpenAI 兼容 Base URL 与模型映射", status: "待配置", targetId: "custom-openai-compatible" }
    ],
    assistant: [
      { id: "assistant-preference", categoryId: "assistant", label: "问答入口偏好", summary: "入口显示、提示数量与本页会话", status: "正常" }
    ],
    safety: [
      { id: "safety-locks", categoryId: "safety", label: "安全锁解释", summary: "纸面、人审、券商阻断与 Agent 保护", status: "已锁定" }
    ],
    appearance: [
      { id: "appearance-copy", categoryId: "appearance", label: "文字表达模式", summary: "天机版、通用版、英文版即时预览", status: "正常" },
      { id: "appearance-display", categoryId: "appearance", label: "显示与主题", summary: "文字大小、深浅主题、页面密度", status: "正常" }
    ],
    backup: [
      { id: "backup-snapshot", categoryId: "backup", label: "配置快照", summary: "导出当前显示、账户与连接引用状态", status: "可导出" },
      { id: "backup-restore", categoryId: "backup", label: "恢复保护", summary: "恢复前生成草案并进入人工确认", status: "已锁定" }
    ]
  },
  accountDisplay: {
    nickname: "Z-Prime",
    avatarInitial: "Z",
    accountDisplayName: "稳健成长型",
    profileTags: ["中长为主", "纪律优先", "风险可控"],
    defaultHome: "/holdings"
  },
  dataSources: [
    {
      id: "tushare",
      label: "Tushare Token",
      status: "可测试",
      lastChecked: "09:35",
      detail: "保存为密钥引用，页面不显示原文。",
      secretPreview: "***REDACTED***"
    },
    { id: "sina-market", label: "新浪行情", status: "备用", lastChecked: "09:34", detail: "只显示连通状态，异常时进入数据源提醒。" },
    { id: "research-import", label: "本地数据导入", status: "待导入", lastChecked: "待选择", detail: "价格、财务与复盘文件先校验，再进入导入草案。" },
    { id: "audit-export", label: "审计导出", status: "正常", lastChecked: "09:42", detail: "当前 workspace 可导出配置记录。" }
  ],
  llmProviders: [
    {
      id: "openai",
      label: "OpenAI",
      region: "国际",
      endpointMode: "官方 API",
      baseUrl: "https://api.openai.com/v1",
      defaultModel: "gpt-5.1",
      fallbackModel: "gpt-4.1",
      testTarget: "models.list + lightweight response",
      lastTested: "未测试",
      latency: "待测试",
      keyStatus: "未配置",
      status: "可配置",
      modelScope: "GPT 系列、语音与多模态能力",
      detail: "用于高质量推理、代码审核与复杂研究编排。"
    },
    {
      id: "anthropic",
      label: "Anthropic Claude",
      region: "国际",
      endpointMode: "官方 API",
      baseUrl: "https://api.anthropic.com/v1",
      defaultModel: "claude-opus-4",
      fallbackModel: "claude-sonnet-4",
      testTarget: "message dry probe",
      lastTested: "未测试",
      latency: "待测试",
      keyStatus: "未配置",
      status: "备用",
      modelScope: "长文本、审校与稳健写作",
      detail: "可作为研究报告审读与长上下文辅助。"
    },
    {
      id: "gemini",
      label: "Google Gemini",
      region: "国际",
      endpointMode: "官方 API",
      baseUrl: "https://generativelanguage.googleapis.com/v1beta",
      defaultModel: "gemini-2.5-pro",
      fallbackModel: "gemini-2.5-flash",
      testTarget: "generateContent dry probe",
      lastTested: "未测试",
      latency: "待测试",
      keyStatus: "未配置",
      status: "备用",
      modelScope: "多模态、检索增强与轻量问答",
      detail: "适合图片、网页和多源材料理解。"
    },
    {
      id: "deepseek",
      label: "DeepSeek",
      region: "国内",
      endpointMode: "兼容 OpenAI",
      baseUrl: "https://api.deepseek.com/v1",
      defaultModel: "deepseek-chat",
      fallbackModel: "deepseek-reasoner",
      testTarget: "chat.completions dry probe",
      lastTested: "09:32",
      latency: "待复测",
      keyStatus: "待测试",
      status: "可测试",
      modelScope: "工程落地、代码批处理与中文推理",
      detail: "可承接 OpenCode、天师落地和批量工程任务。",
      secretPreview: "***REDACTED***"
    },
    {
      id: "moonshot",
      label: "Moonshot Kimi",
      region: "国内",
      endpointMode: "兼容 OpenAI",
      baseUrl: "https://api.moonshot.cn/v1",
      defaultModel: "kimi-k2",
      fallbackModel: "moonshot-v1-128k",
      testTarget: "chat.completions dry probe",
      lastTested: "未测试",
      latency: "待测试",
      keyStatus: "未配置",
      status: "可配置",
      modelScope: "长文本、资料阅读与中文问答",
      detail: "适合研报、公告和复盘材料的长文本处理。"
    },
    {
      id: "qwen",
      label: "通义千问",
      region: "国内",
      endpointMode: "兼容 OpenAI",
      baseUrl: "https://dashscope.aliyuncs.com/compatible-mode/v1",
      defaultModel: "qwen-max",
      fallbackModel: "qwen-plus",
      testTarget: "compatible chat dry probe",
      lastTested: "未测试",
      latency: "待测试",
      keyStatus: "未配置",
      status: "可配置",
      modelScope: "中文通用问答、工具调用与多模态",
      detail: "适合中文生态下的常规 Agent 调度。"
    },
    {
      id: "zhipu",
      label: "智谱 GLM",
      region: "国内",
      endpointMode: "官方 API",
      baseUrl: "https://open.bigmodel.cn/api/paas/v4",
      defaultModel: "glm-4-plus",
      fallbackModel: "glm-4-air",
      testTarget: "chat dry probe",
      lastTested: "未测试",
      latency: "待测试",
      keyStatus: "未配置",
      status: "可配置",
      modelScope: "中文推理、结构化摘要与知识问答",
      detail: "可作为国内模型冗余和普通问答通道。"
    },
    {
      id: "volcengine",
      label: "火山方舟",
      region: "国内",
      endpointMode: "聚合网关",
      baseUrl: "https://ark.cn-beijing.volces.com/api/v3",
      defaultModel: "doubao-pro",
      fallbackModel: "doubao-lite",
      testTarget: "gateway dry probe",
      lastTested: "未测试",
      latency: "待测试",
      keyStatus: "未配置",
      status: "备用",
      modelScope: "多模型接入、企业网关与成本控制",
      detail: "适合作为多供应商统一入口。"
    },
    {
      id: "siliconflow",
      label: "硅基流动",
      region: "国内",
      endpointMode: "兼容 OpenAI",
      baseUrl: "https://api.siliconflow.cn/v1",
      defaultModel: "Qwen/Qwen3-235B-A22B",
      fallbackModel: "deepseek-ai/DeepSeek-V3",
      testTarget: "compatible chat dry probe",
      lastTested: "未测试",
      latency: "待测试",
      keyStatus: "未配置",
      status: "备用",
      modelScope: "开源模型、低成本补充与实验能力",
      detail: "适合作为实验模型和轻量任务通道。"
    },
    {
      id: "custom-openai-compatible",
      label: "自定义兼容接口",
      region: "自定义",
      endpointMode: "兼容 OpenAI",
      baseUrl: "https://your-provider.example.com/v1",
      defaultModel: "custom-primary",
      fallbackModel: "custom-fallback",
      testTarget: "compatible chat dry probe",
      lastTested: "未测试",
      latency: "待测试",
      keyStatus: "未配置",
      status: "可配置",
      modelScope: "私有网关、代理服务或其他兼容端点",
      detail: "用于接入未列入清单的 OpenAI 兼容服务。"
    }
  ],
  assistantPreference: {
    advisoryVisible: true,
    floatingChatEnabled: true,
    keepPageConversation: false,
    defaultPromptCount: 4,
    style: "克制解释"
  },
  safetyLocks: [
    { id: "paper-only", label: "Paper-only", status: "已锁定", detail: "所有研究结果仅用于纸面观察。" },
    { id: "human-review", label: "Human Review", status: "已锁定", detail: "配置变更、恢复与导出均需人工确认。" },
    { id: "broker-blocked", label: "Broker Blocked", status: "已锁定", detail: "券商运行通道保持阻断。" },
    { id: "real-trade-blocked", label: "Real Trade Blocked", status: "已锁定", detail: "实盘动作不可由本页触发。" },
    { id: "agent-mutation-blocked", label: "Agent Direct Mutation Blocked", status: "已锁定", detail: "随侍童子只能生成草案或解释。" }
  ],
  appearanceBackup: {
    pageDensity: "标准",
    fontScale: "standard",
    themeMode: "dark",
    bottomTickerVisible: true,
    backupStatus: "可导出",
    lastBackup: "2026-06-04 09:17",
    restoreRequiresReview: true
  },
  copyMode: "tianji",
  copyPack,
  systemHealth: [
    { label: "数据源", value: "可测试", tone: "gold", detail: "Tushare 引用可更新" },
    { label: "大模型 API", value: "10 路", tone: "gold", detail: "国内外模型待配置" },
    { label: "安全锁", value: "已锁定", tone: "green", detail: "5 项边界完整" },
    { label: "童子入口", value: "常驻", tone: "green", detail: "仅答疑与草案" },
    { label: "文字表达", value: "天机版", tone: "gold", detail: "可切换预览" },
    { label: "备份", value: "可导出", tone: "green", detail: "恢复需人审" }
  ],
  auditSummary: [
    { time: "09:35", title: "数据源测试记录", status: "已记录" },
    { time: "09:41", title: "安全锁状态复核", status: "已记录" },
    { time: "待触发", title: "文字表达偏好保存", status: "待确认" }
  ],
  productRuntime: defaultProductRuntime,
  productReadiness: defaultProductReadiness,
  operatorActions: defaultOperatorActions,
  researchStatus: defaultResearchStatus,
  researchEvidence: defaultResearchEvidence,
  reportExport: defaultReportExport,
  dataQuality: defaultDataQuality,
  cockpitManifest: defaultCockpitManifest,
  safety
};

function requireSession(session: AuthSession | null): AuthSession {
  if (!session) {
    throw new MockApiError("AUTH_REQUIRED", "settings api requires authenticated session");
  }
  return session;
}

function cloneSettings(packet: SettingsPageData): SettingsPageData {
  return {
    ...packet,
    categories: packet.categories.map((category) => ({ ...category })),
    settingsDrilldowns: Object.fromEntries(
      Object.entries(packet.settingsDrilldowns).map(([categoryId, items]) => [categoryId, items.map((item) => ({ ...item }))])
    ) as Record<SettingsCategoryId, SettingsDrilldownItem[]>,
    accountDisplay: {
      ...packet.accountDisplay,
      profileTags: [...packet.accountDisplay.profileTags]
    },
    dataSources: packet.dataSources.map((source) => ({ ...source })),
    llmProviders: packet.llmProviders.map((provider) => ({ ...provider })),
    assistantPreference: { ...packet.assistantPreference },
    safetyLocks: packet.safetyLocks.map((lock) => ({ ...lock })),
    appearanceBackup: { ...packet.appearanceBackup },
    copyPack: Object.fromEntries(Object.entries(packet.copyPack).map(([key, value]) => [key, { ...value }])) as CopyPack,
    systemHealth: packet.systemHealth.map((item) => ({ ...item })),
    auditSummary: packet.auditSummary.map((item) => ({ ...item })),
    productRuntime: cloneProductRuntime(packet.productRuntime),
    productReadiness: cloneProductReadiness(packet.productReadiness),
    operatorActions: cloneOperatorActions(packet.operatorActions),
    researchStatus: cloneResearchStatus(packet.researchStatus),
    researchEvidence: cloneResearchEvidence(packet.researchEvidence),
    reportExport: cloneReportExport(packet.reportExport),
    dataQuality: cloneDataQuality(packet.dataQuality),
    cockpitManifest: cloneCockpitManifest(packet.cockpitManifest),
    safety: { ...packet.safety }
  };
}

export async function getSettingsPageData(session: AuthSession | null): Promise<SettingsPageData> {
  const current = requireSession(session);
  const [productRuntime, productReadiness, operatorActions, researchStatus, researchEvidence, reportExport, dataQuality, cockpitManifest] = await Promise.all([
    loadProductRuntimeStatus(),
    loadProductReadiness(),
    loadOperatorActions(),
    loadResearchStatus(),
    loadResearchEvidence(),
    loadReportExport(),
    loadDataQuality(),
    loadCockpitManifest()
  ]);
  return cloneSettings({
    ...zPrimeSettings,
    workspaceId: current.workspaceId,
    productRuntime,
    productReadiness,
    operatorActions,
    researchStatus,
    researchEvidence,
    reportExport,
    dataQuality,
    cockpitManifest
  });
}

function cloneProductRuntime(status: ProductRuntimeStatus): ProductRuntimeStatus {
  return {
    ...status,
    service: { ...status.service },
    cockpit: {
      ...status.cockpit,
      missing: [...status.cockpit.missing]
    },
    registry: { ...status.registry },
    data_source: { ...status.data_source },
    safety: { ...status.safety }
  };
}

function cloneProductReadiness(status: ProductReadinessStatus): ProductReadinessStatus {
  return {
    ...status,
    checks: status.checks.map((item) => ({
      ...item,
      missing_required_keys: item.missing_required_keys ? [...item.missing_required_keys] : undefined,
      unsafe_example_value_keys: item.unsafe_example_value_keys ? [...item.unsafe_example_value_keys] : undefined
    })),
    blocking_reasons: [...status.blocking_reasons],
    summary: { ...status.summary },
    safety: { ...status.safety }
  };
}

function getProductRuntimeStatusUrl(): string {
  return import.meta.env.VITE_ZMATRIX_PRODUCT_STATUS_URL || "/api/product/status.json";
}

function getProductReadinessUrl(): string {
  return import.meta.env.VITE_ZMATRIX_PRODUCT_READINESS_URL || "/api/product/readiness.json";
}

function getOperatorActionsUrl(): string {
  return import.meta.env.VITE_ZMATRIX_OPERATOR_ACTIONS_URL || "/api/product/operator_actions.json";
}

function getResearchStatusUrl(): string {
  return import.meta.env.VITE_ZMATRIX_RESEARCH_STATUS_URL || "/api/product/research_status.json";
}

function getResearchEvidenceUrl(): string {
  return import.meta.env.VITE_ZMATRIX_RESEARCH_EVIDENCE_INDEX_URL || "/api/product/research_evidence_index.json";
}

function getReportExportUrl(): string {
  return import.meta.env.VITE_ZMATRIX_REPORT_EXPORT_STATUS_URL || "/api/product/report_export_status.json";
}

function getDataQualityUrl(): string {
  return import.meta.env.VITE_ZMATRIX_DATA_QUALITY_STATUS_URL || "/api/product/data_quality_status.json";
}

function getCockpitManifestUrl(): string {
  return import.meta.env.VITE_ZMATRIX_COCKPIT_MANIFEST_URL || "/api/product/cockpit_manifest.json";
}

async function loadProductRuntimeStatus(): Promise<ProductRuntimeStatus> {
  if (typeof fetch !== "function") {
    return cloneProductRuntime(defaultProductRuntime);
  }
  try {
    const response = await fetch(getProductRuntimeStatusUrl(), {
      method: "GET",
      headers: { Accept: "application/json" }
    });
    if (!response.ok) {
      return cloneProductRuntime(defaultProductRuntime);
    }
    const packet = (await response.json()) as ProductRuntimeStatus;
    return normalizeProductRuntime(packet);
  } catch {
    return cloneProductRuntime(defaultProductRuntime);
  }
}

async function loadProductReadiness(): Promise<ProductReadinessStatus> {
  if (typeof fetch !== "function") {
    return cloneProductReadiness(defaultProductReadiness);
  }
  try {
    const response = await fetch(getProductReadinessUrl(), {
      method: "GET",
      headers: { Accept: "application/json" }
    });
    if (!response.ok) {
      return cloneProductReadiness(defaultProductReadiness);
    }
    const packet = (await response.json()) as ProductReadinessStatus;
    return normalizeProductReadiness(packet);
  } catch {
    return cloneProductReadiness(defaultProductReadiness);
  }
}

async function loadResearchStatus(): Promise<ProductResearchStatus> {
  if (typeof fetch !== "function") {
    return cloneResearchStatus(defaultResearchStatus);
  }
  try {
    const response = await fetch(getResearchStatusUrl(), {
      method: "GET",
      headers: { Accept: "application/json" }
    });
    if (!response.ok) {
      return cloneResearchStatus(defaultResearchStatus);
    }
    const packet = (await response.json()) as ProductResearchStatus;
    return normalizeResearchStatus(packet);
  } catch {
    return cloneResearchStatus(defaultResearchStatus);
  }
}

async function loadResearchEvidence(): Promise<ProductResearchEvidenceIndex> {
  if (typeof fetch !== "function") {
    return cloneResearchEvidence(defaultResearchEvidence);
  }
  try {
    const response = await fetch(getResearchEvidenceUrl(), {
      method: "GET",
      headers: { Accept: "application/json" }
    });
    if (!response.ok) {
      return cloneResearchEvidence(defaultResearchEvidence);
    }
    const packet = (await response.json()) as ProductResearchEvidenceIndex;
    return normalizeResearchEvidence(packet);
  } catch {
    return cloneResearchEvidence(defaultResearchEvidence);
  }
}

async function loadReportExport(): Promise<ProductReportExportStatus> {
  if (typeof fetch !== "function") {
    return cloneReportExport(defaultReportExport);
  }
  try {
    const response = await fetch(getReportExportUrl(), {
      method: "GET",
      headers: { Accept: "application/json" }
    });
    if (!response.ok) {
      return cloneReportExport(defaultReportExport);
    }
    const packet = (await response.json()) as ProductReportExportStatus;
    return normalizeReportExport(packet);
  } catch {
    return cloneReportExport(defaultReportExport);
  }
}

async function loadDataQuality(): Promise<ProductDataQualityStatus> {
  if (typeof fetch !== "function") {
    return cloneDataQuality(defaultDataQuality);
  }
  try {
    const response = await fetch(getDataQualityUrl(), {
      method: "GET",
      headers: { Accept: "application/json" }
    });
    if (!response.ok) {
      return cloneDataQuality(defaultDataQuality);
    }
    const packet = (await response.json()) as ProductDataQualityStatus;
    return normalizeDataQuality(packet);
  } catch {
    return cloneDataQuality(defaultDataQuality);
  }
}

async function loadOperatorActions(): Promise<ProductOperatorActions> {
  if (typeof fetch !== "function") {
    return cloneOperatorActions(defaultOperatorActions);
  }
  try {
    const response = await fetch(getOperatorActionsUrl(), {
      method: "GET",
      headers: { Accept: "application/json" }
    });
    if (!response.ok) {
      return cloneOperatorActions(defaultOperatorActions);
    }
    const packet = (await response.json()) as ProductOperatorActions;
    return normalizeOperatorActions(packet);
  } catch {
    return cloneOperatorActions(defaultOperatorActions);
  }
}

async function loadCockpitManifest(): Promise<ProductCockpitManifest> {
  if (typeof fetch !== "function") {
    return cloneCockpitManifest(defaultCockpitManifest);
  }
  try {
    const response = await fetch(getCockpitManifestUrl(), {
      method: "GET",
      headers: { Accept: "application/json" }
    });
    if (!response.ok) {
      return cloneCockpitManifest(defaultCockpitManifest);
    }
    const packet = (await response.json()) as ProductCockpitManifest;
    return normalizeCockpitManifest(packet);
  } catch {
    return cloneCockpitManifest(defaultCockpitManifest);
  }
}

function normalizeProductReadiness(packet: ProductReadinessStatus): ProductReadinessStatus {
  const checks = Array.isArray(packet.checks) ? packet.checks : [];
  const blockingReasons = Array.isArray(packet.blocking_reasons) ? packet.blocking_reasons.map(String) : [];
  return {
    status: packet.status === "Z_MATRIX_LOCAL_PRODUCT_READINESS_PASS" ? "Z_MATRIX_LOCAL_PRODUCT_READINESS_PASS" : "Z_MATRIX_LOCAL_PRODUCT_READINESS_BLOCKED",
    scope: "LOCAL_PERSONAL_RESEARCH_WORKSTATION",
    checks: checks.map((item) => ({
      id: String(item.id ?? "readiness-check"),
      ready: Boolean(item.ready),
      evidence: String(item.evidence ?? ""),
      missing_required_keys: Array.isArray(item.missing_required_keys) ? item.missing_required_keys.map(String) : undefined,
      unsafe_example_value_keys: Array.isArray(item.unsafe_example_value_keys) ? item.unsafe_example_value_keys.map(String) : undefined,
      value_material: item.value_material === "NOT_EMITTED" ? "NOT_EMITTED" : undefined
    })),
    blocking_reasons: blockingReasons,
    summary: {
      cockpit_packets: Number(packet.summary?.cockpit_packets ?? 0),
      cockpit_routes: Number(packet.summary?.cockpit_routes ?? 0),
      registered_skills: Number(packet.summary?.registered_skills ?? 0),
      research_capabilities: Number(packet.summary?.research_capabilities ?? 0),
      ready_research_capabilities: Number(packet.summary?.ready_research_capabilities ?? 0),
      research_evidence_groups: Number(packet.summary?.research_evidence_groups ?? 0),
      report_export_artifacts: Number(packet.summary?.report_export_artifacts ?? 0),
      data_quality_evidence: Number(packet.summary?.data_quality_evidence ?? 0),
      local_vendor_manifests: Number(packet.summary?.local_vendor_manifests ?? 0),
      agent_intents: Number(packet.summary?.agent_intents ?? 0),
      operator_actions: Number(packet.summary?.operator_actions ?? 0),
      config_templates: Number(packet.summary?.config_templates ?? 0),
      configured_secret_refs: Number(packet.summary?.configured_secret_refs ?? 0),
      required_secret_refs: Number(packet.summary?.required_secret_refs ?? defaultProductReadiness.summary.required_secret_refs)
    },
    safety: {
      alpha_claim: "BLOCKED",
      promotion: "BLOCKED",
      broker_runtime: "BLOCKED",
      real_trade: "BLOCKED",
      agent_direct_mutation: "BLOCKED"
    }
  };
}

function normalizeProductRuntime(packet: ProductRuntimeStatus): ProductRuntimeStatus {
  return {
    status: packet.status === "Z_MATRIX_PRODUCT_RUNTIME_READY" ? "Z_MATRIX_PRODUCT_RUNTIME_READY" : "Z_MATRIX_PRODUCT_RUNTIME_DEGRADED",
    service: {
      name: packet.service?.name ?? defaultProductRuntime.service.name,
      host: packet.service?.host ?? defaultProductRuntime.service.host,
      port: Number(packet.service?.port ?? defaultProductRuntime.service.port)
    },
    cockpit: {
      ready: Boolean(packet.cockpit?.ready),
      packet_count: Number(packet.cockpit?.packet_count ?? 0),
      required_packet_count: Number(packet.cockpit?.required_packet_count ?? defaultProductRuntime.cockpit.required_packet_count),
      missing: Array.isArray(packet.cockpit?.missing) ? [...packet.cockpit.missing] : []
    },
    registry: {
      ready: Boolean(packet.registry?.ready),
      skill_count: Number(packet.registry?.skill_count ?? 0),
      domain_count: Number(packet.registry?.domain_count ?? 0),
      concrete_skill_count: Number(packet.registry?.concrete_skill_count ?? 0)
    },
    data_source: {
      ready: Boolean(packet.data_source?.ready),
      manifest_count: Number(packet.data_source?.manifest_count ?? 0),
      mode: packet.data_source?.mode ?? defaultProductRuntime.data_source.mode
    },
    config: {
      ready: Boolean(packet.config?.ready),
      template_count: Number(packet.config?.template_count ?? defaultProductRuntime.config.template_count),
      ready_count: Number(packet.config?.ready_count ?? 0),
      configured_secret_refs: Number(packet.config?.configured_secret_refs ?? 0),
      required_secret_refs: Number(packet.config?.required_secret_refs ?? defaultProductRuntime.config.required_secret_refs),
      env_reference_policy: "PROCESS_ENV_ONLY_NO_VALUES_EMITTED",
      env_references: normalizeEnvReferences(packet.config?.env_references),
      secret_material_policy: "TEMPLATE_KEYS_ONLY_ENV_VALUES_NEVER_EMITTED"
    },
    safety: {
      alpha_claim: "BLOCKED",
      promotion: "BLOCKED",
      broker_runtime: "BLOCKED",
      real_trade: "BLOCKED",
      agent_direct_mutation: "BLOCKED",
      secret_storage: "ENV_ONLY"
    }
  };
}

function normalizeEnvReferences(value: ProductRuntimeStatus["config"]["env_references"] | undefined): ProductRuntimeStatus["config"]["env_references"] {
  const refs = Array.isArray(value) ? value : defaultProductRuntime.config.env_references;
  return refs.map((item) => ({
    key: String(item.key ?? ""),
    configured: Boolean(item.configured),
    source: "PROCESS_ENV",
    value_material: "NOT_EMITTED"
  }));
}

function cloneOperatorActions(packet: ProductOperatorActions): ProductOperatorActions {
  return {
    ...packet,
    actions: packet.actions.map((action) => ({
      ...action,
      safety: { ...action.safety }
    }))
  };
}

function normalizeOperatorActions(packet: ProductOperatorActions): ProductOperatorActions {
  const actions = Array.isArray(packet.actions) ? packet.actions : [];
  return {
    status: packet.status === "Z_MATRIX_OPERATOR_ACTIONS_READY" ? "Z_MATRIX_OPERATOR_ACTIONS_READY" : "Z_MATRIX_OPERATOR_ACTIONS_DEGRADED",
    auto_run_enabled: false,
    human_review_required: true,
    actions: actions.map((action) => ({
      id: String(action.id ?? "local-action"),
      label: String(action.label ?? "本地工作台动作"),
      category: normalizeOperatorCategory(action.category),
      command: String(action.command ?? ""),
      detail: String(action.detail ?? ""),
      expected: String(action.expected ?? ""),
      mode: "LOCAL_TERMINAL_MANUAL",
      safety: {
        alpha_claim: "BLOCKED",
        promotion: "BLOCKED",
        broker_runtime: "BLOCKED",
        real_trade: "BLOCKED",
        secret_storage: "ENV_ONLY"
      }
    }))
  };
}

function normalizeOperatorCategory(value: ProductOperatorAction["category"]): ProductOperatorAction["category"] {
  if (value === "health" || value === "verification" || value === "research" || value === "cockpit" || value === "package") {
    return value;
  }
  return "health";
}

function cloneResearchStatus(packet: ProductResearchStatus): ProductResearchStatus {
  return {
    ...packet,
    capabilities: packet.capabilities.map((item) => ({
      ...item,
      evidence_paths: [...item.evidence_paths],
      missing_paths: [...item.missing_paths]
    })),
    report_export: { ...packet.report_export },
    monthly_refresh: {
      ...packet.monthly_refresh,
      safety: { ...packet.monthly_refresh.safety }
    },
    safety: { ...packet.safety }
  };
}

function cloneResearchEvidence(packet: ProductResearchEvidenceIndex): ProductResearchEvidenceIndex {
  return {
    ...packet,
    groups: packet.groups.map((group) => ({
      ...group,
      artifacts: group.artifacts.map((artifact) => ({ ...artifact }))
    })),
    safety: { ...packet.safety }
  };
}

function normalizeResearchEvidence(packet: ProductResearchEvidenceIndex): ProductResearchEvidenceIndex {
  const groups = Array.isArray(packet.groups) ? packet.groups : [];
  const normalizedGroups = groups.map((group) => ({
    id: String(group.id ?? "research-evidence"),
    label: String(group.label ?? "研究证据"),
    summary: String(group.summary ?? ""),
    status: group.status === "READY" ? ("READY" as const) : ("PARTIAL" as const),
    ready_count: Number(group.ready_count ?? 0),
    required_count: Number(group.required_count ?? 0),
    artifacts: Array.isArray(group.artifacts)
      ? group.artifacts.map((artifact) => ({
          path: String(artifact.path ?? ""),
          ready: Boolean(artifact.ready),
          bytes: Number(artifact.bytes ?? 0),
          artifact_type: String(artifact.artifact_type ?? "file"),
          status_field: String(artifact.status_field ?? "")
        }))
      : [],
    safety: "RESEARCH_ONLY_NO_ALPHA_PROMOTION" as const
  }));
  return {
    status: packet.status === "Z_MATRIX_RESEARCH_EVIDENCE_INDEX_READY" ? "Z_MATRIX_RESEARCH_EVIDENCE_INDEX_READY" : "Z_MATRIX_RESEARCH_EVIDENCE_INDEX_PARTIAL",
    group_count: Number(packet.group_count ?? normalizedGroups.length),
    ready_group_count: Number(packet.ready_group_count ?? normalizedGroups.filter((group) => group.status === "READY").length),
    groups: normalizedGroups,
    artifact_policy: "LOCAL_RESEARCH_EVIDENCE_ONLY",
    safety: {
      alpha_claim: "BLOCKED",
      promotion: "BLOCKED",
      broker_runtime: "BLOCKED",
      real_trade: "BLOCKED",
      evidence_to_alpha_promotion: "BLOCKED"
    }
  };
}

function cloneReportExport(packet: ProductReportExportStatus): ProductReportExportStatus {
  return {
    ...packet,
    sample_artifacts: [...packet.sample_artifacts],
    data_policy: { ...packet.data_policy },
    safety: { ...packet.safety }
  };
}

function normalizeReportExport(packet: ProductReportExportStatus): ProductReportExportStatus {
  return {
    status: packet.status === "Z_MATRIX_REPORT_EXPORT_READY" ? "Z_MATRIX_REPORT_EXPORT_READY" : "Z_MATRIX_REPORT_EXPORT_EMPTY",
    command: String(packet.command ?? defaultReportExport.command),
    default_output_dir: String(packet.default_output_dir ?? defaultReportExport.default_output_dir),
    artifact_count: Number(packet.artifact_count ?? 0),
    doc_artifact_count: Number(packet.doc_artifact_count ?? 0),
    runtime_artifact_count: Number(packet.runtime_artifact_count ?? 0),
    sample_artifacts: Array.isArray(packet.sample_artifacts) ? packet.sample_artifacts.map(String) : [],
    artifact_policy: "LOCAL_FILES_ONLY",
    data_policy: {
      raw_vendor_data_included: false,
      private_account_data_included: false,
      secret_files_included: false,
      local_files_only: true
    },
    safety: {
      alpha_claim: "BLOCKED",
      promotion: "BLOCKED",
      broker_runtime: "BLOCKED",
      real_trade: "BLOCKED"
    }
  };
}

function cloneDataQuality(packet: ProductDataQualityStatus): ProductDataQualityStatus {
  return {
    ...packet,
    data_source: {
      ...packet.data_source,
      endpoints: [...packet.data_source.endpoints],
      window: { ...packet.data_source.window }
    },
    quality_evidence: {
      ...packet.quality_evidence,
      items: packet.quality_evidence.items.map((item) => ({ ...item }))
    },
    source_health: {
      ...packet.source_health,
      sources: packet.source_health.sources.map((item) => ({ ...item }))
    },
    privacy_guardrail: {
      ...packet.privacy_guardrail,
      violations: [...packet.privacy_guardrail.violations]
    },
    refresh_dry_plan: { ...packet.refresh_dry_plan },
    data_policy: { ...packet.data_policy },
    safety: { ...packet.safety }
  };
}

function normalizeDataQuality(packet: ProductDataQualityStatus): ProductDataQualityStatus {
  const evidenceItems = Array.isArray(packet.quality_evidence?.items) ? packet.quality_evidence.items : [];
  const sources = Array.isArray(packet.source_health?.sources) ? packet.source_health.sources : [];
  const violations = Array.isArray(packet.privacy_guardrail?.violations) ? packet.privacy_guardrail.violations : [];
  return {
    status: packet.status === "Z_MATRIX_DATA_QUALITY_STATUS_READY" ? "Z_MATRIX_DATA_QUALITY_STATUS_READY" : "Z_MATRIX_DATA_QUALITY_STATUS_DEGRADED",
    data_source: {
      ready: Boolean(packet.data_source?.ready),
      path: String(packet.data_source?.path ?? defaultDataQuality.data_source.path),
      resolved_path: String(packet.data_source?.resolved_path ?? defaultDataQuality.data_source.resolved_path),
      manifest_count: Number(packet.data_source?.manifest_count ?? 0),
      latest_manifest: String(packet.data_source?.latest_manifest ?? ""),
      latest_run_id: String(packet.data_source?.latest_run_id ?? ""),
      latest_manifest_status: String(packet.data_source?.latest_manifest_status ?? ""),
      source_vendor: String(packet.data_source?.source_vendor ?? "TUSHARE"),
      write_scope: "LOCAL_VENDOR_STORE_ONLY",
      symbol_count: Number(packet.data_source?.symbol_count ?? 0),
      file_count: Number(packet.data_source?.file_count ?? 0),
      failure_count: Number(packet.data_source?.failure_count ?? 0),
      endpoint_count: Number(packet.data_source?.endpoint_count ?? 0),
      endpoints: Array.isArray(packet.data_source?.endpoints) ? packet.data_source.endpoints.map(String) : [],
      window: {
        start_date: String(packet.data_source?.window?.start_date ?? ""),
        end_date: String(packet.data_source?.window?.end_date ?? ""),
        years: Number(packet.data_source?.window?.years ?? 0)
      },
      mode: "LOCAL_VENDOR_STORE_ONLY"
    },
    quality_evidence: {
      ready_count: Number(packet.quality_evidence?.ready_count ?? 0),
      required_count: Number(packet.quality_evidence?.required_count ?? defaultDataQuality.quality_evidence.required_count),
      items: evidenceItems.map((item) => ({
        id: String(item.id ?? "data-quality-evidence"),
        label: String(item.label ?? "数据质量证据"),
        path: String(item.path ?? ""),
        ready: Boolean(item.ready),
        bytes: Number(item.bytes ?? 0),
        status_field: String(item.status_field ?? ""),
        artifact_type: String(item.artifact_type ?? "file")
      }))
    },
    source_health: {
      status: packet.source_health?.status === "SOURCE_HEALTH_LEDGER_READY" ? "SOURCE_HEALTH_LEDGER_READY" : "SOURCE_HEALTH_LEDGER_EMPTY",
      ledger_path: String(packet.source_health?.ledger_path ?? defaultDataQuality.source_health.ledger_path),
      source_count: Number(packet.source_health?.source_count ?? 0),
      usable_count: Number(packet.source_health?.usable_count ?? 0),
      sources: sources.map((item) => ({
        source_id: String(item.source_id ?? ""),
        ok_count: Number(item.ok_count ?? 0),
        error_count: Number(item.error_count ?? 0),
        freshness_status: String(item.freshness_status ?? "UNKNOWN"),
        usable_now: Boolean(item.usable_now),
        blocked_reason: String(item.blocked_reason ?? "")
      }))
    },
    privacy_guardrail: {
      status: packet.privacy_guardrail?.status === "FAILED" ? "FAILED" : "PASS",
      scan_scope: "GIT_TRACKED_MARKET_DATA_FILES",
      tracked_private_market_data_violation_count: Number(packet.privacy_guardrail?.tracked_private_market_data_violation_count ?? 0),
      violations: violations.map(String),
      production_allowed: false
    },
    refresh_dry_plan: {
      command: String(packet.refresh_dry_plan?.command ?? defaultDataQuality.refresh_dry_plan.command),
      mode: "LOCAL_TERMINAL_MANUAL_DRY_PLAN",
      write_scope: "LOCAL_VENDOR_STORE_ONLY",
      auto_run_enabled: false
    },
    data_policy: {
      raw_vendor_data_included: false,
      private_account_data_included: false,
      secret_files_included: false,
      repository_commit_allowed: false,
      local_vendor_store_only: true
    },
    safety: {
      alpha_claim: "BLOCKED",
      promotion: "BLOCKED",
      broker_runtime: "BLOCKED",
      real_trade: "BLOCKED"
    }
  };
}

function cloneCockpitManifest(packet: ProductCockpitManifest): ProductCockpitManifest {
  return {
    ...packet,
    routes: packet.routes.map((route) => ({
      ...route,
      safety: { ...route.safety }
    })),
    safety: { ...packet.safety }
  };
}

function normalizeCockpitManifest(packet: ProductCockpitManifest): ProductCockpitManifest {
  const routes = Array.isArray(packet.routes) ? packet.routes : [];
  const normalizedRoutes = routes.map((route) => ({
    id: String(route.id ?? "cockpit-route"),
    label: String(route.label ?? "驾驶舱页面"),
    route: String(route.route ?? "/"),
    capability: String(route.capability ?? "readonly_cockpit_packet"),
    packet_file: String(route.packet_file ?? ""),
    api_path: String(route.api_path ?? ""),
    ready: Boolean(route.ready),
    bytes: Number(route.bytes ?? 0),
    mode: "READ_ONLY_PACKET" as const,
    safety: {
      paper_only: true as const,
      human_review_required: true as const,
      broker_runtime: "BLOCKED" as const,
      real_trade: "BLOCKED" as const
    }
  }));
  return {
    status: packet.status === "Z_MATRIX_COCKPIT_MANIFEST_READY" ? "Z_MATRIX_COCKPIT_MANIFEST_READY" : "Z_MATRIX_COCKPIT_MANIFEST_DEGRADED",
    public_root: String(packet.public_root ?? defaultCockpitManifest.public_root),
    route_count: Number(packet.route_count ?? normalizedRoutes.length),
    ready_count: Number(packet.ready_count ?? normalizedRoutes.filter((route) => route.ready).length),
    routes: normalizedRoutes,
    safety: {
      alpha_claim: "BLOCKED",
      promotion: "BLOCKED",
      broker_runtime: "BLOCKED",
      real_trade: "BLOCKED",
      agent_direct_mutation: "BLOCKED"
    }
  };
}

function normalizeResearchStatus(packet: ProductResearchStatus): ProductResearchStatus {
  const capabilities = Array.isArray(packet.capabilities) ? packet.capabilities : [];
  return {
    status: packet.status === "Z_MATRIX_RESEARCH_STATUS_READY" ? "Z_MATRIX_RESEARCH_STATUS_READY" : "Z_MATRIX_RESEARCH_STATUS_DEGRADED",
    capability_count: Number(packet.capability_count ?? capabilities.length),
    ready_count: Number(packet.ready_count ?? 0),
    capabilities: capabilities.map((item) => ({
      id: String(item.id ?? "research-capability"),
      label: String(item.label ?? "研究能力状态"),
      summary: String(item.summary ?? ""),
      status: item.status === "READY" ? "READY" : "PARTIAL",
      available_count: Number(item.available_count ?? 0),
      required_count: Number(item.required_count ?? 0),
      evidence_paths: Array.isArray(item.evidence_paths) ? item.evidence_paths.map(String) : [],
      missing_paths: Array.isArray(item.missing_paths) ? item.missing_paths.map(String) : [],
      module_count: Number(item.module_count ?? 0),
      safety: "RESEARCH_ONLY"
    })),
    report_export: {
      status: packet.report_export?.status === "LOCAL_EXPORT_READY" ? "LOCAL_EXPORT_READY" : "LOCAL_EXPORT_PLANNED",
      command: String(packet.report_export?.command ?? defaultResearchStatus.report_export.command),
      artifact_policy: "LOCAL_FILES_ONLY"
    },
    monthly_refresh: {
      status: packet.monthly_refresh?.status === "MONTHLY_REFRESH_DRY_PLAN_READY" ? "MONTHLY_REFRESH_DRY_PLAN_READY" : "MONTHLY_REFRESH_DEGRADED",
      ready_count: Number(packet.monthly_refresh?.ready_count ?? 0),
      required_count: Number(packet.monthly_refresh?.required_count ?? defaultResearchStatus.monthly_refresh.required_count),
      command: String(packet.monthly_refresh?.command ?? defaultResearchStatus.monthly_refresh.command),
      mode: "LOCAL_TERMINAL_MANUAL_DRY_PLAN",
      safety: {
        alpha_claim: "BLOCKED",
        promotion: "BLOCKED",
        broker_runtime: "BLOCKED",
        real_trade: "BLOCKED"
      }
    },
    safety: {
      alpha_claim: "BLOCKED",
      promotion: "BLOCKED",
      broker_runtime: "BLOCKED",
      real_trade: "BLOCKED"
    }
  };
}

export async function createSettingsActionDraft(
  session: AuthSession | null,
  action: SettingsAction,
  payload: Record<string, unknown> = {}
): Promise<SettingsActionDraft> {
  const current = requireSession(session);
  ensureNoClientTenantFields(payload);

  if (action === "SAVE_SECRET_REFERENCE") {
    const provider = String(payload.provider ?? "tushare");
    const rawSecret = String(payload.rawSecret ?? "");
    const saved = await saveDataSourceSecret(current, provider, rawSecret);
    return {
      draftId: `settings-secret-${Date.now()}`,
      workspaceId: saved.workspaceId,
      status: "REFERENCE_SAVED",
      humanReviewRequired: true,
      auditEvent: "SAVE_SETTINGS_SECRET_REFERENCE",
      userMessage: "密钥引用已保存，原文不会显示在页面中。",
      tokenPreview: saved.tokenPreview,
      secretRef: saved.secretRef
    };
  }

  if (action === "SAVE_LLM_SECRET_REFERENCE") {
    const provider = String(payload.provider ?? "deepseek");
    const rawSecret = String(payload.rawSecret ?? "");
    const saved = await saveDataSourceSecret(current, `llm-${provider}`, rawSecret);
    return {
      draftId: `settings-llm-secret-${Date.now()}`,
      workspaceId: saved.workspaceId,
      status: "REFERENCE_SAVED",
      humanReviewRequired: true,
      auditEvent: "SAVE_SETTINGS_LLM_SECRET_REFERENCE",
      userMessage: "大模型 API 密钥引用已保存，原文不会显示在页面中。",
      tokenPreview: saved.tokenPreview,
      secretRef: saved.secretRef
    };
  }

  const auditEventByAction: Record<Exclude<SettingsAction, "SAVE_SECRET_REFERENCE" | "SAVE_LLM_SECRET_REFERENCE">, SettingsActionDraft["auditEvent"]> = {
    SAVE_ACCOUNT_DISPLAY_DRAFT: "SAVE_SETTINGS_ACCOUNT_DISPLAY",
    TEST_DATA_SOURCE: "TEST_SETTINGS_DATA_SOURCE",
    VALIDATE_LOCAL_IMPORT_DRAFT: "VALIDATE_SETTINGS_LOCAL_IMPORT",
    TEST_LLM_PROVIDER: "TEST_SETTINGS_LLM_PROVIDER",
    SAVE_ASSISTANT_PREFERENCE_DRAFT: "SAVE_SETTINGS_ASSISTANT_PREFERENCE",
    PREVIEW_COPY_MODE: "PREVIEW_SETTINGS_COPY_MODE",
    PREVIEW_THEME_MODE: "PREVIEW_SETTINGS_THEME_MODE",
    PREVIEW_FONT_SCALE: "PREVIEW_SETTINGS_FONT_SCALE",
    SAVE_SETTINGS_DRAFT: "CREATE_SETTINGS_CHANGE_DRAFT",
    EXPORT_SETTINGS_AUDIT_PACK: "EXPORT_SETTINGS_AUDIT_PACK",
    CREATE_BACKUP_RESTORE_DRAFT: "CREATE_BACKUP_RESTORE_DRAFT"
  };
  const auditEvent = auditEventByAction[action];
  const response = await createWorkspaceDraft(current, payload, auditEvent);
  const copyMode = payload.copyMode === "plain" || payload.copyMode === "english" || payload.copyMode === "tianji" ? payload.copyMode : undefined;
  const themeMode = payload.themeMode === "dark" || payload.themeMode === "light" ? payload.themeMode : undefined;
  const fontScale =
    payload.fontScale === "small" || payload.fontScale === "standard" || payload.fontScale === "large" ? payload.fontScale : undefined;

  const userMessageByAction: Record<Exclude<SettingsAction, "SAVE_SECRET_REFERENCE" | "SAVE_LLM_SECRET_REFERENCE">, string> = {
    SAVE_ACCOUNT_DISPLAY_DRAFT: "账户显示草案已生成，等待人工确认。",
    TEST_DATA_SOURCE: "数据源测试已记录，等待人工确认结果。",
    VALIDATE_LOCAL_IMPORT_DRAFT: "本地导入校验草案已生成，等待人工确认。",
    TEST_LLM_PROVIDER: "大模型 API 连通测试已记录，等待人工确认结果。",
    SAVE_ASSISTANT_PREFERENCE_DRAFT: "随侍童子偏好草案已生成，等待人工确认。",
    PREVIEW_COPY_MODE: "文字表达预览已生成，保存后只影响当前用户显示。",
    PREVIEW_THEME_MODE: "主题预览已应用，保存后只影响当前用户显示。",
    PREVIEW_FONT_SCALE: "文字大小预览已应用，保存后只影响当前用户显示。",
    SAVE_SETTINGS_DRAFT: "设置变更草案已生成，等待人工确认。",
    EXPORT_SETTINGS_AUDIT_PACK: "配置审计包已准备好。",
    CREATE_BACKUP_RESTORE_DRAFT: "恢复备份草案已生成，等待人工确认。"
  };

  return {
    draftId: `settings-action-${Date.now()}`,
    workspaceId: response.workspaceId,
    status: action === "EXPORT_SETTINGS_AUDIT_PACK" ? "AUDIT_PACK_READY" : "DRAFT_CREATED",
    humanReviewRequired: true,
    auditEvent,
    userMessage: userMessageByAction[action],
    copyMode,
    themeMode,
    fontScale
  };
}
