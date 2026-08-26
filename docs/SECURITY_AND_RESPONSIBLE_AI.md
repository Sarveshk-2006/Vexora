# FRAUDOSCOPE — Security Policy & Responsible AI Guidelines

> **Mandatory Security Classification:** Synthetic Research Sandbox Only  
> **Target Audience:** All AI Agents, Software Engineers, Security Researchers, and Contributors

---

## 1. Security Policy & Operational Constraints

FRAUDOSCOPE is designed purely as an autonomous, synthetic payment-security research environment. The application acts as a safe, isolated digital twin for evaluating payment defense mechanisms.

### 1.1 Non-Negotiable Boundaries

1. **Zero Real Customer Data (PII):** Real names, Social Security Numbers, National IDs, real email addresses, or actual physical addresses MUST NEVER be introduced into this repository, database, or test files.
2. **Zero Real Credentials or Account Details:** Real Credit/Debit Card Primary Account Numbers (PANs), Card Verification Values (CVVs), Online Banking Passwords, OAuth Tokens, or UPI PINs MUST NEVER be handled, logged, stored, or generated.
3. **Zero External Payment Rail Integration:** The software MUST NOT connect to, communicate with, or invoke any live payment network, ISO 20022 messaging gateway, card network switch (Visa, Mastercard, RuPay), ACH network, or banking API.
4. **Zero Real-World Attack Automation:** All attack simulations, Fraud Genomes, and evolutionary mutations are strictly abstract parameter manipulations (e.g., numerical amount variance, synthetic timestamp shifting, simulated IP reputation headers). No actual malware payloads, exploit scripts, or real-world account takeover tooling shall ever be included.
5. **Sandbox Network Isolation:** The backend API and simulation engines must execute strictly within localhost or containerized isolated networks. Outbound web requests to unauthorized external destinations are forbidden.

---

## 2. Responsible AI Framework

GenAI and Machine Learning models inside FRAUDOSCOPE are governed by strict responsible AI principles:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         RESPONSIBLE AI BOUNDARIES                           │
├──────────────────────────────────────┬──────────────────────────────────────┤
│     PERMITTED USES FOR LLMs          │        FORBIDDEN USES FOR LLMs       │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ - Threat scenario ideation & narrative│ - Primary transaction risk scoring   │
│   synthesis                          │ - Deterministic rule matching        │
│ - Natural-language explainability    │ - Direct financial decision-making   │
│ - Attack mutation hypothesis generator│ - Real-world credential generation   │
│ - Counterfactual text formatting     │ - Automated attack execution outside │
│                                      │   the internal digital twin          │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### 2.1 The LLM Reasoning Boundary
- Large Language Models (LLMs) are **reasoning, ideation, and explanation tools**.
- LLMs MUST NOT act as the sole numerical risk classifier or transaction approval authority.
- All numerical risk decisions MUST rely on evaluated deterministic rules and statistical/ML models (XGBoost, Isolation Forest, Graph Analytics) whose performance can be rigorously benchmarked and audited.

---

## 3. Synthetic Data Guarantees & Integrity

To ensure zero real data exposure:
- All synthetic names, addresses, emails, and device fingerprints are procedurally generated using deterministic seeds and libraries such as `Faker` with synthetic domain names (e.g., `@example-synthetic-bank.com`).
- Synthetic card numbers use standard test-range BINs (e.g., 4000-0000-0000-0000) that fail Luhn checks or map exclusively to test environments.
- Synthetic UPI VPAs use fake handles (e.g., `user123@synthetic-upi`).

---

## 4. Data Leakage & Evaluation Ethics

1. **Unseen Attack Isolation:** Held-out attack combinations reserved for Phase 10 evaluation MUST NEVER be used during Blue Team model training or feature engineering.
2. **No Invented Evaluation Results:** All accuracy, precision, recall, and ROC-AUC metrics displayed in reports or UI dashboards MUST be computed dynamically from actual execution runs. Hardcoding dummy metrics or fabricating evaluation curves is strictly prohibited.
3. **Reproducible Lineage:** Every decision, attack mutation, and retraining run must maintain complete provenance, linking back to the exact parameter manifest, model weights, and random seeds.

---

## 5. Vulnerability Disclosure & Responsible Research

FRAUDOSCOPE is intended to advance payment security research by providing defender-centric tools for proactive defense hardening. 

Insights derived from FRAUDOSCOPE simulations regarding payment rail vulnerabilities or fraud detection gaps are intended to inform financial defense engineering and robust ML system design.
