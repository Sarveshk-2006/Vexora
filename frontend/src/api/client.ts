import {
  OverviewSummary,
  AttackCampaign,
  SyntheticTransaction,
  DefenseGap,
  HardeningRun,
} from './types';

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_BASE = `${API_BASE_URL}/api/v1`;

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

export async function fetchJson<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;
  try {
    const res = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    });
    if (!res.ok) {
      const errText = await res.text().catch(() => res.statusText);
      throw new ApiError(res.status, errText || `HTTP ${res.status}`);
    }
    return (await res.json()) as T;
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError(0, (error as Error).message || 'Network connectivity error');
  }
}

// Deterministic Sandbox Fallback Generator for Offline Demo Mode
export const DEMO_DATA = {
  overview: {
    sandbox_status: 'ONLINE',
    environment: 'SYNTHETIC_ONLY',
    simulation_seed: 42,
    active_model_id: 'v1.1.0-cand-42',
    metrics: {
      transactions_simulated: 1000,
      users_simulated: 100,
      accounts_simulated: 100,
      attacks_generated: 15,
      transactions_flagged: 370,
      detection_rate: 0.6000,
      false_positive_rate: 0.3692,
      benign_approval_rate: 0.7353,
      unseen_attack_recall: 1.0000,
      hybrid_accuracy: 0.6250,
      hybrid_roc_auc: 0.7754,
      defense_gaps_discovered: 1,
      hardening_runs: 1,
      targeted_gap_improvement_delta: 0.6000,
    },
    responsible_ai_disclaimer:
      'Synthetic research environment — no live payment rails or real cardholder data.',
  } as OverviewSummary,

  campaigns: [
    {
      campaign_id: 'CAMP_BEHAVIORAL_MIMICRY_01',
      scenario_id: 'SCEN_G0_BEHAVIORAL_MIMICRY_UPI',
      genome: {
        objective: 'Synthetic behavioural mimicry evasion attack campaign on UPI rail',
        attack_type: 'BEHAVIORAL_MIMICRY',
        identity_state: 'NORMAL',
        device_strategy: 'DEVICE_MIMICRY',
        location_strategy: 'FAMILIAR',
        amount_pattern: 'FRAGMENTED',
        velocity_pattern: 'LOW_AND_SLOW',
        timing_pattern: 'RANDOMIZED',
        merchant_strategy: 'HOPPING',
        behavioral_similarity: 0.85,
        network_coordination: 'LOW',
        payment_rail: 'UPI',
        evasion_strategy: 'BEHAVIORAL_MIMICRY',
        novelty_rating: 0.70,
        campaign_stage: 'EXFILTRATION',
        intended_duration: '24_HOURS',
        target_population: 'HIGH_BALANCE_ACCOUNTS',
      },
      intensity: 1.0,
      seed: 42,
      affected_transaction_count: 15,
      behavioral_fidelity_score: 0.92,
    },
  ] as AttackCampaign[],

  transactions: [
    {
      id: 'TX_SYN_00000001',
      user_id: 'USER_SYN_000001',
      account_id: 'ACC_SYN_000001',
      device_id: 'DEV_SYN_000001',
      merchant_id: 'MERCH_SYN_000001',
      amount: 45000.0,
      currency: 'INR',
      payment_rail: 'UPI',
      timestamp: '2026-08-27T14:30:00Z',
      hour: 14,
      is_weekend: false,
      status: 'SUCCESS',
      risk_score: 85.5,
      decision: 'BLOCK',
      campaign_id: 'CAMP_BEHAVIORAL_MIMICRY_01',
      is_adversarial: true,
    },
    {
      id: 'TX_SYN_00000002',
      user_id: 'USER_SYN_000002',
      account_id: 'ACC_SYN_000002',
      device_id: 'DEV_SYN_000002',
      merchant_id: 'MERCH_SYN_000002',
      amount: 1250.0,
      currency: 'INR',
      payment_rail: 'UPI',
      timestamp: '2026-08-27T14:35:00Z',
      hour: 14,
      is_weekend: false,
      status: 'SUCCESS',
      risk_score: 12.0,
      decision: 'APPROVE',
      is_adversarial: false,
    },
  ] as SyntheticTransaction[],

  gaps: [
    {
      gap_id: 'GAP_EE3E17B80928',
      attack_family: 'BEHAVIORAL_MIMICRY',
      payment_rail: 'UPI',
      failed_layers: ['rules', 'graph', 'ml', 'adversarial'],
      partial_layers: ['behavioral'],
      successful_layers: [],
      hybrid_risk_score_mean: 25.65,
      final_decision_distribution: { APPROVE: 12, MONITOR: 3 },
      severity: 'CRITICAL',
      bypass_count: 15,
      total_attack_count: 15,
      bypass_rate: 1.0,
      affected_user_ids: ['USER_SYN_000001'],
      affected_transaction_ids: ['TX_SYN_00000001'],
      gap_category: 'MULTI_VECTOR_EVASION',
      mutation_dimensions: ['amount_pattern', 'timing_pattern', 'device_strategy'],
      priority_score: 96.0,
    },
  ] as DefenseGap[],

  hardeningRuns: [
    {
      run_id: 'RUN_42_HARDENING_01',
      timestamp: '2026-08-27T14:49:27.419Z',
      parent_model_id: 'v0.1.0',
      selected_gap_ids: ['GAP_EE3E17B80928'],
      adversarial_sample_count: 8,
      candidate_model_id: 'v1.1.0-cand-42',
      promotion_decision: {
        candidate_model_id: 'v1.1.0-cand-42',
        parent_model_id: 'v0.1.0',
        promoted: true,
        decision: 'PROMOTE',
        gates: {
          target_gap_improved: true,
          benign_regression_allowed: true,
          unseen_generalization_stable: true,
          calibration_stable: true,
          feature_schema_compatible: true,
        },
        metrics_before: { accuracy: 0.63, precision: 0.04, recall: 0.60, roc_auc: 0.7851 },
        metrics_after: { accuracy: 0.63, precision: 0.04, recall: 0.60, roc_auc: 0.7579 },
        rejection_reasons: [],
      },
      reproducibility_seed: 42,
    },
  ] as HardeningRun[],
};
