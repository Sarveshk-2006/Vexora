# FRAUDOSCOPE — Technical Judge Demonstration Script

This document provides a step-by-step walkthrough for demonstrating **FRAUDOSCOPE: Autonomous Synthetic Payment-Security Digital Twin & Defense Hardening Engine** in approximately 3 to 5 minutes.

---

## Technical Overview & Judge Value Proposition

> **Why FRAUDOSCOPE is Different:**  
> Traditional fraud detection systems rely on static classifiers that degrade when attack patterns evolve. FRAUDOSCOPE does not merely detect fraud — it generates controlled adversarial attacks inside a synthetic digital-twin payment sandbox, discovers structural defense gaps, autonomously retrains candidate models, evaluates 5 strict promotion gates, re-attacks the same weakness, and proves measurable defense improvement with full provenance auditability.

---

## 3–5 Minute Demonstration Timeline

### 0:00 – Problem Statement & Sandbox Context
- **Presenter Action:** Open `http://localhost:5173/` (FRAUDOSCOPE Command Center).
- **Presenter Script:**  
  *"Welcome to FRAUDOSCOPE. Operating strictly inside an isolated synthetic payment digital twin sandbox, FRAUDOSCOPE addresses the fundamental challenge of payment security: defense degradation against novel, multi-vector evasion attacks."*
- **Visual Highlight:** Point to the top telemetry header displaying `SYNTHETIC RESEARCH SANDBOX | SEED: 42 | SYSTEM: ONLINE`.

---

### 0:30 – Synthetic Digital Twin & Attack DNA
- **Presenter Action:** Scroll to the **Red Team Attack DNA Matrix**.
- **Presenter Script:**  
  *"FRAUDOSCOPE compiles 11-dimension Fraud Genomes defining attack scenarios — varying velocity deviation, amount patterns, device trust shifts, and geo-ip mutations without touching real payment rails or live customer data."*
- **Visual Highlight:** Hover over the genome dimensions showing `amount_multiplier = 4.5`, `velocity_shift = HIGH`, and `device_trust = LOW`.

---

### 1:00 – Launch Closed-Loop Simulation
- **Presenter Action:** Click the prominent **`RUN CLOSED-LOOP SIMULATION`** button (Seed: `42`).
- **Presenter Script:**  
  *"Let's launch an autonomous closed-loop simulation using canonical Seed 42."*
- **Visual Highlight:** Observe the **8-Stage Pipeline Execution State Machine** transition in real time:  
  `SCENARIO PREP` $\rightarrow$ `RED TEAM` $\rightarrow$ `BLUE TEAM` $\rightarrow$ `GAP ANALYSIS` $\rightarrow$ `HARDENING` $\rightarrow$ `EXPLAINABILITY` $\rightarrow$ `RE-ATTACK` $\rightarrow$ `VERDICT`.

---

### 1:30 – Blue Team Detection & Defense Gap Discovery
- **Presenter Action:** Scroll to **Blue Team Defense Gap Discovery**.
- **Presenter Script:**  
  *"In Stage 3 and 4, the Blue Team multi-layered detector evaluates the campaign. The Autonomous Defense Gap Analyzer identifies structural bypasses — in this run, a `MULTI_VECTOR_EVASION` attack bypassing behavioral anomaly rules with a priority score of 87.5."*
- **Visual Highlight:** Show affected layer (`BEHAVIORAL_ANOMALY`) and bypass count.

---

### 2:00 – Autonomous Hardening & 5 Promotion Gates
- **Presenter Action:** Scroll to **5-Gate Promotion Audit Panel**.
- **Presenter Script:**  
  *"Rather than blindly deploying new models, Stage 5 builds targeted adversarial augmentation datasets and evaluates candidate model `v1.1.0-cand-42` against 5 strict promotion gates: Targeted Gap Improvement, Benign Non-Regression, Unseen Stability, Calibration Stability, and Schema Compatibility."*
- **Visual Highlight:** Point to the 5 `PASS` badges and active model update indicator.

---

### 2:30 – Re-Attack Centerpiece: BEFORE vs AFTER Delta
- **Presenter Action:** Focus on the **Re-Attack Validation Centerpiece**.
- **Presenter Script:**  
  *"The centerpiece of FRAUDOSCOPE is re-attack validation. Stage 7 replays the exact same attack scenario against the newly promoted model. Baseline recall was 60.0%. Post-hardening recall is 80.0% — proving a measurable +20.0% targeted defense improvement."*
- **Visual Highlight:** Highlight the green `+20.0% RECALL IMPROVEMENT` metric card.

---

### 3:00 – Structured Explainability ("WHY WAS THIS FLAGGED?")
- **Presenter Action:** Scroll to **Why Flagged Evidence & Counterfactual Explorer**.
- **Presenter Script:**  
  *"Stage 6 extracts deterministic, ranked evidence explanations. Notice our strict scientific policy: because Random Forest does not produce per-sample SHAP values, FRAUDOSCOPE explicitly displays 'Per-sample attribution unavailable' rather than fabricating fake feature weights."*
- **Visual Highlight:** Interact with the **What-If?** slider adjusting transaction amount to demonstrate counterfactual threshold scoring.

---

### 3:30 – Lineage & Audit Provenance
- **Presenter Action:** Scroll to **Interactive Lineage Explorer** (React Flow Graph).
- **Presenter Script:**  
  *"Finally, FRAUDOSCOPE preserves end-to-end auditability: linking Transaction $\rightarrow$ Attack Campaign $\rightarrow$ Detector Evidence $\rightarrow$ Defense Gap $\rightarrow$ Hardening Dataset $\rightarrow$ Promoted Model $\rightarrow$ Final Verdict."*
- **Visual Highlight:** Click on nodes in the lineage graph showing SHA-256 model and dataset hashes.

---

### 4:00 – Final Verdict & Summary
- **Presenter Action:** Point to **Final Verdict Card** (`HARDENED_SUCCESSFULLY`).
- **Presenter Script:**  
  *"Stage 8 issues the final immutable verdict: `HARDENED_SUCCESSFULLY`. In under 60 seconds, FRAUDOSCOPE has autonomously discovered a defense gap, trained a candidate model, validated 5 safety gates, re-attacked, and verified defense hardening — completely closed loop."*
