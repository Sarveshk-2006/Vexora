import React from 'react';
import { CheckCircle2, XCircle, ShieldCheck, Award } from 'lucide-react';

interface HardeningGatePanelProps {
  promoted?: boolean;
  decision?: string;
  gates?: Record<string, boolean>;
  activeModelBefore?: string;
  activeModelAfter?: string;
}

export const HardeningGatePanel: React.FC<HardeningGatePanelProps> = ({
  promoted = true,
  gates = {
    target_gap_improved: true,
    benign_regression_allowed: true,
    unseen_generalization_stable: true,
    calibration_stable: true,
    feature_schema_compatible: true,
  },
  activeModelBefore = 'v0.1.0',
  activeModelAfter = 'v1.1.0-cand-42',
}) => {
  const gateItems = [
    {
      name: 'GATE 1: TARGETED GAP IMPROVEMENT',
      key: 'target_gap_improved',
      desc: 'Candidate recall delta >= +5.0% on targeted gap',
      passed: gates.target_gap_improved ?? true,
    },
    {
      name: 'GATE 2: BENIGN NON-REGRESSION',
      key: 'benign_regression_allowed',
      desc: 'Benign approval rate regression < 0.5%',
      passed: gates.benign_regression_allowed ?? true,
    },
    {
      name: 'GATE 3: UNSEEN ATTACK STABILITY',
      key: 'unseen_generalization_stable',
      desc: 'Zero recall degradation on held-out attack family',
      passed: gates.unseen_generalization_stable ?? true,
    },
    {
      name: 'GATE 4: CALIBRATION STABILITY',
      key: 'calibration_stable',
      desc: 'Brier score degradation < 0.05',
      passed: gates.calibration_stable ?? true,
    },
    {
      name: 'GATE 5: FEATURE SCHEMA MATCH',
      key: 'feature_schema_compatible',
      desc: 'Exact match with 25 Blue Team feature schema',
      passed: gates.feature_schema_compatible ?? true,
    },
  ];

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-2xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200 tracking-wide uppercase font-mono flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            Autonomous Hardening Promotion Gate Audit (ADR-006)
          </h3>
          <p className="text-xs text-slate-400">
            Strict 5-gate audit evaluation determining candidate model promotion or rejection
          </p>
        </div>

        <div className="flex items-center gap-2">
          {promoted ? (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded bg-emerald-950/90 text-emerald-300 border border-emerald-700 text-xs font-mono font-bold shadow-lg shadow-emerald-950/40">
              <Award className="w-4 h-4" /> DECISION: PROMOTE
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded bg-rose-950/90 text-rose-300 border border-rose-700 text-xs font-mono font-bold">
              <XCircle className="w-4 h-4" /> DECISION: REJECT
            </span>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-3 mb-4">
        {gateItems.map((g) => (
          <div
            key={g.key}
            className={`p-3 rounded-lg border flex flex-col justify-between ${
              g.passed
                ? 'bg-slate-950 border-slate-800'
                : 'bg-rose-950/30 border-rose-900/80'
            }`}
          >
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="text-[10px] font-mono text-slate-500 font-semibold truncate">
                  {g.name.split(':')[0]}
                </span>
                {g.passed ? (
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                ) : (
                  <XCircle className="w-3.5 h-3.5 text-rose-400" />
                )}
              </div>
              <div className="text-xs font-bold font-mono text-slate-200 mt-1 truncate">
                {g.name.split(':')[1]}
              </div>
              <div className="text-[10px] text-slate-500 mt-1 leading-tight">
                {g.desc}
              </div>
            </div>

            <div className="mt-3 pt-2 border-t border-slate-800/60">
              {g.passed ? (
                <span className="text-[10px] font-mono text-emerald-400 font-bold">
                  PASS
                </span>
              ) : (
                <span className="text-[10px] font-mono text-rose-400 font-bold">
                  FAIL
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between text-xs font-mono">
        <span className="text-slate-400">
          PROMOTED CANDIDATE ID: <strong className="text-emerald-400">{activeModelAfter}</strong>
        </span>
        <span className="text-slate-500">
          PREVIOUS ACTIVE: {activeModelBefore}
        </span>
      </div>
    </div>
  );
};
