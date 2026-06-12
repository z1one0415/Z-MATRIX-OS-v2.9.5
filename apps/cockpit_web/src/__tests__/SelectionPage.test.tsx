import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import { App } from "../App";

function renderSelection() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={["/selection"]}>
        <App />
      </MemoryRouter>
    </QueryClientProvider>
  );
}

describe("Batch 2 selection page", () => {
  it("renders the research cockpit modules from the approved UI master", async () => {
    renderSelection();

    expect(await screen.findByRole("heading", { name: "投研问股" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "投研问股概览" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "七层过滤链" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "市场机会热度" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "三矩阵选股区" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "候选矩阵和待选分析台" })).toBeInTheDocument();
  });

  it("renders the seven user-facing filter steps without backend gate codes", async () => {
    renderSelection();

    const chain = await screen.findByRole("region", { name: "七层过滤链" });
    expect(within(chain).getByText("宏观水温过滤")).toBeInTheDocument();
    expect(within(chain).getByText("10链×5力产业链分析")).toBeInTheDocument();
    expect(within(chain).getByText("31板块顺逆风排序")).toBeInTheDocument();
    expect(within(chain).getByText("财务健康过滤")).toBeInTheDocument();
    expect(within(chain).getByText("底仓/轮动/黑马角色识别")).toBeInTheDocument();
    expect(within(chain).getByText("催化有效期与退潮过滤")).toBeInTheDocument();
    expect(within(chain).getByText("可执行性与账户适配过滤")).toBeInTheDocument();

    const chainText = chain.textContent || "";
    expect(chainText).not.toContain("ZC35");
    expect(chainText).not.toContain("ZC40");
    expect(chainText).not.toContain("ZC50");
  });

  it("renders candidate sorting and creates safe research drafts", async () => {
    const user = userEvent.setup();
    renderSelection();

    const workbench = await screen.findByRole("region", { name: "候选矩阵和待选分析台" });
    expect(within(workbench).getAllByText("中际旭创").length).toBeGreaterThan(0);
    expect(within(workbench).getByText("低位人机共识信号")).toBeInTheDocument();

    await user.click(within(workbench).getByRole("button", { name: /创建人工研究记录/ }));
    expect(await screen.findByText("已创建人工研究记录草案。")).toBeInTheDocument();
    expect(document.body.textContent || "").not.toContain("CREATE_MANUAL_SELECTION_RESEARCH_RECORD");
  });

  it("switches the Tianji Engine to selection semantics", async () => {
    renderSelection();

    expect(await screen.findByText("天机引擎")).toBeInTheDocument();
    expect(screen.getByText("候选路径判断")).toBeInTheDocument();
    expect(screen.getByText("候选风向")).toBeInTheDocument();
    expect(screen.getByText("打开投研问股工具箱")).toBeInTheDocument();
    expect(screen.getByText("更新候选池过滤结果")).toBeInTheDocument();
  });

  it("does not render forbidden trade commands or backend audit fields", async () => {
    renderSelection();
    await screen.findByRole("heading", { name: "投研问股" });
    const text = document.body.textContent || "";
    const forbidden = [
      "立即买入",
      "立即卖出",
      "买入",
      "卖出",
      "建仓",
      "加仓",
      "减仓",
      "真实下单",
      "连接券商下单",
      "自动交易",
      "目标价",
      "止损",
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
