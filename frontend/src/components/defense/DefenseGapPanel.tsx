import React from 'react';
import { Cpu, AlertTriangle, CheckCircle2 } from 'lucide-react';

interface DefenseGapPanelProps {
  gaps?: any[];
  highestGapCategory?: string;
  highestPriorityScore?: number;
}

export const DefenseGapPanel: React.FC<DefenseGapPanelProps> = ({
  highestGapCategory = 'MULTI_VECTOR_EVASION',
  highestPriorityScore = 87.5,
}) => {
  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-2xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200 tracking-wide uppercase font-mono flex items-center gap-2">
            <Cpu className="w-4 h-4 text-amber-400" />
            Blue Team Defense Gap Discovery & Priority Ranking
          </h3>
          <p className="text-xs text-slate-400">
            Automated analysis of detector failures and structural evasion bypasses
          </p>
        </div>
        <span className="text-xs font-mono px-3 py-1 rounded bg-amber-950/80 text-amber-400 border border-amber-800/80 font-bold flex items-center gap-1">
          <AlertTriangle className="w-3.5 h-3.5" /> PRIORITY INDEX: {highestPriorityScore.toFixed(1)}
        </span>
      </div>

      <div className="p-4 rounded-lg bg-amber-950/20 border border-amber-800/60 mb-4">
        <div className="flex items-center justify-between">
          <span className="text-xs font-mono font-bold text-amber-300 uppercase">
            PRIMARY TARGETED GAP: {highestGapCategory}
          </span>
          <span className="text-xs font-mono text-amber-400 font-bold">
            ACTION THRESHOLD: 60.0 [TRIGGERED]
          </span>
        </div>
        <p className="text-xs text-slate-300 mt-2 font-mono">
          Behavioral mimicry & fragmented payment rail transfers evaded rule-based and static ML threshold boundaries. Retraining candidate model with adversarial sample augmentation.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
          <span className="text-[10px] font-mono text-slate-500">AFFECTED LAYER</span>
          <div className="text-xs font-bold text-slate-200 font-mono mt-1">
            BEHAVIORAL_ANOMALY
          </div>
        </div>
        <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
          <span className="text-[10px] font-mono text-slate-500">BYPASS COUNT</span>
          <div className="text-xs font-bold text-rose-400 font-mono mt-1">
            12 SAMPLES BYPASSED
          </div>
        </div>
        <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
          <span className="text-[10px] font-mono text-slate-500">HARDENING ACTION</span>
          <div className="text-xs font-bold text-emerald-400 font-mono mt-1 flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" /> ADVERSARIAL RETRAINING
          </div>
        </div>
      </div>
    </div>
  );
};
