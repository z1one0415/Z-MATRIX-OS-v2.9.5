import { ArrowRight, FileText, ShieldCheck } from "lucide-react";
import type { AuthSession } from "../auth";
import { securityStates, type CockpitRouteId } from "../data/cockpit";
import { useCockpitPage } from "../hooks/useCockpitPage";
import { StatusPill } from "../components/StatusPill";

type WorkbenchPageProps = {
  pageId: CockpitRouteId;
  session: AuthSession;
};

export function WorkbenchPage({ pageId, session }: WorkbenchPageProps) {
  const { data: copy, isLoading, isError } = useCockpitPage(session, pageId);

  if (isLoading || !copy) {
    return (
      <main className="workbench" aria-label="加载中">
        <section className="chart-panel">
          <div className="panel-title">
            <span>加载驾驶舱数据</span>
            <small>个人档案</small>
          </div>
        </section>
      </main>
    );
  }

  if (isError) {
    return (
      <main className="workbench" aria-label="加载失败">
        <section className="chart-panel">
          <div className="panel-title">
            <span>权限校验失败</span>
            <small>Human Review</small>
          </div>
        </section>
      </main>
    );
  }

  return (
    <main className={`workbench workbench--${pageId}`} aria-labelledby={`${pageId}-title`}>
      <section className="page-heading">
        <div>
          <h1 id={`${pageId}-title`}>{copy.title}</h1>
          <p>{copy.kicker}</p>
          <div className="heading-status" aria-label="全局安全状态">
            {securityStates.map((state) => (
              <StatusPill key={state.label} icon={state.icon} label={state.label} tone={state.tone} />
            ))}
          </div>
        </div>
        <div className="heading-actions">
          <button type="button" className="button button--primary">
            <FileText size={16} aria-hidden="true" />
            {copy.primaryAction}
          </button>
          <button type="button" className="button">
            <ShieldCheck size={16} aria-hidden="true" />
            {copy.secondaryAction}
          </button>
        </div>
      </section>

      <section className="metric-grid" aria-label={`${copy.title}指标`}>
        {copy.stats.map(([label, value, hint]) => (
          <article key={label} className="metric-card">
            <span>{label}</span>
            <strong>{value}</strong>
            <small>{hint}</small>
          </article>
        ))}
      </section>

      <section className="chart-panel" aria-label={`${copy.title}主工作区`}>
        <div className="panel-title">
          <span>{pageId === "dayan" ? "中宫研究链" : "主工作台"}</span>
          <small>Paper-only</small>
        </div>
        <div className="signal-canvas" role="img" aria-label="纸面研究趋势图">
          <span className="signal-line signal-line--one" />
          <span className="signal-line signal-line--two" />
          <span className="signal-dot signal-dot--a" />
          <span className="signal-dot signal-dot--b" />
          <span className="signal-dot signal-dot--c" />
        </div>
      </section>

      <section className="data-panel">
        <div className="panel-title">
          <span>{copy.tableTitle}</span>
          <small>当前档案</small>
        </div>
        <div className="data-table" role="table" aria-label={copy.tableTitle}>
          <div role="row" className="data-row data-row--head">
            <span role="columnheader">对象</span>
            <span role="columnheader">数量 / 类型</span>
            <span role="columnheader">状态</span>
            <span role="columnheader">动作</span>
          </div>
          {copy.rows.map((row) => (
            <div role="row" className="data-row" key={row.join("-")}>
              {row.map((cell, index) => (
                <span role="cell" key={`${cell}-${index}`}>
                  {cell}
                </span>
              ))}
            </div>
          ))}
        </div>
      </section>

      <section className="review-band" aria-label="人工复核边界">
        <div>
          <strong>Human Review Required</strong>
          <span>所有草案、复核、参数、记忆与报告写入均需人工确认。</span>
        </div>
        <button type="button" className="button button--ghost">
          查看审计
          <ArrowRight size={15} aria-hidden="true" />
        </button>
      </section>
    </main>
  );
}
