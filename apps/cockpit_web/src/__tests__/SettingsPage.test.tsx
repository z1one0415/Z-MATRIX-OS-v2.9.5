import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { App } from "../App";

function renderSettings() {
  if (typeof window.localStorage?.clear === "function") {
    window.localStorage.clear();
  }
  document.documentElement.removeAttribute("data-cockpit-theme");
  document.documentElement.removeAttribute("data-cockpit-font-scale");
  document.documentElement.removeAttribute("data-cockpit-copy-mode");
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={["/settings"]}>
        <App />
      </MemoryRouter>
    </QueryClientProvider>
  );
}

describe("settings page", () => {
  it("renders the real system settings cockpit instead of the generic workbench", async () => {
    renderSettings();

    expect(await screen.findByRole("heading", { name: "系统设置" })).toBeInTheDocument();
    expect(screen.getByLabelText("系统设置工作区")).toBeInTheDocument();
    expect(screen.getByLabelText("设置分类")).toBeInTheDocument();
    expect(screen.getByLabelText("设置页统一状态栏")).toBeInTheDocument();
    expect(document.querySelector(".workbench--settings")).not.toBeInTheDocument();
    expect(screen.queryByLabelText("右侧天机栏")).not.toBeInTheDocument();
    expect(screen.queryByRole("region", { name: "童子谏言" })).not.toBeInTheDocument();
  });

  it("renders the approved categories and the copy mode selector", async () => {
    const user = userEvent.setup();
    renderSettings();

    const categories = await screen.findByLabelText("设置分类");
    for (const label of ["账户显示", "数据源", "大模型 API", "随侍童子", "安全锁", "显示设置", "备份恢复"]) {
      expect(within(categories).getByRole("button", { name: new RegExp(label) })).toBeInTheDocument();
    }

    await user.click(within(categories).getByRole("button", { name: /显示设置/ }));
    expect(screen.getByRole("region", { name: "文字表达模式" })).toBeInTheDocument();
    expect(screen.getByRole("radio", { name: /天机版/ })).toHaveAttribute("aria-checked", "true");
    await user.click(screen.getByRole("radio", { name: /通用版/ }));
    expect(screen.getAllByText("持仓检查").length).toBeGreaterThan(0);
    expect(screen.getByRole("link", { name: /持仓检查/ })).toBeInTheDocument();
    await user.click(screen.getByRole("radio", { name: /English/ }));
    expect(screen.getAllByText("Portfolio Review").length).toBeGreaterThan(0);
    expect(screen.getByRole("link", { name: /Portfolio Review/ })).toBeInTheDocument();
  });

  it("renders LLM API provider settings without exposing API keys", async () => {
    const user = userEvent.setup();
    renderSettings();

    const providerList = await screen.findByLabelText("大模型 API 供应商设置");
    expect(within(providerList).getByText("OpenAI")).toBeInTheDocument();
    expect(within(providerList).getByText("Anthropic Claude")).toBeInTheDocument();
    expect(within(providerList).getByText("DeepSeek")).toBeInTheDocument();
    expect(within(providerList).getByText("通义千问")).toBeInTheDocument();
    expect(within(providerList).getByText("自定义兼容接口")).toBeInTheDocument();
    expect(screen.getByLabelText("大模型 API设置详情")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: /DeepSeek/ }));
    expect(screen.getByLabelText("大模型 API 提供商下探")).toBeInTheDocument();
    expect(screen.getByDisplayValue("https://api.deepseek.com/v1")).toBeInTheDocument();
    expect(screen.getByDisplayValue("deepseek-chat")).toBeInTheDocument();
    expect(screen.getByDisplayValue("deepseek-reasoner")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "测试模型连接" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "保存 API 密钥引用" })).toBeInTheDocument();
    expect(screen.getByText("ENV WAITING")).toBeInTheDocument();
    await user.type(screen.getByPlaceholderText("***REDACTED***"), "secret-llm-token");
    expect(document.body.textContent || "").not.toContain("secret-llm-token");
  });

  it("shows Tushare testing and secret reference controls without plaintext", async () => {
    const user = userEvent.setup();
    renderSettings();

    const categories = await screen.findByLabelText("设置分类");
    await user.click(within(categories).getByRole("button", { name: /数据源/ }));
    expect(screen.getByLabelText("数据连接设置")).toBeInTheDocument();
    expect(screen.getAllByText("Tushare Token").length).toBeGreaterThan(0);
    expect(screen.getAllByText("***REDACTED***").length).toBeGreaterThan(0);
    expect(screen.getByPlaceholderText("输入后保存为密钥引用")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "保存密钥引用" })).toBeInTheDocument();
    expect(screen.getByText("ENV WAITING")).toBeInTheDocument();
    expect(document.body.textContent || "").not.toContain("test-token-value");
    expect(screen.getByRole("button", { name: "校验导入文件" })).toBeInTheDocument();
  });

  it("supports font size and light/dark theme preview controls", async () => {
    const user = userEvent.setup();
    renderSettings();

    const categories = await screen.findByLabelText("设置分类");
    await user.click(within(categories).getByRole("button", { name: /显示设置/ }));
    await user.click(screen.getByRole("radio", { name: "大号" }));
    expect(document.documentElement.dataset.cockpitFontScale).toBe("large");
    await user.click(screen.getByRole("radio", { name: "浅色" }));
    expect(document.documentElement.dataset.cockpitTheme).toBe("light");
  });

  it("keeps simple categories as direct second-level settings and reserves drilldown for LLM provider configuration", async () => {
    const user = userEvent.setup();
    renderSettings();

    const categories = await screen.findByLabelText("设置分类");
    await user.click(within(categories).getByRole("button", { name: /账户显示/ }));
    const accountDetail = screen.getByLabelText("账户显示设置详情");
    expect(within(accountDetail).getByText("账户显示")).toBeInTheDocument();
    expect(within(accountDetail).queryByText("大模型 API")).not.toBeInTheDocument();
    expect(screen.getByDisplayValue("Z-Prime")).toBeInTheDocument();
    expect(screen.queryByLabelText(/下探入口/)).not.toBeInTheDocument();

    await user.click(within(categories).getByRole("button", { name: /随侍童子/ }));
    const assistantDetail = screen.getByLabelText("随侍童子设置详情");
    expect(within(assistantDetail).getByText("随侍童子")).toBeInTheDocument();
    expect(within(assistantDetail).queryByText("大模型 API")).not.toBeInTheDocument();
    expect(screen.getByText("随侍童子偏好")).toBeInTheDocument();
    expect(screen.queryByLabelText(/下探入口/)).not.toBeInTheDocument();

    await user.click(within(categories).getByRole("button", { name: /显示设置/ }));
    const appearanceDetail = screen.getByLabelText("显示设置设置详情");
    expect(within(appearanceDetail).getByText("显示设置")).toBeInTheDocument();
    expect(within(appearanceDetail).queryByText("大模型 API")).not.toBeInTheDocument();
    expect(screen.getByLabelText("显示设置")).toBeInTheDocument();
    expect(within(appearanceDetail).queryByText("导出配置快照")).not.toBeInTheDocument();
    expect(within(appearanceDetail).queryByText("创建恢复草案")).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/下探入口/)).not.toBeInTheDocument();

    await user.click(within(categories).getByRole("button", { name: /备份恢复/ }));
    const backupDetail = screen.getByLabelText("备份恢复设置详情");
    expect(within(backupDetail).getByText("备份恢复")).toBeInTheDocument();
    expect(within(backupDetail).getByText("配置快照")).toBeInTheDocument();
    expect(within(backupDetail).getByText("恢复保护")).toBeInTheDocument();
    expect(within(backupDetail).getByText("导出配置快照")).toBeInTheDocument();
    expect(within(backupDetail).getByText("创建恢复草案")).toBeInTheDocument();
    expect(within(backupDetail).getByText(/不含密钥明文、不含持仓数据、不含研究结论/)).toBeInTheDocument();
    expect(screen.queryByLabelText(/下探入口/)).not.toBeInTheDocument();

    await user.click(within(categories).getByRole("button", { name: /大模型 API/ }));
    await user.click(screen.getByRole("button", { name: /自定义兼容接口/ }));
    expect(screen.getByRole("button", { name: "返回" })).toBeInTheDocument();
    expect(screen.getByLabelText("大模型 API 提供商下探")).toBeInTheDocument();
  });

  it("renders safety locks as read-only status and creates safe action feedback", async () => {
    const user = userEvent.setup();
    renderSettings();

    await user.click(await screen.findByRole("button", { name: /安全锁/ }));
    const locks = screen.getByLabelText("安全锁状态");
    expect(locks).toBeInTheDocument();
    expect(within(locks).getByText("Paper-only")).toBeInTheDocument();
    expect(within(locks).getByText("Agent Direct Mutation Blocked")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "导出安全锁审计" }));
    expect(await screen.findByText("配置审计包已准备好。")).toBeInTheDocument();
  });

  it("keeps page health in one unified status bar instead of repeating a large health panel", async () => {
    renderSettings();

    const statusBar = await screen.findByLabelText("设置页统一状态栏");
    expect(within(statusBar).getByText("后端服务")).toBeInTheDocument();
    expect(within(statusBar).getByText("驾驶舱数据")).toBeInTheDocument();
    expect(within(statusBar).getByText("SkillOS")).toBeInTheDocument();
    expect(within(statusBar).getByText("安全保护")).toBeInTheDocument();
    expect(within(statusBar).getByText("本地数据")).toBeInTheDocument();
    expect(within(statusBar).getByText("配置模板")).toBeInTheDocument();
    expect(within(statusBar).getByText("就绪自检")).toBeInTheDocument();
    expect(within(statusBar).getByText("0/2 env refs")).toBeInTheDocument();
    expect(within(statusBar).getByText("2 blockers")).toBeInTheDocument();
    expect(within(statusBar).getByRole("button", { name: /导出审计记录/ })).toBeInTheDocument();
    expect(screen.queryByLabelText("系统体检")).not.toBeInTheDocument();
    expect(screen.queryByRole("region", { name: "童子谏言" })).not.toBeInTheDocument();
  });

  it("shows local workstation actions as manual copyable commands", async () => {
    renderSettings();

    const panel = await screen.findByLabelText("本地工作台动作");
    expect(within(panel).getByText("本地工作台")).toBeInTheDocument();
    expect(within(panel).getByText("手动确认")).toBeInTheDocument();
    expect(within(panel).getByText("本地安装检查")).toBeInTheDocument();
    expect(within(panel).getByText("后端健康检查")).toBeInTheDocument();
    expect(within(panel).getByText("产品 smoke test")).toBeInTheDocument();
    expect(within(panel).getByText(/scripts\/verify_z_matrix_product_smoke\.sh/)).toBeInTheDocument();
    expect(within(panel).getAllByRole("button", { name: "复制命令" }).length).toBeGreaterThan(0);
  });

  it("shows cockpit page packet manifest as a read-only product index", async () => {
    renderSettings();

    const panel = await screen.findByLabelText("驾驶舱页面索引");
    expect(within(panel).getByText("驾驶舱页面索引")).toBeInTheDocument();
    expect(within(panel).getByText("持仓管理")).toBeInTheDocument();
    expect(within(panel).getByText("投研选股")).toBeInTheDocument();
    expect(within(panel).getByText("历史回溯")).toBeInTheDocument();
    expect(within(panel).getByText("天机罗盘")).toBeInTheDocument();
    expect(within(panel).getByText("大衍天问")).toBeInTheDocument();
    expect(within(panel).getAllByText("READ_ONLY_PACKET").length).toBe(5);
    expect(within(panel).getByText("/api/cockpit/holdings_packet.json")).toBeInTheDocument();
  });

  it("shows research capability status and local report export path", async () => {
    renderSettings();

    const panel = await screen.findByLabelText("研究能力状态");
    expect(within(panel).getByText("研究能力状态")).toBeInTheDocument();
    expect(within(panel).getByText("因子库状态")).toBeInTheDocument();
    expect(within(panel).getByText("历史 OOS")).toBeInTheDocument();
    expect(within(panel).getByText("Forward OOS 等待")).toBeInTheDocument();
    expect(within(panel).getByText("报告导出")).toBeInTheDocument();
    expect(within(panel).getByText("Z_MATRIX_REPORT_EXPORT_EMPTY")).toBeInTheDocument();
    expect(within(panel).getByText(/export_research_report_pack\.py/)).toBeInTheDocument();
    expect(within(panel).getByText("月度刷新")).toBeInTheDocument();
    expect(within(panel).getByText(/--dry-plan/)).toBeInTheDocument();
  });

  it("shows local data source and data quality audit status", async () => {
    renderSettings();

    const panel = await screen.findByLabelText("数据源与质量审计");
    expect(within(panel).getByText("数据源与质量审计")).toBeInTheDocument();
    expect(within(panel).getByText("本地 Vendor Store")).toBeInTheDocument();
    expect(within(panel).getByText("质量证据")).toBeInTheDocument();
    expect(within(panel).getByText("私有数据保护")).toBeInTheDocument();
    expect(within(panel).getByText("Source Health")).toBeInTheDocument();
    expect(within(panel).getByText("刷新 dry plan")).toBeInTheDocument();
    expect(within(panel).getByText("LOCAL_TERMINAL_MANUAL_DRY_PLAN")).toBeInTheDocument();
    expect(within(panel).getAllByText("LOCAL_VENDOR_STORE_ONLY").length).toBeGreaterThan(0);
  });

  it("shows research evidence groups without alpha promotion", async () => {
    renderSettings();

    const panel = await screen.findByLabelText("研究证据索引");
    expect(within(panel).getByText("研究证据索引")).toBeInTheDocument();
    expect(within(panel).getByText("因子库状态")).toBeInTheDocument();
    expect(within(panel).getByText("历史 OOS")).toBeInTheDocument();
    expect(within(panel).getByText("Forward OOS 等待")).toBeInTheDocument();
    expect(within(panel).getByText("Gatekeeper 审计")).toBeInTheDocument();
    expect(within(panel).getAllByText("RESEARCH_ONLY_NO_ALPHA_PROMOTION").length).toBeGreaterThan(0);
    expect(within(panel).getAllByText("backend").length).toBeGreaterThan(0);
  });

  it("does not render forbidden operational commands or internal identifiers", async () => {
    renderSettings();
    await screen.findByRole("heading", { name: "系统设置" });
    const text = document.body.textContent || "";
    const phrase = (...parts: string[]) => parts.join("");
    const forbidden = [
      phrase("买", "入"),
      phrase("卖", "出"),
      phrase("下", "单"),
      phrase("自动", "交易"),
      phrase("启用", "实盘"),
      phrase("关闭", "人审"),
      phrase("规则", "立即", "生效"),
      "pipeline",
      "router",
      "workspaceId",
      "rawSecret"
    ];

    for (const term of forbidden) {
      expect(text).not.toContain(term);
    }
  });
});
