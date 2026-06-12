import { demoSession } from "../auth";
import { createHoldingActionDraft, getHoldingsPacket } from "../services/holdingsApi";
import { afterEach, vi } from "vitest";

describe("Batch 1 holdings tenant-aware data", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("returns the real screenshot holdings mock for z-prime workspace", async () => {
    const packet = await getHoldingsPacket(demoSession);

    expect(packet.workspaceId).toBe(demoSession.workspaceId);
    expect(packet.account.totalAssets).toBe(110249.84);
    expect(packet.account.floatingPnl).toBe(-4776.77);
    expect(packet.account.dayReferencePnl).toBe(3733.5);
    expect(packet.account.marketValue).toBe(110137);
    expect(packet.account.cash).toBe(112.84);
    expect(packet.account.withdrawable).toBe(112.84);
    expect(packet.positions.map((position) => position.name)).toEqual(["紫金矿业", "双环传动", "科创创业ETF天弘"]);
  });

  it("uses backend holdings packet when configured", async () => {
    vi.stubEnv("VITE_ZMATRIX_HOLDINGS_PACKET_URL", "/api/cockpit/holdings_packet.json");
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        new Response(
          JSON.stringify({
            workspaceId: demoSession.workspaceId,
            asOf: "2026-06-04",
            account: {
              totalAssets: 110249.84,
              floatingPnl: -4776.77,
              dayReferencePnl: 3733.5,
              marketValue: 110137,
              cash: 112.84,
              withdrawable: 112.84,
              currency: "CNY",
              accountMask: "550***06"
            },
            kpi: {
              todayPnl: 3733.5,
              todayPnlPct: 3.39,
              totalAsset: 110249.84,
              holdingAlphaAnnualized: null,
              cashRatio: 0.1,
              maxDrawdownRecentYear: null,
              dataFreshness: "FRESH"
            },
            curveStats: [],
            positions: [
              {
                symbol: "BACKEND",
                name: "后端真实包",
                role: "CORE",
                marketValue: 1,
                weightPct: 1,
                floatingPnl: 0,
                floatingPnlPct: 0,
                alphaContributionPct: null,
                signalStrength: "MID",
                thesisStatus: "WATCH",
                catalystStatus: "NONE",
                nextAction: "WATCH",
                quantity: 1,
                available: 1,
                costPrice: 1,
                currentPrice: 1,
                reviewStatus: "只读观察",
                riskTag: "正收益观察"
              }
            ],
            observationWarehouses: [],
            todos: [],
            audit: {
              paperOnly: true,
              humanReview: true,
              brokerRuntime: "BLOCKED",
              realTrade: "BLOCKED",
              dataScope: "WORKSPACE_SCOPED"
            }
          }),
          { status: 200, headers: { "Content-Type": "application/json" } }
        )
      )
    );

    const packet = await getHoldingsPacket(demoSession);

    expect(packet.positions[0].symbol).toBe("BACKEND");
    expect(fetch).toHaveBeenCalledWith(
      "/api/cockpit/holdings_packet.json",
      expect.objectContaining({ cache: "no-store" })
    );
  });

  it("returns empty private holdings for another workspace", async () => {
    const packet = await getHoldingsPacket({
      ...demoSession,
      userId: "usr_other",
      workspaceId: "ws_other"
    });

    expect(packet.workspaceId).toBe("ws_other");
    expect(packet.positions).toEqual([]);
    expect(packet.account.totalAssets).toBe(0);
  });

  it("creates only paper review drafts and audit pack references", async () => {
    const review = await createHoldingActionDraft(demoSession, "持仓复核", {
      symbol: "601899",
      name: "紫金矿业"
    });
    const audit = await createHoldingActionDraft(demoSession, "导出审计包", {
      accountMask: "550***06"
    });

    expect(review.workspaceId).toBe(demoSession.workspaceId);
    expect(review.humanReviewRequired).toBe(true);
    expect(review.auditEvent).toBe("CREATE_HOLDING_REVIEW_DRAFT");
    expect(audit.status).toBe("AUDIT_PACK_READY");
    expect(audit.auditEvent).toBe("EXPORT_HOLDINGS_AUDIT_PACK");
  });

  it("rejects tenant spoofing in holdings actions", async () => {
    await expect(
      createHoldingActionDraft(demoSession, "持仓复核", {
        symbol: "601899",
        workspaceId: "ws_external_reviewer"
      })
    ).rejects.toMatchObject({ code: "TENANT_SPOOFING" });
  });
});
