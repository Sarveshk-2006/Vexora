# FRAUDOSCOPE — Engineering Contract & Development Guidelines

> **Project Status:** Phase 0 — Engineering Foundation  
> **Target System:** Autonomous Adversarial Payment Security Lab  
> **Core Architecture:** Modular Monolith (FastAPI + React/TypeScript)

---

## 1. Project Purpose & Philosophy

FRAUDOSCOPE is a controlled, synthetic payment-security research platform designed to evaluate, stress-test, and automatically harden payment defense systems against emerging, GenAI-enabled payment fraud scenarios.

### The Core Closed Loop

```
IDENTIFY
  │
  ▼
MODEL ATTACK (Fraud Genome)
  │
  ▼
GENERATE SYNTHETIC DATA (Digital Twin)
  │
  ▼
SIMULATE ADVERSARIAL CAMPAIGN
  │
  ▼
DETECT (Hybrid Blue Team)
  │
  ▼
MEASURE DEFENSE GAP
  │
  ▼
EVOLVE ATTACK (Red Team Mutations)
  │
  ▼
AUTO-HARDEN (Adversarial Retraining & Model Candidate Validation)
  │
  ▼
REPLAY & EVALUATE ON UNSEEN ATTACKS
  │
  └──────────────► REPEAT
```

### Core Product Principle
FRAUDOSCOPE is **NOT** a generic "AI fraud detector". It is an **adversarial red-team / blue-team laboratory** where:
1. The **Red Team** continuously discovers security gaps in the Blue Team's detection capabilities.
2. Discovered weaknesses automatically feed into the **Auto-Hardening Engine** to train and validate candidate model upgrades.
3. Upgraded models are re-tested against both known and **unseen attack scenarios** before promotion.

---

## 2. Mandatory Security & Operational Sandbox Rules

FRAUDOSCOPE operates strictly as a synthetic research sandbox. All agents and developers must uphold these non-negotiable boundaries:

1. **Synthetic Data Only:** Zero real customer data (PII), real banking credentials, real card numbers, or real transaction records shall ever enter or pass through this codebase.
2. **Zero External Payment Execution:** No integration with live payment gateways, banking APIs, ISO 20022 networks, card processing APIs, or UPI switches.
3. **No Real-World Attack Automation:** Attack generation logic, payload structures, and strategies must remain abstract, simulation-bound, and executing within internal digital twins only.
4. **No Unauthorized Network Traffic:** The application must not perform outbound calls to unauthorized third-party infrastructure.

---

## 3. Technology Stack Specification

All components must adhere strictly to the approved technology stack:

| Layer | Approved Technology |
| :--- | :--- |
| **Frontend UI** | React 18+, TypeScript, Vite, Tailwind CSS, React Flow (attack graph/genealogy), Recharts (metrics), Framer Motion |
| **Backend API & Orchestration** | Python 3.11+, FastAPI, Pydantic v2 (schema validation), SQLAlchemy 2.0+ |
| **Database & Persistence** | PostgreSQL (Supabase compatible for production deployment), Alembic (migrations) |
| **ML & Analytics Engine** | pandas, numpy, scipy, scikit-learn, XGBoost, SHAP (explainability) |
| **Synthetic Generation** | Custom statistical & behavioral engine, Faker, SDV (where applicable) |
| **Graph Intelligence** | NetworkX (for entity network risk & mule graph analysis) |
| **Containerization** | Docker, Docker Compose |
| **Testing Frameworks** | pytest (Backend & ML domain logic), Vitest / React Testing Library (Frontend) |

---

## 4. Fundamental Architectural Principles

### 4.1 Separation of Concerns
- **Domain Decoupling:** Core payment logic, attack evolution math, and ML pipelines MUST NOT depend on HTTP request objects or web framework code. FastAPI route handlers should act purely as thin orchestration layers parsing requests and formatting responses.
- **Modular Monolith:** All services run within a clean, single-repository modular monolith architecture. Avoid introducing microservice boundaries or external RPCs during hackathon implementation.

### 4.2 Determinism & Reproducibility
- **Deterministic Generators:** All synthetic payment generation, behavior noise additions, and attack mutations MUST accept an explicit integer random `seed`. Given identical seeds and configuration, output data streams and mutation trajectories must be 100% reproducible.
- **Lineage Tracking:** Every attack instance must link back to its parent `Attack Genome`, its generating `Attack Campaign`, its `Mutation Sequence`, and the exact `Model Version` evaluated against.
- **Model & Dataset Versioning:** Every model candidate, training run, and evaluation run must record immutably the model version, parameter manifest, dataset version, and scenario seed.

### 4.3 Data Boundaries & Leakage Prevention
- **Strict Train / Test Separation:** Training pipelines MUST NEVER have access to held-out test datasets.
- **Unseen Attack Protection:** A dedicated set of novel, un-mutated attack combinations MUST be reserved exclusively for testing generalization performance. Evaluation pipelines must explicitly report performance broken down by:
  - *Known Attacks* (In-distribution training scenarios)
  - *Evolved Attacks* (Adversarial variants of known attacks)
  - *Unseen Attack Scenarios* (Held-out novel attack families)

### 4.4 Boundary of LLM Usage
- **Reasoning & Ideation, Not Math:** Large Language Models (LLMs) may be utilized for threat scenario ideation, attack mutation narrative synthesis, and generating natural-language risk explanations.
- **Primary Risk Engine Independence:** Risk scoring, transaction classification, graph anomaly computation, and numerical thresholds MUST be computed deterministically or by evaluated ML models (XGBoost/scikit-learn), NEVER delegated solely to an LLM prompt.

### 4.5 Explainability as a First-Class Feature
- Every non-approved transaction (Monitor, Step-Up, Block) MUST generate an interpretable decision payload containing:
  - Numerical composite risk score (0–100)
  - Primary decision tier (Approve, Monitor, Step-Up, Block)
  - Top contributing rule triggers and ML feature attributions (SHAP values)
  - Counterfactual explanation (what changes would alter the risk decision)

---

## 5. Domain Model Standards & Core Entities

All backend domain entities must be represented as strongly-typed Pydantic v2 schemas and SQLAlchemy 2.0 ORM models:

- `User`: Synthetic account holder profile, behavioral baseline, risk tier.
- `Account`: Financial ledger account, balance history, rail associations.
- `Device`: Device fingerprint, OS, IP history, hardware signature, reputation score.
- `Merchant`: Merchant profile, category code (MCC), historical velocity, risk rating.
- `Session`: Authentication session context, biometric signals, IP, geo-location.
- `Transaction`: Individual payment attempt across specified Payment Rail (UPI, Card, Wallet).
- `PaymentRail`: Rail-specific attributes (e.g., VPA for UPI, PAN hash for Card, Wallet ID).
- `PaymentAgent`: Autonomous or automated AI agents executing transactions on behalf of users.
- `Threat`: High-level threat vector taxonomy entry.
- `AttackGenome`: Strongly validated JSON schema defining attack vector dimensions.
- `AttackCampaign`: Batch execution of synthetic transactions modeled after a Fraud Genome.
- `AttackGeneration`: Iteration number in an evolutionary attack timeline (Gen 0 = seed, Gen N = mutated).
- `DetectionResult`: Per-transaction risk scoring, rule hits, ML score, fusion verdict.
- `RiskScore`: Multi-layer composite score (0-100 scale).
- `DefenseGap`: Structural evaluation finding indicating where detection failed.
- `ModelVersion`: Immutable reference to trained ML model weights and feature definitions.
- `TrainingRun`: Record of model training session including hyperparams and dataset hashes.
- `EvaluationRun`: Execution log comparing a model version against an attack dataset.
- `Experiment`: High-level benchmark comparing baseline vs hardened model versions.

---

## 6. Decision Tier Standards

Decision thresholds must be centralized, configurable runtime settings (default values below):

| Score Range | Action | Description |
| :--- | :--- | :--- |
| **0 – 29** | `APPROVE` | Low risk; transaction processed seamlessly. |
| **30 – 59** | `MONITOR` | Elevated risk score; flagged for asynchronous behavioral audit. |
| **60 – 79** | `STEP_UP_AUTH` | High risk; requires secondary authentication (MFA / biometric check). |
| **80 – 100** | `BLOCK` | Critical threat score; immediate execution rejection and alert. |

---

## 7. Developer & Agent Quality Standards

Future AI agents and human developers modifying this repository MUST strictly follow these rules:

1. **Inspect Before Modifying:** Always view existing code, schemas, and tests before making edits. Do not rewrite functioning modules without explicit architectural necessity.
2. **No Fake Results or Dummy Metrics:** Never hardcode dummy model metrics (e.g., `accuracy = 0.99`) in evaluation outputs. If a model has not been evaluated, report un-evaluated status.
3. **No Placeholders Disguised as Logic:** Do not leave empty functions or return hardcoded `True`/`False` stubs without explicit `# TODO` tags and logged warnings.
4. **Mandatory Testing:** All new domain logic, data transformation functions, rule evaluators, and mutation operators MUST include corresponding unit tests in `tests/`.
5. **Pre-Commit Verification:** Run `pytest` and linting commands before completing any implementation phase.
6. **Backward Compatibility:** Maintain API schema stability. Non-breaking extensions are preferred over breaking changes.

---

## 8. Development Lifecycle Workflow

For every implementation phase specified in `IMPLEMENTATION_ROADMAP.md`:

```
1. Inspect existing workspace & references
2. Draft concise implementation plan (in planning mode if required)
3. Identify affected files and API contracts
4. Write domain code & Pydantic models
5. Write unit & integration tests
6. Run test suite & verify code clean
7. Address any warnings or errors
8. Document updates in docs/WALKTHROUGH.md
```
