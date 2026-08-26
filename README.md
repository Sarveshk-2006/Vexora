# FRAUDOSCOPE — Autonomous Adversarial Payment Security Lab

[![Phase 0: Complete](https://img.shields.io/badge/Phase_0-Engineering_Foundation_Complete-blue)](docs/IMPLEMENTATION_ROADMAP.md)
[![License: Synthetic Research Sandbox](https://img.shields.io/badge/License-Synthetic_Research_Sandbox-green)](docs/SECURITY_AND_RESPONSIBLE_AI.md)
[![Architecture: Modular Monolith](https://img.shields.io/badge/Architecture-Modular_Monolith-purple)](docs/ARCHITECTURE.md)

> **FRAUDOSCOPE** is a controlled, synthetic payment-security research platform that continuously models emerging GenAI-enabled payment fraud, simulates adversarial campaigns inside a Payment Digital Twin, detects attacks using a hybrid Blue Team, analyzes defense gaps, evolves attacks using genetic mutations, and automatically hardens payment defense models.

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

## 🎯 Core Innovation & Philosophy

FRAUDOSCOPE is **NOT** a static fraud detection model or generic binary classifier. 

It is an **Adversarial Red-Team / Blue-Team Laboratory** where:
1. The **Red Team** continuously discovers vulnerabilities in the Blue Team's defense layer.
2. Discovered gaps automatically trigger the **Auto-Hardening Engine** to train candidate model upgrades.
3. Candidate models undergo strict replay validation against historical benchmarks and held-out **unseen attack scenarios** before promotion.

---

## 🛡️ Synthetic Sandbox Boundary

FRAUDOSCOPE operates strictly as a synthetic research sandbox:
- ❌ **No Real Payment Execution** (No live banks, UPI gateways, or credit card networks)
- ❌ **No Real Customer Data** (100% procedurally generated synthetic profiles)
- ❌ **No Credentials or Real Accounts** (Zero PII or financial credentials)
- ❌ **No External System Interactions** (Self-contained simulation sandbox)

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, React Flow, Recharts, Framer Motion |
| **Backend** | Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0+, Alembic |
| **Database** | PostgreSQL (Supabase deployment target) |
| **ML & Stats** | pandas, numpy, scipy, scikit-learn, XGBoost, SHAP, NetworkX |
| **Testing & Infra** | Docker, Docker Compose, pytest, Vitest |

---

## 📁 Repository Structure

```
Fraudoscope/
├── docs/                               # Project Architectural Documentation
│   ├── ENGINEERING_CONTRACT.md         # Engineering Rules & Guidelines
│   ├── ARCHITECTURE.md                 # System Architecture & Sequence Flow
│   ├── IMPLEMENTATION_ROADMAP.md       # 19-Phase Implementation Master Plan
│   ├── SECURITY_AND_RESPONSIBLE_AI.md  # Safety, Sandbox & Ethics Policy
│   └── DECISIONS.md                    # Architecture Decision Records (ADR Log)
├── .env.example                        # Environment Variables Template
├── .gitignore                          # Git Ignore Manifest
└── README.md                           # Project Overview & Entry Point
```

---

## 📚 Core Architecture Documents

Before writing any code or contributing, all engineers and subagents MUST read:
1. [Engineering Contract](docs/ENGINEERING_CONTRACT.md)
2. [Architecture Specification](docs/ARCHITECTURE.md)
3. [Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md)
4. [Security & Responsible AI Policy](docs/SECURITY_AND_RESPONSIBLE_AI.md)
5. [Architecture Decision Records (ADRs)](docs/DECISIONS.md)

---

## 🚀 Current Status

**Phase 0 — Engineering Foundation: COMPLETE**

The project foundation, engineering contract, architectural standards, security rules, decision records, and multi-phase roadmap have been formally established. Application source code implementation will begin in **Phase 1** upon user instruction.
