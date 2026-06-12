import { ClipboardCheck, FileSearch, FileText, NotebookPen } from "lucide-react";
import { useMemo, useState } from "react";
import type { AuthSession } from "../auth";
import { StatusPill } from "../components/StatusPill";
import {
  CandidateSortingWorkbench,
  MarketOpportunitySummary,
  MatrixTopCards,
  SelectionKpiStrip,
  SevenLayerFilterChain
} from "../components/selection/SelectionPanels";
import { securityStates } from "../data/cockpit";
import { useSelection, useSelectionAction } from "../hooks/useSelection";
import type { SelectionActionDraft, SelectionCandidate } from "../services/selectionApi";
import { useCockpitPreferences } from "../settings/CockpitPreferences";

type SelectionPageProps = {
  session: AuthSession;
};

const securityTooltips: Record<string, string> = {
  "Paper-only": "仅纸面观察，不触发实盘",
  "Human Review": "人工复核开启",
  "Broker Blocked": "券商通道已阻断"
};

function submitPayload(candidate?: SelectionCandidate) {
  return candidate
    ? {
        symbol: candidate.symbol,
        name: candidate.name,
        recommendedRole: candidate.recommendedRole,
        source: "selection-page"
      }
    : { source: "selection-page" };
}

export function SelectionPage({ session }: SelectionPageProps) {
  const { data, isLoading, isError } = useSelection(session);
  const action = useSelectionAction(session);
  const { copy } = useCockpitPreferences();
  const latestDraft = action.data;
  const [selectedSymbol, setSelectedSymbol] = useState<string | null>(null);

  const selectedCandidate = useMemo(() => {
    if (!data?.candidates.length) {
      return undefined;
    }
    return data.candidates.find((candidate) => candidate.symbol === selectedSymbol) ?? data.candidates[0];
  }, [data, selectedSymbol]);

  if (isLoading || !data) {
    return <main className="holdings-page selection-page">加载投研问股数据</main>;
  }

  if (isError) {
    return <main className="holdings-page selection-page">当前投研问股视图暂不可用</main>;
  }

  function submitAction(actionName: SelectionActionDraft["action"], candidate?: SelectionCandidate) {
    action.mutate({
      action: actionName,
      payload: submitPayload(candidate)
    });
  }

  return (
    <main className="holdings-page selection-page" aria-labelledby="selection-title">
      <section className="holdings-heading selection-heading">
        <div className="heading-copy">
          <div className="heading-title-line">
            <h1 id="selection-title">{copy("copy.selection", "投研问股")}</h1>
          </div>
          <p>从全市场拾取发展最合适的研究方向和观察策略</p>
          <div className="heading-status" aria-label="全局安全状态">
            {securityStates.map((state) => (
              <StatusPill
                key={state.label}
                compact
                icon={state.icon}
                label={state.label}
                tone={state.tone}
                tooltip={securityTooltips[state.label]}
              />
            ))}
          </div>
        </div>
        <div className="heading-control">
          <div className="heading-actions">
            <button
              type="button"
              className="button button--primary"
              aria-label="更新候选池过滤结果"
              title="更新候选池过滤结果"
              onClick={() => submitAction("更新候选池过滤结果")}
            >
              <FileSearch size={18} aria-hidden="true" />
              <span className="button__label">更新候选池过滤结果</span>
              <span className="tool-tooltip">更新候选池过滤结果</span>
            </button>
            <button
              type="button"
              className="button"
              aria-label="生成个股研究"
              title="生成个股研究"
              onClick={() => submitAction("生成个股研究", selectedCandidate)}
            >
              <FileText size={18} aria-hidden="true" />
              <span className="button__label">生成个股研究</span>
              <span className="tool-tooltip">生成个股研究</span>
            </button>
            <button
              type="button"
              className="button"
              aria-label="创建人工研究记录"
              title="创建人工研究记录"
              onClick={() => submitAction("创建人工研究记录", selectedCandidate)}
            >
              <NotebookPen size={18} aria-hidden="true" />
              <span className="button__label">创建人工研究记录</span>
              <span className="tool-tooltip">创建人工研究记录</span>
            </button>
            <button
              type="button"
              className="button button--ghost"
              aria-label="导出审计包"
              title="导出审计包"
              onClick={() => submitAction("导出审计包", selectedCandidate)}
            >
              <ClipboardCheck size={18} aria-hidden="true" />
              <span className="button__label">导出审计包</span>
              <span className="tool-tooltip">导出审计包</span>
            </button>
          </div>
          <small className="heading-action-note" aria-live="polite">
            {latestDraft ? latestDraft.userMessage : "所有动作进入人工确认。"}
          </small>
        </div>
      </section>

      <SelectionKpiStrip kpis={data.kpis} />
      <SevenLayerFilterChain packet={data} />
      <MarketOpportunitySummary groups={data.opportunityGroups} />
      <MatrixTopCards groups={data.matrixGroups} />
      <CandidateSortingWorkbench
        candidates={data.candidates}
        selected={selectedCandidate}
        onSelect={(candidate) => setSelectedSymbol(candidate.symbol)}
        onAction={submitAction}
      />
    </main>
  );
}
