import csv
import os
from typing import List

from app.models import Transaction


class DatasetExporter:
    """Dataset exporter for generated synthetic payment activity."""

    @staticmethod
    def export_transactions_csv(
        transactions: List[Transaction],
        output_dir: str = "data/exports",
        filename: str = "transactions.csv",
    ) -> str:
        """Export synthetic transactions to CSV with deterministic ordering."""
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)

        # Sort deterministically by timestamp then transaction_reference
        sorted_txs = sorted(
            transactions, key=lambda t: (t.timestamp, t.transaction_reference)
        )

        headers = [
            "id",
            "transaction_reference",
            "account_id",
            "user_id",
            "merchant_id",
            "device_id",
            "session_id",
            "payment_rail",
            "payment_agent_id",
            "timestamp",
            "amount",
            "currency",
            "transaction_status",
            "transaction_type",
            "location_country",
            "location_region",
            "location_city",
            "synthetic_ip",
            "metadata_json",
        ]

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            for tx in sorted_txs:
                writer.writerow(
                    [
                        str(tx.id),
                        tx.transaction_reference,
                        str(tx.account_id),
                        str(tx.user_id),
                        str(tx.merchant_id),
                        str(tx.device_id),
                        str(tx.session_id) if tx.session_id else "",
                        (
                            tx.payment_rail.value
                            if hasattr(tx.payment_rail, "value")
                            else str(tx.payment_rail)
                        ),
                        str(tx.payment_agent_id) if tx.payment_agent_id else "",
                        tx.timestamp.isoformat(),
                        str(tx.amount),
                        tx.currency,
                        (
                            tx.transaction_status.value
                            if hasattr(tx.transaction_status, "value")
                            else str(tx.transaction_status)
                        ),
                        (
                            tx.transaction_type.value
                            if hasattr(tx.transaction_type, "value")
                            else str(tx.transaction_type)
                        ),
                        tx.location_country,
                        tx.location_region,
                        tx.location_city,
                        tx.synthetic_ip,
                        str(tx.metadata_json) if tx.metadata_json else "",
                    ]
                )

        return file_path
