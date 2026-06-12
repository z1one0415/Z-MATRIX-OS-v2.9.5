import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { App } from "../App";

function renderDayanAsk() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={["/dayan-ask"]}>
        <App />
      </MemoryRouter>
    </QueryClientProvider>
  );
}

describe("Batch 5 dayan ask page", () => {
  it("renders the nine-palace AI research console from the UI master", async () => {
    renderDayanAsk();

    expect(await screen.findByRole("heading", { name: "大衍天问" })).toBeInTheDocument();
    expect(screen.getByLabelText("大衍天问九宫控制台")).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "问天法坛" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "问天法阵" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "童子谏言" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "问天法门" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "问天对弈" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "天官问策" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "熔炼法门" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "我的法门" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "落子复盘" })).toBeInTheDocument();
  });

  it("renders SkillOS progress as user-facing method capacity", async () => {
    renderDayanAsk();

    const status = await screen.findByLabelText("大衍天问系统状态");
    expect(within(status).getByText(/可召法门 104/)).toBeInTheDocument();
    expect(within(status).getByText("领域 17")).toBeInTheDocument();
    expect(within(status).getByText("最高边界 草案")).toBeInTheDocument();
    expect(within(status).getByText("工作流 仅纸面")).toBeInTheDocument();
    expect(within(status).getByText("正式库改写 已阻断")).toBeInTheDocument();
  });

  it("inserts formations into the central chat input without direct execution", async () => {
    const user = userEvent.setup();
    renderDayanAsk();

    await screen.findByRole("heading", { name: "大衍天问" });
    await user.click(screen.getByRole("button", { name: /趋势破局阵/ }));

    expect(screen.getByLabelText("问天输入")).toHaveValue("请用趋势破局阵拆解当前主题。");
    expect(await screen.findByText("法门提示已插入中宫，可继续编辑。")).toBeInTheDocument();
  });

  it("opens the method drawer and inserts a concrete method prompt", async () => {
    const user = userEvent.setup();
    renderDayanAsk();

    await screen.findByRole("heading", { name: "大衍天问" });
    const skillPanel = screen.getByRole("region", { name: "问天法门" });
    await user.click(within(skillPanel).getByRole("button", { name: /持仓问诊/ }));

    const drawer = await screen.findByLabelText("持仓问诊法门抽屉");
    expect(within(drawer).getByText("今日持仓风向")).toBeInTheDocument();

    await user.click(within(drawer).getByRole("button", { name: /正式仓体检/ }));
    expect(screen.getByLabelText("问天输入")).toHaveValue("请对正式仓进行复核，重点列出原判断是否仍成立，并生成待确认草案。");
    expect(screen.queryByLabelText("持仓问诊法门抽屉")).not.toBeInTheDocument();
  });

  it("creates a research-chain draft from central chat", async () => {
    const user = userEvent.setup();
    renderDayanAsk();

    await screen.findByRole("heading", { name: "大衍天问" });
    await user.clear(screen.getByLabelText("问天输入"));
    await user.type(screen.getByLabelText("问天输入"), "请研究半导体设备国产化机会");
    await user.click(screen.getByRole("button", { name: "发送问天问题" }));

    expect(await screen.findByText(/随侍童子已生成研究链路草案/)).toBeInTheDocument();
    expect(await screen.findByText("研究链路草案已创建，等待人审裁定。")).toBeInTheDocument();
  });

  it("keeps the Hermes advisory panel lightweight inside the nine-palace layout", async () => {
    renderDayanAsk();

    const guidance = await screen.findByRole("region", { name: "童子谏言" });
    expect(within(guidance).queryByRole("button", { name: "问童子" })).not.toBeInTheDocument();
    expect(within(guidance).queryByRole("button", { name: "开始新的研究" })).not.toBeInTheDocument();
    expect(within(guidance).queryByText("我应该先选哪个法阵？")).not.toBeInTheDocument();
    expect(screen.getByRole("region", { name: "问天对弈" })).toHaveAttribute("aria-expanded", "false");
    expect(screen.queryByRole("complementary", { name: "童子谏言悬浮问答" })).not.toBeInTheDocument();
  });

  it("does not keep the old typo for Hermes advisory", async () => {
    renderDayanAsk();
    await screen.findByRole("heading", { name: "大衍天问" });

    expect(document.body.textContent || "").toContain("童子谏言");
    expect(document.body.textContent || "").not.toContain("童子荐言");
  });

  it("does not render forbidden trade commands or backend-only terms", async () => {
    renderDayanAsk();
    await screen.findByRole("heading", { name: "大衍天问" });

    const text = document.body.textContent || "";
    const forbidden = [
      "买入",
      "卖出",
      "真实下单",
      "自动交易",
      "启用实盘",
      "规则立即生效",
      "记忆自动写入正式库",
      "参数自动生效",
      "thesis",
      "pipeline",
      "reviewer",
      "IRF",
      "ZC35",
      "B/R/D",
      "skill",
      "agent",
      "OutputEnvelope",
      "Risk Flag",
      "Proposal"
    ];

    for (const term of forbidden) {
      expect(text).not.toContain(term);
    }
  });
});
