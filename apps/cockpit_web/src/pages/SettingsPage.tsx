import {
  Archive,
  ArrowLeft,
  Bot,
  BrainCircuit,
  CheckCircle2,
  ChevronRight,
  ClipboardCheck,
  Database,
  Download,
  Eye,
  FileKey2,
  FileUp,
  KeyRound,
  Languages,
  Palette,
  Clipboard,
  RefreshCcw,
  Save,
  Server,
  ShieldCheck,
  Type,
  UserRoundCog
} from "lucide-react";
import { useState } from "react";
import type { AuthSession } from "../auth";
import { useSettings, useSettingsAction } from "../hooks/useSettings";
import type {
  CopyMode,
  FontScale,
  LlmProviderStatus,
  SettingsCategoryId,
  SettingsDrilldownItem,
  ThemeMode
} from "../services/settingsApi";
import { useCockpitPreferences } from "../settings/CockpitPreferences";

type SettingsPageProps = {
  session: AuthSession;
};

const categoryIcons: Record<SettingsCategoryId, typeof UserRoundCog> = {
  account: UserRoundCog,
  data: Database,
  llm: BrainCircuit,
  assistant: Bot,
  safety: ShieldCheck,
  appearance: Languages,
  backup: Archive
};

const copyModeMeta: Record<CopyMode, { label: string; detail: string }> = {
  tianji: { label: "天机版", detail: "保留当前驾驶舱语气" },
  plain: { label: "通用版", detail: "简洁中文，不用黑话" },
  english: { label: "English", detail: "English UI copy" }
};

const fontScaleMeta: Record<FontScale, { label: string; detail: string }> = {
  small: { label: "小号", detail: "适合宽屏密集阅读" },
  standard: { label: "标准", detail: "保持当前驾驶舱比例" },
  large: { label: "大号", detail: "提升远距离阅读舒适度" }
};

const themeModeMeta: Record<ThemeMode, { label: string; detail: string }> = {
  dark: { label: "深色", detail: "黑金驾驶舱默认主题" },
  light: { label: "浅色", detail: "白天环境的低眩光主题" }
};

const operatorCategoryLabel = {
  health: "体检",
  verification: "验证",
  research: "研究",
  cockpit: "驾驶舱",
  package: "打包"
} as const;

export function SettingsPage({ session }: SettingsPageProps) {
  const { data, isLoading, isError } = useSettings(session);
  const action = useSettingsAction(session);
  const {
    copy,
    copyMode: selectedCopyMode,
    fontScale: selectedFontScale,
    themeMode: selectedThemeMode,
    setCopyMode,
    setFontScale,
    setThemeMode
  } = useCockpitPreferences();
  const [activeCategory, setActiveCategory] = useState<SettingsCategoryId>("llm");
  const [activeDrilldown, setActiveDrilldown] = useState<SettingsDrilldownItem | null>(null);
  const [selectedLlmProvider, setSelectedLlmProvider] = useState("deepseek");
  const [llmSecretInput, setLlmSecretInput] = useState("");
  const [tokenInput, setTokenInput] = useState("");
  const latestDraft = action.data;

  if (isLoading || !data) {
    return <main className="settings-page">加载系统设置数据</main>;
  }

  if (isError) {
    return <main className="settings-page">当前系统设置暂不可用</main>;
  }

  const settingsData = data;
  const selectedProvider = settingsData.llmProviders.find((provider) => provider.id === selectedLlmProvider) ?? settingsData.llmProviders[0];
  const runtime = settingsData.productRuntime;
  const runtimeReady = runtime.status === "Z_MATRIX_PRODUCT_RUNTIME_READY";

  function submitSettingsAction(actionName: Parameters<typeof action.mutate>[0]["action"], payload: Record<string, unknown> = {}) {
    action.mutate({
      action: actionName,
      payload: {
        source: "settings-page",
        ...payload
      }
    });
  }

  function chooseCategory(categoryId: SettingsCategoryId) {
    setActiveCategory(categoryId);
    setActiveDrilldown(null);
  }

  function openDrilldown(item: SettingsDrilldownItem) {
    setActiveCategory(item.categoryId);
    setActiveDrilldown(item);
    if (item.categoryId === "llm" && item.targetId) {
      setSelectedLlmProvider(item.targetId);
    }
  }

  function previewCopyMode(mode: CopyMode) {
    setCopyMode(mode);
    submitSettingsAction("PREVIEW_COPY_MODE", { copyMode: mode });
  }

  function previewThemeMode(mode: ThemeMode) {
    setThemeMode(mode);
    submitSettingsAction("PREVIEW_THEME_MODE", { themeMode: mode });
  }

  function previewFontScale(scale: FontScale) {
    setFontScale(scale);
    submitSettingsAction("PREVIEW_FONT_SCALE", { fontScale: scale });
  }

  const activeCategoryCopy = settingsData.categories.find((category) => category.id === activeCategory) ?? settingsData.categories[0];
  const activeCategoryLabel = copy(`settings.category.${activeCategoryCopy.id}.label`, activeCategoryCopy.label);
  const activeCategorySummary = copy(`settings.category.${activeCategoryCopy.id}.summary`, activeCategoryCopy.summary);

  return (
    <main className="settings-page" aria-labelledby="settings-title">
      <section className="holdings-heading settings-heading">
        <div className="heading-copy">
          <div className="heading-title-line">
            <h1 id="settings-title">{copy("settings.page.title", settingsData.title)}</h1>
          </div>
          <p>{copy("settings.page.subtitle", settingsData.subtitle)}</p>
        </div>
      </section>

      {renderSettingsStatusBar()}
      {renderOperatorActions()}
      {renderResearchStatus()}

      <section className="settings-layout" aria-label="系统设置工作区">
        <aside className="settings-category-rail panel-shell" aria-label="设置分类">
          <div className="panel-title">
            <span>设置分类</span>
            <small>{activeCategoryCopy.status}</small>
          </div>
          <div className="settings-category-list">
            {settingsData.categories.map((category) => {
              const Icon = categoryIcons[category.id];
              const categoryLabel = copy(`settings.category.${category.id}.label`, category.label);
              const categorySummary = copy(`settings.category.${category.id}.summary`, category.summary);
              return (
                <button
                  type="button"
                  className={`settings-category-button${category.id === activeCategory ? " is-active" : ""}`}
                  key={category.id}
                  onClick={() => chooseCategory(category.id)}
                >
                  <Icon size={17} aria-hidden="true" />
                  <span>
                    <strong>{categoryLabel}</strong>
                    <small>{categorySummary}</small>
                  </span>
                  <em>{category.status}</em>
                </button>
              );
            })}
          </div>
        </aside>

        <section
          className="settings-detail panel-shell"
          aria-label={`${activeCategoryLabel}设置详情`}
          key={`settings-detail-${activeCategory}-${activeDrilldown?.id ?? "overview"}`}
        >
          {activeDrilldown ? (
            renderDrilldown(activeDrilldown)
          ) : (
            <>
              <div className="panel-title settings-detail-title" data-no-localize>
                <span>{activeCategoryLabel}</span>
                <small>{activeCategorySummary}</small>
              </div>

              {renderCategoryBody()}
            </>
          )}
        </section>
      </section>
    </main>
  );

  function renderSettingsStatusBar() {
    return (
      <section className="settings-status-bar panel-shell" aria-label="设置页统一状态栏">
        <article>
          <span>后端服务</span>
          <strong>{runtimeReady ? "READY" : "DEGRADED"}</strong>
          <small>{runtime.service.host}:{runtime.service.port}</small>
        </article>
        <article>
          <span>驾驶舱数据</span>
          <strong>{runtime.cockpit.packet_count}/{runtime.cockpit.required_packet_count}</strong>
          <small>{runtime.cockpit.ready ? "Packets ready" : `${runtime.cockpit.missing.length} missing`}</small>
        </article>
        <article>
          <span>SkillOS</span>
          <strong>{runtime.registry.skill_count}</strong>
          <small>{runtime.registry.concrete_skill_count} active paths</small>
        </article>
        <article>
          <span>安全保护</span>
          <strong>BLOCKED</strong>
          <small className="settings-status-chipline">
            <span>Paper-only</span>
            <span>Broker</span>
            <span>Real Trade</span>
          </small>
        </article>
        <article>
          <span>本地数据</span>
          <strong>{runtime.data_source.ready ? "READY" : "WAITING"}</strong>
          <small>{runtime.data_source.manifest_count} manifests</small>
        </article>
        <article>
          <span>配置模板</span>
          <strong>{runtime.config.ready_count}/{runtime.config.template_count}</strong>
          <small>{runtime.config.ready ? "ENV ONLY" : "Check templates"}</small>
        </article>
        <div className="settings-status-actions">
          <span>{latestDraft ? latestDraft.userMessage : "设置动作都会进入人审草案或审计记录。"}</span>
          <button type="button" onClick={() => submitSettingsAction("EXPORT_SETTINGS_AUDIT_PACK", { target: "settings-status" })}>
            <Download size={15} aria-hidden="true" />
            导出审计记录
          </button>
        </div>
      </section>
    );
  }

  function renderOperatorActions() {
    const actions = settingsData.operatorActions.actions;
    return (
      <section className="settings-operator-panel panel-shell" aria-label="本地工作台动作">
        <div className="panel-title">
          <span>本地工作台</span>
          <small>{settingsData.operatorActions.auto_run_enabled ? "自动启动" : "手动确认"}</small>
        </div>
        <div className="settings-operator-grid">
          {actions.map((item) => (
            <article className="settings-operator-card" key={item.id}>
              <div>
                <RefreshCcw size={16} aria-hidden="true" />
                <span>{item.label}</span>
                <em>{operatorCategoryLabel[item.category]}</em>
              </div>
              <p>{item.detail}</p>
              <code>{item.command}</code>
              <footer>
                <small>{item.expected}</small>
                <button
                  type="button"
                  onClick={() => {
                    void navigator.clipboard?.writeText(item.command);
                  }}
                >
                  <Clipboard size={14} aria-hidden="true" />
                  复制命令
                </button>
              </footer>
            </article>
          ))}
        </div>
      </section>
    );
  }

  function renderResearchStatus() {
    const status = settingsData.researchStatus;
    return (
      <section className="settings-research-panel panel-shell" aria-label="研究能力状态">
        <div className="panel-title">
          <span>研究能力状态</span>
          <small>{status.ready_count}/{status.capability_count} ready</small>
        </div>
        <div className="settings-research-grid">
          {status.capabilities.map((item) => (
            <article className="settings-research-card" key={item.id}>
              <div>
                <CheckCircle2 size={16} aria-hidden="true" />
                <span>{item.label}</span>
                <em className={item.status === "READY" ? "is-ready" : "is-partial"}>{item.status}</em>
              </div>
              <p>{item.summary}</p>
              <dl className="settings-compact-dl">
                <div><dt>证据</dt><dd>{item.available_count}/{item.required_count}</dd></div>
                <div><dt>模块</dt><dd>{item.module_count}</dd></div>
              </dl>
            </article>
          ))}
          <article className="settings-research-card settings-research-card--report">
            <div>
              <Download size={16} aria-hidden="true" />
              <span>报告导出</span>
              <em>{status.report_export.artifact_policy}</em>
            </div>
            <p>通过本地报告导出器输出 manifest、checksums 与可审计材料。</p>
            <code>{status.report_export.command}</code>
          </article>
          <article className="settings-research-card settings-research-card--report">
            <div>
              <RefreshCcw size={16} aria-hidden="true" />
              <span>月度刷新</span>
              <em>{status.monthly_refresh.status}</em>
            </div>
            <p>Forward OOS 等待、月度标签和本地数据刷新只生成 dry plan。</p>
            <dl className="settings-compact-dl">
              <div><dt>证据</dt><dd>{status.monthly_refresh.ready_count}/{status.monthly_refresh.required_count}</dd></div>
              <div><dt>模式</dt><dd>{status.monthly_refresh.mode}</dd></div>
            </dl>
            <code>{status.monthly_refresh.command}</code>
          </article>
        </div>
      </section>
    );
  }

  function renderCategoryBody() {
    if (activeCategory === "llm") {
      return (
        <section className="settings-llm-provider-grid" aria-label="大模型 API 供应商设置">
          {settingsData.llmProviders.map((provider) => (
            <button
              type="button"
              className={`settings-llm-provider-card${provider.id === selectedLlmProvider ? " is-active" : ""}`}
              key={provider.id}
              onClick={() => {
                setSelectedLlmProvider(provider.id);
                openDrilldown({
                  id: `llm-${provider.id}`,
                  categoryId: "llm",
                  label: provider.label,
                  summary: provider.detail,
                  status: provider.keyStatus === "未配置" ? "待配置" : "正常",
                  targetId: provider.id
                });
              }}
            >
              <div>
                <Server size={16} aria-hidden="true" />
                <span>{provider.region}</span>
                <em>{provider.keyStatus}</em>
              </div>
              <strong>{provider.label}</strong>
              <dl>
                <div>
                  <dt>端点</dt>
                  <dd>{provider.endpointMode}</dd>
                </div>
                <div>
                  <dt>默认模型</dt>
                  <dd>{provider.defaultModel}</dd>
                </div>
              </dl>
              <p>{provider.detail}</p>
              <small>点击配置 Base URL、模型与密钥引用</small>
            </button>
          ))}
        </section>
      );
    }

    if (activeCategory === "appearance") {
      return (
        <section className="settings-appearance-composer" aria-label="显示设置">
          <article className="settings-language-card" aria-label="文字表达模式" role="region">
            <div className="settings-language-head">
              <div>
                <Languages size={22} aria-hidden="true" />
                <span>文字表达</span>
                <strong>{copyModeMeta[selectedCopyMode].label}</strong>
              </div>
              <small>{copyModeMeta[selectedCopyMode].detail}</small>
            </div>
            {renderCopyModeControls()}
            {renderCopyPreview()}
          </article>

          <article className="settings-choice-card settings-display-card">
            <div>
              <Type size={21} aria-hidden="true" />
              <span>文字大小</span>
              <strong>{fontScaleMeta[selectedFontScale].label}</strong>
            </div>
            <div className="settings-segmented-control" role="radiogroup" aria-label="文字大小调节">
              {(Object.keys(fontScaleMeta) as FontScale[]).map((scale) => (
                <button
                  key={scale}
                  type="button"
                  role="radio"
                  aria-checked={selectedFontScale === scale}
                  className={selectedFontScale === scale ? "is-active" : ""}
                  onClick={() => previewFontScale(scale)}
                >
                  {fontScaleMeta[scale].label}
                </button>
              ))}
            </div>
            <p>{fontScaleMeta[selectedFontScale].detail}</p>
          </article>

          <article className="settings-choice-card settings-display-card">
            <div>
              <Palette size={21} aria-hidden="true" />
              <span>深浅主题</span>
              <strong>{themeModeMeta[selectedThemeMode].label}</strong>
            </div>
            <div className="settings-segmented-control" role="radiogroup" aria-label="深浅主题切换">
              {(Object.keys(themeModeMeta) as ThemeMode[]).map((mode) => (
                <button
                  key={mode}
                  type="button"
                  role="radio"
                  aria-checked={selectedThemeMode === mode}
                  className={selectedThemeMode === mode ? "is-active" : ""}
                  onClick={() => previewThemeMode(mode)}
                >
                  {themeModeMeta[mode].label}
                </button>
              ))}
            </div>
            <p>{themeModeMeta[selectedThemeMode].detail}</p>
          </article>

          <article className="settings-info-card">
            <Eye size={21} aria-hidden="true" />
            <span>页面密度</span>
            <strong>{settingsData.appearanceBackup.pageDensity}</strong>
            <p>保持驾驶舱信息密度，后续可扩展为紧凑/舒展。</p>
          </article>
        </section>
      );
    }

    if (activeCategory === "backup") {
      return renderBackupCategory();
    }

    if (activeCategory === "data") {
      return (
        <section className="settings-data-config-grid" aria-label="数据连接设置">
          {settingsData.dataSources.map((source) => (
            <article className="settings-detail-card settings-source-config-card" key={source.id}>
              <Database size={20} aria-hidden="true" />
              <span>{source.label}</span>
              <strong>{source.status}</strong>
              <p>{source.detail}</p>
              <dl className="settings-compact-dl">
                <div><dt>最近检查</dt><dd>{source.lastChecked}</dd></div>
                <div><dt>密钥</dt><dd>{source.secretPreview ?? "不需要密钥"}</dd></div>
              </dl>
              {source.id === "research-import" ? (
                <button type="button" onClick={() => submitSettingsAction("VALIDATE_LOCAL_IMPORT_DRAFT", { sourceId: source.id })}>
                  校验导入文件
                </button>
              ) : null}
              {source.id === "tushare" ? (
                <div className="settings-source-secret">
                  <label>
                    <span>Token 输入</span>
                    <input
                      value={tokenInput}
                      type="password"
                      placeholder="输入后保存为密钥引用"
                      onChange={(event) => setTokenInput(event.currentTarget.value)}
                    />
                  </label>
                  <div className="settings-inline-actions">
                    <button type="button" onClick={() => submitSettingsAction("TEST_DATA_SOURCE", { provider: source.id })}>
                      测试数据源
                    </button>
                    <button
                      type="button"
                      onClick={() =>
                        submitSettingsAction("SAVE_SECRET_REFERENCE", {
                          provider: source.id,
                          rawSecret: tokenInput || "demo-token-placeholder"
                        })
                      }
                    >
                      保存密钥引用
                    </button>
                  </div>
                </div>
              ) : null}
            </article>
          ))}
        </section>
      );
    }

    if (activeCategory === "safety") {
      return (
        <section className="settings-safety-composer" aria-label="安全保护设置">
          {renderSafetyLocks()}
          <article className="settings-detail-card settings-safety-note">
            <ShieldCheck size={22} aria-hidden="true" />
            <span>安全锁说明</span>
            <strong>只读锁定</strong>
            <p>本页只允许查看解释和导出记录，不提供关闭入口。</p>
            <button type="button" onClick={() => submitSettingsAction("EXPORT_SETTINGS_AUDIT_PACK", { target: "safety-locks" })}>
              导出安全锁审计
            </button>
          </article>
        </section>
      );
    }

    if (activeCategory === "assistant") {
      return renderAssistantDrilldown();
    }

    return renderAccountDrilldown();
  }

  function renderDrilldown(item: SettingsDrilldownItem) {
    return (
      <section className="settings-detail-shell" aria-label={`${item.label}下探详情`}>
        <div className="settings-drilldown-head">
          <button type="button" className="settings-back-button" onClick={() => setActiveDrilldown(null)}>
            <ArrowLeft size={16} aria-hidden="true" />
            返回
          </button>
          <div className="settings-breadcrumb">
            <span>{copy("settings.page.title", "系统设置")}</span>
            <ChevronRight size={14} aria-hidden="true" />
            <span>{activeCategoryLabel}</span>
            <ChevronRight size={14} aria-hidden="true" />
            <strong>{item.label}</strong>
          </div>
          <div className="settings-detail-actions">
            <button
              type="button"
              onClick={() =>
                submitSettingsAction("SAVE_SETTINGS_DRAFT", {
                  panel: item.id,
                  copyMode: selectedCopyMode,
                  themeMode: selectedThemeMode,
                  fontScale: selectedFontScale
                })
              }
            >
              <Save size={16} aria-hidden="true" />
              保存草案
            </button>
            <button type="button" onClick={() => submitSettingsAction("EXPORT_SETTINGS_AUDIT_PACK", { panel: item.id })}>
              <Download size={16} aria-hidden="true" />
              导出审计包
            </button>
          </div>
        </div>

        {latestDraft ? (
          <div className="settings-action-feedback" role="status">
            {latestDraft.userMessage}
          </div>
        ) : null}

        {activeCategory === "account" ? renderAccountDrilldown() : null}
        {activeCategory === "data" ? renderDataDrilldown(item) : null}
        {activeCategory === "llm" && selectedProvider ? renderLlmDrilldown(selectedProvider) : null}
        {activeCategory === "assistant" ? renderAssistantDrilldown() : null}
        {activeCategory === "safety" ? renderSafetyDrilldown() : null}
        {activeCategory === "appearance" ? renderAppearanceDrilldown(item) : null}
        {activeCategory === "backup" ? renderBackupDrilldown(item) : null}
      </section>
    );
  }

  function renderAccountDrilldown() {
    return (
      <div className="settings-form-grid">
        <label className="settings-field-card">
          <span>昵称</span>
          <input defaultValue={settingsData.accountDisplay.nickname} />
        </label>
        <label className="settings-field-card">
          <span>头像字母</span>
          <input defaultValue={settingsData.accountDisplay.avatarInitial} maxLength={2} />
        </label>
        <label className="settings-field-card">
          <span>账户显示名</span>
          <input defaultValue={settingsData.accountDisplay.accountDisplayName} />
        </label>
        <label className="settings-field-card">
          <span>默认首页</span>
          <select defaultValue={settingsData.accountDisplay.defaultHome}>
            <option value="/holdings">{copy("copy.holdings", "执仓决断")}</option>
            <option value="/selection">{copy("copy.selection", "投研问股")}</option>
            <option value="/dayan-ask">{copy("copy.dayan", "大衍天问")}</option>
            <option value="/control-compass">{copy("copy.compass", "天机罗盘")}</option>
            <option value="/history">{copy("copy.history", "时空回溯")}</option>
            <option value="/settings">{copy("copy.settings", "系统设置")}</option>
          </select>
        </label>
        <article className="settings-wide-card">
          <span>身份标签</span>
          <div className="settings-chip-row">
            {settingsData.accountDisplay.profileTags.map((tag) => (
              <em key={tag}>{tag}</em>
            ))}
          </div>
        </article>
        <div className="settings-action-row">
          <button type="button" onClick={() => submitSettingsAction("SAVE_ACCOUNT_DISPLAY_DRAFT", { target: "account-display" })}>
            <ClipboardCheck size={16} aria-hidden="true" />
            保存账户显示草案
          </button>
        </div>
      </div>
    );
  }

  function renderDataDrilldown(item: SettingsDrilldownItem) {
    const source = settingsData.dataSources.find((entry) => entry.id === item.targetId) ?? settingsData.dataSources[0];
    return (
      <div className="settings-form-grid">
        <article className="settings-detail-card">
          <FileKey2 size={22} aria-hidden="true" />
          <span>当前数据源</span>
          <strong>{source.label}</strong>
          <p>{source.detail}</p>
          <dl className="settings-compact-dl">
            <div><dt>状态</dt><dd>{source.status}</dd></div>
            <div><dt>最近检查</dt><dd>{source.lastChecked}</dd></div>
            <div><dt>密钥</dt><dd>{source.secretPreview ?? "不需要密钥"}</dd></div>
          </dl>
        </article>
        {source.id === "research-import" ? (
          <article className="settings-detail-card">
            <FileUp size={22} aria-hidden="true" />
            <span>本地数据导入</span>
            <strong>先校验，再生成导入草案</strong>
            <p>支持价格、财务与复盘文件的本地选择入口，当前不直接写正式数据。</p>
            <button type="button" onClick={() => submitSettingsAction("VALIDATE_LOCAL_IMPORT_DRAFT", { sourceId: source.id })}>
              校验导入文件
            </button>
          </article>
        ) : (
          <article className="settings-secret-card">
            <div>
              <KeyRound size={22} aria-hidden="true" />
              <span>Token 引用</span>
              <strong>{source.secretPreview ?? "***REDACTED***"}</strong>
              <p>保存后只显示密钥引用状态，不显示原文。</p>
            </div>
            <label>
              <span>Token 输入</span>
              <input
                value={tokenInput}
                type="password"
                placeholder="输入后保存为密钥引用"
                onChange={(event) => setTokenInput(event.currentTarget.value)}
              />
            </label>
            <div className="settings-action-row">
              <button type="button" onClick={() => submitSettingsAction("TEST_DATA_SOURCE", { provider: source.id })}>
                测试数据源
              </button>
              <button
                type="button"
                onClick={() =>
                  submitSettingsAction("SAVE_SECRET_REFERENCE", {
                    provider: source.id,
                    rawSecret: tokenInput || "demo-token-placeholder"
                  })
                }
              >
                保存密钥引用
              </button>
            </div>
          </article>
        )}
      </div>
    );
  }

  function renderLlmDrilldown(provider: LlmProviderStatus) {
    return (
      <div className="settings-provider-detail-grid" aria-label="大模型 API 提供商下探">
        <article className="settings-detail-card settings-provider-identity">
          <BrainCircuit size={24} aria-hidden="true" />
          <span>Provider</span>
          <strong>{provider.label}</strong>
          <p>{provider.detail}</p>
          <dl className="settings-compact-dl">
            <div><dt>区域</dt><dd>{provider.region}</dd></div>
            <div><dt>端点模式</dt><dd>{provider.endpointMode}</dd></div>
            <div><dt>最近测试</dt><dd>{provider.lastTested}</dd></div>
          </dl>
        </article>
        <label className="settings-field-card">
          <span>供应商</span>
          <select value={selectedLlmProvider} onChange={(event) => setSelectedLlmProvider(event.currentTarget.value)}>
            {settingsData.llmProviders.map((entry) => (
              <option key={entry.id} value={entry.id}>
                {entry.label}
              </option>
            ))}
          </select>
        </label>
        <label className="settings-field-card">
          <span>Base URL</span>
          <input defaultValue={provider.baseUrl} />
        </label>
        <label className="settings-field-card">
          <span>默认模型</span>
          <input defaultValue={provider.defaultModel} />
        </label>
        <label className="settings-field-card">
          <span>备用模型</span>
          <input defaultValue={provider.fallbackModel} />
        </label>
        <label className="settings-field-card">
          <span>API Key 引用</span>
          <input
            value={llmSecretInput}
            type="password"
            placeholder={provider.secretPreview ?? "输入后保存为密钥引用"}
            onChange={(event) => setLlmSecretInput(event.currentTarget.value)}
          />
          <small>{provider.keyStatus}</small>
        </label>
        <article className="settings-detail-card">
          <Server size={22} aria-hidden="true" />
          <span>测试目标</span>
          <strong>{provider.testTarget}</strong>
          <p>当前批次只生成连接测试记录，不做真实外网调用。</p>
          <dl className="settings-compact-dl">
            <div><dt>状态</dt><dd>{provider.status}</dd></div>
            <div><dt>延迟</dt><dd>{provider.latency}</dd></div>
            <div><dt>密钥</dt><dd>{provider.keyStatus}</dd></div>
          </dl>
        </article>
        <div className="settings-action-row">
          <button type="button" onClick={() => submitSettingsAction("TEST_LLM_PROVIDER", { provider: provider.id })}>
            测试模型连接
          </button>
          <button
            type="button"
            onClick={() =>
              submitSettingsAction("SAVE_LLM_SECRET_REFERENCE", {
                provider: provider.id,
                rawSecret: llmSecretInput || "llm-secret-placeholder"
              })
            }
          >
            保存 API 密钥引用
          </button>
        </div>
      </div>
    );
  }

  function renderAssistantDrilldown() {
    return (
      <div className="settings-form-grid">
        <article className="settings-detail-card">
          <Bot size={22} aria-hidden="true" />
          <span>随侍童子偏好</span>
          <strong>{settingsData.assistantPreference.style}</strong>
          <p>只负责答疑解释、页面引导和草案生成，不改正式库。</p>
          <dl className="settings-compact-dl">
            <div><dt>页面入口</dt><dd>{settingsData.assistantPreference.advisoryVisible ? "显示" : "隐藏"}</dd></div>
            <div><dt>提示数量</dt><dd>{settingsData.assistantPreference.defaultPromptCount} 条</dd></div>
            <div><dt>会话策略</dt><dd>{settingsData.assistantPreference.keepPageConversation ? "保留" : "关闭后清理"}</dd></div>
          </dl>
        </article>
        <div className="settings-card-grid settings-card-grid--three">
          {["显示入口", "紧凑提示", "关闭后清理"].map((label) => (
            <article className="settings-choice-card" key={label}>
              <div>
                <CheckCircle2 size={21} aria-hidden="true" />
                <span>偏好</span>
                <strong>{label}</strong>
              </div>
              <p>保存后只影响当前用户和当前 workspace。</p>
            </article>
          ))}
        </div>
        <div className="settings-action-row">
          <button type="button" onClick={() => submitSettingsAction("SAVE_ASSISTANT_PREFERENCE_DRAFT", { target: "assistant" })}>
            保存随侍童子偏好草案
          </button>
        </div>
      </div>
    );
  }

  function renderSafetyDrilldown() {
    return (
      <div className="settings-form-grid">
        {renderSafetyLocks()}
        <article className="settings-detail-card">
          <ShieldCheck size={22} aria-hidden="true" />
          <span>安全锁说明</span>
          <strong>只读锁定</strong>
          <p>本页只允许查看解释和导出记录，不提供关闭入口。</p>
          <button type="button" onClick={() => submitSettingsAction("EXPORT_SETTINGS_AUDIT_PACK", { target: "safety-locks" })}>
            导出安全锁审计
          </button>
        </article>
      </div>
    );
  }

  function renderBackupCategory() {
    return (
      <section className="settings-backup-composer" aria-label="备份恢复设置">
        <article className="settings-detail-card settings-backup-card">
          <Archive size={22} aria-hidden="true" />
          <span>配置快照</span>
          <strong>{settingsData.appearanceBackup.backupStatus}</strong>
          <p>保存用户设置快照，不含密钥明文、不含持仓数据、不含研究结论。</p>
          <dl className="settings-compact-dl">
            <div><dt>最近快照</dt><dd>{settingsData.appearanceBackup.lastBackup}</dd></div>
            <div><dt>包含</dt><dd>显示偏好、默认首页、数据源与模型密钥引用状态</dd></div>
            <div><dt>不包含</dt><dd>密钥原文、持仓数据、研究报告正文</dd></div>
          </dl>
          <button type="button" onClick={() => submitSettingsAction("EXPORT_SETTINGS_AUDIT_PACK", { target: "settings-backup-snapshot" })}>
            导出配置快照
          </button>
        </article>

        <article className="settings-detail-card settings-backup-card">
          <RefreshCcw size={22} aria-hidden="true" />
          <span>恢复保护</span>
          <strong>{settingsData.appearanceBackup.restoreRequiresReview ? "需人审" : "待确认"}</strong>
          <p>恢复前必须生成草案并由人工确认，避免误覆盖当前配置。</p>
          <dl className="settings-compact-dl">
            <div><dt>恢复方式</dt><dd>只生成草案，不直接覆盖</dd></div>
            <div><dt>审计记录</dt><dd>记录快照编号、发起时间与确认状态</dd></div>
            <div><dt>安全边界</dt><dd>不恢复密钥明文，不触发任何业务动作</dd></div>
          </dl>
          <button
            type="button"
            onClick={() => submitSettingsAction("CREATE_BACKUP_RESTORE_DRAFT", { backupId: settingsData.appearanceBackup.lastBackup })}
          >
            创建恢复草案
          </button>
        </article>
      </section>
    );
  }

  function renderBackupDrilldown(item: SettingsDrilldownItem) {
    if (item.id === "backup-restore") {
      return (
        <div className="settings-form-grid">
          <article className="settings-detail-card">
            <RefreshCcw size={22} aria-hidden="true" />
            <span>恢复草案</span>
            <strong>{settingsData.appearanceBackup.restoreRequiresReview ? "需人审" : "待确认"}</strong>
            <p>恢复动作只会生成待确认草案，不会直接覆盖当前设置。</p>
          </article>
          <article className="settings-detail-card">
            <ShieldCheck size={22} aria-hidden="true" />
            <span>恢复边界</span>
            <strong>安全隔离</strong>
            <p>密钥原文、持仓数据、研究结论和交易相关信息不会进入恢复包。</p>
          </article>
          <div className="settings-action-row">
            <button
              type="button"
              onClick={() => submitSettingsAction("CREATE_BACKUP_RESTORE_DRAFT", { backupId: settingsData.appearanceBackup.lastBackup })}
            >
              创建恢复草案
            </button>
            <button type="button" onClick={() => submitSettingsAction("EXPORT_SETTINGS_AUDIT_PACK", { target: "settings-backup-restore" })}>
              导出审计记录
            </button>
          </div>
        </div>
      );
    }

    return (
      <div className="settings-form-grid">
        <article className="settings-detail-card">
          <Archive size={22} aria-hidden="true" />
          <span>配置快照</span>
          <strong>{settingsData.appearanceBackup.backupStatus}</strong>
          <p>最近快照 {settingsData.appearanceBackup.lastBackup}。用于迁移或回滚个人设置，不是业务数据导出。</p>
        </article>
        <article className="settings-detail-card">
          <FileKey2 size={22} aria-hidden="true" />
          <span>快照内容</span>
          <strong>引用状态</strong>
          <p>包含显示偏好、默认首页、数据源与模型密钥引用状态，不包含任何密钥明文。</p>
        </article>
        <div className="settings-action-row">
          <button type="button" onClick={() => submitSettingsAction("EXPORT_SETTINGS_AUDIT_PACK", { target: "settings-backup-snapshot" })}>
            导出配置快照
          </button>
          <button
            type="button"
            onClick={() => submitSettingsAction("CREATE_BACKUP_RESTORE_DRAFT", { backupId: settingsData.appearanceBackup.lastBackup })}
          >
            创建恢复草案
          </button>
        </div>
      </div>
    );
  }

  function renderAppearanceDrilldown(item: SettingsDrilldownItem) {
    if (item.id === "appearance-copy") {
      return (
        <div className="settings-appearance-panel">
          <section className="settings-language-card" aria-label="文字表达模式" role="region">
            <div className="settings-language-head">
              <div>
                <Languages size={22} aria-hidden="true" />
                <span>文字表达模式</span>
                <strong>{copyModeMeta[selectedCopyMode].label}</strong>
              </div>
              <small>{copyModeMeta[selectedCopyMode].detail}</small>
            </div>
            {renderCopyModeControls()}
            {renderCopyPreview()}
          </section>
        </div>
      );
    }

    return (
      <div className="settings-card-grid settings-card-grid--three">
        <article className="settings-choice-card">
          <div>
            <Type size={21} aria-hidden="true" />
            <span>文字大小</span>
            <strong>{fontScaleMeta[selectedFontScale].label}</strong>
          </div>
          <div className="settings-segmented-control" role="radiogroup" aria-label="文字大小调节">
            {(Object.keys(fontScaleMeta) as FontScale[]).map((scale) => (
              <button
                key={scale}
                type="button"
                role="radio"
                aria-checked={selectedFontScale === scale}
                className={selectedFontScale === scale ? "is-active" : ""}
                onClick={() => previewFontScale(scale)}
              >
                {fontScaleMeta[scale].label}
              </button>
            ))}
          </div>
          <p>{fontScaleMeta[selectedFontScale].detail}</p>
        </article>
        <article className="settings-choice-card">
          <div>
            <Palette size={21} aria-hidden="true" />
            <span>深浅主题</span>
            <strong>{themeModeMeta[selectedThemeMode].label}</strong>
          </div>
          <div className="settings-segmented-control" role="radiogroup" aria-label="深浅主题切换">
            {(Object.keys(themeModeMeta) as ThemeMode[]).map((mode) => (
              <button
                key={mode}
                type="button"
                role="radio"
                aria-checked={selectedThemeMode === mode}
                className={selectedThemeMode === mode ? "is-active" : ""}
                onClick={() => previewThemeMode(mode)}
              >
                {themeModeMeta[mode].label}
              </button>
            ))}
          </div>
          <p>{themeModeMeta[selectedThemeMode].detail}</p>
        </article>
        <article className="settings-info-card">
          <Eye size={21} aria-hidden="true" />
          <span>页面密度</span>
          <strong>{settingsData.appearanceBackup.pageDensity}</strong>
          <p>保持驾驶舱信息密度，后续可扩展为紧凑/舒展。</p>
        </article>
      </div>
    );
  }

  function renderCopyModeControls() {
    return (
      <div className="settings-copy-mode-list" role="radiogroup" aria-label="选择文字表达模式">
        {(Object.keys(copyModeMeta) as CopyMode[]).map((mode) => (
          <button
            type="button"
            role="radio"
            aria-checked={selectedCopyMode === mode}
            className={selectedCopyMode === mode ? "is-active" : ""}
            key={mode}
            onClick={() => previewCopyMode(mode)}
          >
            <strong>{copyModeMeta[mode].label}</strong>
            <span>{copyModeMeta[mode].detail}</span>
          </button>
        ))}
      </div>
    );
  }

  function renderCopyPreview() {
    return (
      <div className="settings-copy-preview" aria-label="文字表达预览">
        {Object.entries(settingsData.copyPack).slice(0, 10).map(([key, entry]) => (
          <div key={key}>
            <span>{entry.tianji}</span>
            <strong>{entry[selectedCopyMode]}</strong>
          </div>
        ))}
      </div>
    );
  }

  function renderSafetyLocks() {
    return (
      <section className="settings-lock-list" aria-label="安全锁状态">
        {settingsData.safetyLocks.map((lock) => (
          <article className="settings-lock-row" key={lock.id}>
            <ShieldCheck size={17} aria-hidden="true" />
            <span>
              <strong>{lock.label}</strong>
              <small>{lock.detail}</small>
            </span>
            <em>{lock.status}</em>
          </article>
        ))}
      </section>
    );
  }
}
