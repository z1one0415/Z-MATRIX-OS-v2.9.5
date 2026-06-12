import { demoSession } from "../auth";
import { createControlCompassActionDraft, getControlCompassPageData } from "../services/controlCompassApi";
import { afterEach, vi } from "vitest";

describe("Batch 3B control compass tenant-aware data", () => {
  afterEach(() => {
    vi.unstubAllEnvs();
    vi.unstubAllGlobals();
  });

  it("returns the z-prime quant parameter compass packet", async () => {
    const packet = await getControlCompassPageData(demoSession);

    expect(packet.workspaceId).toBe(demoSession.workspaceId);
    expect(packet.kpi.governanceDomainCount).toBe(8);
    expect(packet.kpi.healthScore).toBe(82);
    expect(packet.kpi.latestPaperHitRatePct).toBe(87.3);
    expect(packet.kpi.pendingAdjudicationCount).toBe(6);
    expect(packet.kpi.optimizationSnapshotStatus).toBe("READY");
    expect(packet.kpi.pendingChangeCount).toBe(6);
    expect(packet.kpi.blockedChangeCount).toBe(2);
    expect(packet.kpi.monthlyInternalizationPct).toBe(56);
    expect(packet.kpi.auditCompletenessPct).toBe(92.4);
    expect(packet.governanceDomains.map((domain) => domain.displayName)).toEqual([
      "数据质量门",
      "样本池韧性",
      "因子信号门",
      "催化周期门",
      "B-Matrix 底仓",
      "R-Matrix 轮动",
      "D-Matrix 黑马",
      "经验内化"
    ]);
    expect(packet.selectedDomain.selectedDomainName).toBe("催化周期门");
    expect(packet.parameterFamilies).toHaveLength(8);
    expect(packet.parameterFamilies.find((family) => family.domainId === "CATALYST_CYCLE")).toEqual(
      expect.objectContaining({
        label: "催化周期门",
        backendMapping: expect.stringContaining("催化生命周期")
      })
    );
    expect(packet.optimizationSummary.snapshotStatus).toBe("READY");
    expect(packet.optimizationSummary.restoreAvailable).toBe(true);
    expect(JSON.stringify(packet)).not.toContain("SkillOS");
    expect(JSON.stringify(packet)).not.toContain("schema hash");
    expect(packet.safety.paperOnly).toBe(true);
    expect(packet.safety.humanReviewRequired).toBe(true);
    expect(packet.safety.realTradeAllowed).toBe(false);
    expect(packet.safety.brokerOrderAllowed).toBe(false);
    expect(packet.safety.agentDirectMutationAllowed).toBe(false);
  });

  it("uses backend control compass packet when configured", async () => {
    vi.stubEnv("VITE_ZMATRIX_CONTROL_COMPASS_PACKET_URL", "/api/cockpit/control_compass_packet.json");
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        new Response(
          JSON.stringify({
            workspaceId: demoSession.workspaceId,
            asOf: "2026-06-13",
            safety: {
              paperOnly: true,
              humanReviewRequired: true,
              realTradeAllowed: false,
              brokerOrderAllowed: false,
              productionAllowed: false,
              agentDirectMutationAllowed: false
            },
            kpi: {
              governanceDomainCount: 8,
              healthyDomainCount: 7,
              healthScore: 88,
              latestPaperHitRatePct: 0,
              weakenedSignalCount: 4,
              pendingAdjudicationCount: 1,
              optimizationSnapshotStatus: "READY",
              pendingChangeCount: 0,
              blockedChangeCount: 1,
              monthlyInternalizationPct: 56,
              auditCompletenessPct: 88,
              configVersion: "v13.5.13",
              dataFreshness: "FRESH"
            },
            governanceDomains: [
              {
                domainId: "FACTOR_SIGNAL",
                index: 3,
                displayName: "因子信号门",
                ringIndex: 6,
                status: "UNDER_REVIEW",
                pendingChanges: 1,
                riskLevel: "MID",
                lastReviewedAt: "2026-06-13"
              }
            ],
            selectedDomain: {
              selectedDomainId: "FACTOR_SIGNAL",
              selectedDomainName: "因子信号门",
              currentValue: { label: "当前阶段", value: "backend" },
              suggestedValue: { label: "系统建议", value: "等待复核" },
              impactScope: { relatedParameterCount: 104, affectedModuleCount: 20, affectedPages: ["天机罗盘"] },
              validationStatus: { paperValidationPassed: false, confidencePct: 88, method: "runtime reports" },
              auditStatus: { status: "PENDING_EXPERT_REVIEW" }
            },
            sandbox: {
              draft: { draftId: "CC-TEST", domainId: "FACTOR_SIGNAL", affectedParameterCount: 104, version: "v13.5.13" },
              impact: { impactLevel: "MID", coverage: "HIGH", strategyImpact: "只读复核", internalizationImpactPct: 4 },
              risk: { riskLevel: "MID", potentialImpact: "等待样本", varianceRange: [-1, 1], blockingCount: 1 },
              paperValidation: { method: "paper", sampleSize: 8, passRatePct: 88, conclusion: "INSUFFICIENT" },
              humanReview: { status: "PENDING", requiredReviewerCount: 2, estimatedMinutes: 90 }
            },
            ruling: {
              draftId: "CC-TEST",
              evidenceChain: { linkedEvidenceCount: 6, completenessPct: 88 },
              expertReview: { required: 2, passed: 0 },
              auditResult: { status: "PENDING", completenessPct: 88 },
              rulingStatus: { status: "PENDING", changeWindowOpen: false }
            },
            optimizationSummary: {
              systemVersion: "Z-MATRIX v13.5.13",
              suggestedVersion: "review",
              latestCycleId: "V13.5.13",
              headline: "backend",
              evidence: "registry",
              snapshotId: "CC-SNAP",
              snapshotStatus: "READY",
              restoreAvailable: true
            },
            parameterFamilies: [],
            calibrationDisputes: [],
            derivationPanel: {
              dashboard: { configVersion: "v13.5.13", pendingApprovalCount: 1, blockedCount: 1, internalizationPct: 56, doNotChangeTodayCount: 3 },
              riftAlerts: [],
              seals: []
            },
            todos: [],
            systemStatus: {
              marketData: "READY",
              financialData: "READY",
              macroData: "READY",
              strategyEngine: "READY",
              riskEngine: "READY",
              dataService: "READY",
              configRegistry: "READY",
              auditService: "READY",
              lastUpdatedAt: "2026-06-13"
            }
          }),
          { status: 200, headers: { "Content-Type": "application/json" } }
        )
      )
    );

    const packet = await getControlCompassPageData(demoSession);

    expect(packet.kpi.configVersion).toBe("v13.5.13");
    expect(packet.optimizationSummary.headline).toBe("backend");
    expect(fetch).toHaveBeenCalledWith("/api/cockpit/control_compass_packet.json", expect.objectContaining({ cache: "no-store" }));
  });

  it("returns an isolated partial compass view for another workspace", async () => {
    const packet = await getControlCompassPageData({
      ...demoSession,
      userId: "usr_other",
      workspaceId: "ws_other"
    });

    expect(packet.workspaceId).toBe("ws_other");
    expect(packet.kpi.healthScore).toBe(0);
    expect(packet.kpi.optimizationSnapshotStatus).toBe("MISSING");
    expect(packet.kpi.pendingChangeCount).toBe(0);
    expect(packet.kpi.blockedChangeCount).toBe(0);
    expect(packet.kpi.monthlyInternalizationPct).toBe(0);
    expect(packet.kpi.auditCompletenessPct).toBe(0);
    expect(packet.kpi.dataFreshness).toBe("PARTIAL");
    expect(packet.todos).toEqual([
      expect.objectContaining({
        title: "等待治理数据导入",
        status: "PENDING"
      })
    ]);
  });

  it("creates only human-review calibration drafts", async () => {
    const calibrationDraft = await createControlCompassActionDraft(demoSession, "创建校准草案", {
      draftId: "D-20260604-03",
      snapshotId: "OPT-SNAP-20260604-01"
    });
    const restoreDraft = await createControlCompassActionDraft(demoSession, "恢复系统自优化结果", {
      draftId: "D-20260604-03"
    });
    const auditPack = await createControlCompassActionDraft(demoSession, "导出审计包", {
      draftId: "D-20260604-03"
    });

    expect(calibrationDraft.workspaceId).toBe(demoSession.workspaceId);
    expect(calibrationDraft.humanReviewRequired).toBe(true);
    expect(calibrationDraft.auditEvent).toBe("CREATE_CALIBRATION_PARAMETER_DRAFT");
    expect(calibrationDraft.userMessage).toBe("参数校准草案已生成，已保留自优化快照。");
    expect(restoreDraft.auditEvent).toBe("RESTORE_SYSTEM_OPTIMIZATION_DRAFT");
    expect(restoreDraft.userMessage).toBe("系统自优化恢复草案已生成，等待人审与审计。");
    expect(auditPack.status).toBe("AUDIT_PACK_READY");
    expect(auditPack.auditEvent).toBe("EXPORT_CONTROL_COMPASS_AUDIT_PACK");
  });

  it("rejects tenant spoofing in compass actions", async () => {
    await expect(
      createControlCompassActionDraft(demoSession, "查看参数族详情", {
        domainId: "FACTOR_SIGNAL",
        workspaceId: "ws_external_reviewer"
      })
    ).rejects.toMatchObject({ code: "TENANT_SPOOFING" });
  });
});
