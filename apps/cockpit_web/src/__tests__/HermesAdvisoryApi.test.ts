import { demoSession } from "../auth";
import {
  createHermesActionDraft,
  createHermesChatResponse,
  getHermesAdvisoryPacket
} from "../services/hermesAdvisoryApi";

describe("global Hermes advisory api", () => {
  it("returns tenant-aware page advisory packets", async () => {
    const packet = await getHermesAdvisoryPacket(demoSession, "holdings");

    expect(packet.workspaceId).toBe(demoSession.workspaceId);
    expect(packet.title).toBe("童子谏言");
    expect(packet.pageContext.safetyBoundary.paperOnly).toBe(true);
    expect(packet.pageContext.safetyBoundary.humanReviewRequired).toBe(true);
    expect(packet.pageContext.safetyBoundary.brokerRuntime).toBe("BLOCKED");
    expect(packet.pageContext.safetyBoundary.realTrade).toBe("BLOCKED");
    expect(packet.promptSeeds).toContain("当前持仓最需要复核的风险是什么？");
  });

  it("rejects client tenant spoofing in chat requests", async () => {
    await expect(
      createHermesChatResponse(demoSession, {
        pageId: "selection",
        question: "解释候选池",
        pageSnapshot: "client",
        workspaceId: "ws_external_reviewer"
      } as never)
    ).rejects.toMatchObject({ code: "TENANT_SPOOFING" });
  });

  it("creates only human-review chat drafts", async () => {
    const response = await createHermesChatResponse(demoSession, {
      pageId: "compass",
      question: "生成参数校准草案。",
      pageSnapshot: "系统健康 82"
    });

    expect(response.workspaceId).toBe(demoSession.workspaceId);
    expect(response.humanReviewRequired).toBe(true);
    expect(response.auditEvent).toBe("HERMES_CHAT_DRAFT");
    expect(response.draftAction).toBe("参数校准草案");
    expect(response.handoffTarget).toBe("/dayan-ask");
  });

  it("keeps global actions draft-only or audit-reference only", async () => {
    const draft = await createHermesActionDraft(demoSession, {
      pageId: "history",
      actionLabel: "生成复盘草案",
      pageSnapshot: "规则候选 156"
    });
    const audit = await createHermesActionDraft(demoSession, {
      pageId: "settings",
      actionLabel: "导出审计包",
      pageSnapshot: "安全锁已锁定"
    });

    expect(draft.status).toBe("DRAFT_CREATED");
    expect(draft.humanReviewRequired).toBe(true);
    expect(audit.status).toBe("AUDIT_PACK_READY");
    expect(audit.humanReviewRequired).toBe(true);
  });
});
