import React, { useEffect, useState } from 'react';
import {
  fetchHealthStatus,
  runClosedLoopSimulation,
  listClosedLoopRuns,
} from '../services/api';
import {
  ClosedLoopRunResult,
  ClosedLoopVerdict,
  StageStatus,
} from '../types/orchestration';

import { ClosedLoopPipeline } from '../components/pipeline/ClosedLoopPipeline';
import { RunControlPanel } from '../components/pipeline/RunControlPanel';
import { ReAttackVisualization } from '../components/pipeline/ReAttackVisualization';
import { RunHistoryPanel } from '../components/pipeline/RunHistoryPanel';
import { MetricCards } from '../components/metrics/MetricCards';
import { AttackGenomePanel } from '../components/attack/AttackGenomePanel';
import { DefenseGapPanel } from '../components/defense/DefenseGapPanel';
import { HardeningGatePanel } from '../components/hardening/HardeningGatePanel';
import { WhyFlaggedPanel } from '../components/explainability/WhyFlaggedPanel';
import { CounterfactualPanel } from '../components/explainability/CounterfactualPanel';
import { LineageExplorer } from '../components/pipeline/LineageExplorer';

import { Shield, Activity, AlertTriangle } from 'lucide-react';

export const CommandCenterPage: React.FC = () => {
  const [healthStatus, setHealthStatus] = useState<string>('CHECKING');
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [runs, setRuns] = useState<ClosedLoopRunResult[]>([]);
  const [currentRun, setCurrentRun] = useState<ClosedLoopRunResult | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    // 1. Health check
    fetchHealthStatus()
      .then(() => setHealthStatus('ONLINE'))
      .catch(() => setHealthStatus('OFFLINE'));

    // 2. Fetch runs
    listClosedLoopRuns()
      .then((data) => {
        setRuns(data);
        if (data.length > 0) {
          setCurrentRun(data[data.length - 1]);
        }
      })
      .catch(() => setRuns([]));
  }, []);

  const handleRunSimulation = async (seed: number = 42) => {
    setIsRunning(true);
    setErrorMsg(null);

    try {
      const res = await runClosedLoopSimulation({ seed });
      setCurrentRun(res);
      const updatedRuns = await listClosedLoopRuns();
      setRuns(updatedRuns);
    } catch (err: any) {
      setErrorMsg(err.message || 'Simulation failed to execute.');
    } finally {
      setIsRunning(false);
    }
  };

  // Mock / default metrics if no run completed yet
  const defaultMetrics = {
    precision_before: 0.04,
    precision_after: 0.04,
    recall_before: 0.6,
    recall_after: 0.6,
    f1_before: 0.075,
    f1_after: 0.075,
    roc_auc_before: 0.7851,
    roc_auc_after: 0.7579,
    false_positive_rate_before: 0.3692,
    false_positive_rate_after: 0.3692,
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
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6 font-sans">
      {/* Top Banner / System Status Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-4 rounded-xl bg-slate-900 border border-slate-800 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-emerald-950/80 border border-emerald-800 text-emerald-400">
            <Shield className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-lg font-bold font-mono tracking-wider text-slate-100 flex items-center gap-2">
              FRAUDOSCOPE COMMAND CENTER
              <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 font-mono">
                SYNTHETIC RESEARCH SANDBOX
              </span>
            </h1>
            <p className="text-xs text-slate-400">
              Autonomous Synthetic Payment-Security Research & Defense Hardening Engine
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 text-xs font-mono">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded bg-slate-950 border border-slate-800">
            <Activity className="w-3.5 h-3.5 text-emerald-400" />
            <span className="text-slate-400">BACKEND:</span>
            <span
              className={`font-bold ${
                healthStatus === 'ONLINE'
                  ? 'text-emerald-400'
                  : 'text-rose-400'
              }`}
            >
              {healthStatus}
            </span>
          </div>

          <div className="px-3 py-1.5 rounded bg-slate-950 border border-slate-800 text-slate-300">
            ACTIVE MODEL: <span className="text-emerald-400 font-bold">{currentRun?.active_model_after || 'v1.1.0-cand-42'}</span>
          </div>
        </div>
      </div>

      {healthStatus === 'OFFLINE' && (
        <div className="p-4 rounded-xl bg-rose-950/50 border border-rose-800 text-rose-300 text-xs font-mono flex items-center justify-between">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-rose-400" />
            <span>
              BACKEND SERVICE OFFLINE. Ensure FastAPI server is running on http://localhost:8000.
            </span>
          </div>
          <button
            onClick={() =>
              fetchHealthStatus()
                .then(() => setHealthStatus('ONLINE'))
                .catch(() => setHealthStatus('OFFLINE'))
            }
            className="px-3 py-1 bg-rose-900 hover:bg-rose-800 text-slate-100 rounded text-xs"
          >
            RETRY
          </button>
        </div>
      )}

      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-800 text-rose-300 text-xs font-mono">
          ERROR: {errorMsg}
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

      {/* 4. Metric Cards */}
      <MetricCards metrics={activeMetrics} />

      {/* 5. Two Column Section: Attack DNA & Defense Gap */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AttackGenomePanel genome={currentRun?.summary?.genome} />
        <DefenseGapPanel />
      </div>

      {/* 6. 5-Gate Promotion Audit */}
      <HardeningGatePanel
        promoted={currentRun?.verdict === ClosedLoopVerdict.HARDENED_SUCCESSFULLY}
        activeModelBefore={currentRun?.active_model_before || 'v0.1.0'}
        activeModelAfter={currentRun?.active_model_after || 'v1.1.0-cand-42'}
      />

      {/* 7. Why Flagged & Counterfactuals */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <WhyFlaggedPanel explanations={currentRun?.explanations} />
        <CounterfactualPanel />
      </div>

      {/* 8. Lineage Explorer */}
      <LineageExplorer
        runId={currentRun?.run_id || 'RUN_LOOP_5F5C6038BCEC'}
        genomeHash={currentRun?.provenance?.genome_hash || '3fcc41a4'}
        scenarioId={currentRun?.provenance?.scenario_id || 'SCEN_BEHAVIORAL_01'}
        hardeningRunId={currentRun?.provenance?.hardening_run_id || 'RUN_42_HARDENING_01'}
        candidateModelId={currentRun?.active_model_after || 'v1.1.0-cand-42'}
      />

      {/* 9. Run History Panel */}
      <RunHistoryPanel
        runs={runs}
        onSelectRun={(r) => setCurrentRun(r)}
        selectedRunId={currentRun?.run_id}
      />
    </div>
  );
};
