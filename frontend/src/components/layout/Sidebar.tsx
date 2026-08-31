import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Zap,
  Search,
  FileText,
  ShieldAlert,
  Cpu,
  GitBranch,
  BarChart3,
  Sliders,
} from 'lucide-react';

const NAV_ITEMS = [
  { path: '/', label: 'Command Center', icon: LayoutDashboard },
  { path: '/overview', label: 'Overview Metrics', icon: BarChart3 },
  { path: '/attack-lab', label: 'Attack Lab', icon: Zap },
  { path: '/investigator', label: 'Transaction Investigator', icon: Search },
  { path: '/explainability', label: 'Why Flagged?', icon: FileText },
  { path: '/waterfall', label: 'Risk Waterfall', icon: BarChart3 },
  { path: '/gaps', label: 'Defense Gaps', icon: ShieldAlert },
  { path: '/hardening', label: 'Hardening & Models', icon: Cpu },
  { path: '/lineage', label: 'Lineage Graph', icon: GitBranch },
  { path: '/counterfactual', label: 'Counterfactual Explorer', icon: Sliders },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 text-slate-300 flex flex-col justify-between shrink-0 min-h-[calc(100vh-65px)]">
      <div className="py-4">
        <div className="px-4 mb-3 text-[10px] font-mono font-bold tracking-widest text-slate-500 uppercase">
          NAVIGATION COMMANDS
        </div>
        <nav className="space-y-1 px-2">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center space-x-3 px-3 py-2 rounded-md text-xs font-medium transition-colors ${
                    isActive
                      ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`
                }
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </div>

      <div className="p-4 border-t border-slate-800/80 bg-slate-950/40 text-[11px] text-slate-500 space-y-1 font-mono">
        <div>SANDBOX ENGINE: SEED 42</div>
        <div>BENCHMARK ROC-AUC: 0.7754</div>
        <div className="text-emerald-500/80 text-[10px]">ADR-001 THROUGH ADR-017 PASSED</div>
      </div>
    </aside>
  );
};
