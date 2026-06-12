import { demoSession } from "../auth";
import { createHistoryActionDraft, getHistoryPageData } from "../services/historyApi";

describe("Batch 4 history tenant-aware data", () => {
  it("returns the z-prime space-time history cockpit mock", async () => {
    const packet = await getHistoryPageData(demoSession);

    expect(packet.workspaceId).toBe(demoSession.workspaceId);
    expect(packet.kpis.map((kpi) => kpi.label)).toEqual(["累计报告", "实盘案例", "系统记忆", "规则候选", "待清理记忆"]);
    expect(packet.learningPipeline.map((node) => node.displayName)).toEqual(["分析报告", "实盘案例", "系统记忆", "规则候选", "固化规则"]);
    expect(packet.events.length).toBeGreaterThan(0);
    expect(packet.reportLibrary.length).toBeGreaterThan(0);
    expect(packet.caseLibrary.length).toBeGreaterThan(0);
    expect(packet.spaceTimeSeal.alert.title).toBe("时空预鉴");
    expect(packet.safety.paperOnly).toBe(true);
    expect(packet.safety.humanReviewRequired).toBe(true);
    expect(packet.safety.brokerRuntime).toBe("BLOCKED");
    expect(packet.safety.realTrade).toBe("BLOCKED");
    expect(packet.safety.agentDirectMutationAllowed).toBe(false);
  });

  it("returns an isolated partial history view for another workspace", async () => {
    const packet = await getHistoryPageData({
      ...demoSession,
      userId: "usr_other",
      workspaceId: "ws_other"
    });

    expect(packet.workspaceId).toBe("ws_other");
    expect(packet.events).toEqual([]);
    expect(packet.reportLibrary).toEqual([]);
    expect(packet.caseLibrary).toEqual([]);
    expect(packet.learningPipeline.every((node) => node.count === 0)).toBe(true);
    expect(packet.systemStatus.reportIndex).toBe("PARTIAL");
  });

  it("creates only human-review history drafts and audit pack references", async () => {
    const review = await createHistoryActionDraft(demoSession, "生成复盘草案", {
      eventId: "HE-20260604-001"
    });
    const memory = await createHistoryActionDraft(demoSession, "提交入记忆草案", {
      eventId: "HE-20260604-001"
    });
    const audit = await createHistoryActionDraft(demoSession, "导出审计包", {
      targetId: "HISTORY_AUDIT"
    });

    expect(review.workspaceId).toBe(demoSession.workspaceId);
    expect(review.humanReviewRequired).toBe(true);
    expect(review.auditEvent).toBe("CREATE_HISTORY_REVIEW_DRAFT");
    expect(memory.status).toBe("DRAFT_CREATED");
    expect(memory.humanReviewRequired).toBe(true);
    expect(audit.status).toBe("AUDIT_PACK_READY");
    expect(audit.auditEvent).toBe("EXPORT_HISTORY_AUDIT_PACK");
  });

  it("rejects tenant spoofing in history actions", async () => {
    await expect(
      createHistoryActionDraft(demoSession, "创建人工研究记录", {
        eventId: "HE-20260604-001",
        workspaceId: "ws_external_reviewer"
      })
    ).rejects.toMatchObject({ code: "TENANT_SPOOFING" });
  });
});
