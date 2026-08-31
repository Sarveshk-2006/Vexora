export interface OverviewSummary {
  sandbox_status: string;
  environment: string;
  simulation_seed: number;
  active_model_id: string;
  metrics: {
    transactions_simulated: number;
    users_simulated: number;
    accounts_simulated: number;
    attacks_generated: number;
    transactions_flagged: number;
    detection_rate: number;
    false_positive_rate: number;
    benign_approval_rate: number;
    unseen_attack_recall: number;
    hybrid_accuracy: number;
    hybrid_roc_auc: number;
    defense_gaps_discovered: number;
    hardening_runs: number;
    targeted_gap_improvement_delta: number;
  };
  responsible_ai_disclaimer: string;
}

export interface FraudGenome {
  objective: string;
  attack_type: string;
  identity_state: string;
  device_strategy: string;
  location_strategy: string;
  amount_pattern: string;
  velocity_pattern: string;
  timing_pattern: string;
  merchant_strategy: string;
  behavioral_similarity: number;
  network_coordination: string;
  payment_rail: string;
  evasion_strategy: string;
  novelty_rating: number;
  campaign_stage: string;
  intended_duration: string;
  target_population: string;
}

export interface AttackCampaign {
  campaign_id: string;
  scenario_id: string;
  genome: FraudGenome;
  intensity: number;
  seed: number;
  affected_transaction_count: number;
  behavioral_fidelity_score: number;
}

export interface SyntheticTransaction {
  id: string;
  user_id: string;
  account_id: string;
  device_id: string;
  merchant_id: string;
  amount: number;
  currency: string;
  payment_rail: string;
  timestamp: string;
  hour: number;
  is_weekend: boolean;
  status: string;
  risk_score?: number;
  decision?: 'APPROVE' | 'MONITOR' | 'STEP_UP_AUTH' | 'BLOCK';
  campaign_id?: string;
  is_adversarial?: boolean;
}

export interface RuleEvidence {
  rule_id: string;
  rule_name: string;
  triggered: boolean;
  observed_value: unknown;
  threshold_value: unknown;
  severity: string;
  source_transaction_id: string;
}

export interface FeatureEvidence {
  feature_name: string;
  feature_value: number;
  contribution: number | null;
  direction: string | null;
  model_version: string;
  transaction_id: string;
  attribution_available: boolean;
  unavailability_reason: string | null;
}

export interface AnomalyEvidence {
  anomaly_score: number;
  anomaly_threshold: number;
  triggered: boolean;
  baseline_reference: string;
  transaction_id: string;
}

export interface GraphEvidence {
  graph_risk_score: number;
  triggered: boolean;
  node_identifiers: Record<string, string>;
  connected_component_size: number;
  suspicious_network_indicators: string[];
  transaction_id: string;
}

export interface AttackEvidence {
  genome_id: string;
  genome_version: string;
  attack_family: string;
  payment_rail: string;
  mutation_parameters: Record<string, unknown>;
  parent_genome_id: string | null;
  campaign_id: string;
  affected_transaction_id: string;
  behavioral_fidelity_score: number;
}

export interface DetectorEvidenceModel {
  detector_name: string;
  detector_version: string;
  raw_score: number;
  normalized_score: number;
  triggered: boolean;
  confidence: number;
  contribution_weight: number;
  decision_relevance: string;
}

export interface FusionEvidence {
  composite_risk_score: number;
  final_decision: string;
  layer_scores: Record<string, number>;
  layer_weights: Record<string, number>;
  reason_codes: string[];
}

export interface BypassEvidence {
  genome_id: string;
  affected_transaction_id: string;
  layer_bypass_status: Record<string, string>;
  gap_category: string;
  priority_score: number;
}

export interface HardeningEvidence {
  active_model_version: string;
  candidate_model_version: string;
  metrics_before: Record<string, unknown>;
  metrics_after: Record<string, unknown>;
  metric_deltas: Record<string, number>;
  promotion_decision: string;
  gate_results: Record<string, boolean>;
}

export interface CounterfactualEvidence {
  feature_name: string;
  original_value: number;
  proposed_value: number;
  detector_output_before: number;
  detector_output_after: number;
  decision_before: string;
  decision_after: string;
  validity_status: boolean;
  invalidity_reason: string | null;
}

export interface EvidenceItem {
  evidence_id: string;
  category: 'RULE' | 'FEATURE' | 'ANOMALY' | 'GRAPH' | 'ADVERSARIAL' | 'FUSION' | 'BYPASS' | 'HARDENING' | 'COUNTERFACTUAL';
  source_subsystem: string;
  summary: string;
  detail: Record<string, unknown>;
  normalized_strength: number;
  relevance_explanation: string;
}

export interface ExplanationProvenance {
  explanation_id: string;
  transaction_id?: string;
  campaign_id?: string;
  genome_id?: string;
  model_version: string;
  dataset_reference: string;
  random_seed: number;
  generated_at: string;
  source_subsystem: string;
  source_artifacts: string[];
}

export interface ExplanationResult {
  explanation_id: string;
  provenance: ExplanationProvenance;
  primary_decision: 'APPROVE' | 'MONITOR' | 'STEP_UP_AUTH' | 'BLOCK';
  composite_risk_score: number;
  why_flagged_ranking: EvidenceItem[];
  detector_evidences: Record<string, DetectorEvidenceModel>;
  fusion_evidence: FusionEvidence;
  rule_evidences: RuleEvidence[];
  feature_evidences: FeatureEvidence[];
  anomaly_evidence?: AnomalyEvidence;
  graph_evidence?: GraphEvidence;
  attack_evidence?: AttackEvidence;
  bypass_evidence?: BypassEvidence;
  hardening_evidence?: HardeningEvidence;
  counterfactual_evidences: CounterfactualEvidence[];
}

export interface DefenseGap {
  gap_id: string;
  attack_family: string;
  payment_rail: string;
  failed_layers: string[];
  partial_layers: string[];
  successful_layers: string[];
  hybrid_risk_score_mean: number;
  final_decision_distribution: Record<string, number>;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  bypass_count: number;
  total_attack_count: number;
  bypass_rate: number;
  affected_user_ids: string[];
  affected_transaction_ids: string[];
  gap_category: string;
  mutation_dimensions: string[];
  priority_score: number;
}

export interface HardeningRun {
  run_id: string;
  timestamp: string;
  parent_model_id: string;
  selected_gap_ids: string[];
  adversarial_sample_count: number;
  candidate_model_id: string;
  promotion_decision: {
    candidate_model_id: string;
    parent_model_id: string;
    promoted: boolean;
    decision: 'PROMOTE' | 'REJECT';
    gates: {
      target_gap_improved: boolean;
      benign_regression_allowed: boolean;
      unseen_generalization_stable: boolean;
      calibration_stable: boolean;
      feature_schema_compatible: boolean;
    };
    metrics_before: Record<string, unknown>;
    metrics_after: Record<string, unknown>;
    rejection_reasons: string[];
  };
  reproducibility_seed: number;
}
