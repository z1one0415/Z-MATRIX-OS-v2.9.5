import { Activity, Archive, BookOpenCheck, ChevronRight, Compass, Gauge, Radar, ShieldCheck, Sparkles, TrendingUp } from "lucide-react";
import type { AuthSession } from "../auth";
import { systemVitals } from "../data/cockpit";
import { useHermesAdvisory } from "../hooks/useHermesAdvisory";
import type { HermesPageId } from "../services/hermesAdvisoryApi";
import { HermesAdvisoryPanel } from "./hermes/HermesAdvisoryPanel";

export type RightRailVariant = Exclude<HermesPageId, "dayan">;

type TianjiItem = {
  label: string;
  value: string;
  detail: string;
  icon: typeof Activity;
  tone: "gold" | "green" | "red";
};

const defaultVitals: readonly (readonly [string, string])[] = systemVitals.map(([name, value]) => [name, value] as const);

const holdingsTianjiDesk: TianjiItem[] = [
  { label: "今日总势", value: "偏多", detail: "震荡偏强", icon: Activity, tone: "gold" },
  { label: "持仓风向", value: "顺风", detail: "主线未破", icon: Compass, tone: "green" },
  { label: "观察候变", value: "2 项", detail: "需复核", icon: ShieldCheck, tone: "gold" },
  { label: "催化水位", value: "中位", detail: "旧催化衰减", icon: TrendingUp, tone: "gold" },
  { label: "今日勿为", value: "追高", detail: "防冲动", icon: Radar, tone: "red" }
] as const;

const selectionTianjiDesk: TianjiItem[] = [
  { label: "今日总势", value: "偏强", detail: "震荡偏强", icon: Activity, tone: "gold" },
  { label: "候选风向", value: "顺风", detail: "科技主线", icon: Compass, tone: "green" },
  { label: "观察候变", value: "增加", detail: "128只待研", icon: ShieldCheck, tone: "gold" },
  { label: "催化水位", value: "56%", detail: "中位偏上", icon: TrendingUp, tone: "gold" },
  { label: "今日勿为", value: "追高", detail: "热度防冲", icon: Radar, tone: "red" }
];

const compassTianyanDesk: TianjiItem[] = [
  { label: "参数版本", value: "v2.6.0", detail: "量化总览", icon: Activity, tone: "gold" },
  { label: "成功复盘", value: "87.3%", detail: "纸面通过", icon: ShieldCheck, tone: "green" },
  { label: "参数分歧", value: "6 项", detail: "待裁定", icon: Radar, tone: "gold" },
  { label: "快照状态", value: "已备份", detail: "可恢复", icon: TrendingUp, tone: "green" },
  { label: "退潮项", value: "2 项", detail: "旧催化", icon: Compass, tone: "red" }
];

const historySealDesk: TianjiItem[] = [
  { label: "今日报告", value: "12", detail: "新增", icon: BookOpenCheck, tone: "gold" },
  { label: "实盘案例", value: "8", detail: "只读复盘", icon: Archive, tone: "gold" },
  { label: "记忆沉淀", value: "25", detail: "新增", icon: Sparkles, tone: "green" },
  { label: "规则候选", value: "4", detail: "待处理", icon: ShieldCheck, tone: "gold" },
  { label: "清理记忆", value: "6", detail: "待处理", icon: Radar, tone: "red" }
];

const settingsDesk: TianjiItem[] = [
  { label: "数据源", value: "可测", detail: "Token 不回显", icon: Activity, tone: "green" },
  { label: "安全锁", value: "3 道", detail: "均已锁定", icon: ShieldCheck, tone: "green" },
  { label: "隔离域", value: "独立", detail: "workspace", icon: Compass, tone: "green" },
  { label: "备份", value: "可导出", detail: "审计可查", icon: Archive, tone: "gold" },
  { label: "变更", value: "草案", detail: "人审保存", icon: Radar, tone: "gold" }
];

const profileDesk: TianjiItem[] = [
  { label: "纪律", value: "稳定", detail: "中长为主", icon: ShieldCheck, tone: "green" },
  { label: "偏差", value: "待记", detail: "复盘补录", icon: Radar, tone: "gold" },
  { label: "风险", value: "可控", detail: "保护优先", icon: Compass, tone: "green" },
  { label: "记录", value: "草案", detail: "人审沉淀", icon: BookOpenCheck, tone: "gold" },
  { label: "节奏", value: "稳", detail: "避免冲动", icon: Activity, tone: "green" }
];

const holdingsTianjiSigns = [
  { title: "顺风签", body: "组合趋势未破", verdict: "宜守", tone: "green" },
  { title: "退潮签", body: "高位旧催化衰减", verdict: "慎追", tone: "gold" },
  { title: "复核签", body: "双环路径需确认", verdict: "复核", tone: "gold" }
] as const;

const selectionTianjiSigns = [
  { title: "顺风签", body: "主线强化", verdict: "宜审", tone: "green" },
  { title: "退潮签", body: "旧题材分化", verdict: "慎追", tone: "gold" },
  { title: "复核签", body: "黑马条件增强", verdict: "复核", tone: "gold" }
] as const;

const compassDerivationSeals = [
  { title: "稳定印", body: "数据、样本与经验内核稳定", verdict: "稳定", tone: "green" },
  { title: "校准印", body: "因子、催化与轮动待校准", verdict: "校准", tone: "gold" },
  { title: "禁改印", body: "禁改域禁止越权", verdict: "禁改", tone: "red" }
] as const;

const historyBookmarks = [
  { title: "高胜率", body: "趋势突破类", verdict: "标签", tone: "green" },
  { title: "易失效", body: "高估高位类", verdict: "标签", tone: "gold" },
  { title: "待优化", body: "事件驱动类", verdict: "标签", tone: "gold" }
] as const;

const settingsSigns = [
  { title: "安全签", body: "安全锁完整", verdict: "稳定", tone: "green" },
  { title: "数据签", body: "数据源可测试", verdict: "检查", tone: "gold" },
  { title: "审计签", body: "配置草案留痕", verdict: "人审", tone: "gold" }
] as const;

const profileSigns = [
  { title: "纪律签", body: "节奏稳定", verdict: "稳守", tone: "green" },
  { title: "偏差签", body: "需补反思", verdict: "复盘", tone: "gold" },
  { title: "记录签", body: "人工沉淀", verdict: "草案", tone: "gold" }
] as const;

const holdingsTasks = [
  { time: "09:30", title: "复核紫金矿业回撤路径" },
  { time: "10:00", title: "复核双环传动 thesis" },
  { time: "14:30", title: "补一条人工研究记录" }
];

const selectionTasks = [
  { time: "09:30", title: "更新候选池过滤结果" },
  { time: "10:00", title: "深研 2 只高优先级候选" },
  { time: "14:30", title: "观察黑马候选变化" }
];

const compassTasks = [
  { time: "09:30", title: "复核经验内化草案" },
  { time: "10:15", title: "确认催化周期门校准" },
  { time: "14:00", title: "补齐量化审计证据" }
];

const historyTasks = [
  { time: "09:30", title: "复盘昨日关键案例" },
  { time: "10:00", title: "清理过期系统记忆" },
  { time: "14:30", title: "规则候选验证复盘" }
];

const settingsTasks = [
  { time: "09:30", title: "检查数据源测试结果" },
  { time: "10:15", title: "复核安全锁状态" },
  { time: "14:00", title: "导出配置审计草案" }
];

const profileTasks = [
  { time: "09:30", title: "补充昨日复盘记录" },
  { time: "10:30", title: "查看纪律偏差提示" },
  { time: "14:30", title: "生成个人复盘草案" }
];

const historyVitals = [
  ["报告库", "READY"],
  ["案例库", "PARTIAL"],
  ["记忆库", "PARTIAL"],
  ["规则库", "PARTIAL"],
  ["审计包", "READY"],
  ["研究库", "READY"]
] as const;

const railCopy = {
  holdings: {
    title: "天机引擎",
    subtitle: "持仓路径判断",
    deskTitle: "天机台",
    alertTitle: "天机预警",
    alertTone: "中度预警",
    alertBody: "双环传动路径偏航，板块修复但个股不跟，需 thesis 复核。",
    alertAction: "查看预警详情",
    signsTitle: "天机签",
    actionTitle: "天机卜算",
    desk: holdingsTianjiDesk,
    signs: holdingsTianjiSigns,
    tasks: holdingsTasks,
    divination: "打开天机手册工具箱",
    vitals: defaultVitals
  },
  selection: {
    title: "天机引擎",
    subtitle: "候选路径判断",
    deskTitle: "天机台",
    alertTitle: "天机预警",
    alertTone: "中度预警",
    alertBody: "旧热点高位分歧，候选需先进入研究池复核，不触发交易动作。",
    alertAction: "查看预警详情",
    signsTitle: "天机签",
    actionTitle: "天机卜算",
    desk: selectionTianjiDesk,
    signs: selectionTianjiSigns,
    tasks: selectionTasks,
    divination: "打开投研问股工具箱",
    vitals: defaultVitals
  },
  compass: {
    title: "天机衍算",
    subtitle: "量化参数判断",
    deskTitle: "校准台",
    alertTitle: "参数分歧",
    alertTone: "中风险",
    alertBody: "催化周期门、因子晋级门与 D-Matrix 假预热惩罚待裁定，需保留快照后进入人审。",
    alertAction: "查看分歧详情",
    signsTitle: "天衍印鉴",
    actionTitle: "参数落盘",
    desk: compassTianyanDesk,
    signs: compassDerivationSeals,
    tasks: compassTasks,
    divination: "打开参数校准工具箱",
    vitals: defaultVitals
  },
  history: {
    title: "时空印鉴",
    subtitle: "历史学习判断",
    deskTitle: "时空印",
    alertTitle: "时空预鉴",
    alertTone: "H3 预鉴",
    alertBody: "部分历史模式出现失效迹象，3 条记忆即将过期，2 条规则候选待复核。",
    alertAction: "查看预鉴详情",
    signsTitle: "时空书签",
    actionTitle: "时空工具",
    desk: historySealDesk,
    signs: historyBookmarks,
    tasks: historyTasks,
    divination: "打开时空工具箱",
    vitals: historyVitals
  },
  settings: {
    title: "系统护栏",
    subtitle: "数据源与安全锁",
    deskTitle: "安全台",
    alertTitle: "配置提醒",
    alertTone: "人审保存",
    alertBody: "数据源测试与配置变更只进入草案，不回显密钥明文。",
    alertAction: "查看配置审计",
    signsTitle: "系统签",
    actionTitle: "护栏工具",
    desk: settingsDesk,
    signs: settingsSigns,
    tasks: settingsTasks,
    divination: "打开系统设置工具箱",
    vitals: defaultVitals
  },
  profile: {
    title: "画像镜鉴",
    subtitle: "纪律与复盘",
    deskTitle: "自省台",
    alertTitle: "复盘提醒",
    alertTone: "待补记录",
    alertBody: "近期决策记录可补充人工复盘，先生成草案再由你确认。",
    alertAction: "查看复盘提醒",
    signsTitle: "自省签",
    actionTitle: "画像工具",
    desk: profileDesk,
    signs: profileSigns,
    tasks: profileTasks,
    divination: "打开画像复盘工具箱",
    vitals: defaultVitals
  }
} satisfies Record<RightRailVariant, {
  title: string;
  subtitle: string;
  deskTitle: string;
  alertTitle: string;
  alertTone: string;
  alertBody: string;
  alertAction: string;
  signsTitle: string;
  actionTitle: string;
  desk: readonly TianjiItem[];
  signs: readonly { title: string; body: string; verdict: string; tone: "green" | "gold" | "red" }[];
  tasks: readonly { time: string; title: string }[];
  divination: string;
  vitals: readonly (readonly [string, string])[];
}>;

export function RightRail({
  variant = "holdings",
  session,
  onOpenHermesChat
}: {
  variant?: RightRailVariant;
  session: AuthSession;
  onOpenHermesChat: (pageId: RightRailVariant, question?: string) => void;
}) {
  const copy = railCopy[variant];
  const { data: hermesPacket } = useHermesAdvisory(session, variant);

  return (
    <aside className={`right-rail right-rail--${variant}`} aria-label="右侧天机栏">
      {hermesPacket ? (
        <HermesAdvisoryPanel packet={hermesPacket} onOpenChat={(question) => onOpenHermesChat(variant, question)} />
      ) : null}

      <section className="rail-panel rail-panel--tianji">
        <div className="tianji-orbit" aria-hidden="true" />
        <div className="panel-title panel-title--tianji">
          <span>{copy.title}</span>
          <small>{copy.subtitle}</small>
        </div>

        <div className="tianji-section-title">{copy.deskTitle}</div>
        <div className="tianji-desk" aria-label={copy.deskTitle}>
          {copy.desk.map((item) => (
            <article className={`tianji-desk__item tianji-desk__item--${item.tone}`} key={item.label}>
              <item.icon size={18} aria-hidden="true" />
              <span>{item.label}</span>
              <strong>{item.value}</strong>
              <small>{item.detail}</small>
            </article>
          ))}
        </div>

        <div className="tianji-alert">
          <div>
            <strong>{copy.alertTitle}</strong>
            <em>{copy.alertTone}</em>
          </div>
          <p>{copy.alertBody}</p>
          <button type="button">{copy.alertAction}</button>
        </div>

        <div className="tianji-section-title">{copy.signsTitle}</div>
        <div className="tianji-signs" aria-label={copy.signsTitle}>
          {copy.signs.map((sign) => (
            <article className={`tianji-sign tianji-sign--${sign.tone}`} key={sign.title}>
              <span>{sign.title}</span>
              <small>{sign.body}</small>
              <strong>{sign.verdict}</strong>
            </article>
          ))}
        </div>

        <button className="tianji-divination" type="button">
          <Gauge size={16} aria-hidden="true" />
          {copy.actionTitle}
          <span>{copy.divination}</span>
          <ChevronRight size={15} aria-hidden="true" />
        </button>
      </section>

      <section className="rail-panel">
        <div className="panel-title">
          <span>今日待办</span>
          <small>待处理</small>
        </div>
        <ul className="task-list">
          {copy.tasks.map((task) => (
            <li key={`${variant}-${task.time}-${task.title}`}>
              <time>{task.time}</time>
              <span>{task.title}</span>
              <em>待处理</em>
            </li>
          ))}
        </ul>
      </section>

      <section className="rail-panel">
        <div className="panel-title">
          <span>数据与系统状态</span>
          <small>正常</small>
        </div>
        <div className="vital-grid">
          {copy.vitals.map(([name, value]) => (
            <div key={name}>
              <span>{name}</span>
              <strong>{value}</strong>
            </div>
          ))}
        </div>
      </section>

      <button className="rail-more" type="button">
        查看更多
        <ChevronRight size={15} aria-hidden="true" />
      </button>
    </aside>
  );
}
