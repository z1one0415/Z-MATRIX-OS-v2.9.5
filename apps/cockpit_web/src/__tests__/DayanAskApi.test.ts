import { demoSession } from "../auth";
import { createDayanActionDraft, getDayanAskPageData } from "../services/dayanAskApi";

describe("Batch 5 dayan ask tenant-aware data", () => {
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
