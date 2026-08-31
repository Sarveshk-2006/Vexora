# VEXORA — Autonomous Adversarial Payment Security Sandbox

> **Synthetic Payment Security & Closed-Loop Defense Hardening Platform**

---

## 📌 Problem

Modern payment-security systems must detect increasingly adaptive fraud patterns. However, static detection rules and traditional machine learning models often suffer from evasive blind spots when fraud rings mutate behavioral patterns, device signatures, and transfer velocity.

---

## 🛡️ Solution

**VEXORA** is an autonomous synthetic payment-security research platform. It simulates adversarial transaction campaigns (Red Team), evaluates hybrid detection layers (Blue Team), discovers multi-vector defense gaps, automatically hardens candidate models through 5-gate promotion verification, and validates defense improvement against deterministic re-attacks.

---

## 🔄 Core Workflow

```text
Scenario Preparation
  └─► 01. Attack Generation (Red Team Evasion Campaign)
       └─► 02. Multi-Layer Detection (Blue Team Rules & ML)
            └─► 03. Defense Gap Discovery (Evasion Ranking)
                 └─► 04. Model Hardening (Adversarial Data Augmentation)
                      └─► 05. 5-Gate Promotion Verification
                           └─► 06. Explainability Signal Attribution
                                └─► 07. Re-Attack Validation
                                     └─► 08. Final Verdict
```

---

## 🎛️ Key Modules & Capabilities

1. **Command Center**: End-to-end execution controls and real-time 8-stage closed-loop pipeline state.
2. **Security Overview**: High-level telemetry dashboard detailing simulation metrics, ROC-AUC, and detection layer recall.
3. **Attack Lab**: 11-dimension Fraud Genome mutation profile and campaign profiling.
4. **Transaction Investigator**: Deep-dive transaction inspector, risk score breakdown, and attack attribution context.
5. **Why Flagged?**: Ranked evidence extraction explaining decision signals without inventing synthetic SHAP weights.
6. **Risk Breakdown**: Subsystem risk contribution waterfall across Rules, ML, Behavioral, Graph, and Adversarial detectors.
7. **Defense Gaps**: Automated evasion discovery, bypass rate metrics, and targeted hardening priorities.
8. **Hardening & Models**: 5-gate automated model candidate promotion audit (Benign non-regression, unseen attack recall, calibration stability).
9. **Attack Lineage**: Interactive React Flow provenance graph connecting Fraud Genome to promoted model candidates.
10. **What-if Analysis**: Interactive slider-based counterfactual perturbation and decision re-computation engine.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Recharts, React Flow (`@xyflow/react`), Lucide Icons.
- **Backend**: FastAPI (Python 3.11+), Pydantic v2, Uvicorn, SQLAlchemy.
- **Database**: PostgreSQL 16, Alembic Migrations.
- **Infrastructure**: Docker, Docker Compose, Nginx.

---

## ⚠️ Important Disclaimer

> **VEXORA uses synthetic data for research and demonstration purposes.**
> It is **NOT** connected to live payment rails, real banking infrastructure, or actual cardholder data.

---

## 🚀 Local Quickstart (Docker Compose)

### Prerequisites
- Docker Engine & Docker Compose (`docker compose`)
- Git

### Commands

```bash
# 1. Clone the repository
git clone https://github.com/Sarveshk-2006/Vexora.git
cd Vexora

# 2. Copy environment template
cp .env.example .env

# 3. Build and launch containers
docker compose up --build -d
```

### Access Local Endpoints
- **Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)
- **FastAPI Backend**: [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check Endpoint**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🌐 Production Deployment Architecture

- **Frontend**: Deployed on [Vercel](https://vercel.com) (Vite SPA Production Build).
- **Backend Service**: Deployed on [Render](https://render.com) (FastAPI / Uvicorn).
- **Managed Database**: Render PostgreSQL Service.

---

## 📄 License & Team

Developed for security research and competitive demonstration. All synthetic fraud patterns, metrics, and models operate deterministically via Seed 42 for 100% auditability.
