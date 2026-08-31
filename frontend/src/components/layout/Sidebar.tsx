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
  TrendingDown,
  X,
} from 'lucide-react';

interface NavSection {
  title: string;
  items: { path: string; label: string; icon: React.FC<{ className?: string }> }[];
}

const NAV_SECTIONS: NavSection[] = [
  {
    title: 'COMMAND',
    items: [
      { path: '/', label: 'Command Center', icon: LayoutDashboard },
      { path: '/overview', label: 'Security Overview', icon: BarChart3 },
    ],
  },
  {
    title: 'INVESTIGATE',
    items: [
      { path: '/attack-lab', label: 'Attack Lab', icon: Zap },
      { path: '/investigator', label: 'Transaction Investigator', icon: Search },
      { path: '/explainability', label: 'Why Flagged?', icon: FileText },
      { path: '/waterfall', label: 'Risk Breakdown', icon: TrendingDown },
    ],
  },
  {
    title: 'DEFEND',
    items: [
      { path: '/gaps', label: 'Defense Gaps', icon: ShieldAlert },
      { path: '/hardening', label: 'Hardening & Models', icon: Cpu },
    ],
  },
  {
    title: 'TRACE',
    items: [
      { path: '/lineage', label: 'Attack Lineage', icon: GitBranch },
      { path: '/counterfactual', label: 'What-if Analysis', icon: Sliders },
    ],
  },
];

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen = false, onClose }) => {
  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs z-40 lg:hidden"
        />
      )}

      <aside
        className={`fixed lg:static top-0 left-0 bottom-0 z-50 w-64 bg-white border-r border-[#D9DEE8] text-[#0F172A] flex flex-col justify-between shrink-0 min-h-screen lg:min-h-[calc(100vh-65px)] shadow-sm transition-transform duration-200 ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="py-5 space-y-4 overflow-y-auto">
          <div className="px-5 flex items-center justify-between lg:hidden pb-3 border-b border-[#D9DEE8]">
            <span className="font-bold font-mono text-[#0F172A]">NAVIGATION</span>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg bg-[#F8F7F4] text-[#475569] hover:text-[#0F172A]"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {NAV_SECTIONS.map((section) => (
            <div key={section.title} className="px-4">
              <div className="px-3 mb-2 text-[10px] font-mono font-bold tracking-wider text-[#64748B] uppercase">
                {section.title}
              </div>
              <nav className="space-y-1">
                {section.items.map((item) => {
                  const Icon = item.icon;
                  return (
                    <NavLink
                      key={item.path}
                      to={item.path}
                      onClick={onClose}
                      className={({ isActive }) =>
                        `flex items-center space-x-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition-all duration-150 ${
                          isActive
                            ? 'bg-[#EEF3FF] text-[#172554] border border-[#172554]/30 font-bold shadow-xs'
                            : 'text-[#475569] hover:text-[#0F172A] hover:bg-[#F8F7F4]'
                        }`
                      }
                    >
                      <Icon className="w-4 h-4 shrink-0 text-[#172554]" />
                      <span>{item.label}</span>
                    </NavLink>
                  );
                })}
              </nav>
            </div>
          ))}
        </div>

        <div className="p-4 border-t border-[#D9DEE8] bg-[#F8F7F4] text-[11px] text-[#64748B] font-mono space-y-1">
          <div className="flex items-center justify-between text-[#0F172A] font-bold">
            <span>SANDBOX ENVIRONMENT</span>
            <span className="text-[#10B981]">ONLINE</span>
          </div>
          <div>SEED 42 · DETERMINISTIC DEPLOYMENT</div>
        </div>
      </aside>
    </>
  );
};
