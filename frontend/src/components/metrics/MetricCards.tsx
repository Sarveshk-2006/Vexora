import React from 'react';
import { ClosedLoopMetrics } from '../../types/orchestration';
import { Zap, Target, Activity, Cpu, CheckCircle2 } from 'lucide-react';

interface MetricCardsProps {
  metrics: ClosedLoopMetrics;
  fidelityScore?: number;
  gapPriorityScore?: number;
}

export const MetricCards: React.FC<MetricCardsProps> = ({
  metrics,
  fidelityScore = 0.92,
  gapPriorityScore = 87.5,
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Metric 1: Precision & Recall */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-xl">
        <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-1">
          <span>PRECISION / RECALL</span>
          <Target className="w-4 h-4 text-emerald-400" />
        </div>
        <div className="flex items-baseline justify-between mt-2">
          <div>
            <span className="text-xl font-bold font-mono text-emerald-400">
              {(metrics.precision_after * 100).toFixed(1)}%
            </span>
            <span className="text-[10px] font-mono text-slate-500 block">
              PRECISION
            </span>
          </div>
          <div className="text-right">
            <span className="text-xl font-bold font-mono text-blue-400">
              {(metrics.recall_after * 100).toFixed(1)}%
            </span>
            <span className="text-[10px] font-mono text-slate-500 block">
              RECALL
            </span>
          </div>
        </div>
      </div>

      {/* Metric 2: Behavioral Fidelity Score */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-xl">
        <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-1">
          <span>BEHAVIORAL FIDELITY</span>
          <Activity className="w-4 h-4 text-purple-400" />
        </div>
        <div className="flex items-baseline justify-between mt-2">
          <span className="text-2xl font-bold font-mono text-purple-400">
            {(fidelityScore * 100).toFixed(1)}%
          </span>
          <span className="text-[10px] font-mono text-emerald-400 font-semibold border border-emerald-900/80 bg-emerald-950/60 px-2 py-0.5 rounded">
            CANONICAL
          </span>
        </div>
        <div className="text-[10px] font-mono text-slate-500 mt-1">
          Attack mutation realism against Digital Twin
        </div>
      </div>

      {/* Metric 3: Defense Gap Priority Score */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-xl">
        <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-1">
          <span>HIGHEST GAP PRIORITY</span>
          <Cpu className="w-4 h-4 text-amber-400" />
        </div>
        <div className="flex items-baseline justify-between mt-2">
          <span className="text-2xl font-bold font-mono text-amber-400">
            {gapPriorityScore.toFixed(1)} / 100
          </span>
          <span className="text-[10px] font-mono text-amber-400 font-semibold border border-amber-900/80 bg-amber-950/60 px-2 py-0.5 rounded">
            HIGH
          </span>
        </div>
        <div className="text-[10px] font-mono text-slate-500 mt-1">
          Multi-Vector Evasion Priority Index
        </div>
      </div>

      {/* Metric 4: Targeted Gap Improvement Delta */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-4 shadow-xl">
        <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-1">
          <span>HARDENING DELTA</span>
          <Zap className="w-4 h-4 text-emerald-400" />
        </div>
        <div className="flex items-baseline justify-between mt-2">
          <span className="text-2xl font-bold font-mono text-emerald-400">
            +{(metrics.targeted_gap_recall_delta * 100).toFixed(1)}%
          </span>
          <span className="text-[10px] font-mono text-emerald-400 font-semibold flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> PROMOTED
          </span>
        </div>
        <div className="text-[10px] font-mono text-slate-500 mt-1">
          Targeted gap recall improvement
        </div>
      </div>
    </div>
  );
};
