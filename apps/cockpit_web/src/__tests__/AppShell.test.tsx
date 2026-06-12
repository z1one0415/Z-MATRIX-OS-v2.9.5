import { render, screen, within } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import userEvent from "@testing-library/user-event";
import { App } from "../App";

function ensureLocalStorage() {
  if (typeof window.localStorage?.getItem === "function" && typeof window.localStorage?.setItem === "function") {
    return;
  }

  const memoryStorage = new Map<string, string>();
  Object.defineProperty(window, "localStorage", {
    configurable: true,
    value: {
      clear: () => memoryStorage.clear(),
      getItem: (key: string) => memoryStorage.get(key) ?? null,
      removeItem: (key: string) => memoryStorage.delete(key),
      setItem: (key: string, value: string) => memoryStorage.set(key, value)
    }
  });
}

function renderAt(path = "/holdings", options: { copyMode?: "tianji" | "plain" | "english" } = {}) {
  ensureLocalStorage();
  if (typeof window.localStorage?.clear === "function") {
    window.localStorage.clear();
  }
  if (options.copyMode) {
    window.localStorage.setItem("zmatrix.cockpit.copyMode", options.copyMode);
  }
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[path]}>
        <App />
      </MemoryRouter>
    </QueryClientProvider>
  );
}

describe("Cockpit AppShell Batch 0C", () => {
  it("renders the frozen navigation labels in order", () => {
    renderAt();
    const nav = screen.getByLabelText("全局导航");
    const labels = within(nav)
      .getAllByRole("link")
      .map((link) => link.textContent || "");

    expect(labels[0]).toContain("Z-MATRIX");
    expect(labels[1]).toContain("Z-Prime");
    expect(labels[2]).toContain("执仓决断");
    expect(labels[3]).toContain("投研问股");
    expect(labels[4]).toContain("大衍天问");
    expect(labels[5]).toContain("天机罗盘");
    expect(labels[6]).toContain("时空回溯");
    expect(labels[7]).toContain("系统设置");
  });

  it("keeps safety states visible in the top bar", async () => {
    renderAt("/selection");

    expect((await screen.findAllByText("Paper-only")).length).toBeGreaterThan(0);
    expect(screen.getByText("Human Review")).toBeInTheDocument();
    expect(screen.getByText("Broker Blocked")).toBeInTheDocument();
    expect(await screen.findByRole("heading", { name: "投研问股" })).toBeInTheDocument();
  });

  it("uses approved action copy for selection and holdings", async () => {
    renderAt("/selection");
    expect((await screen.findAllByRole("button", { name: /创建人工研究记录/ })).length).toBeGreaterThan(0);

    renderAt("/holdings");
    expect((await screen.findAllByRole("button", { name: /持仓复核/ })).length).toBeGreaterThan(0);
  });

  it("switches history route to the space-time seal rail", async () => {
    renderAt("/history");

    expect(await screen.findByRole("heading", { name: "时空回溯" })).toBeInTheDocument();
    expect(screen.getByText("时空印鉴")).toBeInTheDocument();
    expect(screen.getByText("历史学习判断")).toBeInTheDocument();
    expect(screen.getByText("时空书签")).toBeInTheDocument();
  });

  it("renders the global Hermes advisory entry in non-dayan rails", async () => {
    renderAt("/holdings");

    const advisory = await screen.findByRole("region", { name: "童子谏言" });
    const rail = screen.getByLabelText("右侧天机栏");
    expect(rail.querySelector(".rail-panel")?.getAttribute("aria-label")).toBe("童子谏言");
    expect(within(advisory).getByRole("button", { name: /问童子/ })).toBeInTheDocument();
    expect(within(advisory).queryByRole("button", { name: /当前持仓最需要复核的风险是什么/ })).not.toBeInTheDocument();
  });

  it("applies copy mode to page body and right rail, not only navigation", async () => {
    renderAt("/holdings", { copyMode: "plain" });

    expect(await screen.findByRole("heading", { name: "持仓检查" })).toBeInTheDocument();
    expect(await screen.findByText("研究提示")).toBeInTheDocument();
    expect(screen.getByText("状态概览")).toBeInTheDocument();
    expect(screen.getByText("风险提醒")).toBeInTheDocument();
    expect(screen.getByText("判断标签")).toBeInTheDocument();
    expect(screen.queryByText("天机引擎")).not.toBeInTheDocument();
    expect(screen.queryByText("天机台")).not.toBeInTheDocument();
  });

  it("opens the floating Hermes chat with page prompt suggestions from the ask button", async () => {
    const user = userEvent.setup();
    renderAt("/selection");

    const advisory = await screen.findByRole("region", { name: "童子谏言" });
    await user.click(within(advisory).getByRole("button", { name: /问童子/ }));

    const chat = await screen.findByRole("complementary", { name: "童子谏言悬浮问答" });
    expect(within(chat).getByRole("button", { name: "当前候选池最大的筛选瓶颈是什么？" })).toBeInTheDocument();
    expect(within(chat).getByLabelText("问童子输入")).toHaveValue("");
  });

  it("uses full-canvas layout for dayan ask instead of the generic right rail", async () => {
    renderAt("/dayan-ask");

    expect(await screen.findByRole("heading", { name: "大衍天问" })).toBeInTheDocument();
    expect(screen.getByLabelText("大衍天问九宫控制台")).toBeInTheDocument();
    expect(document.querySelector(".cockpit-body--full")).toBeInTheDocument();
    expect(screen.queryByText("天机引擎")).not.toBeInTheDocument();
    expect(screen.queryByText("时空印鉴")).not.toBeInTheDocument();
    expect(screen.queryByRole("complementary", { name: "童子谏言悬浮问答" })).not.toBeInTheDocument();
  });

  it("routes operator profile through the user card, not the normal nav list", async () => {
    renderAt("/operator-profile");

    expect(await screen.findByRole("heading", { name: "操盘者画像" })).toBeInTheDocument();
    expect(screen.getByText("中长为主 · 纪律优先 · 风险可控")).toBeInTheDocument();
    expect(document.body.textContent || "").not.toContain("ws_personal_z_prime");
  });

  it("does not render forbidden real-trade commands", async () => {
    renderAt("/settings");
    await screen.findByRole("heading", { name: "系统设置" });
    const html = document.body.textContent || "";
    const forbidden = ["立即买入", "立即卖出", "真实下单", "连接券商下单", "自动交易"];

    for (const term of forbidden) {
      expect(html).not.toContain(term);
    }
  });

  it("uses the dedicated settings layout without the generic right rail", async () => {
    renderAt("/settings");

    expect(await screen.findByRole("heading", { name: "系统设置" })).toBeInTheDocument();
    expect(document.querySelector(".cockpit-body--full")).toBeInTheDocument();
    expect(screen.getByLabelText("设置页统一状态栏")).toBeInTheDocument();
    expect(screen.queryByLabelText("全局工具")).not.toBeInTheDocument();
    expect(screen.queryByLabelText("右侧天机栏")).not.toBeInTheDocument();
    expect(screen.queryByText("系统护栏")).not.toBeInTheDocument();
  });
});
