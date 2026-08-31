import React from 'react';
import { FileText, ShieldAlert, Info } from 'lucide-react';

interface WhyFlaggedPanelProps {
  explanations?: any[];
}

export const WhyFlaggedPanel: React.FC<WhyFlaggedPanelProps> = ({
  explanations = [],
}) => {
  const sampleExplanation = explanations[0] || {
    explanation_id: 'EXP_ADV_42',
    transaction_id: 'TX_ADV_001',
    primary_decision: 'BLOCK',
    composite_risk_score: 87.5,
    evidence_items: [
      {
        evidence_type: 'ATTACK',
        detector_name: 'RedTeamMutationEngine',
        strength_score: 0.95,
        normalized_strength: 0.95,
        attribution_available: true,
        explanation:
          'Transaction originated from Red Team behavioral mimicry campaign.',
      },
      {
        evidence_type: 'RULE',
        detector_name: 'HighAmountFragmentedRule',
        strength_score: 0.85,
        normalized_strength: 0.85,
        attribution_available: true,
        explanation: 'Fragmented transfer pattern matched known evasion vector.',
      },
      {
        evidence_type: 'FEATURE',
        detector_name: 'TransactionMLDetector',
        strength_score: 0.65,
        normalized_strength: 0.65,
        attribution_available: false,
        invalidity_reason:
          'Per-sample SHAP attribution unavailable for RandomForestClassifier.',
        explanation: 'RandomForestClassifier composite probability 0.65.',
      },
    ],
  };

  const evidenceItems =
    sampleExplanation?.evidence_items ||
    sampleExplanation?.why_flagged_ranking ||
    [];

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-5 shadow-2xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-sm font-semibold text-slate-200 tracking-wide uppercase font-mono flex items-center gap-2">
            <FileText className="w-4 h-4 text-emerald-400" />
            "WHY WAS THIS TRANSACTION FLAGGED?" Structured Evidence Panel
          </h3>
          <p className="text-xs text-slate-400">
            Phase 7A Explainability Engine evidence extraction & deterministic strength ranking
          </p>
        </div>
        <span className="text-xs font-mono px-3 py-1 rounded bg-slate-950 text-slate-300 border border-slate-800 font-bold">
          {sampleExplanation.primary_decision}: {(sampleExplanation.composite_risk_score || 0).toFixed(1)} RISK SCORE
        </span>
      </div>

      <div className="space-y-3">
        {evidenceItems.map((item: any, idx: number) => (
          <div
            key={idx}
            className="p-3.5 rounded-lg bg-slate-950 border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-3"
          >
            <div className="flex items-start gap-3">
              <div className="p-2 rounded bg-slate-900 border border-slate-800 text-emerald-400 mt-0.5">
                <ShieldAlert className="w-4 h-4" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-slate-200 uppercase">
                    {item.evidence_type} EVIDENCE
                  </span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800">
                    {item.detector_name}
                  </span>
                </div>
                <p className="text-xs text-slate-300 font-mono mt-1">
                  {item.explanation}
                </p>
                {!item.attribution_available && (
                  <div className="mt-1 flex items-center gap-1 text-[10px] font-mono text-amber-400">
                    <Info className="w-3 h-3" />
                    <span>Per-sample attribution unavailable: {item.invalidity_reason}</span>
                  </div>
                )}
              </div>
            </div>

            <div className="text-right font-mono">
              <span className="text-sm font-bold text-emerald-400">
                {(item.normalized_strength * 100).toFixed(0)}% STRENGTH
              </span>
              <span className="text-[10px] text-slate-500 block">
                DETERMINISTIC RANKING
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
