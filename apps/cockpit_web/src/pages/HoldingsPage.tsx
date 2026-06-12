import { ClipboardCheck, FileSearch, FileText, Layers3, NotebookPen } from "lucide-react";
import type { AuthSession } from "../auth";
import { securityStates } from "../data/cockpit";
import { useHoldingAction, useHoldings } from "../hooks/useHoldings";
import type { HoldingPosition, HoldingReviewDraft } from "../services/holdingsApi";
import { StatusPill } from "../components/StatusPill";
import { useCockpitPreferences } from "../settings/CockpitPreferences";

type HoldingsPageProps = {
  session: AuthSession;
};

const currency = new Intl.NumberFormat("zh-CN", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
});

const integer = new Intl.NumberFormat("zh-CN", {
  maximumFractionDigits: 0
});

const roleLabel: Record<HoldingPosition["role"], string> = {
  CORE: "核心底仓",
  ROTATION: "中期轮动",
  EVENT: "事件观察",
  DEFENSIVE: "防御配置"
};

const actionLabel: Record<HoldingPosition["nextAction"], string> = {
  HOLD_RESEARCH: "继续研究",
  WATCH: "观察",
  THESIS_REVIEW: "Thesis 复核",
  RISK_REVIEW: "风险复核",
  MOVE_TO_OBSERVATION: "移入观察",
  DATA_INSUFFICIENT: "数据不足"
};

const signalLabel: Record<HoldingPosition["signalStrength"], string> = {
  LOW: "低",
  MID: "中",
  HIGH: "高"
};

const securityTooltips: Record<string, string> = {
  "Paper-only": "仅纸面观察，不触发实盘",
  "Human Review": "人工复核开启",
  "Broker Blocked": "券商通道已阻断"
};

function signed(value: number, digits = 2) {
  const formatted = value.toLocaleString("zh-CN", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits
  });
  return value > 0 ? `+${formatted}` : formatted;
}

function toneClass(value: number) {
  if (value > 0) {
    return "is-positive";
  }
  if (value < 0) {
    return "is-negative";
  }
  return "";
}

function alphaText(value: number | null) {
  return value === null ? "待归因" : `${signed(value)}%`;
}

function submitPayload(position?: HoldingPosition) {
  return position
    ? {
        symbol: position.symbol,
        name: position.name,
        source: "holdings-page"
      }
    : { source: "holdings-page" };
}

export function HoldingsPage({ session }: HoldingsPageProps) {
  const { data, isLoading, isError } = useHoldings(session);
  const action = useHoldingAction(session);
  const { copy } = useCockpitPreferences();
  const latestDraft = action.data;

  if (isLoading || !data) {
    return <main className="holdings-page">加载执仓决断数据</main>;
  }

  if (isError) {
    return <main className="holdings-page">当前账户视图暂不可用</main>;
  }

  const packet = data;

  function submitAction(
    actionName: HoldingReviewDraft["action"],
    position?: HoldingPosition
  ) {
    action.mutate({
      action: actionName,
      payload: submitPayload(position)
    });
  }

  return (
    <main className="holdings-page" aria-labelledby="holdings-title">
      <section className="holdings-heading">
        <div className="heading-copy">
          <div className="heading-title-line">
            <h1 id="holdings-title">{copy("copy.holdings", "执仓决断")}</h1>
          </div>
          <p>全局视角 · 精准配置 · 动态进化</p>
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
            <button type="button" className="button button--primary" aria-label={copy("copy.holdingReview", "持仓复核")} title={copy("copy.holdingReview", "持仓复核")} onClick={() => submitAction("持仓复核")}>
              <FileSearch size={18} aria-hidden="true" />
              <span className="button__label">{copy("copy.holdingReview", "持仓复核")}</span>
              <span className="tool-tooltip">{copy("copy.holdingReview", "持仓复核")}</span>
            </button>
            <button type="button" className="button" aria-label={copy("copy.reviewDraft", "生成复核草案")} title={copy("copy.reviewDraft", "生成复核草案")} onClick={() => submitAction("生成复核草案")}>
              <FileText size={18} aria-hidden="true" />
              <span className="button__label">{copy("copy.reviewDraft", "生成复核草案")}</span>
              <span className="tool-tooltip">{copy("copy.reviewDraft", "生成复核草案")}</span>
            </button>
            <button type="button" className="button" aria-label="创建人工研究记录" title="创建人工研究记录" onClick={() => submitAction("创建人工研究记录")}>
              <NotebookPen size={18} aria-hidden="true" />
              <span className="button__label">创建人工研究记录</span>
              <span className="tool-tooltip">创建人工研究记录</span>
            </button>
            <button type="button" className="button button--ghost" aria-label={copy("copy.auditPack", "导出审计包")} title={copy("copy.auditPack", "导出审计包")} onClick={() => submitAction("导出审计包")}>
              <ClipboardCheck size={18} aria-hidden="true" />
              <span className="button__label">{copy("copy.auditPack", "导出审计包")}</span>
              <span className="tool-tooltip">{copy("copy.auditPack", "导出审计包")}</span>
            </button>
          </div>
          <small className="heading-action-note" aria-live="polite">
            {latestDraft ? latestDraft.userMessage : "所有动作进入人工确认。"}
          </small>
        </div>
      </section>

      <section className="holdings-kpi-strip" aria-label="账户状态">
        <article className="kpi-card kpi-card--strong">
          <span>今日盈亏</span>
          <strong className={toneClass(packet.kpi.todayPnl)}>{signed(packet.kpi.todayPnl)}</strong>
          <small className={toneClass(packet.kpi.todayPnlPct)}>{signed(packet.kpi.todayPnlPct)}%</small>
          <small className={toneClass(packet.account.floatingPnl)}>浮动盈亏 {signed(packet.account.floatingPnl)}</small>
          <i className="spark spark--up" aria-hidden="true" />
        </article>
        <article className="kpi-card kpi-card--strong">
          <span>总资产</span>
          <strong>{currency.format(packet.kpi.totalAsset)}</strong>
          <small>{packet.account.currency} · {packet.account.accountMask}</small>
          <i className="spark spark--flat" aria-hidden="true" />
        </article>
        <article className="kpi-card kpi-card--strong">
          <span>持仓 Alpha</span>
          <strong>{alphaText(packet.kpi.holdingAlphaAnnualized)}</strong>
          <small>导入历史后计算</small>
          <i className="spark spark--soft" aria-hidden="true" />
        </article>
        <article className="kpi-card kpi-card--weak">
          <span>现金比例</span>
          <strong>{packet.kpi.cashRatio.toFixed(2)}%</strong>
          <small>现金 {currency.format(packet.account.cash)} · 市值 {integer.format(packet.account.marketValue)}</small>
        </article>
        <article className="kpi-card kpi-card--weak">
          <span>最大回撤</span>
          <strong>{packet.kpi.maxDrawdownRecentYear === null ? "待计算" : `${packet.kpi.maxDrawdownRecentYear}%`}</strong>
          <small>近一年</small>
        </article>
      </section>

      <section className="capital-card panel-shell" aria-label="资金曲线">
        <div className="panel-title">
          <span>资金曲线</span>
          <div className="period-tabs" aria-label="时间筛选">
            {["近1月", "近3月", "近6月", "近1年", "近3年", "全部"].map((label) => (
              <button className={label === "近1年" ? "is-active" : ""} type="button" key={label}>
                {label}
              </button>
            ))}
          </div>
        </div>
        <div className="capital-card__body">
          <div className="portfolio-chart" role="img" aria-label="账户净值与基准的纸面曲线">
            <span className="chart-axis chart-axis--top" />
            <span className="chart-axis chart-axis--middle" />
            <span className="chart-axis chart-axis--bottom" />
            <span className="chart-line chart-line--portfolio" />
            <span className="chart-line chart-line--benchmark" />
            <span className="chart-glow chart-glow--one" />
            <span className="chart-glow chart-glow--two" />
            <span className="chart-label chart-label--portfolio">组合净值</span>
            <span className="chart-label chart-label--benchmark">沪深300</span>
          </div>
          <aside className="curve-stat-list" aria-label="区间表现">
            <strong>区间表现</strong>
            {packet.curveStats.map((stat) => (
              <div key={stat.label}>
                <span>{stat.label}</span>
                <em className={`curve-stat--${stat.tone}`}>{stat.value}</em>
              </div>
            ))}
          </aside>
        </div>
      </section>

      <section className="positions-panel panel-shell">
        <div className="panel-title">
          <span>正式仓位研究表</span>
          <small>研究型持仓 · {packet.positions.length} 只</small>
        </div>
        <div className="positions-table" role="table" aria-label="正式仓位研究表">
          <div role="row" className="positions-row positions-row--head">
            <span role="columnheader">名称</span>
            <span role="columnheader">角色</span>
            <span role="columnheader">仓位</span>
            <span role="columnheader">浮盈亏</span>
            <span role="columnheader">Alpha贡献</span>
            <span role="columnheader">信号强度</span>
            <span role="columnheader">当前动作</span>
          </div>
          {packet.positions.map((position) => (
            <button
              type="button"
              role="row"
              className="positions-row positions-row--button"
              key={position.symbol}
              onClick={() => submitAction("持仓复核", position)}
            >
              <span role="cell">
                <b className="cell-label">名称</b>
                <strong>{position.name}</strong>
                <small>{position.symbol}</small>
              </span>
              <span role="cell">
                <b className="cell-label">角色</b>
                <em className="position-tag">{roleLabel[position.role]}</em>
              </span>
              <span role="cell">
                <b className="cell-label">仓位</b>
                <strong>{position.weightPct.toFixed(2)}%</strong>
                <small>{integer.format(position.quantity)} 股</small>
              </span>
              <span role="cell" className={toneClass(position.floatingPnl)}>
                <b className="cell-label">浮盈亏</b>
                <strong>{signed(position.floatingPnlPct)}%</strong>
                <small>{signed(position.floatingPnl)}</small>
              </span>
              <span role="cell">
                <b className="cell-label">Alpha贡献</b>
                <strong>{alphaText(position.alphaContributionPct)}</strong>
                <small>{position.catalystStatus === "DECAYING" ? "催化衰减" : "继续观察"}</small>
              </span>
              <span role="cell">
                <b className="cell-label">信号强度</b>
                <span className={`signal-dots signal-dots--${position.signalStrength.toLowerCase()}`}>
                  <i />
                  <i />
                  <i />
                  <i />
                  <i />
                </span>
                <small>{signalLabel[position.signalStrength]}</small>
              </span>
              <span role="cell">
                <b className="cell-label">当前动作</b>
                <em className={`position-tag ${position.nextAction.includes("REVIEW") ? "position-tag--risk" : ""}`}>
                  {actionLabel[position.nextAction]}
                </em>
              </span>
            </button>
          ))}
        </div>
      </section>

      <section className="observation-grid" aria-label="三类观察仓">
        {packet.observationWarehouses.map((warehouse) => (
          <article className={`observation-card observation-card--${warehouse.tone}`} key={warehouse.warehouseType}>
            <div className="observation-card__head">
              <div>
                <span>{warehouse.title}</span>
                <strong>{warehouse.count} 只</strong>
              </div>
              <Layers3 size={26} aria-hidden="true" />
            </div>
            <dl>
              <div>
                <dt>今日变化</dt>
                <dd>{warehouse.todayChange}</dd>
              </div>
              <div>
                <dt>待确认</dt>
                <dd>{warehouse.pendingActionCount} 项</dd>
              </div>
              <div>
                <dt>Outcome</dt>
                <dd>{warehouse.outcomeStatus}</dd>
              </div>
            </dl>
            <ul>
              {warehouse.topCandidates.map((candidate) => (
                <li key={`${warehouse.warehouseType}-${candidate.ticker}`}>
                  <span>{candidate.name}</span>
                  <em>{candidate.oneLineReason}</em>
                </li>
              ))}
            </ul>
            <button type="button" onClick={() => submitAction("生成复核草案")}>
              查看详情
            </button>
          </article>
        ))}
      </section>

    </main>
  );
}
