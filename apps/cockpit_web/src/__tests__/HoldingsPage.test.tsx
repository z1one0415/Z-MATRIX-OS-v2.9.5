import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import { App } from "../App";

function renderHoldings() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={["/holdings"]}>
        <App />
      </MemoryRouter>
    </QueryClientProvider>
  );
}

describe("Batch 1 holdings page", () => {
  it("renders account summary from the provided screenshot data", async () => {
    renderHoldings();

    expect(await screen.findByRole("heading", { name: "执仓决断" })).toBeInTheDocument();
    expect(screen.getByText("110,249.84")).toBeInTheDocument();
    expect(screen.getByText(/-4,776.77/)).toBeInTheDocument();
    expect(screen.getByText("+3,733.50")).toBeInTheDocument();
    expect(screen.getByText(/110,137/)).toBeInTheDocument();
    expect(screen.getByText(/现金 112.84/)).toBeInTheDocument();
  });

  it("renders the formal research table and observation warehouses from the design blueprint", async () => {
    renderHoldings();

    const table = await screen.findByRole("table", { name: "正式仓位研究表" });
    expect(within(table).getByText("紫金矿业")).toBeInTheDocument();
    expect(within(table).getByText("双环传动")).toBeInTheDocument();
    expect(within(table).getByText("科创创业ETF天弘")).toBeInTheDocument();
    expect(within(table).getAllByText("角色").length).toBeGreaterThan(0);
    expect(within(table).getAllByText("仓位").length).toBeGreaterThan(0);
    expect(within(table).getAllByText("Alpha贡献").length).toBeGreaterThan(0);
    expect(screen.getByRole("region", { name: "三类观察仓" })).toBeInTheDocument();
    expect(screen.getByText("底仓观察")).toBeInTheDocument();
    expect(screen.getByText("轮动观察")).toBeInTheDocument();
    expect(screen.getByText("黑马观察")).toBeInTheDocument();
  });

  it("keeps Tianji Engine as the right-rail cockpit feature", async () => {
    renderHoldings();

    expect(await screen.findByText("天机引擎")).toBeInTheDocument();
    expect(screen.getByLabelText("天机台")).toBeInTheDocument();
    expect(screen.getByText("天机预警")).toBeInTheDocument();
    expect(screen.getByText("天机签")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /天机卜算/ })).toBeInTheDocument();
  });

  it("creates a user-facing review draft message without exposing audit internals", async () => {
    const user = userEvent.setup();
    renderHoldings();

    const actions = await screen.findAllByRole("button", { name: "持仓复核" });
    await user.click(actions[0]);

    expect(await screen.findByText("持仓复核已进入人工确认队列。")).toBeInTheDocument();
    expect(document.body.textContent || "").not.toContain("CREATE_HOLDING_REVIEW_DRAFT");
  });

  it("does not render forbidden trade commands", async () => {
    renderHoldings();
    await screen.findByRole("heading", { name: "执仓决断" });
    const text = document.body.textContent || "";
    const forbidden = [
      "立即买入",
      "立即卖出",
      "真实下单",
      "连接券商下单",
      "自动交易",
      "调仓建议",
      "Workspace ·",
      "ws_personal_z_prime",
      "Broker Runtime",
      "Real Trade",
      "WORKSPACE_SCOPED"
    ];

    for (const term of forbidden) {
      expect(text).not.toContain(term);
    }
  });
});
