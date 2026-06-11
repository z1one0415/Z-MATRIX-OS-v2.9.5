import { NavLink } from 'react-router-dom';

interface NavItem {
  id: string;
  label: string;
  route: string;
  icon: string;
}

interface NavSection {
  section_id: string;
  label: string;
  icon: string;
  items: NavItem[];
}

const NAV_STRUCTURE: NavSection[] = [
  {
    section_id: 'section_overview',
    label: 'Overview',
    icon: '\u{1F3E0}',
    items: [
      { id: 'nav_dashboard', label: 'Dashboard', route: '/', icon: '\u{1F4CA}' },
    ],
  },
  {
    section_id: 'section_capabilities',
    label: 'Capabilities',
    icon: '\u{26A1}',
    items: [
      { id: 'nav_capabilities', label: 'Capability OS', route: '/capabilities', icon: '\u{1F5A5}\u{FE0F}' },
      { id: 'nav_factor_library', label: 'Factor Library', route: '/factor-library', icon: '\u{1F9E9}' },
      { id: 'nav_composition_graph', label: 'Composition Graph', route: '/composition-graph', icon: '\u{1F500}' },
    ],
  },
  {
    section_id: 'section_research',
    label: 'Research & Review',
    icon: '\u{1F50D}',
    items: [
      { id: 'nav_research_report', label: 'Research Report', route: '/research-report', icon: '\u{1F4C4}' },
      { id: 'nav_z9_review', label: 'Z9 Review', route: '/z9-review', icon: '\u{2705}' },
    ],
  },
  {
    section_id: 'section_evidence',
    label: 'Evidence & State',
    icon: '\u{1F6E1}\u{FE0F}',
    items: [
      { id: 'nav_evidence_chain', label: 'Evidence Chain', route: '/evidence-chain', icon: '\u{1F517}' },
      { id: 'nav_run_state', label: 'Run State', route: '/run-state', icon: '\u{25B6}\u{FE0F}' },
      { id: 'nav_gate_state', label: 'Gate State', route: '/gate-state', icon: '\u{1F6A6}' },
      { id: 'nav_audit_trail', label: 'Audit Trail', route: '/audit-trail', icon: '\u{1F4CB}' },
    ],
  },
  {
    section_id: 'section_system',
    label: 'System',
    icon: '\u{2699}\u{FE0F}',
    items: [
      { id: 'nav_settings', label: 'Settings / Safety', route: '/settings', icon: '\u{1F512}' },
    ],
  },
];

export function Sidebar() {
  return (
    <aside className="w-64 flex-shrink-0 border-r border-slate-800 bg-slate-900/80 flex flex-col">
      {/* Branding */}
      <div className="flex items-center gap-2 px-4 py-4 border-b border-slate-800">
        <span className="text-xl">{'\u{1F6E1}\u{FE0F}'}</span>
        <div>
          <h1 className="text-sm font-bold text-slate-100">Z-SkillOS</h1>
          <p className="text-xs text-slate-500">Dashboard v0.1.0</p>
        </div>
      </div>

      {/* Nav sections */}
      <nav className="flex-1 overflow-y-auto py-3 px-2 space-y-4">
        {NAV_STRUCTURE.map((section) => (
          <div key={section.section_id}>
            <div className="flex items-center gap-1.5 px-3 mb-1.5">
              <span className="text-xs">{section.icon}</span>
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                {section.label}
              </span>
            </div>
            <ul className="space-y-0.5">
              {section.items.map((item) => (
                <li key={item.id}>
                  <NavLink
                    to={item.route}
                    end={item.route === '/'}
                    className={({ isActive }) =>
                      `flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors ${
                        isActive
                          ? 'bg-slate-800 text-slate-100 font-medium'
                          : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                      }`
                    }
                  >
                    <span className="text-base">{item.icon}</span>
                    <span>{item.label}</span>
                  </NavLink>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div className="border-t border-slate-800 px-4 py-3 space-y-1.5">
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <span>{'\u{1F512}'}</span>
          <span>Read-Only Mode</span>
        </div>
        <div className="flex items-center gap-2 text-xs text-slate-600">
          <span>{'\u{1F4DC}'}</span>
          <span>A1_CONTRACT_FREEZE</span>
        </div>
      </div>
    </aside>
  );
}
