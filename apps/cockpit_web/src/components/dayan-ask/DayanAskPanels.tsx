import {
  Archive,
  Bot,
  BrainCircuit,
  ChevronRight,
  ClipboardCheck,
  Compass,
  FileText,
  FlameKindling,
  Layers3,
  Mic,
  PanelRightOpen,
  Plus,
  Search,
  Send,
  ShieldCheck,
  Sparkles,
  WandSparkles,
  X
} from "lucide-react";
import { useEffect, useRef, useState } from "react";
import type {
  AdvisoryGroup,
  AskFormation,
  AskMessage,
  AskSkill,
  AskSkillCategory,
  DayanAction,
  DayanAskPageData,
  HermesGuidance,
  MethodForgeCandidate,
  MoveReviewItem,
  MyMethod
} from "../../services/dayanAskApi";

type ActionHandler = (action: DayanAction, payload?: Record<string, unknown>) => void;

function safetyLabel(level: string) {
  if (level === "READ_ONLY") return "只读";
  if (level === "DRAFT_ONLY") return "草案";
  if (level === "PROPOSAL_REQUIRED") return "人审";
  return "禁用";
}

function safetyTone(level: string) {
  if (level === "READ_ONLY") return "green";
  if (level === "DRAFT_ONLY") return "gold";
  if (level === "PROPOSAL_REQUIRED") return "amber";
  return "red";
}

export function AskAltarPanel({ data }: { data: DayanAskPageData }) {
  return (
    <section className="dayan-panel dayan-altar" aria-label="问天法坛">
      <PanelTitle icon={Compass} title="问天法坛" subtitle="状态 · 搜索 · 当前上下文" />
      <div className="dayan-altar-mode">
        <span>当前模式</span>
        <strong>{data.altar.modeLabel}</strong>
        <ChevronRight size={16} aria-hidden="true" />
      </div>
      <label className="dayan-search">
        <Search size={16} aria-hidden="true" />
        <input aria-label="搜索法门或研究主题" placeholder="请输入研究主题或关键词" />
      </label>
      <div className="dayan-select-row">
        <span>
          <small>研究范围</small>
          <strong>{data.altar.researchScopeLabel}</strong>
        </span>
        <span>
          <small>记忆上下文</small>
          <strong>{data.altar.memoryContextLabel}</strong>
        </span>
      </div>
    </section>
  );
}

export function AskFormationPanel({
  formations,
  onInsert
}: {
  formations: AskFormation[];
  onInsert: (formation: AskFormation) => void;
}) {
  return (
    <section className="dayan-panel dayan-formation" aria-label="问天法阵">
      <PanelTitle icon={WandSparkles} title="问天法阵" subtitle="成熟阵法组合 · 一键启用草案" />
      <div className="formation-grid">
        {formations.map((formation, index) => (
          <button type="button" key={formation.id} onClick={() => onInsert(formation)}>
            <span className="formation-orb" aria-hidden="true">
              {index + 1}
            </span>
            <strong>{formation.name}</strong>
            <small>{formation.description}</small>
          </button>
        ))}
      </div>
    </section>
  );
}

export function HermesGuidancePanel({ guidance }: { guidance: HermesGuidance }) {
  return (
    <section className="dayan-panel hermes-guidance" aria-label="童子谏言">
      <PanelTitle icon={Bot} title="童子谏言" subtitle="随侍提醒 · 不占中宫" />
      <div className="hermes-avatar-row">
        <div className="hermes-avatar" aria-hidden="true">
          <span />
          <i />
          <b />
        </div>
        <p>{guidance.contextSummary}</p>
      </div>
      <ul>
        {guidance.suggestions.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}

export function AskSkillPanel({
  categories,
  onOpenCategory
}: {
  categories: AskSkillCategory[];
  onOpenCategory: (category: AskSkillCategory) => void;
}) {
  return (
    <section className="dayan-panel ask-skill-panel" aria-label="问天法门">
      <PanelTitle icon={Layers3} title="问天法门" subtitle="底层能力 · 按需调用" />
      <div className="ask-skill-grid">
        {categories.map((category) => (
          <button type="button" key={category.id} onClick={() => onOpenCategory(category)}>
            <strong>{category.name}</strong>
            <small>{category.skillCount} 项 · {safetyLabel(category.safetyLevel)}</small>
          </button>
        ))}
      </div>
      <button className="dayan-link-button" type="button" onClick={() => onOpenCategory(categories[0])}>
        更多法门
        <ChevronRight size={15} aria-hidden="true" />
      </button>
    </section>
  );
}

export function AskDuelChat({
  topic,
  messages,
  fragments,
  inputValue,
  voiceAvailable,
  draftMessage,
  onInputChange,
  onSend,
  onClear,
  onVoiceClick
}: {
  topic: string;
  messages: AskMessage[];
  fragments: string[];
  inputValue: string;
  voiceAvailable: boolean;
  draftMessage?: string;
  onInputChange: (value: string) => void;
  onSend: () => void;
  onClear: () => void;
  onVoiceClick: () => void;
}) {
  const [isExpanded, setIsExpanded] = useState(false);
  const panelRef = useRef<HTMLElement | null>(null);
  const messageListRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!isExpanded) return;

    function handlePointerDown(event: PointerEvent) {
      if (panelRef.current?.contains(event.target as Node)) return;
      setIsExpanded(false);
    }

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setIsExpanded(false);
      }
    }

    document.addEventListener("pointerdown", handlePointerDown, true);
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("pointerdown", handlePointerDown, true);
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isExpanded]);

  useEffect(() => {
    const list = messageListRef.current;
    if (!list) return;

    const frame = window.requestAnimationFrame(() => {
      list.scrollTop = list.scrollHeight;
    });

    return () => window.cancelAnimationFrame(frame);
  }, [messages.length, draftMessage, isExpanded]);

  const fragmentSummary = fragments.length > 0 ? fragments.join(" / ") : "";
  const topicLabel = topic.startsWith("研究主题") ? topic : `研究主题：${topic}`;

  return (
    <section
      ref={panelRef}
      className={`dayan-panel ask-duel${isExpanded ? " ask-duel--expanded" : ""}`}
      aria-label="问天对弈"
      aria-expanded={isExpanded}
    >
      <div className="ask-duel-head">
        <div className="ask-duel-title">
          <button
            type="button"
            className="ask-immersive-toggle"
            aria-label={isExpanded ? "退出沉浸对话模式" : "放大窗口进入沉浸对话模式"}
            title={isExpanded ? "退出沉浸对话模式" : "点击放大窗口进入沉浸对话模式"}
            onClick={() => setIsExpanded((current) => !current)}
          >
            <Sparkles size={18} aria-hidden="true" />
            <span className="ask-immersive-tooltip" role="tooltip">
              {isExpanded ? "退出沉浸对话" : "点击进入沉浸对话"}
            </span>
          </button>
          <div>
            <strong>问天对弈</strong>
            <small>{topicLabel}</small>
          </div>
        </div>
        <div className="ask-duel-head-actions">
          {fragments.length > 0 ? (
            <span
              className="selected-fragments-compact"
              aria-label={`已选法门：${fragmentSummary}`}
              title={fragmentSummary}
            >
              已选 {fragments.length}
            </span>
          ) : null}
          <button type="button" onClick={onClear}>清空对话</button>
        </div>
      </div>
      <div className="ask-message-list" ref={messageListRef}>
        {messages.map((message) => (
          <article className={`ask-message ask-message--${message.role.toLowerCase()}`} key={message.id}>
            <strong>{message.label}</strong>
            <p>{message.content}</p>
            <small>{message.createdAt}</small>
          </article>
        ))}
        {draftMessage ? (
          <article className="ask-message ask-message--system">
            <p>{draftMessage}</p>
          </article>
        ) : null}
      </div>
      <div className="ask-input-row">
        <button
          type="button"
          className="ask-attach"
          aria-label="添加资料或附件"
          title="添加资料或附件"
        >
          <Plus size={19} aria-hidden="true" />
        </button>
        <textarea
          aria-label="问天输入"
          value={inputValue}
          onChange={(event) => onInputChange(event.currentTarget.value)}
          placeholder="输入问题，或 / 调用法门"
          rows={1}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              onSend();
            }
          }}
        />
        <button
          type="button"
          className="ask-voice"
          aria-label={voiceAvailable ? "语音输入" : "语音输入不可用"}
          title={voiceAvailable ? "语音输入" : "当前浏览器未开放语音输入"}
          onClick={onVoiceClick}
        >
          <Mic size={18} aria-hidden="true" />
        </button>
        <button type="button" className="ask-send" aria-label="发送问天问题" onClick={onSend}>
          <Send size={20} aria-hidden="true" />
        </button>
      </div>
    </section>
  );
}

export function HeavenlyAdvisoryPanel({ groups }: { groups: AdvisoryGroup[] }) {
  return (
    <section className="dayan-panel heavenly-advisory" aria-label="天官问策">
      <PanelTitle icon={BrainCircuit} title="天官问策" subtitle="决策支持 · 多维推演" />
      <div className="advisory-list">
        {groups.map((group) => (
          <button type="button" key={group.id}>
            <span>{group.title}</span>
            <small>{group.description}</small>
            <ChevronRight size={16} aria-hidden="true" />
          </button>
        ))}
      </div>
    </section>
  );
}

export function MethodForgePanel({
  candidates,
  onAction
}: {
  candidates: MethodForgeCandidate[];
  onAction: ActionHandler;
}) {
  const candidate = candidates[0];
  return (
    <section className="dayan-panel method-forge" aria-label="熔炼法门">
      <PanelTitle icon={FlameKindling} title="熔炼法门" subtitle="组合能力 · 熔炼成个人法门" />
      {candidate ? (
        <div className="forge-card">
          <small>当前阵法组合</small>
          <strong>{candidate.sourceCombination.join(" + ")}</strong>
          <small>熔炼建议名称</small>
          <span>{candidate.suggestedName}</span>
          <div className="forge-actions">
            <button type="button" onClick={() => onAction("创建法门草案", { candidateId: candidate.id })}>重命名</button>
            <button type="button" onClick={() => onAction("试运行草案", { candidateId: candidate.id })}>试运行</button>
            <button type="button" onClick={() => onAction("加入我的法门草案", { candidateId: candidate.id })}>加入我的法门</button>
            <button type="button" onClick={() => onAction("忽略熔炼候选", { candidateId: candidate.id })}>忽略</button>
          </div>
        </div>
      ) : (
        <p>暂无熔炼候选。</p>
      )}
    </section>
  );
}

export function MoveReviewPanel({ items }: { items: MoveReviewItem[] }) {
  return (
    <section className="dayan-panel move-review" aria-label="落子复盘">
      <PanelTitle icon={Archive} title="落子复盘" subtitle="记录每一次推演" />
      <div className="move-review-table" role="table" aria-label="落子复盘记录">
        <div role="row" className="move-review-row move-review-row--head">
          <span role="columnheader">日期</span>
          <span role="columnheader">研究主题</span>
          <span role="columnheader">阵法组合</span>
          <span role="columnheader">结论要点</span>
          <span role="columnheader">记忆状态</span>
        </div>
        {items.map((item) => (
          <div role="row" className="move-review-row" key={item.id}>
            <span role="cell">{item.date}</span>
            <span role="cell">{item.researchTopic}</span>
            <span role="cell">{item.methodCombination}</span>
            <span role="cell">{item.conclusion}</span>
            <span role="cell">{item.memoryStatus}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

export function MyMethodsPanel({ methods }: { methods: MyMethod[] }) {
  return (
    <section className="dayan-panel my-methods" aria-label="我的法门">
      <PanelTitle icon={ClipboardCheck} title="我的法门" subtitle="个人法门库 · 快速调用" />
      <div className="my-method-list" role="table" aria-label="我的法门列表">
        <div role="row" className="my-method-row my-method-row--head">
          <span role="columnheader">法门名称</span>
          <span role="columnheader">通用场景</span>
          <span role="columnheader">更新时间</span>
        </div>
        {methods.map((method) => (
          <button type="button" role="row" className="my-method-row" key={method.id}>
            <span role="cell">{method.name}</span>
            <span role="cell">{method.scenario}</span>
            <span role="cell">{method.lastUsedAt}</span>
          </button>
        ))}
      </div>
      <button className="dayan-link-button" type="button">
        查看全部
        <ChevronRight size={15} aria-hidden="true" />
      </button>
    </section>
  );
}

export function AskSkillDrawer({
  category,
  onClose,
  onInsert
}: {
  category: AskSkillCategory | null;
  onClose: () => void;
  onInsert: (skill: AskSkill) => void;
}) {
  if (!category) return null;

  return (
    <div className="ask-drawer-backdrop" role="presentation" onClick={onClose}>
      <aside
        className="ask-skill-drawer"
        aria-label={`${category.name}法门抽屉`}
        onClick={(event) => event.stopPropagation()}
      >
        <div className="ask-drawer-head">
          <div>
            <strong>{category.name}</strong>
            <small>{category.description}</small>
          </div>
          <button type="button" aria-label="关闭法门抽屉" onClick={onClose}>
            <X size={18} aria-hidden="true" />
          </button>
        </div>
        <label className="dayan-search">
          <Search size={16} aria-hidden="true" />
          <input aria-label="搜索具体法门" placeholder="搜索具体法门" />
        </label>
        <div className="drawer-filter-row" aria-label="法门筛选">
          <span>全部</span>
          <span>最近使用</span>
          <span>收藏</span>
          <span>只读</span>
          <span>草案</span>
          <span>人审</span>
        </div>
        <div className="drawer-skill-grid">
          {category.skills.map((skill) => (
            <button type="button" key={skill.id} onClick={() => onInsert(skill)}>
              <strong>{skill.userVisibleName}</strong>
              <small>{skill.description}</small>
              <em className={`safety-badge safety-badge--${safetyTone(skill.safetyLevel)}`}>{safetyLabel(skill.safetyLevel)}</em>
            </button>
          ))}
        </div>
        <div className="drawer-bottom-actions">
          <button type="button" onClick={onClose}>插入所选</button>
          <button type="button" onClick={onClose}>预览提示词</button>
          <button type="button" onClick={onClose}>加入我的法门</button>
          <button type="button" onClick={onClose}>关闭</button>
        </div>
      </aside>
    </div>
  );
}

function PanelTitle({
  icon: Icon,
  title,
  subtitle
}: {
  icon: typeof FileText;
  title: string;
  subtitle: string;
}) {
  return (
    <div className="dayan-panel-title">
      <Icon size={18} aria-hidden="true" />
      <strong>{title}</strong>
      <small>{subtitle}</small>
    </div>
  );
}

export function DayanSystemLine({ data }: { data: DayanAskPageData }) {
  return (
    <section className="dayan-system-line" aria-label="大衍天问系统状态">
      <span>
        <ShieldCheck size={15} aria-hidden="true" />
        可召法门 {data.systemStatus.registeredMethodCount}
      </span>
      <span>领域 {data.systemStatus.concreteDomainCount}</span>
      <span>随侍 {data.agentBridge.default_agent}</span>
      <span>问答能力 {data.agentBridge.allowed_intents.length}</span>
      <span>最高边界 草案</span>
      <span>工作流 仅纸面</span>
      <span>人审锁 已开启</span>
      <span>正式库改写 已阻断</span>
      <span>命令通道 已阻断</span>
    </section>
  );
}
