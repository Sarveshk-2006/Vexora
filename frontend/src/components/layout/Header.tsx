import React from 'react';
import { Shield, Database, Cpu, Activity, Info } from 'lucide-react';
import { OverviewSummary } from '../../api/types';

interface HeaderProps {
  overviewData: OverviewSummary | null;
  apiConnected: boolean;
}

export const Header: React.FC<HeaderProps> = ({ overviewData, apiConnected }) => {
  return (
    <header className="bg-slate-900 border-b border-slate-800 text-slate-100 px-6 py-3 sticky top-0 z-50 flex flex-wrap items-center justify-between gap-4 shadow-md">
      <div className="flex items-center space-x-3">
        <div className="p-2 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
          <Shield className="w-6 h-6 text-emerald-400" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="font-bold text-lg tracking-wider text-white">FRAUDOSCOPE</h1>
            <span className="bg-slate-800 text-slate-300 text-xs px-2 py-0.5 rounded font-mono border border-slate-700">
              v1.0.0
            </span>
          </div>
          <p className="text-xs text-slate-400 tracking-wide font-medium">
            AUTONOMOUS PAYMENT SECURITY RESEARCH SANDBOX
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-4 text-xs font-mono">
        <div className="flex items-center space-x-1.5 bg-slate-950 px-3 py-1.5 rounded border border-slate-800">
          <span className="text-slate-500">ENV:</span>
          <span className="text-emerald-400 font-semibold">SYNTHETIC ONLY</span>
        </div>

        <div className="flex items-center space-x-1.5 bg-slate-950 px-3 py-1.5 rounded border border-slate-800">
          <Database className="w-3.5 h-3.5 text-blue-400" />
          <span className="text-slate-500">SEED:</span>
          <span className="text-blue-300 font-semibold">
            {overviewData?.simulation_seed ?? 42}
          </span>
        </div>

        <div className="flex items-center space-x-1.5 bg-slate-950 px-3 py-1.5 rounded border border-slate-800">
          <Cpu className="w-3.5 h-3.5 text-amber-400" />
          <span className="text-slate-500">MODEL:</span>
          <span className="text-amber-300 font-semibold">
            {overviewData?.active_model_id ?? 'v1.1.0-cand-42'}
          </span>
        </div>

        <div className="flex items-center space-x-1.5 bg-slate-950 px-3 py-1.5 rounded border border-slate-800">
          <Activity className="w-3.5 h-3.5 text-emerald-400" />
          <span className="text-slate-500">API:</span>
          {apiConnected ? (
            <span className="text-emerald-400 font-semibold flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              ONLINE
            </span>
          ) : (
            <span className="text-amber-400 font-semibold flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-amber-400"></span>
              SANDBOX DEMO
            </span>
          )}
        </div>
      </div>

      <div className="w-full text-right text-[11px] text-slate-500 flex items-center justify-end space-x-1 font-sans">
        <Info className="w-3 h-3 text-slate-400" />
        <span>
          Synthetic research environment — risk decisions produced by evaluated deterministic/ML components (no live payment rails).
        </span>
      </div>
    </header>
  );
};
