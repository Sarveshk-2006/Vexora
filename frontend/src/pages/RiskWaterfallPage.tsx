import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { BarChart3 } from 'lucide-react';
import { explainTransaction } from '../api/explainability';
import { ExplanationResult } from '../api/types';
import { RiskWaterfallComponent } from '../components/RiskWaterfallComponent';

export const RiskWaterfallPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const txQuery = searchParams.get('tx') || 'TX_SYN_00000001';

  const [exp, setExp] = useState<ExplanationResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    explainTransaction(txQuery).then((res) => {
      setExp(res);
      setLoading(false);
    });
  }, [txQuery]);

  if (loading || !exp) {
    return (
      <div className="p-8 text-center text-slate-400 font-mono text-sm">
        Loading Blue Team Risk Decision Waterfall...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center space-x-2">
            <BarChart3 className="w-5 h-5 text-emerald-400" />
            <span>Blue Team Risk Decision Waterfall</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1 font-mono">
            Layered Risk Score Evaluation & Composite Decision Pipeline for {txQuery}
          </p>
        </div>
      </div>

      <RiskWaterfallComponent
        detectorEvidences={exp.detector_evidences}
        fusionEvidence={exp.fusion_evidence}
      />
    </div>
  );
};
