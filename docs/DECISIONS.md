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
