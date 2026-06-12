import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import { App } from "../App";

function renderHistory() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={["/history"]}>
        <App />
      </MemoryRouter>
    </QueryClientProvider>
  );
}

describe("Batch 4 history page", () => {
  it("renders the space-time history cockpit modules from the approved UI master", async () => {
    renderHistory();

    expect(await screen.findByRole("heading", { name: "时空回溯" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "时空回溯概览" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "学习流水线" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "历史事件流" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "历史三库汇总" })).toBeInTheDocument();
    expect(screen.getByLabelText("审计证据链状态")).toBeInTheDocument();
  });

  it("renders kpis, learning pipeline, event stream, and library summaries", async () => {
    renderHistory();

    const kpis = await screen.findByRole("region", { name: "时空回溯概览" });
    expect(within(kpis).getByText("累计报告")).toBeInTheDocument();
    expect(within(kpis).getByText("实盘案例")).toBeInTheDocument();
    expect(within(kpis).getByText("系统记忆")).toBeInTheDocument();
    expect(within(kpis).getByText("规则候选")).toBeInTheDocument();
    expect(within(kpis).getByText("待清理记忆")).toBeInTheDocument();

    const pipeline = screen.getByRole("region", { name: "学习流水线" });
    expect(within(pipeline).getByText("分析报告")).toBeInTheDocument();
    expect(within(pipeline).getByText("固化规则")).toBeInTheDocument();
    expect(within(pipeline).getByLabelText("本月统计")).toBeInTheDocument();

    const timeline = screen.getByRole("region", { name: "历史事件流" });
    expect(within(timeline).getByText("宁德时代")).toBeInTheDocument();
    expect(within(timeline).getByText("历史事件流 / 复盘时间轴")).toBeInTheDocument();

    const libraries = screen.getByRole("region", { name: "历史三库汇总" });
    expect(within(libraries).getByLabelText("分析报告库")).toBeInTheDocument();
    expect(within(libraries).getByLabelText("实盘案例库")).toBeInTheDocument();
    expect(within(libraries).getByLabelText("系统记忆 / 规则候选")).toBeInTheDocument();
  });

  it("switches the right rail to space-time seal semantics", async () => {
    renderHistory();

    expect(await screen.findByText("时空印鉴")).toBeInTheDocument();
    expect(screen.getByText("历史学习判断")).toBeInTheDocument();
    expect(screen.getByLabelText("时空印")).toBeInTheDocument();
    expect(screen.getByText("时空预鉴")).toBeInTheDocument();
    expect(screen.getByText("时空书签")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /时空工具/ })).toBeInTheDocument();
    expect(screen.getByText("报告库")).toBeInTheDocument();
    expect(screen.getByText("规则库")).toBeInTheDocument();
  });

  it("creates safe history review drafts from page actions", async () => {
    const user = userEvent.setup();
    renderHistory();

    await screen.findByRole("heading", { name: "时空回溯" });
    await user.click(screen.getByRole("button", { name: "生成复盘草案" }));

    expect(await screen.findByText("复盘草案已生成，等待人工确认。")).toBeInTheDocument();
    expect(document.body.textContent || "").not.toContain("CREATE_HISTORY_REVIEW_DRAFT");
  });

  it("does not render forbidden commands or backend-only identifiers", async () => {
    renderHistory();
    await screen.findByRole("heading", { name: "时空回溯" });
    const text = document.body.textContent || "";
    const forbidden = [
      "立即买入",
      "立即卖出",
      "买入",
      "卖出",
      "真实下单",
      "连接券商下单",
      "自动交易",
      "启用实盘",
      "一键生效",
      "历史智囊",
      "History Agent",
      "Workspace ·",
      "ws_personal_z_prime",
      "WORKSPACE_SCOPED",
      "OutputEnvelope",
      "AuditEvent",
      "ReportRenderer"
    ];

    for (const term of forbidden) {
      expect(text).not.toContain(term);
    }
  });
});
