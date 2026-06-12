import { demoSession } from "../auth";
import { createControlCompassActionDraft, getControlCompassPageData } from "../services/controlCompassApi";

describe("Batch 3B control compass tenant-aware data", () => {
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
