from decimal import Decimal
from typing import Any

from app.core.enums import PaymentRail
from app.digital_twin.sessions import RFC5737_PREFIXES


class MutationConstraints:
    """Enforces domain validity constraints on mutated transaction attributes."""

    @staticmethod
    def enforce(tx: Any) -> Any:
        """Enforce domain bounds and invariants on mutated transaction object."""
        # 1. Ensure positive amount
        if tx.amount <= Decimal("0.00"):
            tx.amount = Decimal("1.00")

        # 2. Ensure valid PaymentRail
        if not isinstance(tx.payment_rail, PaymentRail):
            if (
                isinstance(tx.payment_rail, str)
                and tx.payment_rail in PaymentRail.__members__
            ):
                tx.payment_rail = PaymentRail(tx.payment_rail)
            else:
                tx.payment_rail = PaymentRail.UPI

        # 3. Ensure RFC 5737 synthetic IP
        if not any(tx.synthetic_ip.startswith(prefix) for prefix in RFC5737_PREFIXES):
            tx.synthetic_ip = "192.0.2.1"

        return tx
