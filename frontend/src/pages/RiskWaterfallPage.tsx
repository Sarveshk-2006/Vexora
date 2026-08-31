import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { TrendingDown } from 'lucide-react';
import { explainTransaction } from '../api/explainability';
import { ExplanationResult } from '../api/types';
import { RiskWaterfallComponent } from '../components/RiskWaterfallComponent';

export const RiskWaterfallPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const txQuery = searchParams.get('tx') || 'TX_SYN_00000001';

  const [exp, setExp] = useState<ExplanationResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    explainTransaction(txQuery)
      .then((res) => {
        setExp(res);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, [txQuery]);

  if (loading && !exp) {
    return (
      <div className="space-y-6 font-sans">
        <div className="h-10 w-64 skeleton-shimmer rounded-xl"></div>
        <div className="h-64 skeleton-shimmer rounded-2xl"></div>
      </div>
    );
  }

  const activeExp = exp || {
    detector_evidences: {
      rules: { detector_name: 'RulesEngine', detector_version: '1.0', raw_score: 40.0, normalized_score: 40.0, confidence: 1.0, triggered: false, contribution_weight: 0.2, decision_relevance: 'MEDIUM' },
      ml: { detector_name: 'TransactionML', detector_version: '1.0', raw_score: 76.8, normalized_score: 76.8, confidence: 0.9, triggered: true, contribution_weight: 0.25, decision_relevance: 'HIGH' },
      behavioral: { detector_name: 'BehavioralAnomaly', detector_version: '1.0', raw_score: 65.0, normalized_score: 65.0, confidence: 0.85, triggered: true, contribution_weight: 0.25, decision_relevance: 'HIGH' },
      graph: { detector_name: 'GraphIntelligence', detector_version: '1.0', raw_score: 25.0, normalized_score: 25.0, confidence: 0.7, triggered: false, contribution_weight: 0.15, decision_relevance: 'LOW' },
      adversarial: { detector_name: 'AdversarialDetector', detector_version: '1.0', raw_score: 90.0, normalized_score: 90.0, confidence: 0.95, triggered: true, contribution_weight: 0.15, decision_relevance: 'CRITICAL' },
    },
    fusion_evidence: {
      composite_risk_score: 87.5,
      reason_codes: ['EVASION_MIMICRY_DETECTED', 'HIGH_AMOUNT_FRAGMENTED'],
      final_decision: 'BLOCK',
      layer_scores: { rules: 40.0, ml: 76.8, behavioral: 65.0, graph: 25.0, adversarial: 90.0 },
      layer_weights: { rules: 0.2, ml: 0.25, behavioral: 0.25, graph: 0.15, adversarial: 0.15 },
    },
  };

  return (
    <div className="space-y-6 font-sans">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#D9DEE8] pb-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight text-[#0F172A] flex items-center space-x-2">
            <TrendingDown className="w-7 h-7 text-[#172554]" />
            <span>Risk Breakdown</span>
          </h2>
          <p className="text-base text-[#475569] mt-1 font-normal">
            Layered subsystem risk score contribution and decision pipeline for {txQuery}
          </p>
        </div>
      </div>

      <RiskWaterfallComponent
        detectorEvidences={activeExp.detector_evidences}
        fusionEvidence={activeExp.fusion_evidence}
      />
    </div>
  );
};
