import {
  ArrowDownRight,
  ArrowUpRight,
  BarChart3,
  Bot,
  Boxes,
  Brain,
  CheckCircle2,
  FileText,
  Gauge,
  Layers3,
  NotebookPen,
  ShieldCheck,
  Sparkles,
  Thermometer,
  TrendingUp
} from "lucide-react";
import type {
  SelectionActionDraft,
  SelectionCandidate,
  SelectionDashboardPacket,
  SelectionFilterStep,
  SelectionKpi,
  SelectionMatrixGroup,
  SelectionOpportunityGroup
} from "../../services/selectionApi";

type SelectionAction = SelectionActionDraft["action"];

type ActionHandler = (action: SelectionAction, candidate?: SelectionCandidate) => void;

const stepIcons = [Thermometer, Boxes, BarChart3, ShieldCheck, Layers3, Sparkles, CheckCircle2] as const;

const matrixTone: Record<SelectionMatrixGroup["matrix"], string> = {
  B: "gold",
  R: "green",
  D: "red",
  ALL: "gold"
};

function signed(value: number) {
  return `${value > 0 ? "+" : ""}${value.toFixed(2)}%`;
}

function kpiVisual(kpi: SelectionKpi) {
  if (kpi.visual === "bars") {
    return (
      <span className="selection-kpi-visual selection-kpi-visual--bars" aria-hidden="true">
        <i />
        <i />
        <i />
        <i />
        <i />
        <i />
        <i />
      </span>
    );
  }
  if (kpi.visual === "donut") {
    return <span className="selection-kpi-visual selection-kpi-visual--donut" aria-hidden="true" />;
  }
  return <span className={`selection-kpi-visual selection-kpi-visual--line selection-kpi-visual--${kpi.tone}`} aria-hidden="true" />;
}

export function SelectionKpiStrip({ kpis }: { kpis: SelectionKpi[] }) {
  return (
    <section className="holdings-kpi-strip selection-kpi-strip" aria-label="投研问股概览">
      {kpis.map((kpi) => (
        <article className={`kpi-card selection-kpi-card selection-kpi-card--${kpi.tone}`} key={kpi.label}>
          <span>{kpi.label}</span>
          <strong>{kpi.value}</strong>
          <small>{kpi.note}</small>
          {kpiVisual(kpi)}
        </article>
      ))}
    </section>
  );
}

function SelectionConclusionCard({ packet }: { packet: SelectionDashboardPacket }) {
  return (
    <aside className="selection-conclusion" aria-label="本轮筛选结论">
      <strong>本轮筛选结论</strong>
      <dl>
        <div>
          <dt>优先方向</dt>
          <dd>{packet.conclusion.priorityDirection}</dd>
        </div>
        <div>
          <dt>理由</dt>
          <dd>{packet.conclusion.reasons.join(" / ")}</dd>
        </div>
        <div>
          <dt>置信度</dt>
          <dd>{packet.conclusion.confidence}</dd>
        </div>
        <div>
          <dt>今日避开</dt>
          <dd>{packet.conclusion.avoidToday.join(" / ")}</dd>
        </div>
      </dl>
    </aside>
  );
}

export function SevenLayerFilterChain({ packet }: { packet: SelectionDashboardPacket }) {
  return (
    <section className="selection-filter-panel panel-shell" aria-label="七层过滤链">
      <div className="panel-title">
        <span>七层过滤链</span>
        <small>从全市场到研究候选</small>
      </div>
      <div className="filter-chain-layout">
        <div className="filter-chain">
          {packet.filterChain.map((step, index) => {
            const Icon = stepIcons[index] ?? CheckCircle2;
            return <FilterStepCard key={step.step} step={step} icon={Icon} />;
          })}
        </div>
        <SelectionConclusionCard packet={packet} />
      </div>
    </section>
  );
}

function FilterStepCard({ step, icon: Icon }: { step: SelectionFilterStep; icon: typeof CheckCircle2 }) {
  return (
    <article className={`filter-step filter-step--${step.status.toLowerCase()}`}>
      <span className="filter-step__index">{step.step}</span>
      <div className="filter-step__body">
        <strong>{step.title}</strong>
        <small>{step.detail}</small>
        <Icon size={20} aria-hidden="true" />
      </div>
      <div className="filter-step__numbers">
        <span>剩余 {step.remaining.toLocaleString("zh-CN")}</span>
        <em>剔除率 {step.dropRatePct.toFixed(1)}%</em>
      </div>
    </article>
  );
}

export function MarketOpportunitySummary({ groups }: { groups: SelectionOpportunityGroup[] }) {
  return (
    <section className="market-opportunity panel-shell" aria-label="市场机会热度">
      <div className="panel-title">
        <span>市场机会热度</span>
        <small>顺风与避雷同步展示</small>
      </div>
      <div className="opportunity-grid">
        {groups.map((group) => (
          <article className={`opportunity-card opportunity-card--${group.tone}`} key={group.title}>
            <div className="opportunity-card__title">
              {group.tone === "green" ? <ArrowUpRight size={16} aria-hidden="true" /> : <ArrowDownRight size={16} aria-hidden="true" />}
              <strong>{group.title}</strong>
            </div>
            <ol>
              {group.items.map((item) => (
                <li key={`${group.title}-${item.rank}`}>
                  <span>{item.rank}</span>
                  <em>{item.name}</em>
                  <strong>{signed(item.changePct)}</strong>
                </li>
              ))}
            </ol>
          </article>
        ))}
      </div>
    </section>
  );
}

export function MatrixTopCards({ groups }: { groups: SelectionMatrixGroup[] }) {
  return (
    <section className="matrix-section panel-shell" aria-label="三矩阵选股区">
      <div className="panel-title">
        <span>三矩阵选股区</span>
        <small>B/R/D 分流只用于研究角色识别</small>
      </div>
      <div className="matrix-grid">
        {groups.map((group) => (
          <article className={`matrix-card matrix-card--${matrixTone[group.matrix]}`} key={group.title}>
            <div className="matrix-card__title">
              <Gauge size={15} aria-hidden="true" />
              <strong>{group.title}</strong>
              <span>{group.subtitle}</span>
            </div>
            <ul>
              {group.items.map((item) => (
                <li key={`${group.title}-${item.symbol}`}>
                  <code>{item.symbol}</code>
                  <span>{item.name}</span>
                  <em>{item.tags[0]}</em>
                  <em>{item.tags[1]}</em>
                </li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  );
}

export function CandidateSortingWorkbench({
  candidates,
  selected,
  onSelect,
  onAction
}: {
  candidates: SelectionCandidate[];
  selected?: SelectionCandidate;
  onSelect: (candidate: SelectionCandidate) => void;
  onAction: ActionHandler;
}) {
  return (
    <section className="candidate-workbench panel-shell" aria-label="候选矩阵和待选分析台">
      <div className="panel-title">
        <span>候选矩阵 / 待选分析台</span>
        <small>只做研究分拣，不输出交易动作</small>
      </div>
      <div className="candidate-workbench__grid">
        <div className="candidate-table" role="table" aria-label="候选矩阵">
          <div role="row" className="candidate-row candidate-row--head">
            <span role="columnheader">序号</span>
            <span role="columnheader">代码</span>
            <span role="columnheader">股票简称</span>
            <span role="columnheader">人机识别</span>
            <span role="columnheader">投研强度</span>
            <span role="columnheader">事件驱动</span>
            <span role="columnheader">风险画像</span>
            <span role="columnheader">适配度</span>
          </div>
          {candidates.map((candidate, index) => (
            <button
              type="button"
              role="row"
              className={`candidate-row candidate-row--button ${selected?.symbol === candidate.symbol ? "is-selected" : ""}`}
              key={candidate.symbol}
              onClick={() => onSelect(candidate)}
            >
              <span role="cell">{index + 1}</span>
              <span role="cell">{candidate.symbol}</span>
              <span role="cell">{candidate.name}</span>
              <span role="cell" className="cell-hot">{candidate.humanMachineConsensus}</span>
              <span role="cell" className="cell-green">{candidate.researchStrength}</span>
              <span role="cell">{candidate.eventDriver}</span>
              <span role="cell">{candidate.riskProfile}</span>
              <span role="cell">{candidate.allocationFit}</span>
            </button>
          ))}
        </div>

        {selected ? (
          <article className="candidate-detail" aria-label="候选个股研判">
            <header>
              <div>
                <strong>{selected.symbol}</strong>
                <span>{selected.name}</span>
              </div>
              <em>{selected.recommendedRole}</em>
            </header>
            <dl>
              <div>
                <dt>基本面亮点</dt>
                <dd>{selected.keyPoint}</dd>
              </div>
              <div>
                <dt>人机共识</dt>
                <dd>{selected.chain}</dd>
              </div>
              <div>
                <dt>投研逻辑</dt>
                <dd>{selected.financialHealth}</dd>
              </div>
              <div>
                <dt>风险提示</dt>
                <dd>{selected.catalystStatus}</dd>
              </div>
              <div>
                <dt>天机判断</dt>
                <dd>{selected.tianjiDiagnosis}</dd>
              </div>
            </dl>
            <div className="candidate-radar" aria-label="候选评分雷达">
              <span />
              <i>动能</i>
              <i>成长</i>
              <i>估值</i>
              <i>情绪</i>
              <i>风险</i>
            </div>
            <div className="candidate-actions" aria-label="候选安全动作">
              <button type="button" onClick={() => onAction("生成个股研究", selected)}>
                <FileText size={16} aria-hidden="true" />
                生成个股研究
              </button>
              <button type="button" onClick={() => onAction("创建人工研究记录", selected)}>
                <NotebookPen size={16} aria-hidden="true" />
                创建人工研究记录
              </button>
              <button type="button" onClick={() => onAction(selected.recommendedRole === "底仓观察" ? "进入底仓观察仓" : selected.recommendedRole === "轮动观察" ? "进入轮动观察仓" : "进入黑马观察仓", selected)}>
                <Bot size={16} aria-hidden="true" />
                进入观察仓提案
              </button>
              <button type="button" onClick={() => onAction("暂不研究", selected)}>
                <Brain size={16} aria-hidden="true" />
                暂不研究
              </button>
            </div>
          </article>
        ) : (
          <article className="candidate-detail candidate-detail--empty">等待候选输入</article>
        )}
      </div>
    </section>
  );
}
