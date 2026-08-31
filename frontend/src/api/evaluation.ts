import { fetchJson, DEMO_DATA } from './client';

export interface EvaluationBenchmarkReport {
  timestamp: string;
  hybrid_metrics: Record<string, number>;
  unseen_attack_metrics: Record<string, number>;
  active_model_version: string;
}

export async function getEvaluationBenchmark(): Promise<EvaluationBenchmarkReport> {
  try {
    return await fetchJson<EvaluationBenchmarkReport>('/evaluation/benchmark');
  } catch (err) {
    console.warn('[VEXORA Sandbox API] Using fallback EvaluationBenchmarkReport demo data');
    return {
      timestamp: new Date().toISOString(),
      hybrid_metrics: {
        accuracy: DEMO_DATA.overview.metrics.hybrid_accuracy,
        roc_auc: DEMO_DATA.overview.metrics.hybrid_roc_auc,
        false_positive_rate: DEMO_DATA.overview.metrics.false_positive_rate,
        benign_approval_rate: DEMO_DATA.overview.metrics.benign_approval_rate,
      },
      unseen_attack_metrics: {
        recall: DEMO_DATA.overview.metrics.unseen_attack_recall,
      },
      active_model_version: DEMO_DATA.overview.active_model_id,
    };
  }
}
