from dataclasses import dataclass, field
from typing import Dict, List, Set

from app.digital_twin.sessions import RFC5737_PREFIXES
from app.models import Account, Device, Merchant, Session, Transaction, User


@dataclass
class ValidationReport:
    """Report summarizing data quality and referential integrity checks."""

    is_valid: bool = True
    error_count: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    total_checks_passed: int = 0


class DigitalTwinValidator:
    """Data quality validator for generated Digital Twin datasets."""

    @staticmethod
    def validate(
        users: List[User],
        accounts: List[Account],
        devices: List[Device],
        merchants: List[Merchant],
        sessions: List[Session],
        transactions: List[Transaction],
    ) -> ValidationReport:
        """Validate relational consistency, IP safety, amounts, and references."""
        report = ValidationReport()

        user_ids: Set = {u.id for u in users}
        account_map: Dict = {a.id: a for a in accounts}
        device_ids: Set = {d.id for d in devices}
        merchant_ids: Set = {m.id for m in merchants}
        session_ids: Set = {s.id for s in sessions}

        # 1. Unique Business References Check
        user_refs = {u.synthetic_external_id for u in users}
        if len(user_refs) != len(users):
            report.errors.append("Duplicate user references found")
            report.error_count += 1
        else:
            report.total_checks_passed += 1

        tx_refs = {t.transaction_reference for t in transactions}
        if len(tx_refs) != len(transactions):
            report.errors.append("Duplicate transaction references found")
            report.error_count += 1
        else:
            report.total_checks_passed += 1

        # 2. Account -> User foreign key check
        for acc in accounts:
            if acc.user_id not in user_ids:
                report.errors.append(
                    f"Orphan Account {acc.id} linked to non-existent User {acc.user_id}"
                )
                report.error_count += 1
            else:
                report.total_checks_passed += 1

        # 3. Transaction Referential Integrity & User-Account Consistency Check
        for tx in transactions:
            if tx.user_id not in user_ids:
                report.errors.append(
                    f"Transaction {tx.id} references missing User {tx.user_id}"
                )
                report.error_count += 1

            if tx.account_id not in account_map:
                report.errors.append(
                    f"Transaction {tx.id} references missing Account {tx.account_id}"
                )
                report.error_count += 1
            else:
                # User-Account Consistency Invariant check
                acc = account_map[tx.account_id]
                if acc.user_id != tx.user_id:
                    msg = (
                        f"Consistency Invariant Violation: Tx {tx.id} user_id "
                        f"{tx.user_id} != Account owner {acc.user_id}"
                    )
                    report.errors.append(msg)
                    report.error_count += 1

            if tx.merchant_id not in merchant_ids:
                report.errors.append(
                    f"Transaction {tx.id} references missing Merchant {tx.merchant_id}"
                )
                report.error_count += 1

            if tx.device_id not in device_ids:
                report.errors.append(
                    f"Transaction {tx.id} references missing Device {tx.device_id}"
                )
                report.error_count += 1

            if tx.session_id and tx.session_id not in session_ids:
                report.errors.append(
                    f"Transaction {tx.id} references missing Session {tx.session_id}"
                )
                report.error_count += 1

            # 4. Amount Validation
            if tx.amount <= 0:
                report.errors.append(
                    f"Transaction {tx.id} has invalid non-positive amount {tx.amount}"
                )
                report.error_count += 1
            else:
                report.total_checks_passed += 1

            # 5. RFC 5737 Synthetic IP Check
            ip_valid = any(
                tx.synthetic_ip.startswith(prefix) for prefix in RFC5737_PREFIXES
            )
            if not ip_valid:
                msg = (
                    f"Transaction {tx.id} synthetic_ip {tx.synthetic_ip} "
                    "is outside RFC 5737 prefixes"
                )
                report.errors.append(msg)
                report.error_count += 1
            else:
                report.total_checks_passed += 1

        report.is_valid = report.error_count == 0
        return report
