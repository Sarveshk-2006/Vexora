import React, { useEffect, useState } from 'react';
import { ShieldAlert } from 'lucide-react';
import { getDefenseGaps } from '../api/hardening';
import { DefenseGap } from '../api/types';

export const DefenseGapsPage: React.FC = () => {
  const [gaps, setGaps] = useState<DefenseGap[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    getDefenseGaps().then((res) => {
      setGaps(res);
      setLoading(false);
    });
  }, []);

  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400 font-mono text-sm">
        Analyzing Blue Team Defense Gaps...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center space-x-2">
            <ShieldAlert className="w-5 h-5 text-rose-400" />
            <span>Defense Gap Discovery & Taxonomy Dashboard</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Deterministic 9-Category Evasion Taxonomy & Prioritization Engine
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {gaps.map((gap) => (
          <div key={gap.gap_id} className="bg-slate-900 border border-slate-800 p-5 rounded-lg space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center space-x-3">
                <span className="bg-rose-500/10 text-rose-400 border border-rose-500/30 px-3 py-1 rounded text-xs font-mono font-bold">
                  {gap.severity}
                </span>
                <h3 className="text-base font-bold text-white font-mono">{gap.gap_id}</h3>
              </div>
              <div className="text-right font-mono text-xs">
                <span className="text-slate-400">PRIORITY SCORE: </span>
                <span className="text-rose-400 font-bold text-sm">{gap.priority_score.toFixed(1)} / 100</span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-mono">
              <div className="bg-slate-950 p-3 rounded border border-slate-800">
                <span className="text-slate-500 block">TAXONOMY CATEGORY</span>
                <span className={`font-bold ${gap.gap_category === 'MULTI_VECTOR_EVASION' ? 'text-rose-400 font-extrabold' : 'text-amber-400'}`}>
                  {gap.gap_category}
                </span>
              </div>

              <div className="bg-slate-950 p-3 rounded border border-slate-800">
                <span className="text-slate-500 block">ATTACK FAMILY / RAIL</span>
                <span className="text-slate-200 font-bold">{gap.attack_family} ({gap.payment_rail})</span>
              </div>

              <div className="bg-slate-950 p-3 rounded border border-slate-800">
                <span className="text-slate-500 block">BYPASS RATE</span>
                <span className="text-rose-400 font-bold">
                  {(gap.bypass_rate * 100).toFixed(1)}% ({gap.bypass_count} / {gap.total_attack_count} TXs)
                </span>
              </div>
            </div>

            <div className="bg-slate-950 p-3 rounded border border-slate-800 font-mono text-xs space-y-1">
              <span className="text-slate-400 block font-bold">FAILED / BYPASSED DEFENSE LAYERS:</span>
              <div className="flex flex-wrap gap-2 pt-1">
                {gap.failed_layers.map((l) => (
                  <span key={l} className="bg-rose-500/10 text-rose-400 border border-rose-500/30 px-2 py-0.5 rounded text-[10px]">
                    {l.toUpperCase()} BYPASSED
                  </span>
                ))}
                {gap.partial_layers.map((l) => (
                  <span key={l} className="bg-amber-500/10 text-amber-400 border border-amber-500/30 px-2 py-0.5 rounded text-[10px]">
                    {l.toUpperCase()} PARTIAL
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
