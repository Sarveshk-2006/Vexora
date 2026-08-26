# FRAUDOSCOPE — Architecture Decision Records (ADR Log)

> **Format:** Standard ADR (Context, Decision, Consequences, Status)

---

## ADR-001: Selection of Modular Monolith Architecture over Microservices

### Status
**APPROVED** — 2026-08-26

### Context
FRAUDOSCOPE requires high-frequency communication between the Payment Digital Twin, Red Team Mutation Engine, Hybrid Blue Team Detectors, Auto-Hardening Retrainer, and Explainability Subsystems. A distributed microservices architecture introduces network latency, deployment complexity, distributed transaction overhead, and RPC serialization friction that is counter-productive for a fast, research-grade hackathon prototype.

### Decision
We will build FRAUDOSCOPE as a clean **Modular Monolith** using Python (FastAPI + Pydantic + SQLAlchemy) for the backend core and React (TypeScript + Vite) for the frontend command center. Python packages will be strictly decoupled by domain (`digital_twin`, `threat_intel`, `red_team`, `blue_team`, `hardening`, `explainability`, `core`).

### Consequences
- **Positive:** Maximum execution velocity, simple single-command deployment (`docker-compose up`), zero network latency between simulation and ML engines, straightforward test execution.
- **Negative:** Requires disciplined internal module boundary enforcement to prevent tight coupling.

---

## ADR-002: Synthetic Digital Twin & Strict Sandbox Isolation

### Status
**APPROVED** — 2026-08-26

### Context
Payment security research must comply with stringent data privacy (GDPR, PCI-DSS), financial regulations, and ethical safety standards. Using real customer transaction data or connecting to real payment rails introduces legal risk, credential theft vectors, and regulatory compliance issues.

### Decision
FRAUDOSCOPE will operate strictly within an internal **Synthetic Digital Twin Sandbox**. All users, accounts, devices, merchants, sessions, transactions, and payment rail interactions (UPI, Card, Wallet) will be generated deterministically via statistical distributions and synthetic seed parameters. Zero real customer data, real banking credentials, or external network connections will be permitted.

### Consequences
- **Positive:** Complete safety, zero privacy liability, 100% reproducible scenarios, arbitrary scale without external dependencies.
- **Negative:** Synthetic distributions must be carefully tuned to avoid trivial or unrepresentative fraud patterns.

---

## ADR-003: Evolvable Fraud Genome Schema Design

### Status
**APPROVED** — 2026-08-26

### Context
Adversarial fraud attacks evolve continuously across multiple vectors (amount fragmentation, device spoofing, velocity manipulation, merchant hopping, etc.). Representing attacks as ad-hoc code scripts prevents lineage tracking, mathematical mutation, and automated defense gap analysis.

### Decision
We establish the **Fraud Genome** — a strongly validated, versioned JSON schema representing an attack across 15 structured dimensions: objective, attack type, identity state, device strategy, location strategy, amount pattern, velocity pattern, timing pattern, merchant strategy, behavioral similarity, network coordination, payment rail, evasion strategy, novelty rating, and campaign context.

### Consequences
- **Positive:** Enables mathematical genetic mutations ($G_0 \rightarrow G_N$), exact parent-child lineage tracking, and explicit root-cause mapping for defense gaps.
- **Negative:** Schema must be kept version-compatible as new attack dimensions are added.

---

## ADR-004: Multi-Layered Hybrid Blue Team Defense Architecture

### Status
**APPROVED** — 2026-08-26

### Context
Single-technology defense mechanisms (e.g., rules alone or ML models alone) are vulnerable to targeted evasion. Real-world payment security relies on defense-in-depth combining deterministic rules, ML risk scoring, behavioral anomaly detection, and graph intelligence.

### Decision
We adopt a **Hybrid Blue Team Architecture** consisting of 6 specialized defense layers feeding into a Risk Fusion & Decision Engine:
1. Deterministic Rule Engine
2. Transaction-level ML (XGBoost)
3. Behavioral Anomaly Detector (Isolation Forest)
4. Graph Intelligence (NetworkX for mule network detection)
5. Adversarial Detector
6. Risk Fusion Engine (mapping composite 0-100 scores to APPROVE, MONITOR, STEP_UP_AUTH, BLOCK)

### Consequences
- **Positive:** Robust defense-in-depth, realistic security simulation, ability to test multi-vector evasion attacks.
- **Negative:** Requires tuning fusion weights to prevent false-positive inflation.

---

## ADR-005: Strict Boundary of LLM Usage in Security Engine

### Status
**APPROVED** — 2026-08-26

### Context
While GenAI/LLMs excel at narrative generation and reasoning, relying on non-deterministic LLMs for core numerical risk scoring or high-throughput payment transaction classification introduces latency, non-reproducibility, hallucination risk, and high operational costs.

### Decision
LLMs will be used exclusively for **high-level reasoning, threat ideation, attack mutation narrative synthesis, and natural-language explainability**. Core transaction processing, feature extraction, graph calculations, and primary risk decisions MUST be computed by deterministic rules and evaluated numerical ML models (XGBoost / scikit-learn).

### Consequences
- **Positive:** High performance (sub-millisecond evaluation), 100% deterministic reproducibility, auditability, zero reliance on external LLM availability during risk evaluation.
- **Negative:** Narrative explanations require an explicit step to convert numerical feature attributions into natural language text.

---

## ADR-006: Auto-Hardening Retraining & Model Promotion Criteria

### Status
**APPROVED** — 2026-08-26

### Context
Automatically retraining defense models on adversarial bypasses carries the risk of model regression, catastrophic forgetting, or over-fitting to adversarial noise at the expense of benign transaction accuracy.

### Decision
The Auto-Hardening Engine will implement a **Strict Promotion Gate**. Candidate models trained on adversarial variants will ONLY be promoted to active status if:
1. Detection rate on the targeted adversarial gap strictly increases.
2. Accuracy on benign historical transactions does not regress beyond a strict threshold ($<0.5\%$ degradation permitted).
3. Performance on held-out unseen attack scenarios improves or remains stable.
Models failing any condition are logged and discarded without modifying the active deployment.

### Consequences
- **Positive:** Prevents silent model degradation and guarantees monotonic defense improvements.
- **Negative:** Candidate models may be rejected if adversarial training data causes benign performance trade-offs, requiring hyperparameter tuning.

---

## ADR-007: Approved Technology Stack Selection

### Status
**APPROVED** — 2026-08-26

### Context
The stack must balance high developer productivity, rich web visualization capability, statistical/ML ecosystem strength, and rapid prototype execution.

### Decision
We standardize on:
- **Backend:** Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0+, Alembic, PostgreSQL.
- **ML / Stats:** pandas, numpy, scipy, scikit-learn, XGBoost, NetworkX, SHAP.
- **Frontend:** React 18+, TypeScript, Vite, Tailwind CSS, React Flow, Recharts, Framer Motion.
- **Infra / Testing:** Docker, Docker Compose, pytest, Vitest.

### Consequences
- **Positive:** Modern standard stack with maximum ecosystem support for payment analytics, ML explainability, and interactive UI graphs.
- **Negative:** None.

---

## ADR-008: Phase 1 Repository Architecture, Packaging & Runtime Shell

### Status
**APPROVED** — 2026-08-26

### Context
Phase 1 requires establishing a production-grade repository architecture and application runtime shell without implementing premature business models or fake ML estimators.

### Decision
1. Standardize on `backend/pyproject.toml` with setuptools/hatchling standards for Python packaging.
2. Structure domain packages as empty packages with `__init__.py` files under `backend/app/` (`core`, `digital_twin`, `threat_intel`, `red_team`, `blue_team`, `hardening`, `explainability`, `evaluation`).
3. Implement `app/core/config.py` using `pydantic-settings` with environment variable overrides and safe local defaults.
4. Implement `app/core/database.py` using SQLAlchemy 2.0 with safe offline initialization so `/health` endpoints run cleanly even if PostgreSQL is offline.
5. Setup `frontend/` as a Vite + React 18 + TypeScript application with Tailwind CSS, Vitest, and an API health check service querying `/api/v1/health`.
6. Configure Docker Compose, GitHub Actions CI, and comprehensive `.gitignore` rules.

### Consequences
- **Positive:** Clean modular monolithic structure, immediate testability, resilient offline startup capability, zero technical debt for Phase 2 onward.
- **Negative:** None.

---

## ADR-009: Phase 2A Domain Entity Modeling & Pydantic v2 Schema Conventions

### Status
**APPROVED** — 2026-08-26

### Context
Phase 2A requires establishing database ORM models and Pydantic v2 validation schemas for foundational actors (`User`, `Account`, `Device`, `Merchant`) without implementing premature business execution logic or payment rail handlers.

### Decision
1. Use modern SQLAlchemy 2.0 typed declarative mappings (`Mapped[]`, `mapped_column()`, `relationship()`).
2. Utilize `UUIDPrimaryKeyMixin` and timezone-aware UTC `TimestampMixin` across all domain entities.
3. Separate SQLAlchemy ORM models (`app/models/`) completely from API/Pydantic schemas (`app/schemas/`).
4. Centralize domain enums (`AccountStatus`, `AccountType`, `DeviceType`, `MerchantStatus`, `RiskTier`) in `app/core/enums.py`.
5. Enforce unique synthetic identifiers (`synthetic_external_id`, `synthetic_account_reference`, `synthetic_device_id`, `synthetic_merchant_id`).
6. Enforce strict Pydantic v2 field validation (`0.0 <= score <= 1.0`, non-blank strings, non-negative values).
7. Create DDL database migration script `001_phase2a_domain_foundation.py` under Alembic.

### Consequences
- **Positive:** Strongly typed domain layer, strict train/test synthetic data boundary, 100% reproducible schemas, seamless readiness for Phase 2B.
- **Negative:** None.

---

## ADR-010: Phase 2B Payment Activity Event Modeling & Indexing Conventions

### Status
**APPROVED** — 2026-08-26

### Context
Phase 2B requires implementing synthetic payment activity entities (`Session`, `PaymentRail`, `Transaction`, `PaymentAgent`) to act as the central event stream of the Payment Digital Twin, optimizing for future high-scale time-series analytics, behavioral feature extraction, and graph intelligence.

### Decision
1. Represent `PaymentRail` as a central string enum (`UPI`, `CARD`, `WALLET`) with indexed column mappings.
2. Implement `Session` to capture synthetic interaction windows, RFC 5737 documentation IP addresses (`192.0.2.x`), location metadata, and user agents.
3. Model `Transaction` as the primary event stream table with exact financial decimal representation (`Numeric(15, 2)`), currency defaulting to `INR`, and optional `metadata_json` JSON column for non-indexed simulation attributes.
4. Enforce `ondelete="RESTRICT"` for core transaction relationships (`account_id`, `user_id`, `merchant_id`, `device_id`) to prevent accidental deletion of historical audit trails.
5. Create composite indexes (`ix_transactions_user_timestamp`, `ix_transactions_account_timestamp`) to accelerate time-windowed feature aggregation and baseline windowing queries.
6. Enforce denormalized user ownership consistency (`transaction.user_id == transaction.account.user_id`) in Pydantic schema validation layers.
7. Create Alembic DDL migration script `002_phase2b_payment_activity.py`.

### Consequences
- **Positive:** High-performance event stream queries, referentially safe audit trails, zero PII/credential exposure, instant readiness for Phase 3 Digital Twin generation.
- **Negative:** None.

---

## ADR-011: Phase 2C Hybrid Genome Representation, Schema Versioning & Immutability

### Status
**APPROVED** — 2026-08-26

### Context
Phase 2C requires establishing structured Threat Intelligence (`Threat`) and Fraud Genome domain models (`AttackGenome`, `AttackCampaign`, `AttackGeneration`) to represent synthetic payment fraud attacks across 15 explicit dimensions (ADR-003) while maintaining versioning, evolutionary lineage, and strict reproducibility.

### Decision
1. Represent `AttackGenome` using a hybrid model: strongly validated Pydantic v2 schemas (`FraudGenomePayload`) for all 15 dimensions stored in PostgreSQL JSONB (`structured_payload`).
2. Treat `AttackGenome` definitions as **immutable records**. Evolutionary mutations generate new `AttackGenome` records and new `AttackGeneration` iterations rather than mutating historical genomes.
3. Track attack lineage ($G_0 \rightarrow G_N$) in `AttackGeneration` using a self-referential `parent_generation_id` foreign key with `ondelete="RESTRICT"` to prevent accidental loss of historical campaign trees.
4. Enforce strict `[0.0, 1.0]` bounds for normalized evaluation scores (`behavioral_similarity`, `novelty_rating`, `attack_difficulty`, `detection_rate`, `attack_success_rate`).
5. Decouple `genome_schema_version` ("1.0") from Alembic migration versions for persistent contract stability.
6. Create Alembic DDL migration script `003_phase2c_threat_genome.py`.

### Consequences
- **Positive:** Strongly validated 15-dimension genome contract, immutable campaign lineage, 100% reproducible simulation runs, clean readiness for Red Team evolution.
- **Negative:** None.

---

## ADR-012: Phase 3 Synthetic Payment Digital Twin Architecture & Deterministic PRNG Seeding

### Status
**APPROVED** — 2026-08-26

### Context
Phase 3 requires building a synthetic payment environment generator (`DigitalTwinGenerator`) producing 100% benign baseline payment activity across Users, Accounts, Devices, Merchants, PaymentAgents, Sessions, and Transactions while ensuring strict 100% deterministic reproducibility across generation runs.

### Decision
1. Implement a centralized `SeedManager` controlling `numpy.random.Generator`, Python `random.Random`, and `Faker`. Running with the same seed guarantees 100% byte-for-byte identical generated datasets.
2. Establish 8 legitimate simulation behavioral archetypes (`LOW_ACTIVITY`, `REGULAR`, `HIGH_ACTIVITY`, `BUSINESS`, `TRAVELER`, `NIGHT_OWL`, `SUBSCRIPTION_HEAVY`, `DIGITAL_NATIVE`) governing diurnal timing curves, merchant category selection, payment rail choices, and log-normal financial amount parameters ($\mu, \sigma$).
3. Strictly enforce RFC 5737 documentation IPv4 address prefixes (`192.0.2.x`, `198.51.100.x`, `203.0.113.x`) for all synthetic IP attributes.
4. Decouple memory data generation (`generate()`) from database persistence (`DatabasePersister.persist()`) and dataset exporting (`DatasetExporter.export_transactions_csv()`).
5. Require JSON generation manifests (`data/manifests/`) containing SHA-256 configuration hashes, run seeds, timestamp bounds, entity counts, and distribution statistics.
6. Explicitly tag all generated transactions with `dataset_type = "BENIGN"` to prevent future train/test data leakage.

### Consequences
- **Positive:** 100% reproducible benign baseline datasets, zero PII/credential exposure, referentially coherent payment event streams, instant readiness for Phase 4 Red Team attack simulation.
- **Negative:** None.

---

## ADR-013: Phase 4 Red Team Attack Synthesis Engine Architecture & Immutable Baseline Pairing

### Status
**APPROVED** — 2026-08-26

### Context
Phase 4 requires building a deterministic Red Team attack synthesis engine (`backend/app/red_team/`) to compile 15-dimension Fraud Genomes and benign Digital Twin datasets into Generation 0 ($G_0$) synthetic adversarial payment scenarios while ensuring 100% baseline dataset immutability, baseline-adversarial event pairing, and strict sandbox safety validation.

### Decision
1. Implement `AttackScenarioCompiler` to translate declarative `FraudGenomePayload` contracts into structured `AttackScenario` execution plans with derived transformation intensity ($1.0 - \text{behavioral\_similarity}$).
2. Implement non-trivial `TargetSelector` targeting users based on baseline behavioral profiles, archetype alignment, merchant diversity, and device history.
3. Enforce **100% baseline dataset immutability**. Baseline transactions are never modified in place; targeted perturbations create derived adversarial events tagged as `dataset_type = "ADVERSARIAL"` linked via `AdversarialEventPair` (`baseline_transaction_id -> adversarial_transaction`).
4. Implement `BehaviorMutationEngine` and `MutationConstraints` enforcing abstract parameter transformations (amount fragmentation/spikes, velocity burst/low-and-slow, merchant hopping, device mimicry, timing shifts) while guaranteeing strictly positive amounts and RFC 5737 documentation IPv4 addresses (`192.0.2.x`, `198.51.100.x`, `203.0.113.x`).
5. Implement `AttackFidelityEvaluator` computing statistical distribution divergence (Kolmogorov-Smirnov distance, mean shift ratio, affected transaction ratio) and deriving `behavioral_fidelity_score` in $[0.0, 1.0]$ explicitly defined as a normalized measure of adversarial-vs-benign behavioral similarity. Higher values indicate greater statistical similarity to benign baseline; lower values indicate larger behavioral shifts. High fidelity score does not imply automatic attack effectiveness.
6. Implement `RedTeamSafetyValidator` enforcing synthetic-only business references (`SYN_*`), RFC 5737 IPs, and non-negative bounds.
7. Limit Phase 4 scope strictly to Generation 0 ($G_0$). Zero evolutionary mutation loops ($G_{1+}$), zero LLM calls, zero Blue Team detectors, zero business APIs, and zero real-world attack tooling are introduced.

### Consequences
- **Positive:** Scientifically reproducible adversarial scenario generation, 100% baseline immutability, referentially linked event pairs for delta analysis, zero security/PII risk, instant readiness for Phase 5 Blue Team detection.
- **Negative:** None.






