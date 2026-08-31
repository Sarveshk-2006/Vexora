# FRAUDOSCOPE — Phase Walkthrough Documentation

> **Current Phase:** Phase 4 — Red Team Attack Synthesis Engine  
> **Status:** Fully Implemented & Verified

---

## Phase 2A: Domain Foundation Walkthrough

### 1. Entity Purpose & Domain Concepts
Phase 2A establishes the foundational database ORM models and Pydantic v2 schemas for the payment digital twin's core actors:

- **`User` (`users` table):** Synthetic account holder profile capturing behavioral baseline metadata (country, region, city, timezone, account age, risk tier). Zero real PII stored.
- **`Account` (`accounts` table):** Synthetic financial ledger account associated with a parent `User`. Models balance history baselines, account age, type (Consumer vs. Business), and operational status.
- **`Device` (`devices` table):** Synthetic device fingerprint entity capturing form factor (`DeviceType`), operating system, first/last seen timestamps, and normalized trust/reputation metrics (`[0.0, 1.0]`).
- **`Merchant` (`merchants` table):** Synthetic merchant profile representing payment destinations with standard Merchant Category Codes (MCC) and regional risk classifications.

---

## Phase 2B: Payment Activity Domain Walkthrough

### 1. Entity Purpose & Domain Concepts
Phase 2B implements the synthetic payment activity event stream entities required for digital twin simulations:

- **`Session` (`sessions` table):** Models synthetic user interaction sessions linked to a specific `User`, `Account`, and `Device`. Captures session type (`LOGIN`, `PAYMENT`, `BROWSING`, `MIXED`), timezone-aware timestamps, location metadata, synthetic IP addresses (`192.0.2.x`), and user-agent families.
- **`PaymentAgent` (`payment_agents` table):** Represents synthetic autonomous AI payment actors operating on behalf of a parent `User` (`PERSONAL_ASSISTANT`, `SHOPPING_AGENT`, `BILLING_AGENT`, `SUBSCRIPTION_AGENT`).
- **`Transaction` (`transactions` table):** The central synthetic payment event stream entity. References `Account`, `User`, `Merchant`, `Device`, `Session` (optional), `PaymentRail` (`UPI`, `CARD`, `WALLET`), and `PaymentAgent` (optional). Features exact financial decimal precision (`Numeric(15, 2)`), composite indexing (`user_id + timestamp`, `account_id + timestamp`), referential integrity protection (`RESTRICT` delete behavior), and non-indexed JSON simulation metadata (`metadata_json`).

---

## Phase 2C: Threat Intelligence & Fraud Genome Walkthrough

### 1. Entity Purpose & Domain Concepts
Phase 2C establishes the structured Threat Intelligence taxonomy and Fraud Genome lineage models for describing synthetic fraud campaigns:

- **`Threat` (`threats` table):** Represents documented synthetic threat hypotheses across 13 core attack families (`ACCOUNT_TAKEOVER`, `SYNTHETIC_IDENTITY`, `DEVICE_MIMICRY`, `BEHAVIORAL_MIMICRY`, `AMOUNT_FRAGMENTATION`, `VELOCITY_MANIPULATION`, `MERCHANT_HOPPING`, `COORDINATED_NETWORK`, `MULE_NETWORK`, `CROSS_RAIL`, `MICROTRANSACTION_PROBING`, `ADAPTIVE_EVASION`, `AGENTIC_PAYMENT_ABUSE`).
- **`AttackGenome` (`attack_genomes` table):** Hybrid structured metadata + JSONB persistence model storing the **15 validated Fraud Genome dimensions** (objective, attack_type, identity_state, device_strategy, location_strategy, amount_pattern, velocity_pattern, timing_pattern, merchant_strategy, behavioral_similarity, network_coordination, payment_rail, evasion_strategy, novelty_rating, campaign_context). Genome records are **immutable definitions**.
- **`AttackCampaign` (`attack_campaigns` table):** Coordinated synthetic fraud scenario linking a `Threat`, an initial seed `AttackGenome`, and generation iterations.
- **`AttackGeneration` (`attack_generations` table):** Evolutionary lineage entity tracking attack mutations ($G_0 \rightarrow G_N$). Features a self-referential `parent_generation_id` link (`RESTRICT` delete semantics), generation index, structured `mutation_summary`, and normalized evaluation metrics (`attack_difficulty`, `detection_rate`, `attack_success_rate` in `[0.0, 1.0]`).

---

## Phase 3: Synthetic Payment Digital Twin Walkthrough

### 1. Generator Architecture & Core Principles
Phase 3 builds the `DigitalTwinGenerator` orchestrator (`backend/app/digital_twin/`) producing 100% benign, relationally coherent, temporally realistic, and deterministically reproducible synthetic payment datasets (`dataset_type = "BENIGN"`):

- **Deterministic PRNG Seeding (`SeedManager`):** Centralizes `numpy.random.Generator`, Python `random.Random`, and seeded `Faker`.
- **Legitimate Behavioral Archetypes (`behavior.py`):** Defines 8 simulation archetypes (`LOW_ACTIVITY`, `REGULAR`, `HIGH_ACTIVITY`, `BUSINESS`, `TRAVELER`, `NIGHT_OWL`, `SUBSCRIPTION_HEAVY`, `DIGITAL_NATIVE`).
- **Relational & Temporal Realism:** Account and device continuity, RFC 5737 IP safety (`192.0.2.x`), and log-normal amount distributions.
- **Data Quality & Integrity (`validators.py`):** `DigitalTwinValidator` checks 0 orphan transactions, positive amounts, and reference uniqueness.

---

## Phase 4: Red Team Attack Synthesis Engine Walkthrough

### 1. Synthesis Engine Architecture & Core Principles
Phase 4 builds the deterministic Red Team Attack Synthesis Engine (`backend/app/red_team/`) translating 15-dimension Fraud Genomes and benign Digital Twin datasets into paired Generation 0 ($G_0$) synthetic adversarial payment scenarios:

- **Attack Scenario Compiler (`compiler.py`):** Compiles declarative `FraudGenomePayload` into an `AttackScenario` plan, deriving intensity ($1.0 - \text{behavioral\_similarity}$) and target user requirements.
- **Non-Trivial Target Selector (`target_selector.py`):** Selects target users based on baseline behavioral profiles, archetype alignment, merchant diversity, and device history.
- **Behavior Mutation Engine (`mutations.py`):** Implements abstract parameter transformations (amount fragmentation/spikes, velocity burst/low-and-slow, merchant hopping, device mimicry, timing randomization, location shifts) while enforcing `MutationConstraints` (positive amounts, valid payment rails, RFC 5737 IPs).
- **Campaign Simulator & Baseline Immutability (`campaign.py`):** Runs Generation 0 ($G_0$) attack simulation. The baseline Digital Twin dataset is **100% immutable** (never modified in place). Creates derived adversarial dataset tagged as `dataset_type = "ADVERSARIAL"` and preserves `AdversarialEventPair` links (`baseline_transaction_id -> adversarial_transaction`).
- **Attack Fidelity Evaluator (`fidelity.py`):** Computes statistical divergence metrics (Kolmogorov-Smirnov distance, mean shift ratio, affected transaction ratio) and derives `behavioral_fidelity_score` in $[0.0, 1.0]$ explicitly defined as a **normalized measure of adversarial-vs-benign behavioral similarity** (high similarity/low divergence $\approx 1.0$; high shift/prominent attack $\rightarrow$ lower score). Does not imply automatic attack effectiveness.
- **Red Team Safety Validator (`safety.py`):** Enforces synthetic-only references (`SYN_*`), RFC 5737 documentation IPs, and non-negative bounds.

---

## 2. Complete Entity Relationship Topology

```
User (users)
 ├──1:N──► Account (accounts)
 ├──1:N──► Device (devices)
 ├──1:N──► Session (sessions)
 ├──1:N──► PaymentAgent (payment_agents)
 └──1:N──► Transaction (transactions)

Threat (threats)
 ├──1:N──► AttackGenome (attack_genomes)
 └──1:N──► AttackCampaign (attack_campaigns)

AttackCampaign (attack_campaigns)
 ├──1:1──► Initial Genome (attack_genomes)
 └──1:N──► AttackGeneration (attack_generations)

AttackGeneration (attack_generations)
 ├──1:1──► Genome (attack_genomes)
 └──0:1──► Parent Generation (attack_generations) [Self-Referential Lineage]
```

---

## 3. Identifier Strategy & Synthetic Data Controls

- **Primary Keys:** Every table uses a 128-bit UUID v4 (`uuid.UUID`) primary key generated via `UUIDPrimaryKeyMixin`.
- **Synthetic Business References:**
  - `User.synthetic_external_id` (e.g. `SYN_USER_000001`)
  - `Account.synthetic_account_reference` (e.g. `SYN_ACC_000001`)
  - `Device.synthetic_device_id` (e.g. `SYN_DEV_000001`)
  - `Merchant.synthetic_merchant_id` (e.g. `SYN_MERCH_000001`)
  - `Session.id` (UUID PK)
  - `PaymentAgent.agent_reference` (e.g. `SYN_AGENT_000001`)
  - `Transaction.transaction_reference` (e.g. `SYN_TXN_00000001`, `SYN_TXN_ADV_...`)
  - `Threat.threat_reference` (e.g. `SYN_THREAT_000001`)
  - `AttackGenome.genome_reference` (e.g. `SYN_GENOME_000001`)
  - `AttackCampaign.campaign_reference` (e.g. `SYN_CAMPAIGN_000001`)
  - `AttackGeneration.generation_reference` (e.g. `SYN_GENERATION_000001`)
- **Strict Network Safety:** All synthetic IP addresses strictly use RFC 5737 documentation blocks (`192.0.2.x`, `198.51.100.x`, `203.0.113.x`).

---

## 4. Alembic Database Migration Strategy

1. **`001_phase2a_domain_foundation.py`:** Creates `users`, `accounts`, `devices`, and `merchants` tables.
2. **`002_phase2b_payment_activity.py`:** Creates `sessions`, `payment_agents`, and `transactions` tables with composite time-series indexes.
3. **`003_phase2c_threat_genome.py`:** Creates `threats`, `attack_genomes`, `attack_campaigns`, and `attack_generations` tables with self-referential parent lineage foreign keys (`parent_generation_id`).

---

## 5. Phase 5 — FRAUDOSCOPE Hybrid Blue Team Defense Engine

The Hybrid Blue Team Defense Engine (`backend/app/blue_team/`) is a multi-layered detection architecture evaluating synthetic payment transactions from both benign Digital Twin baselines (Phase 3) and Red Team Generation 0 attack scenarios (Phase 4).

### 5.1 Architecture & Detector Layers
1. **Deterministic Rule Engine (`rules/engine.py`):** Evaluates baseline rules R001–R007 (amount spikes, off-hours timing, session velocity, new device trust, merchant category risk, payment rail novelty, rapid behavioral change).
2. **Transaction ML Detector (`ml/`):** Supervised classifier predicting `probability_of_adversarial` ($\in [0.0, 1.0]$) using 20+ features, probability calibration (`calibration.py`), and Tree Feature Importances. Versioned artifacts saved in `models/blue_team/v0.1.0/`.
3. **Behavioral Anomaly Detector (`behavioral/anomaly.py`):** `IsolationForest` trained exclusively on legitimate benign baseline features to measure baseline deviation risk.
4. **Graph Intelligence Detector (`graph/intelligence.py`):** `NetworkX` heterogeneous graph topology analyzer measuring shared device concentration, merchant user density, and ego-subgraph community size.
5. **Adversarial Pattern Detector (`adversarial/detector.py`):** Infers observable Red Team attack signatures (fragmentation, low-and-slow velocity, timing shifts, merchant hopping, device rotation) purely from transaction behavioral features without reading attack labels or metadata.
6. **Risk Fusion Engine (`fusion/engine.py`):** Fuses detector risk scores using configurable layer weights:
   $$\text{Composite Risk Score} = \sum w_i \times (\text{detector\_score}_i \times 100) \quad \in [0, 100]$$
7. **Decision Engine (`decisions.py`):** Maps composite risk score to defense actions (`APPROVE` 0–29, `MONITOR` 30–59, `STEP_UP_AUTH` 60–79, `BLOCK` 80–100) and constructs structured human-explainable evidence bundles.

### 5.2 Anti-Leakage & Unseen Attack Generalization
- **Strict Anti-Leakage (`ml/features.py`, `evaluation.py`):** Feature extraction strictly excludes `scenario_id`, `genome_reference`, `generation_number`, `mutation_dimensions`, `target_flag`, `applied_mutations`, `is_fraud`, or any Red Team metadata.
- **Strengthened Leakage Auditor (`LeakageAuditor`):** Verifies zero transaction ID overlap, zero user ID overlap, zero account ID overlap, and zero attack-combination overlap between training and unseen test sets.
- **Corrected Data Splits & Entity Isolation (`benchmark.py`):**
  - `TRAIN`: 60% benign + 60% known adversarial transactions

---

## 6. Phase 6 — FRAUDOSCOPE Autonomous Defense Hardening Engine

The FRAUDOSCOPE Auto-Hardening Engine (`backend/app/hardening/`) completes the closed-loop defensive learning flywheel:
$$\text{Attack Scenario} \rightarrow \text{Blue Team Evaluation} \rightarrow \text{DefenseGapAnalyzer} \rightarrow \text{GapPriorityScore} \rightarrow \text{AdversarialDatasetBuilder} \rightarrow \text{LeakageAuditor Audit} \rightarrow \text{CandidateModelTrainer} \rightarrow \text{PromotionGate} \rightarrow \text{ModelRegistry} (\text{PROMOTE} \mid \text{REJECT})$$

### 6.1 Defense Gap Discovery & Deterministic Taxonomy
- **`DefenseGapAnalyzer` (`gap_analyzer.py`):** Inspects Blue Team risk fusion explanations on simulated attack transactions to identify bypasses ($ risk < 60.0 $) and maps failed/partial/successful layers.
- **Deterministic 9-Category Taxonomy:** `RULE_BYPASS`, `ML_BLIND_SPOT`, `BEHAVIORAL_BLIND_SPOT`, `GRAPH_BLIND_SPOT`, `ADVERSARIAL_BLIND_SPOT`, `FUSION_FAILURE`, `THRESHOLD_FAILURE`, `MULTI_VECTOR_EVASION`, `UNKNOWN_GENERALIZATION_GAP`.
- **`GapPriorityScore` Formula:**
  $$\text{PriorityScore} = 100 \times \left[ 0.30 \cdot \text{SeverityWeight} + 0.30 \cdot \text{BypassRate} + 0.20 \cdot \min\left(1.0, \frac{\text{BypassCount}}{10}\right) + 0.10 \cdot \text{Novelty} + 0.10 \cdot \text{Confidence} \right]$$

### 6.2 Adversarial Training Augmentation & Anti-Leakage Audit
- **`AdversarialDatasetBuilder` (`dataset_builder.py`):** Synthesizes targeted adversarial feature vectors ($ y = 1 $) for prioritized gap transactions.
- **Sample Provenance:** Attaches `AdversarialSampleProvenance` tracking `source_transaction_id`, `parent_attack_genome_id`, `mutation_lineage`, `generation_number`, `random_seed`, `reason_for_inclusion`, and `target_defense_gap_id`.
- **Anti-Leakage Audit Abort Policy:** Passes augmented dataset to `LeakageAuditor.audit_splits`. If any transaction, user, account, device, or feature metadata leakage occurs, raises `DataLeakageError` to immediately terminate the run.

### 6.3 Candidate Model Training & Immutable Versioning
- **`CandidateModelTrainer` (`trainer.py`):** Trains candidate `RandomForestClassifier` (`n_estimators=100`, `max_depth=6`, `random_state=seed`, `n_jobs=1`) on augmented dataset. Computes dataset SHA-256 hash and model byte hash.
- **`ModelRegistry` (`promotion.py`):** Immutable versioning (`v1.0.0`, `v1.1.0-cand-42`) managing model statuses (`ACTIVE`, `CANDIDATE`, `PROMOTED`, `REJECTED`, `ARCHIVED`) and active pointer `models/blue_team/active_model.json`.

### 6.4 Strict 5-Gate Promotion Policy & Rejection Path
- **`PromotionGate` (`promotion.py`):** Evaluates candidate models against active baseline across 5 mandatory ADR-006 criteria:
  1. *Gate 1: Targeted Gap Improvement* (`targeted_gap_cand_recall > targeted_gap_active_recall`)
  2. *Gate 2: Benign Non-Regression* (`benign_approval_rate_cand >= benign_approval_rate_active - 0.005`)
  3. *Gate 3: Held-Out Unseen Stability* (`unseen_recall_cand >= unseen_recall_active - 0.001`; evaluated ONLY as evaluation gate)
  4. *Gate 4: Calibration Stability* (`brier_score_cand <= brier_score_active + 0.02`)
  5. *Gate 5: Feature Schema Compatibility* (`feature_schema_cand == feature_schema_active`)
- **Promotion / Rejection Outcome:** If all 5 gates pass, candidate is promoted and active model pointer is updated; if any gate fails, candidate is marked `REJECTED` with explicit rejection reasons.

### 6.5 Demonstrations, REST API & Machine-Readable Audit Artifacts
- **CLI Demo (`python -m app.hardening.demo`):** Executes 100% deterministic closed-loop hardening cycle demonstrating gap discovery, augmentation, candidate training, multi-gate evaluation, and promotion.
- **REST API Endpoints (`backend/app/api/v1/hardening.py`):**
  - `POST /api/v1/hardening/analyze-gaps`
  - `POST /api/v1/hardening/run`
  - `GET  /api/v1/hardening/runs`
  - `GET  /api/v1/hardening/runs/{run_id}`
  - `GET  /api/v1/hardening/models`
  - `GET  /api/v1/hardening/models/{model_id}`
  - `GET  /api/v1/hardening/active-model`
---

## 7. Phase 7A — FRAUDOSCOPE Explainability Engine & Evidence Contract

The FRAUDOSCOPE Explainability Subsystem (`backend/app/explainability/`) translates existing numerical risk decisions, detector layer evidence, Red Team attack mutations, and Phase 6 hardening metrics into structured, strongly-typed evidence contracts and reproducible explanation results.

### 7.1 Architecture & Core Components
- **Domain Schemas (`models.py`):** Strongly-typed Pydantic v2 evidence contracts (`ExplanationRequest`, `ExplanationResult`, `EvidenceItem`, `DetectorEvidenceModel`, `RuleEvidence`, `FeatureEvidence`, `GraphEvidence`, `AnomalyEvidence`, `AttackEvidence`, `HardeningEvidence`, `CounterfactualEvidence`, `BypassEvidence`).
- **Evidence Extractor (`evidence.py`):** Translates raw detector outputs, rules, features, anomalies, graph metrics, attack genomes, and hardening runs into structured evidence objects without data fabrication. Explicitly marks unavailable per-sample attributions (`attribution_available=False`).
- **Evidence Ranker (`attribution.py`):** Normalizes diverse evidence category signals into $[0.0, 1.0]$ strength scores and deterministically sorts items descending for `"WHY WAS THIS FLAGGED?"`.
- **Lineage Tracker (`lineage.py`):** Assembles immutable `ExplanationProvenance` metadata (`explanation_id`, `transaction_id`, `campaign_id`, `genome_id`, `model_version`, `dataset_reference`, `random_seed`, `generated_at`, `source_subsystem`).
- **Counterfactual Engine (`counterfactual.py`):** Safe, deterministic `"What-If"` re-computation engine for reliable features (`amount`, `device_trust_score`, `velocity_deviation`) under feature perturbations. Unsupported features explicitly return `validity_status=False`.
- **Explainability Engine (`engine.py`):** Main orchestrator assembling top-level `ExplanationResult` bundles.

### 7.2 Service Layer & Endpoints (`backend/app/api/v1/explainability.py`)
- `GET /api/v1/explainability/health`
- `POST /api/v1/explainability/explain`
- `GET /api/v1/explainability/{explanation_id}`

---

## 8. Phase 7B — Explainability Command Center Integration & Closed-Loop Investigation UX

Phase 7B connects the FRAUDOSCOPE backend intelligence (Phases 1–7A) to a state-of-the-art investigator-facing web Command Center built using React, TypeScript, Vite, Tailwind CSS, `@xyflow/react`, Recharts, and Lucide icons.

### 8.1 Information Architecture & Investigation Workflow
- **Application Shell & Sidebar (`Layout.tsx`, `Header.tsx`, `Sidebar.tsx`):** Persistent header displaying `SYNTHETIC ONLY`, seed `42`, active model `v1.1.0-cand-42`, API status, and responsible AI disclaimers.
- **8 Primary Investigation Sections:**
  1. *Overview (`/`):* Executive security command center KPI cards & baseline Recharts graphs.
  2. *Attack Lab (`/attack-lab`):* Red Team campaign selector, metadata inspector & 11-group Fraud Genome matrix.
  3. *Transaction Investigator (`/investigator`):* Transaction inspector grouped into Identity, Transaction, Risk, and Attack.
  4. *Why Flagged? (`/explainability`):* Ranked evidence panel displaying supporting vs contextual evidence across 7 categories. Explicitly displays `"Per-sample attribution unavailable"` for non-SHAP ML models.
  5. *Risk Waterfall (`/waterfall`):* Blue Team layered risk score evaluation & composite decision pipeline.
  6. *Lineage Graph (`/lineage`):* Interactive React Flow graph tracing `Fraud Genome -> Campaign -> Mutation -> Transaction -> Detector -> Evidence -> Defense Gap -> Hardening Run -> Candidate Model -> Promotion Decision`.
  7. *Defense Gaps (`/gaps`):* Defense gap dashboard supporting the 9-category taxonomy.
  8. *Hardening (`/hardening`):* Autonomous defense hardening lifecycle and strict 5-gate promotion results.
  9. *Counterfactual Explorer (`/counterfactual`):* Interactive `"WHAT IF?"` slider/input explorer for supported features (`amount`, `device_trust_score`, `velocity_deviation`).

---

## 9. Phase 7B — Closed-Loop Orchestration Engine & REST API

The FRAUDOSCOPE Closed-Loop Orchestration Layer (`backend/app/orchestration/`) automates the end-to-end synthetic payment-security research pipeline without duplicating subsystem algorithms or ML training logic.

### 9.1 Orchestration Pipeline Architecture & State Machine

```
   ┌──────────────────────┐
   │ Scenario Prep (St.1) │
   └──────────┬───────────┘
              │
   ┌──────────▼───────────┐
   │   Red Team (St.2)    │
   └──────────┬───────────┘
              │
   ┌──────────▼───────────┐
   │   Blue Team (St.3)   │
   └──────────┬───────────┘
              │
   ┌──────────▼───────────┐
   │ Gap Analysis (St.4)  │
   └──────────┬───────────┘
              │
   ┌──────────▼───────────┐
   │   Hardening (St.5)   │
   └──────────┬───────────┘
              │
   ┌──────────▼───────────┐
   │ Explainability(St.6) │
   └──────────┬───────────┘
              │
   ┌──────────▼───────────┐
   │   Re-Attack (St.7)   │
   └──────────┬───────────┘
              │
   ┌──────────▼───────────┐
   │   Verdict (St.8)     │
   └──────────────────────┘
```

- **Domain Schemas (`models.py`):** Strongly-typed Pydantic v2 schemas (`PipelineStage`, `StageStatus`, `ClosedLoopVerdict`, `ClosedLoopStageResult`, `ClosedLoopMetrics`, `ClosedLoopRunRequest`, `ClosedLoopProvenance`, `ClosedLoopRunResult`).
- **Stage Runner (`stages.py`):** Encapsulates execution for each stage, delegating directly to existing Red Team, Blue Team, DefenseGapAnalyzer, AutonomousHardeningEngine, and ExplainabilityEngine.
- **Closed-Loop Orchestrator (`pipeline.py`):** Orchestrates sequential 8-stage execution, manages state transitions (`NOT_STARTED` -> `IN_PROGRESS` -> `COMPLETED` / `FAILED` / `SKIPPED`), enforces error boundary isolation, and persists completed run results.
- **Run Store (`run_store.py`):** JSON file-backed persistence store (`backend/data/orchestration/runs.json`).
- **Service Boundaries (`backend/app/api/v1/orchestration.py`):**
  - `POST /api/v1/orchestration/run`
  - `GET  /api/v1/orchestration/runs`
  - `GET  /api/v1/orchestration/runs/{run_id}`
  - `GET  /api/v1/orchestration/runs/{run_id}/stages`
  - `GET  /api/v1/orchestration/runs/{run_id}/verdict`
  - `GET  /api/v1/orchestration/health`

### 9.2 Quality Gates & Verification Summary
- **Phase 7B Unit & Integration Suite (`backend/tests/unit/test_orchestration.py`, `backend/tests/integration/test_phase7b_closed_loop.py`):** **14 PASS / 0 FAIL**.
- **Full Backend Pytest Suite (`python -m pytest backend/`):** **122 PASS / 0 FAIL**.
- **Backend Linters (`black` & `ruff`):** **128 files left unchanged, All checks passed**.
- **CLI Smoke Test (`seed 42`):** `RUN_ID: RUN_LOOP_5F5C6038BCEC | VERDICT: HARDENED_SUCCESSFULLY | STAGES: 8`.






