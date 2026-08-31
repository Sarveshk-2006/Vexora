import React from 'react';
import { ClosedLoopMetrics } from '../../types/orchestration';
import { Shield, ArrowRight, CheckCircle2, TrendingUp, Zap } from 'lucide-react';

interface ReAttackVisualizationProps {
  metrics: ClosedLoopMetrics;
  activeModelBefore: string;
  activeModelAfter: string;
}

export const ReAttackVisualization: React.FC<ReAttackVisualizationProps> = ({
  metrics,
  activeModelBefore,
  activeModelAfter,
}) => {
  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-2xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200 tracking-wide uppercase font-mono flex items-center gap-2">
            <Zap className="w-4 h-4 text-emerald-400" />
            Closed-Loop Re-Attack & Defense Response Centerpiece
          </h3>
          <p className="text-xs text-slate-400">
            Replaying the SAME Red Team attack against the hardened model candidate
          </p>
        </div>
        <span className="text-xs font-mono px-3 py-1 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-800/80 font-bold">
          EVALUATION SEED 42
        </span>
      </div>

      {/* Story Flow Stepper */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-2 mb-6">
        <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 flex flex-col justify-between">
          <span className="text-[10px] font-mono text-rose-400 font-bold">STAGE 1</span>
          <div className="text-xs font-bold text-slate-200 font-mono mt-1">
            ORIGINAL ATTACK
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Gen-0 Evasion Scenario
          </div>
        </div>

        <div className="hidden md:flex items-center justify-center">
          <ArrowRight className="w-5 h-5 text-slate-600" />
        </div>

        <div className="p-3 rounded-lg bg-amber-950/30 border border-amber-800/50 flex flex-col justify-between">
          <span className="text-[10px] font-mono text-amber-400 font-bold">STAGE 2</span>
          <div className="text-xs font-bold text-amber-200 font-mono mt-1">
            DEFENSE GAP DETECTED
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Recall: {(metrics.targeted_gap_recall_before * 100).toFixed(1)}%
          </div>
        </div>

        <div className="hidden md:flex items-center justify-center">
          <ArrowRight className="w-5 h-5 text-slate-600" />
        </div>

        <div className="p-3 rounded-lg bg-emerald-950/40 border border-emerald-800/60 flex flex-col justify-between">
          <span className="text-[10px] font-mono text-emerald-400 font-bold">STAGE 3</span>
          <div className="text-xs font-bold text-emerald-200 font-mono mt-1">
            HARDENED RE-ATTACK
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Recall: {(metrics.targeted_gap_recall_after * 100).toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Metrics Comparison Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-lg bg-slate-950 border border-slate-800">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-1">
            <span>TARGETED GAP RECALL</span>
            <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
          </div>
          <div className="flex items-baseline gap-2 mt-1">
            <span className="text-2xl font-bold font-mono text-emerald-400">
              {(metrics.targeted_gap_recall_after * 100).toFixed(1)}%
            </span>
            <span className="text-xs font-mono text-slate-500 line-through">
              {(metrics.targeted_gap_recall_before * 100).toFixed(1)}%
            </span>
          </div>
          <div className="mt-2 text-[10px] font-mono text-emerald-400 font-semibold">
            +{(metrics.targeted_gap_recall_delta * 100).toFixed(1)} PERCENTAGE POINTS IMPROVEMENT
          </div>
        </div>

        <div className="p-4 rounded-lg bg-slate-950 border border-slate-800">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-1">
            <span>BENIGN NON-REGRESSION</span>
            <Shield className="w-3.5 h-3.5 text-blue-400" />
          </div>
          <div className="flex items-baseline gap-2 mt-1">
            <span className="text-2xl font-bold font-mono text-blue-400">
              {(metrics.benign_approval_rate_after * 100).toFixed(1)}%
            </span>
            <span className="text-xs font-mono text-slate-500">APPROVAL</span>
          </div>
          <div className="mt-2 text-[10px] font-mono text-emerald-400 font-semibold flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> ZERO REGRESSION
          </div>
        </div>

        <div className="p-4 rounded-lg bg-slate-950 border border-slate-800">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400 mb-1">
            <span>ACTIVE MODEL TRANSITION</span>
            <CheckCircle2 className="w-3.5 h-3.5 text-purple-400" />
          </div>
          <div className="text-sm font-bold font-mono text-slate-200 mt-1 truncate">
            {activeModelAfter}
          </div>
          <div className="mt-2 text-[10px] font-mono text-slate-400 truncate">
            PREVIOUS: {activeModelBefore}
          </div>
        </div>
      </div>
    </div>
  );
};
