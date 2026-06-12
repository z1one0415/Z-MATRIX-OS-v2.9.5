import { ClipboardCheck, FileSearch, FileText, NotebookPen } from "lucide-react";
import type { AuthSession } from "../auth";
import {
  HistoryEventTimeline,
  HistoryEvidenceBand,
  HistoryKpiStrip,
  HistoryLibraryCards,
  LearningPipelinePanel
} from "../components/history/HistoryPanels";
import { StatusPill } from "../components/StatusPill";
import { securityStates } from "../data/cockpit";
import { useHistory, useHistoryAction } from "../hooks/useHistory";
import type { HistoryActionDraft } from "../services/historyApi";
import { useCockpitPreferences } from "../settings/CockpitPreferences";

type HistoryPageProps = {
  session: AuthSession;
};

const securityTooltips: Record<string, string> = {
  "Paper-only": "仅纸面复盘，不触发实盘",
  "Human Review": "记忆与规则草案必须人工复核",
  "Broker Blocked": "券商与实盘通道已阻断"
};

export function HistoryPage({ session }: HistoryPageProps) {
  const { data, isLoading, isError } = useHistory(session);
  const action = useHistoryAction(session);
  const { copy } = useCockpitPreferences();
  const latestDraft = action.data;

  if (isLoading || !data) {
    return <main className="holdings-page history-page">加载时空回溯数据</main>;
  }

  if (isError) {
    return <main className="holdings-page history-page">当前时空回溯视图暂不可用</main>;
  }

  function submitAction(actionName: HistoryActionDraft["action"], payload: Record<string, unknown> = {}) {
    action.mutate({
      action: actionName,
      payload: {
        source: "history-page",
        ...payload
      }
    });
  }

  return (
    <main className="holdings-page history-page" aria-labelledby="history-title">
      <section className="holdings-heading history-heading">
        <div className="heading-copy">
          <div className="heading-title-line">
            <h1 id="history-title">{copy("copy.history", "时空回溯")}</h1>
          </div>
          <p>研究沉淀 · 复盘进化 · 规则内化</p>
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
              aria-label="查看全部报告"
              title="查看全部报告"
              onClick={() => submitAction("查看全部报告", { targetId: "REPORT_LIBRARY" })}
            >
              <FileSearch size={18} aria-hidden="true" />
              <span className="button__label">查看全部报告</span>
              <span className="tool-tooltip">查看全部报告</span>
            </button>
            <button
              type="button"
              className="button"
              aria-label="生成复盘草案"
              title="生成复盘草案"
              onClick={() => submitAction("生成复盘草案", { targetId: "HISTORY_REVIEW" })}
            >
              <FileText size={18} aria-hidden="true" />
              <span className="button__label">生成复盘草案</span>
              <span className="tool-tooltip">生成复盘草案</span>
            </button>
            <button
              type="button"
              className="button"
              aria-label="创建人工研究记录"
              title="创建人工研究记录"
              onClick={() => submitAction("创建人工研究记录", { targetId: "MANUAL_RESEARCH" })}
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
              onClick={() => submitAction("导出审计包", { targetId: "HISTORY_AUDIT" })}
            >
              <ClipboardCheck size={18} aria-hidden="true" />
              <span className="button__label">导出审计包</span>
              <span className="tool-tooltip">导出审计包</span>
            </button>
          </div>
          <small className="heading-action-note" aria-live="polite">
            {latestDraft ? latestDraft.userMessage : "所有记忆与规则动作进入人工确认。"}
          </small>
        </div>
      </section>

      <HistoryKpiStrip kpis={data.kpis} />
      <LearningPipelinePanel data={data} />
      <HistoryEventTimeline events={data.events} onAction={submitAction} />
      <HistoryLibraryCards
        reports={data.reportLibrary}
        cases={data.caseLibrary}
        data={data}
        onAction={submitAction}
      />
      <HistoryEvidenceBand data={data} />
    </main>
  );
}
