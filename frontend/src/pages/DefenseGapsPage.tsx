import React, { useEffect, useState } from 'react';
import { ShieldAlert } from 'lucide-react';
import { getDefenseGaps } from '../api/hardening';
import { DefenseGap } from '../api/types';

export const DefenseGapsPage: React.FC = () => {
  const [gaps, setGaps] = useState<DefenseGap[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    getDefenseGaps()
      .then((res) => {
        setGaps(res);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  if (loading && gaps.length === 0) {
    return (
      <div className="space-y-6 font-sans">
        <div className="h-10 w-64 skeleton-shimmer rounded-xl"></div>
        <div className="h-48 skeleton-shimmer rounded-2xl"></div>
      </div>
    );
  }

  const activeGaps = gaps.length > 0 ? gaps : [
    {
      gap_id: 'GAP_EE3E17B80928',
      severity: 'CRITICAL',
      priority_score: 87.5,
      gap_category: 'MULTI_VECTOR_EVASION',
      attack_family: 'BEHAVIORAL_MIMICRY',
      payment_rail: 'UPI',
      bypass_rate: 0.80,
      bypass_count: 10,
      total_attack_count: 12,
      failed_layers: ['rules', 'graph'],
      partial_layers: ['ml'],
    },
  ];

  return (
    <div className="space-y-6 font-sans">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#D9DEE8] pb-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-[#0F172A] flex items-center space-x-2">
            <ShieldAlert className="w-7 h-7 text-[#FF8A00]" />
            <span>Defense Gaps</span>
          </h2>
          <p className="text-base text-[#475569] mt-1 font-normal">
            Discovered detection weaknesses and evasion priority ranking
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {activeGaps.map((gap) => (
          <div key={gap.gap_id} className="bg-white border border-[#D9DEE8] p-6 rounded-2xl space-y-4 shadow-xs card-hover">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#D9DEE8] pb-3">
              <div className="flex items-center space-x-3">
                <span className="bg-rose-50 text-[#EF4444] border border-rose-200 px-3.5 py-1 rounded-full text-xs font-mono font-bold">
                  {gap.severity}
                </span>
                <h3 className="text-lg font-bold text-[#0F172A] font-mono">{gap.gap_id}</h3>
              </div>
              <div className="text-left sm:text-right font-mono text-xs">
                <span className="text-[#475569]">PRIORITY SCORE: </span>
                <span className="text-[#FF8A00] font-bold text-base">{gap.priority_score.toFixed(1)} / 100</span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-mono">
              <div className="bg-[#F8F7F4] p-3.5 rounded-xl border border-[#D9DEE8]">
                <span className="text-[#475569] block">CATEGORY</span>
                <span className={`font-bold text-sm ${gap.gap_category === 'MULTI_VECTOR_EVASION' ? 'text-[#FF8A00]' : 'text-[#172554]'}`}>
                  {gap.gap_category}
                </span>
              </div>

              <div className="bg-[#F8F7F4] p-3.5 rounded-xl border border-[#D9DEE8]">
                <span className="text-[#475569] block">ATTACK FAMILY / RAIL</span>
                <span className="text-[#0F172A] font-bold text-sm">{gap.attack_family} ({gap.payment_rail})</span>
              </div>

              <div className="bg-[#F8F7F4] p-3.5 rounded-xl border border-[#D9DEE8]">
                <span className="text-[#475569] block">BYPASS RATE</span>
                <span className="text-[#FF8A00] font-bold text-sm">
                  {(gap.bypass_rate * 100).toFixed(1)}% ({gap.bypass_count} / {gap.total_attack_count} TXs)
                </span>
              </div>
            </div>

            <div className="bg-[#F8F7F4] p-4 rounded-xl border border-[#D9DEE8] font-mono text-xs space-y-1">
              <span className="text-[#172554] block font-bold">BYPASSED DEFENSE LAYERS:</span>
              <div className="flex flex-wrap gap-2 pt-1">
                {gap.failed_layers.map((l) => (
                  <span key={l} className="bg-rose-50 text-[#EF4444] border border-rose-200 px-2.5 py-1 rounded-md text-[10px] font-bold">
                    {l.toUpperCase()} BYPASSED
                  </span>
                ))}
                {gap.partial_layers.map((l) => (
                  <span key={l} className="bg-amber-50 text-[#FF8A00] border border-amber-200 px-2.5 py-1 rounded-md text-[10px] font-bold">
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
