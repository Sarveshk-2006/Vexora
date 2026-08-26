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
