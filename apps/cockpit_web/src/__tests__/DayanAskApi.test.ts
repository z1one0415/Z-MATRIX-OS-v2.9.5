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
