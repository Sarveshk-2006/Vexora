import React, { useState } from 'react';
import {
  ClosedLoopStageResult,
  PipelineStage,
  StageStatus,
} from '../../types/orchestration';
import {
  CheckCircle2,
  XCircle,
  Clock,
  Shield,
  Zap,
  Cpu,
  FileText,
  RotateCcw,
  Award,
} from 'lucide-react';

interface ClosedLoopPipelineProps {
  stages: ClosedLoopStageResult[];
  activeStage?: PipelineStage;
}

export const ClosedLoopPipeline: React.FC<ClosedLoopPipelineProps> = ({
  stages,
  activeStage,
}) => {
  const [expandedStage, setExpandedStage] = useState<string | null>(null);

  const getStageIcon = (stage: PipelineStage) => {
    switch (stage) {
      case PipelineStage.SCENARIO_PREPARATION:
        return <FileText className="w-3.5 h-3.5 text-[#273A91]" />;
      case PipelineStage.RED_TEAM:
        return <Zap className="w-3.5 h-3.5 text-[#F98513]" />;
      case PipelineStage.BLUE_TEAM:
        return <Shield className="w-3.5 h-3.5 text-[#273A91]" />;
      case PipelineStage.GAP_ANALYSIS:
        return <Cpu className="w-3.5 h-3.5 text-[#F98513]" />;
      case PipelineStage.HARDENING:
        return <Cpu className="w-3.5 h-3.5 text-[#16A36F]" />;
      case PipelineStage.EXPLAINABILITY:
        return <FileText className="w-3.5 h-3.5 text-[#273A91]" />;
      case PipelineStage.RE_ATTACK_VALIDATION:
        return <RotateCcw className="w-3.5 h-3.5 text-indigo-600" />;
      case PipelineStage.VERDICT:
        return <Award className="w-3.5 h-3.5 text-[#16A36F]" />;
      default:
        return <Clock className="w-3.5 h-3.5 text-[#64748B]" />;
    }
  };

  const getStageLabel = (stage: PipelineStage) => {
    switch (stage) {
      case PipelineStage.SCENARIO_PREPARATION:
        return 'Scenario';
      case PipelineStage.RED_TEAM:
        return 'Attack';
      case PipelineStage.BLUE_TEAM:
        return 'Detect';
      case PipelineStage.GAP_ANALYSIS:
        return 'Gap';
      case PipelineStage.HARDENING:
        return 'Harden';
      case PipelineStage.EXPLAINABILITY:
        return 'Explain';
      case PipelineStage.RE_ATTACK_VALIDATION:
        return 'Re-attack';
      case PipelineStage.VERDICT:
        return 'Verdict';
      default:
        return stage;
    }
  };

  const getStatusBadge = (status: StageStatus) => {
    switch (status) {
      case StageStatus.COMPLETED:
        return (
          <span className="inline-flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded bg-[#E8F8F2] text-[#16A36F] border border-[#16A36F]/30 font-mono font-semibold">
            <CheckCircle2 className="w-2.5 h-2.5" /> PASSED
          </span>
        );
      case StageStatus.IN_PROGRESS:
        return (
          <span className="inline-flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded bg-amber-50 text-[#F98513] border border-amber-200 font-mono font-semibold animate-pulse">
            <Clock className="w-2.5 h-2.5 animate-spin" /> RUNNING
          </span>
        );
      case StageStatus.FAILED:
        return (
          <span className="inline-flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded bg-rose-50 text-[#DC3545] border border-rose-200 font-mono font-semibold">
            <XCircle className="w-2.5 h-2.5" /> FAILED
          </span>
        );
      case StageStatus.SKIPPED:
        return (
          <span className="inline-flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded bg-[#F8F7F4] text-[#64748B] border border-[#D9DDE5] font-mono">
            SKIPPED
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded bg-[#F8F7F4] text-[#64748B] border border-[#D9DDE5] font-mono">
            WAITING
          </span>
        );
    }
  };

  return (
    <div className="bg-white border border-[#D9DDE5] rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-[#111827] tracking-wide font-mono flex items-center gap-2">
            <Zap className="w-4 h-4 text-[#F98513]" />
            Pipeline Execution State
          </h3>
          <p className="text-xs text-[#475569] font-sans">
            Scenario → Attack → Detect → Gap Analysis → Hardening → Re-Attack → Verdict
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-2">
        {stages.map((st, idx) => {
          const isActive = activeStage === st.stage;
          const isExpanded = expandedStage === st.stage;

          return (
            <div
              key={st.stage}
              onClick={() => setExpandedStage(isExpanded ? null : st.stage)}
              className={`cursor-pointer transition-all duration-200 p-3 rounded-lg border flex flex-col justify-between card-hover ${
                isActive
                  ? 'bg-[#E8EEF9] border-[#273A91] shadow-sm ring-1 ring-[#273A91]'
                  : st.status === StageStatus.COMPLETED
                  ? 'bg-[#F8F7F4] border-[#D9DDE5] hover:border-[#9BACD8]'
                  : st.status === StageStatus.FAILED
                  ? 'bg-rose-50 border-rose-200'
                  : 'bg-slate-50 border-slate-200 opacity-60'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-[10px] font-mono text-[#273A91] font-bold">
                    0{idx + 1}
                  </span>
                  {getStageIcon(st.stage)}
                </div>
                <div className="text-xs font-bold text-[#111827] font-mono truncate">
                  {getStageLabel(st.stage)}
                </div>
              </div>

              <div className="mt-2 pt-2 border-t border-[#D9DDE5] flex items-center justify-between">
                {getStatusBadge(st.status)}
                {st.duration_ms > 0 && (
                  <span className="text-[10px] font-mono text-[#64748B]">
                    {st.duration_ms.toFixed(0)}ms
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {expandedStage && (
        <div className="mt-4 p-4 rounded-lg bg-[#F8F7F4] border border-[#D9DDE5] text-xs font-mono text-[#111827]">
          {(() => {
            const detailStage = stages.find((s) => s.stage === expandedStage);
            if (!detailStage) return null;
            return (
              <div>
                <div className="flex items-center justify-between mb-2 text-[#273A91] font-bold border-b border-[#D9DDE5] pb-2">
                  <span>STAGE DETAILS: {detailStage.stage}</span>
                  <button
                    onClick={() => setExpandedStage(null)}
                    className="text-[#64748B] hover:text-[#111827] text-xs font-mono font-semibold"
                  >
                    [Close]
                  </button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-[11px]">
                  <div>
                    <span className="text-[#475569] font-bold">STATUS:</span>{' '}
                    {detailStage.status}
                  </div>
                  <div>
                    <span className="text-[#475569] font-bold">DURATION:</span>{' '}
                    {detailStage.duration_ms.toFixed(2)} ms
                  </div>
                  <div>
                    <span className="text-[#475569] font-bold">INPUTS:</span>{' '}
                    {JSON.stringify(detailStage.input_identifiers)}
                  </div>
                  <div>
                    <span className="text-[#475569] font-bold">OUTPUTS:</span>{' '}
                    {JSON.stringify(detailStage.output_identifiers)}
                  </div>
                </div>
                {detailStage.error_message && (
                  <div className="mt-2 text-[#DC3545] bg-rose-50 p-2 rounded border border-rose-200">
                    ERROR: {detailStage.error_message}
                  </div>
                )}
              </div>
            );
          })()}
        </div>
      )}
    </div>
  );
};
