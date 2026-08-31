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
    { key: 'rules', title: '1. Deterministic Rules', color: 'border-blue-500/40 text-blue-400' },
    { key: 'ml', title: '2. Transaction ML', color: 'border-emerald-500/40 text-emerald-400' },
    { key: 'behavioral', title: '3. Behavioral Anomaly', color: 'border-purple-500/40 text-purple-400' },
    { key: 'graph', title: '4. Graph Intelligence', color: 'border-cyan-500/40 text-cyan-400' },
    { key: 'adversarial', title: '5. Adversarial Detector', color: 'border-amber-500/40 text-amber-400' },
  ];

  const getDecisionBadge = (dec: string) => {
    switch (dec) {
      case 'BLOCK':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      case 'STEP_UP_AUTH':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'MONITOR':
        return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30';
      default:
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg space-y-6">
        <div className="border-b border-slate-800 pb-3 flex items-center justify-between">
          <h3 className="text-base font-bold text-white font-mono tracking-wider">
            BLUE TEAM DEFENSE LAYER RISK WATERFALL
          </h3>
          <span className="text-xs font-mono text-slate-400">
            Composite Score: <span className="text-rose-400 font-bold">{fusionEvidence.composite_risk_score.toFixed(1)} / 100</span>
          </span>
        </div>

        {/* Pipeline Nodes Flow */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
          {layers.map((l) => {
            const det = detectorEvidences[l.key];
            const rawScore = det ? det.normalized_score : 0.0;
            const triggered = det ? det.triggered : false;

            return (
              <div key={l.key} className={`bg-slate-950 p-4 rounded-lg border ${l.color} space-y-2 font-mono text-xs`}>
                <div className="text-[11px] font-bold text-slate-300">{l.title}</div>
                <div className="text-lg font-bold text-white">
                  {rawScore.toFixed(1)} <span className="text-[10px] text-slate-500">/ 100</span>
                </div>
                <div className="flex items-center space-x-1.5">
                  {triggered ? (
                    <span className="bg-rose-500/10 text-rose-400 border border-rose-500/30 px-2 py-0.5 rounded text-[10px] font-bold">
                      TRIGGERED
                    </span>
                  ) : (
                    <span className="bg-slate-800 text-slate-400 px-2 py-0.5 rounded text-[10px]">
                      NOT TRIGGERED
                    </span>
                  )}
                </div>
                <div className="text-[10px] text-slate-500 pt-1">
                  Weight: {det ? (det.contribution_weight * 100).toFixed(0) : 20}%
                </div>
              </div>
            );
          })}
        </div>

        {/* Fusion Engine & Final Decision */}
        <div className="bg-slate-950 border border-slate-800 p-5 rounded-lg flex flex-wrap items-center justify-between gap-4 font-mono">
          <div className="space-y-1">
            <div className="text-xs text-slate-400 font-bold">RISK FUSION ENGINE</div>
            <div className="text-slate-300 text-xs">
              Reason Codes: <span className="text-amber-400">{fusionEvidence.reason_codes.join(', ') || 'NONE'}</span>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="text-right">
              <span className="text-[10px] text-slate-500 block">FINAL ACTION</span>
              <span className={`text-base font-bold px-4 py-1.5 rounded border ${getDecisionBadge(fusionEvidence.final_decision)}`}>
                {fusionEvidence.final_decision}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
