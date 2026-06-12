import { demoSession } from "../auth";
import {
  attemptWorkspaceRead,
  buildAgentTaskEnvelope,
  createWorkspaceDraft,
  findClientTenantFields,
  getCockpitPagePacket,
  MockApiError,
  saveDataSourceSecret
} from "../services/mockApi";

describe("tenant-aware mock api Batch 0D", () => {
  it("returns only current workspace data", async () => {
    const packet = await getCockpitPagePacket(demoSession, "holdings");

    expect(packet.workspaceId).toBe(demoSession.workspaceId);
    expect(packet.rows.map((row) => row[0])).toEqual(["紫金矿业", "双环传动", "科创创业ETF天弘"]);
    expect(packet.rows.map((row) => row[0])).not.toContain("600519 贵州茅台");
    expect(packet.audit.dataScope).toBe("WORKSPACE_SCOPED");
  });

  it("rejects client supplied tenant fields", async () => {
    await expect(
      createWorkspaceDraft(
        demoSession,
        {
          ticker: "300750",
          workspaceId: "ws_external_reviewer"
        },
        "CREATE_RESEARCH_RECORD"
      )
    ).rejects.toMatchObject({ code: "TENANT_SPOOFING" });
  });

  it("detects nested tenant spoofing fields", () => {
    expect(findClientTenantFields({ meta: { created_by: "attacker" }, rows: [{ updatedBy: "x" }] })).toEqual([
      "created_by",
      "updatedBy"
    ]);
  });

  it("blocks cross workspace reads", async () => {
    await expect(attemptWorkspaceRead(demoSession, "ws_external_reviewer")).rejects.toMatchObject({
      code: "FORBIDDEN_WORKSPACE"
    });
  });

  it("saves data source secret as a redacted reference", async () => {
    const rawToken = "tushare-secret-value-123456";
    const response = await saveDataSourceSecret(demoSession, "tushare", rawToken);

    expect(response.workspaceId).toBe(demoSession.workspaceId);
    expect(response.tokenPreview).toBe("***REDACTED***");
    expect(JSON.stringify(response)).not.toContain(rawToken);
  });

  it("agent task envelope carries workspace context and blocks runtime", () => {
    const envelope = buildAgentTaskEnvelope(demoSession, "hermes", "BUILD_RESEARCH_DRAFT", { ticker: "300750" });

    expect(envelope.workspaceId).toBe(demoSession.workspaceId);
    expect(envelope.currentUserId).toBe(demoSession.userId);
    expect(envelope.writeLayers).toEqual(["workspace_scoped_drafts"]);
    expect(envelope.production).toBe("BLOCKED");
    expect(envelope.brokerRuntime).toBe("BLOCKED");
    expect(envelope.realTrade).toBe("BLOCKED");
  });

  it("raises typed errors", async () => {
    await expect(attemptWorkspaceRead(null, "ws_personal_z_prime")).rejects.toBeInstanceOf(MockApiError);
  });
});
