import { NavLink } from "react-router-dom";
import { Activity, Shield } from "lucide-react";
import type { AuthSession } from "../auth";
import { navItems, profileRoute } from "../data/cockpit";
import { useCockpitPreferences } from "../settings/CockpitPreferences";

type SideNavProps = {
  session: AuthSession;
};

export function SideNav({ session }: SideNavProps) {
  const { copy } = useCockpitPreferences();

  return (
    <aside className="side-nav" aria-label="全局导航">
      <NavLink className="brand" to="/holdings" aria-label="Z-MATRIX 首页">
        <span className="brand-mark">Z</span>
        <span>
          <strong>Z-MATRIX</strong>
          <small>Research Cockpit</small>
        </span>
      </NavLink>

      <NavLink className="operator-card" to={profileRoute.path}>
        <span className="operator-avatar" aria-hidden="true">
          Z
        </span>
        <span className="operator-copy">
          <strong>{session.displayName}</strong>
          <small>稳健成长型</small>
          <em>中长为主 · 纪律优先 · 风险可控</em>
        </span>
      </NavLink>

      <nav className="nav-list">
        {navItems.map((item) => (
          <NavLink
            key={item.id}
            to={item.path}
            className={({ isActive }) => `nav-item ${isActive ? "is-active" : ""}`}
          >
            <item.icon aria-hidden="true" size={18} strokeWidth={1.9} />
            <span>
              <strong>{copy(`nav.${item.id}.label`, item.label)}</strong>
              <small>{copy(`nav.${item.id}.subtitle`, item.subtitle)}</small>
            </span>
          </NavLink>
        ))}
      </nav>

      <div className="nav-footer" aria-label="系统保护状态">
        <span>
          <Shield aria-hidden="true" size={15} />
          Z-MATRIX 研究终端
        </span>
        <span>
          <Activity aria-hidden="true" size={15} />
          v0.0.0 Batch 1
        </span>
      </div>
    </aside>
  );
}
