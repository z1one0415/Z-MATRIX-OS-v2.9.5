import { demoSession } from "../auth";
import { createSettingsActionDraft, getSettingsPageData } from "../services/settingsApi";

describe("settings api tenant-aware contract", () => {
  it("returns the workspace scoped settings cockpit data without secret plaintext", async () => {
    const packet = await getSettingsPageData(demoSession);

    expect(packet.workspaceId).toBe(demoSession.workspaceId);
    expect(packet.title).toBe("系统设置");
    expect(packet.categories.map((category) => category.label)).toEqual([
      "账户显示",
      "数据源",
      "大模型 API",
      "随侍童子",
      "安全锁",
      "显示设置",
      "备份恢复"
    ]);
    expect(packet.dataSources.find((source) => source.id === "tushare")?.secretPreview).toBe("***REDACTED***");
    expect(packet.llmProviders.map((provider) => provider.label)).toEqual(
      expect.arrayContaining([
        "OpenAI",
        "Anthropic Claude",
        "Google Gemini",
        "DeepSeek",
        "Moonshot Kimi",
        "通义千问",
        "智谱 GLM",
        "自定义兼容接口"
      ])
    );
    const deepseek = packet.llmProviders.find((provider) => provider.id === "deepseek");
    expect(deepseek?.secretPreview).toBe("***REDACTED***");
    expect(deepseek?.baseUrl).toBe("https://api.deepseek.com/v1");
    expect(deepseek?.defaultModel).toBe("deepseek-chat");
    expect(deepseek?.fallbackModel).toBe("deepseek-reasoner");
    expect(packet.llmProviders.find((provider) => provider.id === "custom-openai-compatible")?.endpointMode).toBe("兼容 OpenAI");
    expect(packet.settingsDrilldowns.llm.map((item) => item.label)).toEqual(
      expect.arrayContaining(["OpenAI", "DeepSeek", "自定义兼容接口"])
    );
    expect(packet.settingsDrilldowns.appearance.map((item) => item.label)).toEqual(expect.arrayContaining(["文字表达模式", "显示与主题"]));
    expect(packet.settingsDrilldowns.backup.map((item) => item.label)).toEqual(expect.arrayContaining(["配置快照", "恢复保护"]));
    expect(JSON.stringify(packet)).not.toContain("demo-token");
    expect(JSON.stringify(packet)).not.toContain("rawSecret");
    expect(packet.safety.paperOnly).toBe(true);
    expect(packet.safety.humanReviewRequired).toBe(true);
    expect(packet.safety.brokerRuntime).toBe("BLOCKED");
    expect(packet.safety.realTrade).toBe("BLOCKED");
    expect(packet.safety.agentDirectMutation).toBe("BLOCKED");
    expect(packet.productRuntime.cockpit.packet_count).toBe(5);
    expect(packet.productRuntime.registry.skill_count).toBeGreaterThanOrEqual(100);
    expect(packet.productRuntime.safety.broker_runtime).toBe("BLOCKED");
    expect(packet.productRuntime.safety.real_trade).toBe("BLOCKED");
    expect(packet.operatorActions.auto_run_enabled).toBe(false);
    expect(packet.operatorActions.human_review_required).toBe(true);
    expect(packet.operatorActions.actions.map((item) => item.id)).toEqual(expect.arrayContaining(["backend-check", "product-smoke", "product-readiness"]));
    expect(packet.operatorActions.actions.every((item) => item.safety.broker_runtime === "BLOCKED")).toBe(true);
    expect(packet.researchStatus.capability_count).toBeGreaterThanOrEqual(4);
    expect(packet.researchStatus.report_export.artifact_policy).toBe("LOCAL_FILES_ONLY");
    expect(packet.researchStatus.monthly_refresh.mode).toBe("LOCAL_TERMINAL_MANUAL_DRY_PLAN");
    expect(packet.researchStatus.monthly_refresh.safety.broker_runtime).toBe("BLOCKED");
    expect(packet.researchStatus.safety.real_trade).toBe("BLOCKED");
  });

  it("includes tianji, plain, and english copy packs for core cockpit labels", async () => {
    const packet = await getSettingsPageData(demoSession);

    expect(packet.copyMode).toBe("tianji");
    expect(packet.copyPack.holdings).toEqual({
      tianji: "执仓决断",
      plain: "持仓检查",
      english: "Portfolio Review"
    });
    expect(packet.copyPack.hermes.plain).toBe("帮助助手");
    expect(packet.copyPack.auditPack.english).toBe("Export Audit Pack");
  });

  it("creates only human-review setting drafts, audit packs, and secret references", async () => {
    const test = await createSettingsActionDraft(demoSession, "TEST_DATA_SOURCE", {
      provider: "tushare"
    });
    const preview = await createSettingsActionDraft(demoSession, "PREVIEW_COPY_MODE", {
      copyMode: "plain"
    });
    const secret = await createSettingsActionDraft(demoSession, "SAVE_SECRET_REFERENCE", {
      provider: "tushare",
      rawSecret: "test-token-value"
    });
    const llmTest = await createSettingsActionDraft(demoSession, "TEST_LLM_PROVIDER", {
      provider: "deepseek"
    });
    const llmSecret = await createSettingsActionDraft(demoSession, "SAVE_LLM_SECRET_REFERENCE", {
      provider: "deepseek",
      rawSecret: "llm-test-token-value"
    });
    const theme = await createSettingsActionDraft(demoSession, "PREVIEW_THEME_MODE", {
      themeMode: "light"
    });
    const font = await createSettingsActionDraft(demoSession, "PREVIEW_FONT_SCALE", {
      fontScale: "large"
    });
    const audit = await createSettingsActionDraft(demoSession, "EXPORT_SETTINGS_AUDIT_PACK", {
      target: "settings"
    });
    const account = await createSettingsActionDraft(demoSession, "SAVE_ACCOUNT_DISPLAY_DRAFT", {
      target: "account-display"
    });
    const localImport = await createSettingsActionDraft(demoSession, "VALIDATE_LOCAL_IMPORT_DRAFT", {
      sourceId: "research-import"
    });
    const assistant = await createSettingsActionDraft(demoSession, "SAVE_ASSISTANT_PREFERENCE_DRAFT", {
      target: "assistant"
    });

    expect(test.humanReviewRequired).toBe(true);
    expect(test.auditEvent).toBe("TEST_SETTINGS_DATA_SOURCE");
    expect(preview.copyMode).toBe("plain");
    expect(secret.status).toBe("REFERENCE_SAVED");
    expect(secret.tokenPreview).toBe("***REDACTED***");
    expect(secret.secretRef).toContain(`secret://workspace/${demoSession.workspaceId}/tushare/`);
    expect(JSON.stringify(secret)).not.toContain("test-token-value");
    expect(llmTest.auditEvent).toBe("TEST_SETTINGS_LLM_PROVIDER");
    expect(llmSecret.status).toBe("REFERENCE_SAVED");
    expect(llmSecret.secretRef).toContain(`secret://workspace/${demoSession.workspaceId}/llm-deepseek/`);
    expect(JSON.stringify(llmSecret)).not.toContain("llm-test-token-value");
    expect(theme.themeMode).toBe("light");
    expect(font.fontScale).toBe("large");
    expect(audit.status).toBe("AUDIT_PACK_READY");
    expect(audit.humanReviewRequired).toBe(true);
    expect(account.auditEvent).toBe("SAVE_SETTINGS_ACCOUNT_DISPLAY");
    expect(localImport.auditEvent).toBe("VALIDATE_SETTINGS_LOCAL_IMPORT");
    expect(assistant.auditEvent).toBe("SAVE_SETTINGS_ASSISTANT_PREFERENCE");
  });

  it("rejects client tenant fields in settings actions", async () => {
    await expect(
      createSettingsActionDraft(demoSession, "SAVE_SETTINGS_DRAFT", {
        copyMode: "english",
        workspaceId: "ws_other"
      })
    ).rejects.toMatchObject({ code: "TENANT_SPOOFING" });
  });
});
