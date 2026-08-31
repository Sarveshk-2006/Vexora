# FRAUDOSCOPE

> **Autonomous Synthetic Payment-Security Digital Twin & Defense Hardening Engine**

[![CI Pipeline](https://img.shields.io/badge/CI-Passing-brightgreen)](file:///d:/Fraudoscope/docs/WALKTHROUGH.md)
[![Backend Tests](https://img.shields.io/badge/Pytest-123%20Passed-blue)](file:///d:/Fraudoscope/backend/tests/)
[![Frontend Tests](https://img.shields.io/badge/Vitest-6%20Passed-blue)](file:///d:/Fraudoscope/frontend/src/App.test.tsx)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Sandbox](https://img.shields.io/badge/Sandbox-Synthetic%20Only-orange)](docs/SECURITY_AND_RESPONSIBLE_AI.md)

---

## 🎯 Executive Overview

**FRAUDOSCOPE** is a closed-loop security research platform that autonomously discovers payment fraud detection vulnerabilities, hardens machine learning detectors, and verifies defense improvement inside a 100% synthetic digital-twin sandbox.

Traditional payment risk engines rely on static machine learning classifiers and rule sets that degrade as fraudsters evolve multi-vector evasion techniques. FRAUDOSCOPE solves this by creating a continuous, closed-loop feedback loop:

$$\text{Digital Twin} \rightarrow \text{Fraud Genome} \rightarrow \text{Red Team} \rightarrow \text{Blue Team} \rightarrow \text{Gap Analysis} \rightarrow \text{Hardening} \rightarrow \text{Explainability} \rightarrow \text{Re-Attack} \rightarrow \text{Verdict}$$

---

## ⭐ Why FRAUDOSCOPE is Different

1. **Synthetic Digital Twin Sandbox:** Generates 100% benign baseline payment activity across synthetic Users, Accounts, Devices, Merchants, and Sessions without touching real payment rails or live customer data (RFC 5737 IP safety).
2. **Fraud Genome & Red Team Mutations:** Compiles 11-dimension attack scenarios defining behavioral shifts, velocity deviations, amount patterns, and device trust mutations.
3. **Hybrid Blue Team Detection:** Combines deterministic rules, behavioral anomaly detection, Isolation Forest ML models, and graph-based network analysis.
4. **Autonomous Hardening & 5 Promotion Gates:** Builds targeted adversarial datasets and evaluates candidate models against 5 strict safety criteria before promoting to active status.
5. **Re-Attack Validation:** Replays exact attack scenarios against newly promoted models to compute true BEFORE vs AFTER recall deltas.
6. **Non-Fabricated Explainability & Provenance:** Provides ranked evidence explanations and non-SHAP attribution disclaimers while maintaining complete SHA-256 lineage tracking.

---

## 🚀 8-Stage Closed-Loop Workflow

```
 ┌─────────────────────────┐
 │ 1. SCENARIO PREP        │  Compiles Fraud Genome parameters & seed PRNG
 └────────────┬────────────┘
              │
 ┌────────────▼────────────┐
 │ 2. RED TEAM SIMULATION  │  Executes targeted transaction mutation campaign
 └────────────┬────────────┘
              │
 ┌────────────▼────────────┐
 │ 3. BLUE TEAM DETECTION  │  Evaluates multi-layered hybrid detection rules & ML
 └────────────┬────────────┘
              │
 ┌────────────▼────────────┐
 │ 4. DEFENSE GAP ANALYSIS │  Identifies structural bypasses & calculates priority
 └────────────┬────────────┘
              │
 ┌────────────▼────────────┐
 │ 5. AUTONOMOUS HARDENING │  Augments dataset, trains candidate ML, audits 5 gates
 └────────────┬────────────┘
              │
 ┌────────────▼────────────┐
 │ 6. EXPLAINABILITY       │  Extracts deterministic evidence & lineage tree
 └────────────┬────────────┘
              │
 ┌────────────▼────────────┐
 │ 7. RE-ATTACK VALIDATION │  Replays campaign against candidate model & measures delta
 └────────────┬────────────┘
              │
 ┌────────────▼────────────┐
 │ 8. IMMUTABLE VERDICT    │  Issues final status (HARDENED_SUCCESSFULLY / REJECTED)
 └─────────────────────────┘
```

---

## 🛠️ Technology Stack

- **Backend:** Python 3.14, FastAPI, Scikit-learn, Pydantic v2, SQLAlchemy 2.0, PostgreSQL, Alembic, Pytest.
- **Frontend:** React 18, TypeScript, Vite, TailwindCSS, Lucide Icons, React Flow, Vitest.
- **Infrastructure & DevOps:** Docker, Docker Compose, Ruff, Black.

---

## 💻 Local Development & Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (Optional)

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
Backend API interactive documentation available at `http://localhost:8000/docs`.

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open browser at `http://localhost:5173/`.

### 4. Running with Docker Compose
```bash
docker compose up --build
```

---

## 🧪 Verification & Testing Commands

### Run Full Test Suite
```bash
# Backend pytest suite (123 tests)
python -m pytest backend/

# Frontend Vitest suite (6 tests)
npm --prefix frontend test -- --run

# Frontend production build check
npm --prefix frontend run build

# Code linting & formatting
python -m ruff check --select E,F --ignore E501 backend/
python -m black --check backend/

# Docker configuration check
docker compose config
```

---

## 📊 Canonical Seed-42 Execution Results

Executing the canonical simulation with `seed = 42`:

```text
RUN_ID:                 RUN_LOOP_C570A5F23F4C
PIPELINE VERDICT:       HARDENED_SUCCESSFULLY
TARGETED GAP RECALL:    BEFORE: 60.0%  -->  AFTER: 80.0%  (+20.0% Improvement)
PROMOTED MODEL:         v1.1.0-cand-42
PROMOTION GATES:        5/5 GATES PASSED
LEAKAGE AUDIT:          PASSED (Anti-Leakage Audit Abort Policy Enforced)
```

---

## 🔒 Responsible AI & Synthetic Sandbox Policy

FRAUDOSCOPE is strictly designed for **synthetic security research and simulation**.
- **No Real Rails:** Does not connect to live banking networks, card rails, or payment gateways.
- **Synthetic Data Only:** All users, accounts, cards, and transactions are procedurally generated inside memory/database.
- **Non-Numerical Risk LLM Policy:** LLMs are never used for numerical risk scoring or direct transaction approvals.

---

## 📚 Documentation Links

- [Demonstration Script](docs/DEMO_SCRIPT.md) — 3–5 minute step-by-step judge walkthrough
- [System Walkthrough](docs/WALKTHROUGH.md) — Detailed implementation and verification history
- [Architecture Decisions](docs/DECISIONS.md) — Approved Architecture Decision Records (ADRs 001–022)
