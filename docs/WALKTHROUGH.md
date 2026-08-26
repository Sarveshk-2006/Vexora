# FRAUDOSCOPE — Phase Walkthrough Documentation

> **Current Phase:** Phase 2A — Domain Foundation  
> **Status:** Fully Implemented & Verified

---

## Phase 2A: Domain Foundation Walkthrough

### 1. Entity Purpose & Domain Concepts
Phase 2A establishes the foundational database ORM models and Pydantic v2 schemas for the payment digital twin's core actors:

- **`User` (`users` table):** Synthetic account holder profile capturing behavioral baseline metadata (country, region, city, timezone, account age, risk tier). Zero real PII stored.
- **`Account` (`accounts` table):** Synthetic financial ledger account associated with a parent `User`. Models balance history baselines, account age, type (Consumer vs. Business), and operational status.
- **`Device` (`devices` table):** Synthetic device fingerprint entity capturing form factor (`DeviceType`), operating system, first/last seen timestamps, and normalized trust/reputation metrics (`[0.0, 1.0]`).
- **`Merchant` (`merchants` table):** Synthetic merchant profile representing payment destinations with standard Merchant Category Codes (MCC) and regional risk classifications.

---

## 2. Entity Relationship Topology

```
User (users)
 └──1:N──► Account (accounts)
```

- **`User` to `Account`:** One-to-many relationship using foreign key `accounts.user_id` pointing to `users.id` with `CASCADE` delete rules.

---

## 3. Identifier Strategy & Synthetic Data Controls

- **Primary Keys:** Every table uses a 128-bit UUID v4 (`uuid.UUID`) primary key generated via `UUIDPrimaryKeyMixin`.
- **Synthetic Business References:** Each entity exposes a unique, indexed synthetic business identifier:
  - `User.synthetic_external_id` (e.g. `SYN_USER_000001`)
  - `Account.synthetic_account_reference` (e.g. `SYN_ACC_000001`)
  - `Device.synthetic_device_id` (e.g. `SYN_DEV_000001`)
  - `Merchant.synthetic_merchant_id` (e.g. `SYN_MERCH_000001`)
- **Strict Synthetic Data Guarantee:** Zero real PII, zero real credit card PANs, zero real banking credentials, and zero real device serial numbers are stored.

---

## 4. Alembic Database Migration Strategy

Migration script `alembic/versions/001_phase2a_domain_foundation.py` executes schema migrations using pure DDL commands:
- Creates `users`, `accounts`, `devices`, and `merchants` tables.
- Applies indexes on synthetic identifiers and foreign keys (`ix_accounts_user_id`).
- Supports zero-downtime deterministic rollback (`downgrade()` function).
