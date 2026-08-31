import React, { useState, useEffect } from 'react';
import { Shield, Activity, AlertTriangle } from 'lucide-react';
import { RunControlPanel } from '../components/pipeline/RunControlPanel';
import { ClosedLoopPipeline } from '../components/pipeline/ClosedLoopPipeline';
import { ReAttackVisualization } from '../components/pipeline/ReAttackVisualization';
import { HardeningGatePanel } from '../components/hardening/HardeningGatePanel';
import { WhyFlaggedPanel } from '../components/explainability/WhyFlaggedPanel';
import { LineageExplorer } from '../components/pipeline/LineageExplorer';
import { RunHistoryPanel } from '../components/pipeline/RunHistoryPanel';

import {
  runClosedLoopSimulation,
  listClosedLoopRuns,
  fetchHealthStatus,
} from '../services/api';
import {
  ClosedLoopRunResult,
  ClosedLoopMetrics,
  ClosedLoopVerdict,
  StageStatus,
} from '../types/orchestration';

export const CommandCenterPage: React.FC = () => {
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [currentRun, setCurrentRun] = useState<ClosedLoopRunResult | null>(null);
  const [runs, setRuns] = useState<ClosedLoopRunResult[]>([]);
  const [healthStatus, setHealthStatus] = useState<string>('ONLINE');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    fetchHealthStatus()
      .then(() => setHealthStatus('ONLINE'))
      .catch(() => setHealthStatus('OFFLINE'));

    listClosedLoopRuns()
      .then((res: ClosedLoopRunResult[]) => {
        setRuns(res);
        if (res.length > 0) {
          setCurrentRun(res[0]);
        }
      })
      .catch(() => {
        setRuns([]);
      });
  }, []);

  const handleRunSimulation = async (seed: number) => {
    setIsRunning(true);
    setErrorMsg(null);
    try {
      const runResult = await runClosedLoopSimulation({ seed });
      setCurrentRun(runResult);
      setRuns((prev) => [runResult, ...prev]);
    } catch (err: any) {
      setErrorMsg(err?.message || 'Simulation failed to execute. Utilizing fallback demo data.');
    } finally {
      setIsRunning(false);
    }
  };

  const defaultMetrics: ClosedLoopMetrics = {
    precision_before: 0.85,
    precision_after: 0.85,
    recall_before: 0.6,
    recall_after: 0.6,
    f1_before: 0.71,
    f1_after: 0.71,
    roc_auc_before: 0.78,
    roc_auc_after: 0.78,
    false_positive_rate_before: 0.359,
    false_positive_rate_after: 0.359,
    targeted_gap_recall_before: 0.2,
    targeted_gap_recall_after: 0.8,
    unseen_attack_recall_before: 1.0,
    unseen_attack_recall_after: 1.0,
    benign_approval_rate_before: 0.7353,
    benign_approval_rate_after: 0.7353,
    recall_delta: 0.0,
    targeted_gap_recall_delta: 0.6,
  };

  const activeMetrics = currentRun?.metrics || defaultMetrics;

  return (
    <div className="space-y-6 font-sans">
      {/* Top Banner / System Status Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-white border border-[#D9DEE8] shadow-xs">
        <div className="flex items-center gap-4">
          <div className="p-3 rounded-xl bg-[#EEF3FF] border border-[#D9DEE8] text-[#172554]">
            <Shield className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold font-mono tracking-wide text-[#0F172A] flex flex-wrap items-center gap-3">
              VEXORA COMMAND CENTER
              <span className="text-xs px-2.5 py-1 rounded-full bg-[#EEF3FF] text-[#172554] border border-[#D9DEE8] font-mono font-bold">
                SYNTHETIC SANDBOX
              </span>
            </h1>
            <p className="text-sm text-[#475569] font-sans mt-0.5">
              Synthetic payment-security sandbox and defense simulation runner
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 text-xs font-mono">
          <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-[#F8F7F4] border border-[#D9DEE8]">
            <Activity className="w-4 h-4 text-[#172554]" />
            <span className="text-[#475569]">BACKEND:</span>
            <span
              className={`font-bold ${
                healthStatus === 'ONLINE'
                  ? 'text-[#10B981]'
                  : 'text-[#EF4444]'
              }`}
            >
              {healthStatus}
            </span>
          </div>

          <div className="px-3 py-2 rounded-xl bg-[#F8F7F4] border border-[#D9DEE8] text-[#0F172A]">
            {currentRun ? (
              <>
                ACTIVE MODEL: <span className="text-[#FF8A00] font-bold">{currentRun.active_model_after}</span>
              </>
            ) : (
              <>
                BASELINE MODEL: <span className="text-[#172554] font-bold">v0.1.0</span>
              </>
            )}
          </div>
        </div>
      </div>

      {healthStatus === 'OFFLINE' && (
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-[#F59E0B] text-xs font-mono flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-[#F59E0B]" />
            <span>
              Live backend server unavailable. Operating in offline synthetic research sandbox mode.
            </span>
          </div>
          <button
            onClick={() =>
              fetchHealthStatus()
                .then(() => setHealthStatus('ONLINE'))
                .catch(() => setHealthStatus('OFFLINE'))
            }
            className="px-3 py-1 bg-[#172554] hover:bg-[#0F172A] text-white rounded-lg text-xs font-semibold"
          >
            RETRY API
          </button>
        </div>
      )}

      {errorMsg && (
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-[#F59E0B] text-xs font-mono">
          NOTICE: {errorMsg}
        </div>
      )}

      {/* 1. Run Control Panel */}
      <RunControlPanel
        onRunSimulation={handleRunSimulation}
        isRunning={isRunning}
        activeSeed={currentRun?.provenance?.random_seed || 42}
      />

      {/* 2. Closed-Loop Pipeline Execution State Machine */}
      <ClosedLoopPipeline
        stages={
          currentRun?.stage_results || [
            {
              stage: 'SCENARIO_PREPARATION' as any,
              status: StageStatus.COMPLETED,
              duration_ms: 0.8,
              input_identifiers: { seed: 42 },
              output_identifiers: { genome_hash: '3fcc41a4' },
              detail: {},
            },
            {
              stage: 'RED_TEAM' as any,
              status: StageStatus.COMPLETED,
              duration_ms: 12.4,
              input_identifiers: {},
              output_identifiers: { affected_tx_count: 12 },
              detail: {},
            },
            {
              stage: 'BLUE_TEAM' as any,
              status: StageStatus.COMPLETED,
              duration_ms: 45.2,
              input_identifiers: {},
              output_identifiers: { active_model: 'v0.1.0' },
              detail: {},
            },
            {
              stage: 'GAP_ANALYSIS' as any,
              status: StageStatus.COMPLETED,
              duration_ms: 8.1,
              input_identifiers: {},
              output_identifiers: { gap_category: 'MULTI_VECTOR_EVASION' },
              detail: {},
            },
            {
              stage: 'HARDENING' as any,
              status: StageStatus.COMPLETED,
              duration_ms: 320.5,
              input_identifiers: {},
              output_identifiers: { decision: 'PROMOTE' },
              detail: {},
            },
            {
              stage: 'EXPLAINABILITY' as any,
              status: StageStatus.COMPLETED,
              duration_ms: 18.3,
              input_identifiers: {},
              output_identifiers: {},
              detail: {},
            },
            {
              stage: 'RE_ATTACK_VALIDATION' as any,
              status: StageStatus.COMPLETED,
              duration_ms: 14.1,
              input_identifiers: {},
              output_identifiers: { targeted_gap_recall_after: 0.8 },
              detail: {},
            },
            {
              stage: 'VERDICT' as any,
              status: StageStatus.COMPLETED,
              duration_ms: 0.2,
              input_identifiers: {},
              output_identifiers: { verdict: 'HARDENED_SUCCESSFULLY' },
              detail: {},
            },
          ]
        }
      />

      {/* 3. Re-Attack Centerpiece Visualization */}
      <ReAttackVisualization
        metrics={activeMetrics}
        activeModelBefore={currentRun?.active_model_before || 'v0.1.0'}
        activeModelAfter={currentRun?.active_model_after || 'v1.1.0-cand-42'}
      />

      {/* 4. 5-Gate Promotion Audit */}
      <HardeningGatePanel
        promoted={currentRun?.verdict === ClosedLoopVerdict.HARDENED_SUCCESSFULLY}
        activeModelBefore={currentRun?.active_model_before || 'v0.1.0'}
        activeModelAfter={currentRun?.active_model_after || 'v1.1.0-cand-42'}
      />

      {/* 5. Why Flagged Evidence Panel */}
      <WhyFlaggedPanel explanations={currentRun?.explanations} />

      {/* 6. Lineage Explorer */}
      <LineageExplorer
        runId={currentRun?.run_id || 'RUN_LOOP_5F5C6038BCEC'}
        genomeHash={currentRun?.provenance?.genome_hash || '3fcc41a4'}
        scenarioId={currentRun?.provenance?.scenario_id || 'SCEN_BEHAVIORAL_01'}
        hardeningRunId={currentRun?.provenance?.hardening_run_id || 'RUN_42_HARDENING_01'}
        candidateModelId={currentRun?.active_model_after || 'v1.1.0-cand-42'}
      />

      {/* 7. Run History Panel */}
      <RunHistoryPanel
        runs={runs}
        onSelectRun={(r) => setCurrentRun(r)}
        selectedRunId={currentRun?.run_id}
      />
    </div>
  );
};
