import { CheckCircle2, CircleAlert, FileSearch, GitBranch, ShieldAlert, ShieldCheck } from "lucide-react";
import { useState } from "react";
import type {
  CalibrationParameterFamily,
  ControlCompassActionDraft,
  ControlCompassPageData,
  GovernanceDomainStatus,
  GovernanceStatus,
  OptimizationSnapshotStatus
} from "../../services/controlCompassApi";

type CompassAction = ControlCompassActionDraft["action"];

type ActionHandler = (action: CompassAction, payload?: Record<string, unknown>) => void;

const statusLabel: Record<GovernanceStatus, string> = {
  STABLE: "稳定",
  NEED_CALIBRATION: "待校准",
  UNDER_REVIEW: "复核中",
  BLOCKED: "阻断中",
  PENDING_APPROVAL: "待审批"
};

const statusTone: Record<GovernanceStatus, "green" | "gold" | "red"> = {
  STABLE: "green",
  NEED_CALIBRATION: "gold",
  UNDER_REVIEW: "gold",
  BLOCKED: "red",
  PENDING_APPROVAL: "gold"
};

const riskLabel: Record<GovernanceDomainStatus["riskLevel"], string> = {
  LOW: "低风险",
  MID: "中风险",
  HIGH: "高风险",
  CRITICAL: "极高风险"
};

const driftLabel: Record<CalibrationParameterFamily["driftStatus"], string> = {
  STABLE: "稳定",
  DRIFTING: "漂移",
  WEAKENED: "弱化",
  LOW_SAMPLE: "低样本",
  BLOCKED: "阻断"
};

const snapshotLabel: Record<OptimizationSnapshotStatus, string> = {
  READY: "已备份",
  REQUIRED: "需备份",
  MISSING: "缺失"
};

const rulingLabel: Record<ControlCompassPageData["ruling"]["rulingStatus"]["status"], string> = {
  PENDING: "待裁定",
  APPROVED: "已通过",
  REJECTED: "已拒绝",
  DEFERRED: "已延后"
};

const domainShortLabel: Record<GovernanceDomainStatus["domainId"], string> = {
  DATA_QUALITY: "数据",
  SAMPLE_POOL: "样本",
  FACTOR_SIGNAL: "因子",
  CATALYST_CYCLE: "催化",
  B_MATRIX: "B",
  R_MATRIX: "R",
  D_MATRIX: "D",
  EXPERIENCE_INTERNALIZATION: "经验"
};

function percent(value: number) {
  return `${value.toFixed(value % 1 === 0 ? 0 : 1)}%`;
}

export function CompassKpiStrip({ data }: { data: ControlCompassPageData }) {
  const snapshotTone = data.kpi.optimizationSnapshotStatus === "READY" ? "green" : data.kpi.optimizationSnapshotStatus === "MISSING" ? "red" : "gold";
  const cards = [
    { label: "系统健康", value: `${data.kpi.healthScore}`, note: `${data.kpi.healthyDomainCount}/${data.kpi.governanceDomainCount} 域稳定`, tone: "green" },
    { label: "成功率复盘", value: percent(data.kpi.latestPaperHitRatePct), note: data.optimizationSummary.latestCycleId, tone: "gold" },
    { label: "自优化建议", value: `${data.kpi.pendingChangeCount}`, note: data.optimizationSummary.suggestedVersion, tone: "gold" },
    { label: "参数分歧", value: `${data.kpi.pendingAdjudicationCount} 项`, note: `${data.kpi.weakenedSignalCount} 个弱化信号`, tone: "red" },
    { label: "快照保护", value: snapshotLabel[data.kpi.optimizationSnapshotStatus], note: data.optimizationSummary.snapshotId, tone: snapshotTone }
  ] as const;

  return (
    <section className="holdings-kpi-strip compass-kpi-strip" aria-label="天机罗盘指标">
      {cards.map((card) => (
        <article className={`kpi-card compass-kpi-card compass-kpi-card--${card.tone}`} key={card.label}>
          <span>{card.label}</span>
          <strong>{card.value}</strong>
          <small>{card.note}</small>
        </article>
      ))}
    </section>
  );
}

export function SevenLayerCompassMap({
  domains,
  selectedDomainId,
  onSelect,
  family,
  onAction
}: {
  domains: GovernanceDomainStatus[];
  selectedDomainId: GovernanceDomainStatus["domainId"];
  onSelect: (domain: GovernanceDomainStatus) => void;
  family?: CalibrationParameterFamily;
  onAction: ActionHandler;
}) {
  const [linkedDomainId, setLinkedDomainId] = useState<GovernanceDomainStatus["domainId"] | null>(null);
  const selectedDomain = domains.find((domain) => domain.domainId === selectedDomainId) ?? domains[0];
  const selectedFamily = family ?? {
    familyId: selectedDomain.domainId,
    domainId: selectedDomain.domainId,
    label: selectedDomain.displayName,
    scope: "等待参数族映射",
    backendMapping: "Config Registry",
    currentVersion: "待导入",
    systemOptimizedVersion: "待导入",
    currentSignal: "等待数据",
    optimizationAdvice: "等待系统自优化结果",
    paperReview: "等待纸面复盘",
    driftStatus: "LOW_SAMPLE",
    editableMode: "DRAFT_ONLY",
    snapshotRequired: true,
    restoreAvailable: false
  } satisfies CalibrationParameterFamily;

  return (
    <section className="compass-map-panel panel-shell" aria-label="主干量化参数罗盘">
      <div className="panel-title">
        <span>主干量化参数罗盘</span>
        <small>八域量化参数校准</small>
      </div>
      <div className="compass-map-layout">
        <div className="governance-status-list" aria-label="量化参数域状态列">
          {domains.map((domain) => (
            <button
              type="button"
              className={`governance-domain-item governance-domain-item--${statusTone[domain.status]} ${domain.domainId === selectedDomainId ? "is-selected" : ""} ${domain.domainId === linkedDomainId ? "is-linked" : ""}`}
              key={domain.domainId}
              data-domain-list-index={domain.index}
              onBlur={() => setLinkedDomainId(null)}
              onClick={() => onSelect(domain)}
              onFocus={() => setLinkedDomainId(domain.domainId)}
              onMouseEnter={() => setLinkedDomainId(domain.domainId)}
              onMouseLeave={() => setLinkedDomainId(null)}
            >
              <span>{String(domain.index).padStart(2, "0")}</span>
              <strong>{domain.displayName}</strong>
              <em>{statusLabel[domain.status]}</em>
            </button>
          ))}
        </div>
        <div className="eastern-compass-plate" role="img" aria-label="八域量化参数校准罗盘">
          <div className="compass-ring-metrics" aria-label="罗盘关键指标">
            <span>待裁 {selectedDomain.pendingChanges}</span>
            <span>环层 {selectedDomain.ringIndex}</span>
          </div>
          <div className="compass-dial">
            {domains.map((domain) => (
              <button
                type="button"
                key={domain.domainId}
                aria-label={`${domain.displayName} ${statusLabel[domain.status]}`}
                className={`compass-ring compass-ring--${domain.ringIndex} compass-ring--${statusTone[domain.status]} ${domain.domainId === selectedDomainId ? "is-selected" : ""} ${domain.domainId === linkedDomainId ? "is-linked" : ""}`}
                data-domain-ring-index={domain.ringIndex}
                onBlur={() => setLinkedDomainId(null)}
                onClick={() => onSelect(domain)}
                onFocus={() => setLinkedDomainId(domain.domainId)}
                onMouseEnter={() => setLinkedDomainId(domain.domainId)}
                onMouseLeave={() => setLinkedDomainId(null)}
              />
            ))}
            <svg className="compass-spiral-guide" viewBox="0 0 100 100" aria-hidden="true" focusable="false">
              <path d="M 50 0 C 62 2 75 10 80.4 19.6 C 88 32 88 42 86 50 C 83 63 78 68 71.6 71.6 C 63 78 56 78 50 75 C 41 73 37 68 36.2 63.8 C 34 58 34 53 36 50 C 39 47 45 47 50 50" />
            </svg>
            <span className="compass-core">经验</span>
            <div className="compass-domain-markers" aria-hidden="true">
              {domains.filter((domain) => domain.domainId !== "EXPERIENCE_INTERNALIZATION").map((domain) => (
                <span
                  className={`compass-domain-marker compass-domain-marker--${domain.index} compass-domain-marker--${statusTone[domain.status]}`}
                  key={`${domain.domainId}-marker`}
                >
                  {domainShortLabel[domain.domainId]}
                </span>
              ))}
            </div>
          </div>
        </div>
        <section className="compass-domain-detail" aria-label="参数族校准详情">
          <div className="panel-title">
            <span>参数族校准详情</span>
            <small>当前参数域：{String(selectedDomain.index).padStart(2, "0")} {selectedDomain.displayName}</small>
          </div>
          <aside className="compass-domain-summary" role="complementary" aria-label="当前参数域摘要">
            <div className="compass-domain-summary__hero">
              <span>{String(selectedDomain.index).padStart(2, "0")} / 08</span>
              <strong>{selectedDomain.displayName}</strong>
              <em>{statusLabel[selectedDomain.status]}</em>
            </div>
            <dl>
              <div>
                <dt>风险</dt>
                <dd>{riskLabel[selectedDomain.riskLevel]}</dd>
              </div>
              <div>
                <dt>待审</dt>
                <dd>{selectedDomain.pendingChanges} 项</dd>
              </div>
              <div>
                <dt>环层</dt>
                <dd>{selectedDomain.ringIndex}</dd>
              </div>
              <div>
                <dt>最近复核</dt>
                <dd>{selectedDomain.lastReviewedAt}</dd>
              </div>
            </dl>
          </aside>
          <dl className="derivation-detail-list compass-detail-list">
            <div>
              <dt>参数族</dt>
              <dd>{selectedFamily.label}</dd>
            </div>
            <div>
              <dt>当前版本</dt>
              <dd>{selectedFamily.currentVersion}</dd>
            </div>
            <div>
              <dt>系统建议</dt>
              <dd>{selectedFamily.optimizationAdvice}</dd>
            </div>
            <div>
              <dt>成功复盘</dt>
              <dd>{selectedFamily.paperReview}</dd>
            </div>
            <div>
              <dt>关联链路</dt>
              <dd>{selectedFamily.backendMapping}</dd>
            </div>
            <div>
              <dt>漂移状态</dt>
              <dd>{driftLabel[selectedFamily.driftStatus]} · {selectedFamily.restoreAvailable ? "可恢复自优化结果" : "待生成恢复点"}</dd>
            </div>
          </dl>
          <button
            type="button"
            onClick={() => onAction("查看参数族详情", { domainId: selectedDomain.domainId, familyId: selectedFamily.familyId })}
          >
            查看参数族详情
          </button>
        </section>
      </div>
    </section>
  );
}

export function DerivationDetailCard({
  family,
  selectedDomain,
  onAction
}: {
  family?: CalibrationParameterFamily;
  selectedDomain: GovernanceDomainStatus;
  onAction: ActionHandler;
}) {
  const selectedFamily = family ?? {
    familyId: selectedDomain.domainId,
    domainId: selectedDomain.domainId,
    label: selectedDomain.displayName,
    scope: "等待参数族映射",
    backendMapping: "Config Registry",
    currentVersion: "待导入",
    systemOptimizedVersion: "待导入",
    currentSignal: "等待数据",
    optimizationAdvice: "等待系统自优化结果",
    paperReview: "等待纸面复盘",
    driftStatus: "LOW_SAMPLE",
    editableMode: "DRAFT_ONLY",
    snapshotRequired: true,
    restoreAvailable: false
  } satisfies CalibrationParameterFamily;

  return (
    <section className="derivation-detail-card panel-shell" aria-label="参数族校准详情">
      <div className="panel-title">
        <span>参数族校准详情</span>
        <small>当前参数域：{String(selectedDomain.index).padStart(2, "0")} {selectedDomain.displayName}</small>
      </div>
      <dl className="derivation-detail-list">
        <div>
          <dt>参数族</dt>
          <dd>{selectedFamily.label}</dd>
        </div>
        <div>
          <dt>当前版本</dt>
          <dd>{selectedFamily.currentVersion}</dd>
        </div>
        <div>
          <dt>系统建议</dt>
          <dd>{selectedFamily.optimizationAdvice}</dd>
        </div>
        <div>
          <dt>成功复盘</dt>
          <dd>{selectedFamily.paperReview}</dd>
        </div>
        <div>
          <dt>关联链路</dt>
          <dd>{selectedFamily.backendMapping}</dd>
        </div>
        <div>
          <dt>漂移状态</dt>
          <dd>{driftLabel[selectedFamily.driftStatus]} · {selectedFamily.restoreAvailable ? "可恢复自优化结果" : "待生成恢复点"}</dd>
        </div>
      </dl>
      <button type="button" onClick={() => onAction("查看参数族详情", { domainId: selectedDomain.domainId, familyId: selectedFamily.familyId })}>
        查看参数族详情
      </button>
    </section>
  );
}

export function DerivationSandboxPanel({ data, onAction }: { data: ControlCompassPageData; onAction: ActionHandler }) {
  const items = [
    { title: "自优化建议", body: data.optimizationSummary.headline, icon: FileSearch },
    { title: "影响范围", body: `${data.sandbox.draft.affectedParameterCount} 项参数 · ${data.sandbox.impact.strategyImpact}`, icon: GitBranch },
    { title: "联动压测", body: `${data.sandbox.paperValidation.method} · 通过率 ${percent(data.sandbox.paperValidation.passRatePct)}`, icon: CheckCircle2 },
    { title: "风险分歧", body: `${data.calibrationDisputes.length} 项待裁定 · ${data.sandbox.risk.potentialImpact}`, icon: ShieldAlert },
    { title: "人审草案", body: `需 ${data.sandbox.humanReview.requiredReviewerCount} 位复核 · 快照 ${data.optimizationSummary.snapshotId}`, icon: ShieldCheck }
  ];

  return (
    <section className="derivation-sandbox-panel panel-shell" aria-label="天机推衍区">
      <div className="panel-title">
        <span>天机推衍区</span>
        <small>自优化建议与纸面沙盘</small>
      </div>
      <div className="derivation-flow">
        {items.map((item) => (
          <article key={item.title}>
            <item.icon size={16} aria-hidden="true" />
            <strong>{item.title}</strong>
            <p>{item.body}</p>
          </article>
        ))}
      </div>
      <button type="button" onClick={() => onAction("创建校准草案", { draftId: data.sandbox.draft.draftId, snapshotId: data.optimizationSummary.snapshotId })}>
        创建校准草案
      </button>
    </section>
  );
}

export function DerivationRulingCard({ data, onAction }: { data: ControlCompassPageData; onAction: ActionHandler }) {
  return (
    <section className="derivation-ruling-card panel-shell" aria-label="天机衍变裁定">
      <div className="panel-title">
        <span>天机衍变裁定</span>
        <small>审计链与裁定状态</small>
      </div>
      <ul>
        <li>
          <CircleAlert size={16} aria-hidden="true" />
          <span>快照保护</span>
          <strong>{snapshotLabel[data.optimizationSummary.snapshotStatus]} · {data.optimizationSummary.snapshotId}</strong>
        </li>
        <li>
          <GitBranch size={16} aria-hidden="true" />
          <span>证据链</span>
          <strong>{data.ruling.evidenceChain.linkedEvidenceCount} 条 · {percent(data.ruling.evidenceChain.completenessPct)}</strong>
        </li>
        <li>
          <ShieldCheck size={16} aria-hidden="true" />
          <span>专家复核</span>
          <strong>{data.ruling.expertReview.passed} / {data.ruling.expertReview.required}</strong>
        </li>
        <li>
          <CheckCircle2 size={16} aria-hidden="true" />
          <span>审计结果</span>
          <strong>{data.ruling.auditResult.status === "PENDING" ? "待审计" : "已同步"}</strong>
        </li>
        <li>
          <CircleAlert size={16} aria-hidden="true" />
          <span>裁定状态</span>
          <strong>{rulingLabel[data.ruling.rulingStatus.status]} · {data.ruling.rulingStatus.changeWindowOpen ? "窗口开放" : "窗口关闭"}</strong>
        </li>
      </ul>
      <div className="ruling-actions">
        <button type="button" onClick={() => onAction("恢复系统自优化结果", { draftId: data.ruling.draftId, snapshotId: data.optimizationSummary.snapshotId })}>
          恢复系统自优化结果
        </button>
        <button type="button" onClick={() => onAction("查看审计链详情", { draftId: data.ruling.draftId })}>
          查看审计链详情
        </button>
      </div>
    </section>
  );
}
