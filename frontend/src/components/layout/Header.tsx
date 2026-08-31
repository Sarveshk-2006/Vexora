import React from 'react';
import { Shield, Database, Cpu, Activity, ShieldCheck, Menu } from 'lucide-react';
import { OverviewSummary } from '../../api/types';

interface HeaderProps {
  overviewData: OverviewSummary | null;
  apiConnected: boolean;
  onToggleSidebar?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ overviewData, apiConnected, onToggleSidebar }) => {
  return (
    <header className="bg-white border-b border-[#D9DEE8] text-[#0F172A] px-4 md:px-8 py-3.5 sticky top-0 z-50 flex items-center justify-between gap-4 shadow-sm">
      <div className="flex items-center space-x-3">
        {onToggleSidebar && (
          <button
            onClick={onToggleSidebar}
            className="lg:hidden p-2 rounded-lg bg-[#EEF3FF] text-[#172554] hover:bg-[#172554] hover:text-white transition-colors border border-[#D9DEE8]"
            aria-label="Toggle Navigation"
          >
            <Menu className="w-5 h-5" />
          </button>
        )}
        <div className="p-2 bg-[#EEF3FF] border border-[#D9DEE8] rounded-xl text-[#FF8A00]">
          <Shield className="w-5 h-5" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="font-bold text-lg tracking-wider text-[#0F172A] font-mono">VEXORA</h1>
            <span className="bg-[#EEF3FF] text-[#172554] text-[11px] px-2.5 py-0.5 rounded-full font-mono border border-[#D9DEE8] font-bold">
              v1.0.0
            </span>
          </div>
          <p className="text-xs text-[#475569] font-medium hidden sm:block">
            Synthetic Payment Security Sandbox
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-2 md:space-x-3 text-xs font-mono">
        <div className="hidden lg:flex items-center space-x-1.5 bg-[#F8F7F4] px-3 py-1.5 rounded-lg border border-[#D9DEE8]">
          <ShieldCheck className="w-3.5 h-3.5 text-[#172554]" />
          <span className="text-[#0F172A] font-bold">SYNTHETIC ONLY</span>
        </div>

        <div className="flex items-center space-x-1.5 bg-[#F8F7F4] px-3 py-1.5 rounded-lg border border-[#D9DEE8]">
          <Database className="w-3.5 h-3.5 text-[#172554]" />
          <span className="text-[#475569] hidden sm:inline">SEED:</span>
          <span className="text-[#0F172A] font-bold">
            {overviewData?.simulation_seed ?? 42}
          </span>
        </div>

        <div className="flex items-center space-x-1.5 bg-[#F8F7F4] px-3 py-1.5 rounded-lg border border-[#D9DEE8]">
          <Cpu className="w-3.5 h-3.5 text-[#FF8A00]" />
          <span className="text-[#475569] hidden sm:inline">MODEL:</span>
          <span className="text-[#FF8A00] font-bold">
            {overviewData?.active_model_id ?? 'v0.1.0'}
          </span>
        </div>

        <div className="flex items-center space-x-1.5 bg-[#F8F7F4] px-3 py-1.5 rounded-lg border border-[#D9DEE8]">
          <Activity className="w-3.5 h-3.5 text-[#172554]" />
          <span className="text-[#475569] hidden sm:inline">API:</span>
          {apiConnected ? (
            <span className="text-[#10B981] font-bold flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-[#10B981] animate-pulse"></span>
              ONLINE
            </span>
          ) : (
            <span className="text-[#EF4444] font-bold flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-[#EF4444]"></span>
              OFFLINE
            </span>
          )}
        </div>
      </div>
    </header>
  );
};
