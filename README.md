# FRAUDOSCOPE — Autonomous Adversarial Payment Security Lab

[![Phase 1: Complete](https://img.shields.io/badge/Phase_1-Repo_Architecture_Complete-emerald)](docs/IMPLEMENTATION_ROADMAP.md)
[![License: Synthetic Research Sandbox](https://img.shields.io/badge/License-Synthetic_Research_Sandbox-green)](docs/SECURITY_AND_RESPONSIBLE_AI.md)
[![Architecture: Modular Monolith](https://img.shields.io/badge/Architecture-Modular_Monolith-purple)](docs/ARCHITECTURE.md)

> FRAUDOSCOPE is a controlled, synthetic payment-security research platform that continuously models emerging GenAI-enabled payment fraud, simulates adversarial campaigns inside a Payment Digital Twin, detects attacks using a hybrid Blue Team, measures defense gaps, evolves attacks via genetic math, and automatically hardens payment defense models.

---

## 🔁 The Closed-Loop Core Engine

```
       ┌─────────────────────────────────────────────────────────────┐
       │                       FRAUDOSCOPE                           │
       │            Autonomous Adversarial Loop                      │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
  ┌───────────────────────────────────┴───────────────────────────────────┐
  │                                                                       │
  ▼                                                                       ▼
IDENTIFY (Threat Taxonomies)                                    REPEAT CONTINUOUSLY
  │                                                                       ▲
  ▼                                                                       │
MODEL ATTACK (Fraud Genome)                                               │
  │                                                                       │
  ▼                                                                       │
GENERATE (Payment Digital Twin)                                           │
  │                                                                       │
  ▼                                                                       │
SIMULATE (Adversarial Campaigns)                                          │
  │                                                                       │
  ▼                                                                       │
DETECT (Hybrid Blue Team: Rules + ML + Anomaly + Graph)                  │
  │                                                                       │
  ▼                                                                       │
MEASURE DEFENSE GAP (False Negative Root Cause)                           │
  │                                                                       │
  ▼                                                                       │
EVOLVE ATTACK (Red Team Mutations: GA & Evasion Math)                     │
  │                                                                       │
  ▼                                                                       │
AUTO-HARDEN (Adversarial Data Augmentation & Model Retraining)           │
  │                                                                       │
  ▼                                                                       │
REPLAY & TEST ON UNSEEN ATTACKS (Strict Promotion Validation)            │
  │                                                                       │
  └───────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ System Architecture & Stack Summary

FRAUDOSCOPE is implemented as a high-performance **Modular Monolith**:

- **Backend Core:** Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0+, Alembic, PostgreSQL.
- **ML & Analytics:** pandas, numpy, scipy, scikit-learn, XGBoost, SHAP, NetworkX, Faker.
- **Frontend Command Center:** React 18, TypeScript, Vite, Tailwind CSS, React Flow, Recharts, Framer Motion.
- **Testing & Infra:** Docker, Docker Compose, pytest, Vitest, GitHub Actions CI.

---

## 📁 Repository Structure

```
FRAUDOSCOPE/
├── backend/                  # Python FastAPI Core & Domain Packages
│   ├── app/
│   │   ├── core/             # Configuration, Database Engine, Base Models
│   │   ├── digital_twin/     # Payment Digital Twin Simulator
│   │   ├── threat_intel/     # Fraud Genome & Threat Taxonomy
│   │   ├── red_team/         # Attack Generation & Evolution Engine
│   │   ├── blue_team/        # Multi-Layer Defense & Risk Fusion Suite
│   │   ├── hardening/        # Defense Gap Analyzer & Auto-Hardening
│   │   ├── explainability/   # SHAP & Counterfactual Explainer
│   │   ├── evaluation/       # Benchmark Harness for Unseen Attacks
│   │   └── main.py           # FastAPI Application Entrypoint
│   ├── tests/                # Unit, Integration & Reproducibility Tests
│   ├── alembic/              # Database Migration Framework
│   ├── pyproject.toml        # Backend Dependencies & Package Config
│   └── README.md
├── frontend/                 # React TypeScript Vite Command Center
│   ├── src/
│   │   ├── components/       # UI Components
│   │   ├── pages/            # Application Pages
│   │   ├── services/         # API Service Clients (Health Checker)
│   │   ├── types/            # TypeScript Interfaces
│   │   ├── App.tsx           # Application Shell
│   │   └── main.tsx
│   ├── package.json          # Frontend Dependencies & Scripts
│   ├── vite.config.ts        # Vite & Vitest Setup
│   └── README.md
├── data/                     # Raw, Generated, Split Data Directory
├── models/                   # Active, Candidate & Registry Model Artifacts
├── experiments/              # Research Experiment Logs
├── scripts/                  # Helper Utilities
├── docker/                   # Backend & Frontend Dockerfiles
├── .github/workflows/        # CI Automation Workflows
├── docker-compose.yml        # Development Container Orchestration
├── .env.example              # Environment Configuration Template
├── .gitignore                # Source Control Exclusion Rules
└── README.md
```

---

## 🚀 Quick Setup & Local Execution

### 1. Environment Configuration
Copy the template environment configuration:
```bash
cp .env.example .env
```

### 2. Backend Startup
```bash
# Navigate to backend and install package in editable mode
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```
Verify backend health: `http://localhost:8000/api/v1/health`

### 3. Frontend Startup
```bash
# In a new terminal, navigate to frontend
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` to access the Command Center shell.

---

## 🧪 Verification & Testing Commands

### Backend Verification
```bash
cd backend
pytest                # Run backend test suite
ruff check .          # Run linter
black --check .       # Run formatter check
```

### Frontend Verification
```bash
cd frontend
npm run test          # Run Vitest component tests
npm run build         # Run TypeScript compilation & production bundle
```

### Docker Verification
```bash
docker compose config # Validate compose syntax
docker compose up     # Launch PostgreSQL, Backend, and Frontend containers
```

---

## 🛡️ Security & Synthetic Sandbox Policy

FRAUDOSCOPE is an ethical research environment operating strictly under synthetic sandbox rules:
- ❌ **Zero Real Customer Data (PII):** 100% procedurally generated user profiles.
- ❌ **Zero Real Payment Execution:** No connection to live payment gateways, banking APIs, or card switches.
- ❌ **Zero Credentials:** No real PANs, CVVs, PINs, or online banking passwords.
- ❌ **No External Attack Execution:** All attack scenarios remain internal parameter simulations inside the Digital Twin.

---

## 📋 Current Limitations & Roadmap Pointer

- **Current Status:** **Phase 1 Complete**. Repository architecture, package structure, environment configuration, database engine shell, frontend application shell, testing setup, and CI pipeline are fully initialized.
- **Next Phase:** **Phase 2 (Database and Domain Models)** will implement SQLAlchemy 2.0 ORM entities, Pydantic schemas, and Alembic database migrations.
- Reference: See [IMPLEMENTATION_ROADMAP.md](docs/IMPLEMENTATION_ROADMAP.md) for full phase details.
