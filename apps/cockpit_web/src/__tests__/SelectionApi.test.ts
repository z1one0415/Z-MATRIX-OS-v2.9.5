import { demoSession } from "../auth";
import { createSelectionActionDraft, getSelectionDashboardPacket } from "../services/selectionApi";
import { afterEach, vi } from "vitest";

describe("Batch 2 selection tenant-aware data", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("returns the z-prime research selection dashboard mock", async () => {
    const packet = await getSelectionDashboardPacket(demoSession);

    expect(packet.workspaceId).toBe(demoSession.workspaceId);
    expect(packet.kpis.map((kpi) => kpi.label)).toEqual(["范围覆盖", "初筛候选", "高优先级", "集合分流", "今日主线"]);
    expect(packet.filterChain).toHaveLength(7);
    expect(packet.filterChain.map((step) => step.title)).toContain("底仓/轮动/黑马角色识别");
    expect(packet.matrixGroups.map((group) => group.title)).toEqual(["B-Matrix Top", "R-Matrix Top", "D-Matrix Top", "综合候选"]);
    expect(packet.candidates.map((candidate) => candidate.symbol)).toContain("300308");
    expect(packet.audit.realTrade).toBe("BLOCKED");
  });

  it("uses backend selection packet when configured", async () => {
    vi.stubEnv("VITE_ZMATRIX_SELECTION_PACKET_URL", "/api/cockpit/selection_packet.json");
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        new Response(
          JSON.stringify({
            workspaceId: demoSession.workspaceId,
            asOf: "2026-06-13",
            kpis: [{ label: "候选因子", value: "16", note: "backend", tone: "gold", visual: "bars" }],
            filterChain: [],
            conclusion: { priorityDirection: "backend", confidence: "中高", reasons: ["V11"], avoidToday: ["不交易"] },
            opportunityGroups: [],
            matrixGroups: [],
            candidates: [],
            todos: [],
            audit: { paperOnly: true, humanReview: true, brokerRuntime: "BLOCKED", realTrade: "BLOCKED", dataScope: "WORKSPACE_SCOPED" }
          }),
          { status: 200, headers: { "Content-Type": "application/json" } }
        )
      )
    );

    const packet = await getSelectionDashboardPacket(demoSession);

    expect(packet.kpis[0].note).toBe("backend");
    expect(fetch).toHaveBeenCalledWith("/api/cockpit/selection_packet.json", expect.objectContaining({ cache: "no-store" }));
  });

  it("returns an empty private selection view for another workspace", async () => {
    const packet = await getSelectionDashboardPacket({
      ...demoSession,
      userId: "usr_other",
      workspaceId: "ws_other"
    });

    expect(packet.workspaceId).toBe("ws_other");
    expect(packet.candidates).toEqual([]);
    expect(packet.matrixGroups.every((group) => group.items.length === 0)).toBe(true);
  });

  it("creates paper-only research drafts and observation proposals", async () => {
    const research = await createSelectionActionDraft(demoSession, "生成个股研究", {
      symbol: "300308",
      name: "中际旭创"
    });
    const observation = await createSelectionActionDraft(demoSession, "进入轮动观察仓", {
      symbol: "300308",
      name: "中际旭创"
    });

    expect(research.workspaceId).toBe(demoSession.workspaceId);
    expect(research.humanReviewRequired).toBe(true);
    expect(research.auditEvent).toBe("CREATE_STOCK_RESEARCH_DRAFT");
    expect(observation.auditEvent).toBe("CREATE_OBSERVATION_WAREHOUSE_PROPOSAL");
  });

  it("rejects tenant spoofing in selection actions", async () => {
    await expect(
      createSelectionActionDraft(demoSession, "创建人工研究记录", {
        symbol: "300308",
        workspaceId: "ws_external_reviewer"
      })
    ).rejects.toMatchObject({ code: "TENANT_SPOOFING" });
  });
});
