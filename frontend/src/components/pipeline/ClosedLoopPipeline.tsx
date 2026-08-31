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
        return <FileText className="w-4 h-4 text-cyan-400" />;
      case PipelineStage.RED_TEAM:
        return <Zap className="w-4 h-4 text-rose-400" />;
      case PipelineStage.BLUE_TEAM:
        return <Shield className="w-4 h-4 text-blue-400" />;
      case PipelineStage.GAP_ANALYSIS:
        return <Cpu className="w-4 h-4 text-amber-400" />;
      case PipelineStage.HARDENING:
        return <Cpu className="w-4 h-4 text-emerald-400" />;
      case PipelineStage.EXPLAINABILITY:
        return <FileText className="w-4 h-4 text-purple-400" />;
      case PipelineStage.RE_ATTACK_VALIDATION:
        return <RotateCcw className="w-4 h-4 text-indigo-400" />;
      case PipelineStage.VERDICT:
        return <Award className="w-4 h-4 text-emerald-400" />;
      default:
        return <Clock className="w-4 h-4 text-slate-400" />;
    }
  };

  const getStatusBadge = (status: StageStatus) => {
    switch (status) {
      case StageStatus.COMPLETED:
        return (
          <span className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-400 border border-emerald-800/60 font-mono">
            <CheckCircle2 className="w-3 h-3" /> COMPLETED
          </span>
        );
      case StageStatus.IN_PROGRESS:
        return (
          <span className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded bg-amber-950/80 text-amber-400 border border-amber-800/60 font-mono animate-pulse">
            <Clock className="w-3 h-3 animate-spin" /> IN_PROGRESS
          </span>
        );
      case StageStatus.FAILED:
        return (
          <span className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded bg-rose-950/80 text-rose-400 border border-rose-800/60 font-mono">
            <XCircle className="w-3 h-3" /> FAILED
          </span>
        );
      case StageStatus.SKIPPED:
        return (
          <span className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded bg-slate-900/80 text-slate-400 border border-slate-700/60 font-mono">
            SKIPPED
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded bg-slate-900 text-slate-500 border border-slate-800 font-mono">
            NOT_STARTED
          </span>
        );
    }
  };

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-2xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200 tracking-wide uppercase font-mono flex items-center gap-2">
            <Zap className="w-4 h-4 text-emerald-400" />
            Closed-Loop Pipeline Execution State Machine
          </h3>
          <p className="text-xs text-slate-400">
            Automated 8-stage synthetic attack, detection, hardening & validation flow
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-8 gap-2 mb-4">
        {stages.map((st, idx) => {
          const isActive = activeStage === st.stage;
          const isExpanded = expandedStage === st.stage;

          return (
            <div
              key={st.stage}
              onClick={() =>
                setExpandedStage(isExpanded ? null : st.stage)
              }
              className={`cursor-pointer transition-all duration-200 p-3 rounded-lg border flex flex-col justify-between ${
                isActive
                  ? 'bg-slate-800/90 border-emerald-500 shadow-lg shadow-emerald-950/40 ring-1 ring-emerald-500'
                  : st.status === StageStatus.COMPLETED
                  ? 'bg-slate-900/80 border-slate-800 hover:border-slate-700 hover:bg-slate-850'
                  : st.status === StageStatus.FAILED
                  ? 'bg-rose-950/20 border-rose-900/60'
                  : 'bg-slate-950/40 border-slate-900 opacity-60'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-mono text-slate-500 font-semibold">
                    0{idx + 1}
                  </span>
                  {getStageIcon(st.stage)}
                </div>
                <div className="text-xs font-semibold text-slate-200 font-mono truncate mb-1">
                  {st.stage.replace(/_/g, ' ')}
                </div>
              </div>

              <div className="mt-2 pt-2 border-t border-slate-800/60 flex items-center justify-between">
                <div>{getStatusBadge(st.status)}</div>
                <span className="text-[10px] font-mono text-slate-400">
                  {st.duration_ms.toFixed(1)}ms
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {expandedStage && (
        <div className="mt-4 p-4 rounded-lg bg-slate-950 border border-slate-800 text-xs font-mono text-slate-300">
          {(() => {
            const detailStage = stages.find((s) => s.stage === expandedStage);
            if (!detailStage) return null;
            return (
              <div>
                <div className="flex items-center justify-between mb-2 text-emerald-400 font-bold border-b border-slate-800 pb-2">
                  <span>STAGE DETAILS: {detailStage.stage}</span>
                  <button
                    onClick={() => setExpandedStage(null)}
                    className="text-slate-400 hover:text-slate-200 text-xs"
                  >
                    Close [X]
                  </button>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <span className="text-slate-500 font-bold">STARTED AT:</span>{' '}
                    {detailStage.started_at || 'N/A'}
                  </div>
                  <div>
                    <span className="text-slate-500 font-bold">COMPLETED AT:</span>{' '}
                    {detailStage.completed_at || 'N/A'}
                  </div>
                  <div>
                    <span className="text-slate-500 font-bold">INPUT IDENTIFIERS:</span>{' '}
                    {JSON.stringify(detailStage.input_identifiers)}
                  </div>
                  <div>
                    <span className="text-slate-500 font-bold">OUTPUT IDENTIFIERS:</span>{' '}
                    {JSON.stringify(detailStage.output_identifiers)}
                  </div>
                </div>
                {detailStage.error_message && (
                  <div className="mt-2 text-rose-400 bg-rose-950/40 p-2 rounded border border-rose-900">
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
