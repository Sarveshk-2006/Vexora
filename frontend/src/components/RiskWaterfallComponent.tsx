import React from 'react';
import { DetectorEvidenceModel, FusionEvidence } from '../api/types';

interface WaterfallProps {
  detectorEvidences: Record<string, DetectorEvidenceModel>;
  fusionEvidence: FusionEvidence;
}

export const RiskWaterfallComponent: React.FC<WaterfallProps> = ({
  detectorEvidences,
  fusionEvidence,
}) => {
  const layers = [
    { key: 'rules', title: '1. Deterministic Rules', color: 'border-[#273A91]/30 text-[#273A91]' },
    { key: 'ml', title: '2. Transaction ML', color: 'border-[#273A91]/30 text-[#273A91]' },
    { key: 'behavioral', title: '3. Behavioral Anomaly', color: 'border-[#273A91]/30 text-[#273A91]' },
    { key: 'graph', title: '4. Graph Intelligence', color: 'border-[#273A91]/30 text-[#273A91]' },
    { key: 'adversarial', title: '5. Adversarial Detector', color: 'border-[#F98513]/40 text-[#F98513]' },
  ];

  const getDecisionBadge = (dec: string) => {
    switch (dec) {
      case 'BLOCK':
        return 'bg-rose-50 text-[#DC3545] border-rose-200';
      case 'STEP_UP_AUTH':
        return 'bg-amber-50 text-[#F98513] border-amber-200';
      case 'MONITOR':
        return 'bg-yellow-50 text-yellow-700 border-yellow-200';
      default:
        return 'bg-[#E8F8F2] text-[#16A36F] border-[#16A36F]/30';
    }
  };

  return (
    <div className="space-y-6 font-sans">
      <div className="bg-white border border-[#D9DDE5] p-6 rounded-xl space-y-6 shadow-sm">
        <div className="border-b border-[#D9DDE5] pb-3 flex items-center justify-between font-mono">
          <h3 className="text-base font-bold text-[#111827] tracking-wider">
            BLUE TEAM DEFENSE LAYER RISK WATERFALL
          </h3>
          <span className="text-xs text-[#475569]">
            Composite Score: <span className="text-[#F98513] font-bold">{fusionEvidence.composite_risk_score.toFixed(1)} / 100</span>
          </span>
        </div>

        {/* Pipeline Nodes Flow */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
          {layers.map((l) => {
            const det = detectorEvidences[l.key];
            const rawScore = det ? det.normalized_score : 0.0;
            const triggered = det ? det.triggered : false;

            return (
              <div key={l.key} className={`bg-[#F8F7F4] p-4 rounded-lg border ${l.color} space-y-2 font-mono text-xs`}>
                <div className="text-[11px] font-bold text-[#111827]">{l.title}</div>
                <div className="text-lg font-bold text-[#111827]">
                  {rawScore.toFixed(1)} <span className="text-[10px] text-[#64748B]">/ 100</span>
                </div>
                <div className="flex items-center space-x-1.5">
                  {triggered ? (
                    <span className="bg-rose-50 text-[#DC3545] border border-rose-200 px-2 py-0.5 rounded text-[10px] font-bold">
                      TRIGGERED
                    </span>
                  ) : (
                    <span className="bg-white text-[#64748B] border border-[#D9DDE5] px-2 py-0.5 rounded text-[10px]">
                      NOT TRIGGERED
                    </span>
                  )}
                </div>
                <div className="text-[10px] text-[#475569] pt-1">
                  Weight: {det ? (det.contribution_weight * 100).toFixed(0) : 20}%
                </div>
              </div>
            );
          })}
        </div>

        {/* Fusion Engine & Final Decision */}
        <div className="bg-[#F8F7F4] border border-[#D9DDE5] p-5 rounded-lg flex flex-wrap items-center justify-between gap-4 font-mono">
          <div className="space-y-1">
            <div className="text-xs text-[#273A91] font-bold">RISK FUSION ENGINE</div>
            <div className="text-[#111827] text-xs">
              Reason Codes: <span className="text-[#F98513] font-bold">{fusionEvidence.reason_codes.join(', ') || 'NONE'}</span>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="text-right">
              <span className="text-[10px] text-[#475569] block">FINAL ACTION</span>
              <span className={`text-base font-bold px-4 py-1.5 rounded-lg border ${getDecisionBadge(fusionEvidence.final_decision)}`}>
                {fusionEvidence.final_decision}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
