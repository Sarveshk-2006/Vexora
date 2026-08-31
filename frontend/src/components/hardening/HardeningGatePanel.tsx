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
    <div className="bg-white border border-[#D9DDE5] rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-[#111827] tracking-wide font-mono flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-[#16A36F]" />
            Hardening Promotion Gate Audit
          </h3>
          <p className="text-xs text-[#475569] font-sans">
            Automated verification determining model candidate promotion or rejection
          </p>
        </div>

        <div className="flex items-center gap-2">
          {promoted ? (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-[#E8F8F2] text-[#16A36F] border border-[#16A36F]/30 text-xs font-mono font-bold shadow-sm">
              <Award className="w-4 h-4" /> DECISION: PROMOTE
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-rose-50 text-[#DC3545] border border-rose-200 text-xs font-mono font-bold">
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
                ? 'bg-[#F8F7F4] border-[#D9DDE5]'
                : 'bg-rose-50 border-rose-200'
            }`}
          >
            <div>
              <div className="flex items-center justify-between mb-1">
                <span className="text-[10px] font-mono text-[#475569] font-semibold truncate">
                  {g.name.split(':')[0]}
                </span>
                {g.passed ? (
                  <CheckCircle2 className="w-3.5 h-3.5 text-[#16A36F]" />
                ) : (
                  <XCircle className="w-3.5 h-3.5 text-[#DC3545]" />
                )}
              </div>
              <div className="text-xs font-bold font-mono text-[#111827] mt-1 truncate">
                {g.name.split(':')[1]}
              </div>
              <div className="text-[10px] text-[#475569] mt-1 leading-tight font-sans">
                {g.desc}
              </div>
            </div>

            <div className="mt-3 pt-2 border-t border-[#D9DDE5]">
              {g.passed ? (
                <span className="text-[10px] font-mono text-[#16A36F] font-bold">
                  PASS
                </span>
              ) : (
                <span className="text-[10px] font-mono text-[#DC3545] font-bold">
                  FAIL
                </span>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="p-3 rounded-lg bg-[#F8F7F4] border border-[#D9DDE5] flex items-center justify-between text-xs font-mono">
        <span className="text-[#475569]">
          PROMOTED MODEL: <strong className="text-[#16A36F]">{activeModelAfter}</strong>
        </span>
        <span className="text-[#475569]">
          BASELINE MODEL: {activeModelBefore}
        </span>
      </div>
    </div>
  );
};
