# FRAUDOSCOPE — Backend Core Infrastructure

> **Architecture Pattern:** Modular Monolith Core  
> **Status:** Phase 1 Foundation Established

---

## Overview

The `backend/` directory contains the FastAPI application factory, SQLAlchemy infrastructure, Alembic migration framework, and domain package hierarchy for FRAUDOSCOPE.

---

## Directory Structure

```
backend/
├── app/
│   ├── core/           # Config, Database Engine, Security
│   ├── digital_twin/   # Synthetic Payment Simulator (Phase 3)
│   ├── threat_intel/   # Threat Taxonomy & Fraud Genome Schemas (Phase 4)
│   ├── red_team/       # Attack Campaign & Evolution Engine (Phases 5, 7)
│   ├── blue_team/       # Rule Engine, XGBoost, Anomaly & Graph Detectors (Phase 6)
│   ├── hardening/      # Defense Gap & Auto-Hardening Retrainer (Phases 8, 9)
│   ├── explainability/ # SHAP & Counterfactual Explanations (Phase 6)
│   ├── evaluation/     # Evaluation Benchmark Harness (Phase 10)
│   └── main.py         # FastAPI Application Factory & Endpoints
├── tests/
│   ├── unit/           # Fast isolated unit tests
│   ├── integration/    # System & database integration tests
│   ├── reproducibility/# Deterministic seed tests
│   └── fixtures/       # Shared test fixtures
├── alembic/            # Database migration environment
├── pyproject.toml      # Package dependencies & configuration
└── alembic.ini         # Alembic CLI config
```

---

## Local Backend Setup

1. **Install Python 3.11+**
2. **Create & activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```
4. **Run local server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
5. **Verify health endpoint:**
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/api/v1/health
   ```

---

## Testing & Code Quality

```bash
# Run pytest suite
pytest

# Run Ruff linter
ruff check .

# Run Black formatter check
black --check .
```
