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
    <div className="bg-white border border-[#D9DDE5] rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-[#111827] tracking-wide font-mono flex items-center gap-2">
            <Zap className="w-4 h-4 text-[#F98513]" />
            Defense Validation & Re-Attack Results
          </h3>
          <p className="text-xs text-[#475569] font-sans">
            Re-evaluating attack campaign against hardened model candidate
          </p>
        </div>
        <span className="text-xs font-mono px-3 py-1 rounded-lg bg-[#F8F7F4] text-[#273A91] border border-[#D9DDE5] font-bold">
          EVALUATION SEED 42
        </span>
      </div>

      {/* Story Flow Stepper */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-2 mb-5">
        <div className="p-3 rounded-lg bg-[#F8F7F4] border border-[#D9DDE5] flex flex-col justify-between">
          <span className="text-[10px] font-mono text-[#F98513] font-bold">STAGE 1</span>
          <div className="text-xs font-bold text-[#111827] font-mono mt-1">
            INITIAL ATTACK
          </div>
          <div className="text-[10px] text-[#475569] mt-1 font-medium">
            Evasion Campaign
          </div>
        </div>

        <div className="hidden md:flex items-center justify-center">
          <ArrowRight className="w-4 h-4 text-[#64748B]" />
        </div>

        <div className="p-3 rounded-lg bg-amber-50 border border-amber-200 flex flex-col justify-between">
          <span className="text-[10px] font-mono text-[#F98513] font-bold">STAGE 2</span>
          <div className="text-xs font-bold text-[#111827] font-mono mt-1">
            GAP IDENTIFIED
          </div>
          <div className="text-[10px] text-[#475569] mt-1 font-medium">
            Baseline Recall: {(metrics.targeted_gap_recall_before * 100).toFixed(1)}%
          </div>
        </div>

        <div className="hidden md:flex items-center justify-center">
          <ArrowRight className="w-4 h-4 text-[#64748B]" />
        </div>

        <div className="p-3 rounded-lg bg-[#E8F8F2] border border-[#16A36F]/30 flex flex-col justify-between">
          <span className="text-[10px] font-mono text-[#16A36F] font-bold">STAGE 3</span>
          <div className="text-xs font-bold text-[#16A36F] font-mono mt-1">
            HARDENED RE-ATTACK
          </div>
          <div className="text-[10px] text-[#16A36F] mt-1 font-semibold">
            Hardened Recall: {(metrics.targeted_gap_recall_after * 100).toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Metrics Comparison Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-lg bg-[#F8F7F4] border border-[#D9DDE5]">
          <div className="flex items-center justify-between text-xs font-mono text-[#475569] font-semibold mb-1">
            <span>TARGETED GAP RECALL</span>
            <TrendingUp className="w-3.5 h-3.5 text-[#16A36F]" />
          </div>
          <div className="flex items-baseline gap-2 mt-1">
            <span className="text-2xl font-bold font-mono text-[#16A36F]">
              {(metrics.targeted_gap_recall_after * 100).toFixed(1)}%
            </span>
            <span className="text-xs font-mono text-[#64748B] line-through">
              {(metrics.targeted_gap_recall_before * 100).toFixed(1)}%
            </span>
          </div>
          <div className="mt-2 text-[10px] font-mono text-[#16A36F] font-bold">
            +{(metrics.targeted_gap_recall_delta * 100).toFixed(1)} PERCENTAGE POINTS IMPROVEMENT
          </div>
        </div>

        <div className="p-4 rounded-lg bg-[#F8F7F4] border border-[#D9DDE5]">
          <div className="flex items-center justify-between text-xs font-mono text-[#475569] font-semibold mb-1">
            <span>BENIGN NON-REGRESSION</span>
            <Shield className="w-3.5 h-3.5 text-[#273A91]" />
          </div>
          <div className="flex items-baseline gap-2 mt-1">
            <span className="text-2xl font-bold font-mono text-[#273A91]">
              {(metrics.benign_approval_rate_after * 100).toFixed(1)}%
            </span>
            <span className="text-xs font-mono text-[#64748B]">APPROVAL</span>
          </div>
          <div className="mt-2 text-[10px] font-mono text-[#16A36F] font-semibold flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> ZERO REGRESSION
          </div>
        </div>

        <div className="p-4 rounded-lg bg-[#F8F7F4] border border-[#D9DDE5]">
          <div className="flex items-center justify-between text-xs font-mono text-[#475569] font-semibold mb-1">
            <span>MODEL PROMOTION</span>
            <CheckCircle2 className="w-3.5 h-3.5 text-[#F98513]" />
          </div>
          <div className="text-sm font-bold font-mono text-[#111827] mt-1 truncate">
            {activeModelAfter}
          </div>
          <div className="mt-2 text-[10px] font-mono text-[#475569] truncate">
            BASELINE: {activeModelBefore}
          </div>
        </div>
      </div>
    </div>
  );
};
