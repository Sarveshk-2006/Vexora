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
          <span className="inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded bg-[#E8F8F2] text-[#16A36F] border border-[#16A36F]/30 font-bold">
            <CheckCircle2 className="w-3 h-3" /> HARDENED
          </span>
        );
      case ClosedLoopVerdict.HARDENING_REJECTED:
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded bg-amber-50 text-[#F98513] border border-amber-200 font-bold">
            <XCircle className="w-3 h-3" /> REJECTED
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-mono px-2 py-0.5 rounded bg-rose-50 text-[#DC3545] border border-rose-200 font-bold">
            <XCircle className="w-3 h-3" /> {verdict}
          </span>
        );
    }
  };

  return (
    <div className="bg-white border border-[#D9DDE5] rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-base font-bold text-[#111827] tracking-wide font-mono flex items-center gap-2">
          <History className="w-4 h-4 text-[#273A91]" />
          Audit Log
        </h3>
        <span className="text-[10px] font-mono text-[#64748B]">
          {runs.length} RUNS PERSISTED
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-[#D9DDE5] text-[#475569] bg-[#F8F7F4]">
              <th className="py-2.5 px-3">RUN ID</th>
              <th className="py-2.5 px-3">SEED</th>
              <th className="py-2.5 px-3">VERDICT</th>
              <th className="py-2.5 px-3">ACTIVE MODEL</th>
              <th className="py-2.5 px-3">CREATED AT</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#D9DDE5]">
            {runs.length === 0 ? (
              <tr>
                <td colSpan={5} className="py-4 text-center text-[#64748B] italic">
                  No historical runs found. Click "RUN SIMULATION CYCLE" to execute.
                </td>
              </tr>
            ) : (
              runs.map((r) => (
                <tr
                  key={r.run_id}
                  onClick={() => onSelectRun(r)}
                  className={`cursor-pointer transition-colors ${
                    selectedRunId === r.run_id
                      ? 'bg-[#E8EEF9] text-[#111827] font-bold'
                      : 'hover:bg-[#F8F7F4] text-[#111827]'
                  }`}
                >
                  <td className="py-2.5 px-3 font-bold text-[#111827]">
                    {r.run_id}
                  </td>
                  <td className="py-2.5 px-3 text-[#475569]">
                    {r.provenance?.random_seed ?? 42}
                  </td>
                  <td className="py-2.5 px-3">{getVerdictBadge(r.verdict)}</td>
                  <td className="py-2.5 px-3 text-[#273A91] truncate max-w-[140px]">
                    {r.active_model_after}
                  </td>
                  <td className="py-2.5 px-3 text-[#64748B] text-[10px]">
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
