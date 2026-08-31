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
    <div className="bg-white border border-[#D9DDE5] rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base font-bold text-[#111827] tracking-wide font-mono flex items-center gap-2">
            <FileText className="w-4 h-4 text-[#273A91]" />
            Why Was This Transaction Flagged?
          </h3>
          <p className="text-xs text-[#475569] font-sans">
            Evidence ranking and detector signal attribution
          </p>
        </div>
        <span className="text-xs font-mono px-3 py-1 rounded-lg bg-[#F8F7F4] text-[#F98513] border border-[#D9DDE5] font-bold">
          {sampleExplanation.primary_decision}: {(sampleExplanation.composite_risk_score || 0).toFixed(1)} RISK SCORE
        </span>
      </div>

      <div className="space-y-3">
        {evidenceItems.map((item: any, idx: number) => (
          <div
            key={idx}
            className="p-3.5 rounded-lg bg-[#F8F7F4] border border-[#D9DDE5] flex flex-col md:flex-row md:items-center justify-between gap-3"
          >
            <div className="flex items-start gap-3">
              <div className="p-2 rounded bg-white border border-[#D9DDE5] text-[#F98513] mt-0.5">
                <ShieldAlert className="w-4 h-4" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-[#111827] uppercase">
                    {item.evidence_type} EVIDENCE
                  </span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white text-[#273A91] border border-[#D9DDE5]">
                    {item.detector_name}
                  </span>
                </div>
                <p className="text-xs text-[#111827] font-mono mt-1">
                  {item.explanation}
                </p>
                {!item.attribution_available && (
                  <div className="mt-1 flex items-center gap-1 text-[10px] font-mono text-[#F98513]">
                    <Info className="w-3 h-3" />
                    <span>Attribution unavailable for this model: {item.invalidity_reason}</span>
                  </div>
                )}
              </div>
            </div>

            <div className="text-right font-mono">
              <span className="text-sm font-bold text-[#273A91]">
                {(item.normalized_strength * 100).toFixed(0)}% STRENGTH
              </span>
              <span className="text-[10px] text-[#475569] block font-sans">
                RANKING SCORE
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
