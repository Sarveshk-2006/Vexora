export enum PipelineStage {
  SCENARIO_PREPARATION = 'SCENARIO_PREPARATION',
  RED_TEAM = 'RED_TEAM',
  BLUE_TEAM = 'BLUE_TEAM',
  GAP_ANALYSIS = 'GAP_ANALYSIS',
  HARDENING = 'HARDENING',
  EXPLAINABILITY = 'EXPLAINABILITY',
  RE_ATTACK_VALIDATION = 'RE_ATTACK_VALIDATION',
  VERDICT = 'VERDICT',
}

export enum StageStatus {
  NOT_STARTED = 'NOT_STARTED',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED',
  SKIPPED = 'SKIPPED',
}

export enum ClosedLoopVerdict {
  HARDENED_SUCCESSFULLY = 'HARDENED_SUCCESSFULLY',
  HARDENING_REJECTED = 'HARDENING_REJECTED',
  NO_GAP_FOUND = 'NO_GAP_FOUND',
  HARDENING_FAILED = 'HARDENING_FAILED',
  VALIDATION_FAILED = 'VALIDATION_FAILED',
  PIPELINE_FAILED = 'PIPELINE_FAILED',
}

export interface ClosedLoopStageResult {
  stage: PipelineStage;
  status: StageStatus;
  started_at?: string;
  completed_at?: string;
  duration_ms: number;
  input_identifiers: Record<string, any>;
  output_identifiers: Record<string, any>;
  error_message?: string;
  detail: Record<string, any>;
}

export interface ClosedLoopMetrics {
  precision_before: number;
  precision_after: number;
  recall_before: number;
  recall_after: number;
  f1_before: number;
  f1_after: number;
  roc_auc_before: number;
  roc_auc_after: number;
  false_positive_rate_before: number;
  false_positive_rate_after: number;
  targeted_gap_recall_before: number;
  targeted_gap_recall_after: number;
  unseen_attack_recall_before: number;
  unseen_attack_recall_after: number;
  benign_approval_rate_before: number;
  benign_approval_rate_after: number;
  recall_delta: number;
  targeted_gap_recall_delta: number;
}

export interface ClosedLoopRunRequest {
  seed?: number;
  genome_id?: string;
  genome_payload?: Record<string, any>;
  max_iterations?: number;
  include_counterfactuals?: boolean;
}

export interface ClosedLoopProvenance {
  run_id: string;
  random_seed: number;
  genome_hash: string;
  pipeline_version: string;
  active_model_before: string;
  active_model_after: string;
  scenario_id?: string;
  hardening_run_id?: string;
  candidate_model_id?: string;
  dataset_hash?: string;
  model_hash?: string;
  created_at: string;
}

export interface ClosedLoopRunResult {
  run_id: string;
  provenance: ClosedLoopProvenance;
  verdict: ClosedLoopVerdict;
  pipeline_state: StageStatus;
  stage_results: ClosedLoopStageResult[];
  metrics: ClosedLoopMetrics;
  active_model_before: string;
  active_model_after: string;
  explanations: any[];
  summary: Record<string, any>;
}
