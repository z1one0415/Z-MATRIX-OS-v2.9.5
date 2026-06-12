import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import { App } from "../App";

function renderControlCompass() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={["/control-compass"]}>
        <App />
      </MemoryRouter>
    </QueryClientProvider>
  );
}

describe("Batch 3B control compass page", () => {
  it("renders the control compass modules from the approved UI master", async () => {
    renderControlCompass();

    expect(await screen.findByRole("heading", { name: "天机罗盘" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "天机罗盘指标" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "主干量化参数罗盘" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "参数族校准详情" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "天机推衍区" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "天机衍变裁定" })).toBeInTheDocument();
  });

  it("renders all eight quant parameter domains and switches selected domain context", async () => {
    const user = userEvent.setup();
    renderControlCompass();

    const map = await screen.findByRole("region", { name: "主干量化参数罗盘" });
    const domainList = within(map).getByLabelText("量化参数域状态列");
    expect(within(domainList).getByText("数据质量门")).toBeInTheDocument();
    expect(within(domainList).getByText("样本池韧性")).toBeInTheDocument();
    expect(within(domainList).getByText("因子信号门")).toBeInTheDocument();
    expect(within(domainList).getByText("催化周期门")).toBeInTheDocument();
    expect(within(domainList).getByText("B-Matrix 底仓")).toBeInTheDocument();
    expect(within(domainList).getByText("R-Matrix 轮动")).toBeInTheDocument();
    expect(within(domainList).getByText("D-Matrix 黑马")).toBeInTheDocument();
    expect(within(domainList).getByText("经验内化")).toBeInTheDocument();

    await user.click(within(domainList).getByRole("button", { name: /R-Matrix 轮动/ }));
    expect(screen.getByText(/当前参数域：06 R-Matrix 轮动/)).toBeInTheDocument();

    const compassPlate = within(map).getByRole("img", { name: "八域量化参数校准罗盘" });
    expect(within(map).getByRole("complementary", { name: "当前参数域摘要" })).toBeInTheDocument();
    await user.click(within(compassPlate).getByRole("button", { name: "经验内化 稳定" }));
    expect(screen.getByText(/当前参数域：08 经验内化/)).toBeInTheDocument();
    expect(within(domainList).getByRole("button", { name: /经验内化/ })).toHaveClass("is-selected");
    expect(within(map).getByText("最近复核")).toBeInTheDocument();
    expect(within(map).getByText("2026-06-04 09:22")).toBeInTheDocument();
    expect(within(compassPlate).queryByText("审计落盘")).not.toBeInTheDocument();
    expect(within(compassPlate).queryByText("参数治理")).not.toBeInTheDocument();
    expect(map.querySelector(".compass-connector-layer")).not.toBeInTheDocument();

    await user.hover(within(domainList).getByRole("button", { name: /因子信号门/ }));
    expect(within(compassPlate).getByRole("button", { name: "因子信号门 待校准" })).toHaveClass("is-linked");
  });

  it("switches the right rail to compass semantics", async () => {
    renderControlCompass();

    expect(await screen.findByText("天机衍算")).toBeInTheDocument();
    expect(screen.getByText("量化参数判断")).toBeInTheDocument();
    expect(screen.getByLabelText("校准台")).toBeInTheDocument();
    expect(screen.getAllByText("参数分歧").length).toBeGreaterThan(0);
    expect(screen.getByText("天衍印鉴")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /参数落盘/ })).toBeInTheDocument();
    expect(screen.getByText("打开参数校准工具箱")).toBeInTheDocument();
  });

  it("creates safe calibration drafts from page actions", async () => {
    const user = userEvent.setup();
    renderControlCompass();

    const sandbox = await screen.findByRole("region", { name: "天机推衍区" });
    await user.click(within(sandbox).getByRole("button", { name: "创建校准草案" }));

    expect(await screen.findByText("参数校准草案已生成，已保留自优化快照。")).toBeInTheDocument();
    expect(document.body.textContent || "").not.toContain("CREATE_CALIBRATION_PARAMETER_DRAFT");
  });

  it("does not render forbidden production or real-trade commands", async () => {
    renderControlCompass();
    await screen.findByRole("heading", { name: "天机罗盘" });
    const text = document.body.textContent || "";
    const forbidden = [
      "立即生效",
      "自动生效",
      "启用实盘",
      "连接券商",
      "自动买入",
      "自动卖出",
      "一键调仓",
      "直接清理记忆",
      "直接固化规则",
      "绕过人审",
      "SkillOS",
      "schema hash",
      "记忆清理",
      "催化治理",
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
