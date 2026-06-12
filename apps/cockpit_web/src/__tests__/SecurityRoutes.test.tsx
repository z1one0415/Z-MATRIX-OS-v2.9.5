import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import { App } from "../App";

const routes = ["/holdings", "/selection", "/dayan-ask", "/control-compass", "/history", "/settings", "/operator-profile"];
const forbidden = ["立即买入", "立即卖出", "真实下单", "连接券商下单", "自动交易", "关闭人审", "关闭 Paper-only", "调仓建议"];

describe("Batch 0E frontend route safety", () => {
  it.each(routes)("renders %s without forbidden trade commands", async (route) => {
    const queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false } }
    });
    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={[route]}>
          <App />
        </MemoryRouter>
      </QueryClientProvider>
    );

    const safetyText = route === "/dayan-ask" ? "仅纸面" : "Paper-only";
    expect((await screen.findAllByText(safetyText)).length).toBeGreaterThan(0);
    const text = document.body.textContent || "";

    for (const term of forbidden) {
      expect(text).not.toContain(term);
    }
  });
});
