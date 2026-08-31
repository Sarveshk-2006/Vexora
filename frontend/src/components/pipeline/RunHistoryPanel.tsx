import React from 'react';
import { ClosedLoopRunResult, ClosedLoopVerdict } from '../../types/orchestration';
import { History, CheckCircle2, XCircle } from 'lucide-react';

interface RunHistoryPanelProps {
  runs: ClosedLoopRunResult[];
  onSelectRun: (run: ClosedLoopRunResult) => void;
  selectedRunId?: string;
}

export const RunHistoryPanel: React.FC<RunHistoryPanelProps> = ({
  runs,
  onSelectRun,
  selectedRunId,
}) => {
  const getVerdictBadge = (verdict: ClosedLoopVerdict) => {
    switch (verdict) {
      case ClosedLoopVerdict.HARDENED_SUCCESSFULLY:
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-800/60 font-bold">
            <CheckCircle2 className="w-3 h-3" /> HARDENED
          </span>
        );
      case ClosedLoopVerdict.HARDENING_REJECTED:
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded bg-amber-950/80 text-amber-400 border border-amber-800/60 font-bold">
            <XCircle className="w-3 h-3" /> REJECTED
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded bg-rose-950/80 text-rose-400 border border-rose-800/60 font-bold">
            <XCircle className="w-3 h-3" /> {verdict}
          </span>
        );
    }
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-2xl">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-xs font-semibold text-slate-300 tracking-wide uppercase font-mono flex items-center gap-2">
          <History className="w-4 h-4 text-emerald-400" />
          Orchestration Run Audit Log
        </h3>
        <span className="text-[10px] font-mono text-slate-500">
          {runs.length} RUNS PERSISTED
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-slate-800 text-slate-500">
              <th className="py-2 px-3">RUN ID</th>
              <th className="py-2 px-3">SEED</th>
              <th className="py-2 px-3">VERDICT</th>
              <th className="py-2 px-3">MODEL</th>
              <th className="py-2 px-3">CREATED AT</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {runs.length === 0 ? (
              <tr>
                <td colSpan={5} className="py-4 text-center text-slate-500 italic">
                  No orchestration runs found. Click "RUN CLOSED-LOOP SIMULATION" to execute.
                </td>
              </tr>
            ) : (
              runs.map((r) => (
                <tr
                  key={r.run_id}
                  onClick={() => onSelectRun(r)}
                  className={`cursor-pointer transition-colors ${
                    selectedRunId === r.run_id
                      ? 'bg-slate-800/90 text-emerald-300'
                      : 'hover:bg-slate-850 text-slate-300'
                  }`}
                >
                  <td className="py-2.5 px-3 font-bold text-slate-200">
                    {r.run_id}
                  </td>
                  <td className="py-2.5 px-3 text-slate-400">
                    {r.provenance?.random_seed ?? 42}
                  </td>
                  <td className="py-2.5 px-3">{getVerdictBadge(r.verdict)}</td>
                  <td className="py-2.5 px-3 text-slate-400 truncate max-w-[120px]">
                    {r.active_model_after}
                  </td>
                  <td className="py-2.5 px-3 text-slate-500 text-[10px]">
                    {r.provenance?.created_at
                      ? new Date(r.provenance.created_at).toLocaleTimeString()
                      : 'Just now'}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
