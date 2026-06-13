import { demoSession } from "../auth";
import { createDayanActionDraft, getDayanAskPageData } from "../services/dayanAskApi";
import { afterEach, vi } from "vitest";

describe("Batch 5 dayan ask tenant-aware data", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("returns the Z-SkillOS ask console mock for the current workspace", async () => {
    const packet = await getDayanAskPageData(demoSession);

    expect(packet.workspaceId).toBe(demoSession.workspaceId);
    expect(packet.systemStatus.registeredMethodCount).toBe(104);
    expect(packet.systemStatus.concreteDomainCount).toBe(17);
    expect(packet.systemStatus.maxRiskLevel).toBe("R2_DRAFT");
    expect(packet.formations.length).toBeGreaterThanOrEqual(6);
    expect(packet.skillCategories.map((category) => category.name)).toEqual([
      "持仓问诊",
      "选股问策",
      "催化问因",
      "链上研判",
      "天官问策",
      "历史问迹",
      "报告落盘",
      "案例复盘",
      "记忆沉淀",
      "规则候选",
      "罗盘问治",
      "审计护法"
    ]);
  });

  it("keeps all runtime and mutation safety gates locked", async () => {
    const packet = await getDayanAskPageData(demoSession);

    expect(packet.safety.paperOnly).toBe(true);
    expect(packet.safety.humanReviewRequired).toBe(true);
    expect(packet.safety.brokerRuntime).toBe("BLOCKED");
    expect(packet.safety.realTrade).toBe("BLOCKED");
    expect(packet.safety.productionAllowed).toBe(false);
    expect(packet.safety.agentDirectMutationAllowed).toBe(false);
    expect(packet.safety.registryDirectMutationAllowed).toBe(false);
    expect(packet.safety.memoryDirectWriteAllowed).toBe(false);
    expect(packet.safety.ruleDirectEnableAllowed).toBe(false);
  });

  it("uses backend Dayan ask packet when configured", async () => {
    const safety = {
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
    vi.stubEnv("VITE_ZMATRIX_DAYAN_ASK_PACKET_URL", "/api/cockpit/dayan_ask_packet.json");
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        new Response(
          JSON.stringify({
            workspaceId: demoSession.workspaceId,
            asOf: "2026-06-13",
            safety,
            altar: {
              mode: "DEEP_RESEARCH",
              modeLabel: "深度研究模式",
              currentTopic: "backend",
              researchScope: "ALL_MARKET",
              researchScopeLabel: "A股全市场",
              memoryContext: "LONG_MEMORY",
              memoryContextLabel: "长链记忆",
              safety
            },
            formations: [
              {
                id: "research-chain",
                name: "研究链路编排阵",
                description: "计划与证据",
                promptTemplate: "生成只读研究链路。",
                composedSkillIds: ["workflow-plan"],
                safetyLevel: "PROPOSAL_REQUIRED"
              }
            ],
            hermesGuidance: {
              guidanceId: "HG-BACKEND",
              contextSummary: "backend",
              suggestions: ["保持只读"],
              missingInputs: ["研究主题"],
              recommendedMethods: ["研究链路编排阵"],
              quickQuestions: ["还缺什么证据？"],
              nextActionText: "生成研究链路草案",
              hermesStatus: "常驻"
            },
            advisoryGroups: [],
            forgeCandidates: [],
            moveReview: [],
            myMethods: [],
            skillCategories: [
              {
                id: "audit",
                name: "审计护法",
                description: "硬门检查",
                skillCount: 3,
                safetyLevel: "READ_ONLY",
                skills: [
                  {
                    id: "audit_pack",
                    userVisibleName: "硬门检查",
                    description: "读取审计状态",
                    promptTemplate: "整理审计包。",
                    outputType: "CHAT",
                    safetyLevel: "READ_ONLY",
                    requiredInputs: ["研究主题"],
                    backendBinding: { registrySkillIds: ["SYSTEM_VERIFY.READ_STATUS"], domain: "SYSTEM_VERIFY", operation: "registry_read" }
                  }
                ]
              }
            ],
            currentConversation: {
              conversationId: "ask-backend",
              topic: "backend",
              selectedPromptFragments: ["研究链路编排阵"],
              messages: [{ id: "msg-backend", role: "HERMES", label: "问天", content: "backend", createdAt: "09:42" }]
            },
            latestHermesPlan: {
              planId: "plan-backend",
              userGoal: "backend",
              interpretedTask: "backend",
              recommendedMethods: ["研究链路编排阵"],
              executionSteps: [{ order: 1, actionName: "选择技能组合", userVisiblePurpose: "确认研究路径", requiredInput: ["研究主题"], expectedOutput: "技能清单" }],
              missingInputs: ["研究主题"],
              outputTarget: ["CHAT_ONLY", "AUDIT_CHECK"],
              humanReviewRequired: true
            },
            voice: { state: "READY", label: "语音输入可用", privacyNote: "仅转写" },
            systemStatus: {
              registeredMethodCount: 104,
              concreteDomainCount: 20,
              maxRiskLevel: "R2_DRAFT",
              workflowMode: "DRY_RUN_ONLY",
              registryMutation: "BLOCKED"
            },
            backendMapping: {
              registry: "skill_registry.generated.json",
              contracts: "skill_contract_registry.json",
              invocation: "invoke_skill(command_envelope, context_slice)",
              workflow: "WORKFLOW.RUN_RESEARCH_DRY_CHAIN",
              approval: "Proposal/Human Review"
            }
          }),
          { status: 200, headers: { "Content-Type": "application/json" } }
        )
      )
    );

    const packet = await getDayanAskPageData(demoSession);

    expect(packet.altar.currentTopic).toBe("backend");
    expect(packet.systemStatus.concreteDomainCount).toBe(20);
    expect(fetch).toHaveBeenCalledWith("/api/cockpit/dayan_ask_packet.json", expect.objectContaining({ cache: "no-store" }));
  });

  it("loads the local Hermes bridge status when configured", async () => {
    vi.stubEnv("VITE_ZMATRIX_AGENT_BRIDGE_URL", "/api/product/agent_bridge.json");
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        new Response(
          JSON.stringify({
            status: "Z_MATRIX_AGENT_BRIDGE_READY",
            workspace_id: demoSession.workspaceId,
            generated_at: "2026-06-13T00:00:00Z",
            default_agent: "Hermes",
            interaction_mode: "NATURAL_LANGUAGE_RESEARCH_DRAFT",
            llm_runtime: {
              provider: "ENV_CONFIGURED_BY_USER",
              key_material: "ENV_ONLY",
              response_storage: "DRAFT_LAYER_ONLY",
              external_call_from_backend: "DISABLED_BY_DEFAULT"
            },
            registry: {
              ready: true,
              skill_count: 104,
              domain_count: 17,
              concrete_skill_count: 17
            },
            allowed_intents: [
              { id: "explain-system-status", label: "解释系统状态", output_target: "CHAT_ONLY", requires_review: false },
              { id: "build-research-chain-draft", label: "研究链路草案", output_target: "REPORT_DRAFT", requires_review: true },
              { id: "prepare-audit-reference", label: "审计引用整理", output_target: "AUDIT_CHECK", requires_review: true },
              { id: "summarize-factor-evidence", label: "因子证据摘要", output_target: "REPORT_DRAFT", requires_review: true }
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
          }),
          { status: 200, headers: { "Content-Type": "application/json" } }
        )
      )
    );

    const packet = await getDayanAskPageData(demoSession);

    expect(packet.agentBridge.status).toBe("Z_MATRIX_AGENT_BRIDGE_READY");
    expect(packet.agentBridge.default_agent).toBe("Hermes");
    expect(packet.agentBridge.allowed_intents.length).toBe(4);
    expect(packet.agentBridge.routing.human_review_required).toBe(true);
    expect(packet.agentBridge.safety.real_trade).toBe("BLOCKED");
    expect(fetch).toHaveBeenCalledWith("/api/product/agent_bridge.json", expect.objectContaining({ cache: "no-store" }));
  });

  it("posts research questions to the local Hermes draft bridge when configured", async () => {
    vi.stubEnv("VITE_ZMATRIX_AGENT_DRAFT_URL", "/api/product/agent_draft.json");
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        new Response(
          JSON.stringify({
            status: "Z_MATRIX_AGENT_DRAFT_READY",
            workspace_id: demoSession.workspaceId,
            draft_id: "agent-draft-test",
            default_agent: "Hermes",
            intent_id: "prepare-audit-reference",
            intent_label: "审计引用整理",
            question_summary: "半导体设备国产化研究证据",
            answer: "Hermes 已生成本地研究草案。",
            user_message: "本地研究草案已生成，等待人工复核。",
            suggested_next_steps: ["补充研究对象与时间窗口"],
            draft_layers: ["chat", "drafts"],
            selected_fragments: ["产业洞察阵"],
            human_review_required: true,
            proposal_required: true,
            safety: {
              alpha_claim: "BLOCKED",
              promotion: "BLOCKED",
              broker_runtime: "BLOCKED",
              real_trade: "BLOCKED",
              direct_command_runtime: "BLOCKED",
              formal_memory_write: "BLOCKED"
            }
          }),
          { status: 200, headers: { "Content-Type": "application/json" } }
        )
      )
    );

    const draft = await createDayanActionDraft(demoSession, "生成链路草案", {
      userInput: "请整理半导体设备国产化研究证据",
      selectedFragments: ["产业洞察阵"]
    });

    expect(draft.status).toBe("DRAFT_CREATED");
    expect(draft.draftId).toBe("agent-draft-test");
    expect(draft.intentId).toBe("prepare-audit-reference");
    expect(draft.answer).toContain("Hermes 已生成");
    expect(fetch).toHaveBeenCalledWith(
      "/api/product/agent_draft.json",
      expect.objectContaining({
        method: "POST",
        body: expect.stringContaining("半导体设备国产化研究证据")
      })
    );
  });

  it("returns isolated empty personal layers for another workspace", async () => {
    const packet = await getDayanAskPageData({
      ...demoSession,
      userId: "usr_other",
      workspaceId: "ws_other"
    });

    expect(packet.workspaceId).toBe("ws_other");
    expect(packet.myMethods).toEqual([]);
    expect(packet.forgeCandidates).toEqual([]);
    expect(packet.moveReview).toEqual([]);
    expect(packet.currentConversation.messages[0].content).toContain("请先输入研究目标");
  });

  it("creates only human-review drafts or audit pack references", async () => {
    const chain = await createDayanActionDraft(demoSession, "生成链路草案", {
      prompt: "研究半导体设备"
    });
    const method = await createDayanActionDraft(demoSession, "加入我的法门草案", {
      candidateId: "forge-001"
    });
    const audit = await createDayanActionDraft(demoSession, "导出审计包", {
      conversationId: "ask-20260604-001"
    });

    expect(chain.workspaceId).toBe(demoSession.workspaceId);
    expect(chain.status).toBe("DRAFT_CREATED");
    expect(chain.humanReviewRequired).toBe(true);
    expect(chain.auditEvent).toBe("CREATE_DAYAN_DRAFT");
    expect(method.status).toBe("DRAFT_CREATED");
    expect(method.humanReviewRequired).toBe(true);
    expect(audit.status).toBe("AUDIT_PACK_READY");
    expect(audit.auditEvent).toBe("EXPORT_DAYAN_AUDIT_PACK");
  });

  it("rejects client tenant spoofing in ask actions", async () => {
    await expect(
      createDayanActionDraft(demoSession, "生成链路草案", {
        workspaceId: "ws_external_reviewer",
        prompt: "伪造 workspace"
      })
    ).rejects.toMatchObject({ code: "TENANT_SPOOFING" });
  });
});
